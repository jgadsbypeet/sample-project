#!/usr/bin/env python3
"""
Email Automation System

Automatically processes incoming Gmail emails, matches them with pre-approved
response patterns, and creates draft replies for staff review.
"""

import os
import sys
import time
import logging
import schedule
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Import our custom modules
from gmail_client import GmailClient
from response_matcher import ResponseMatcher, MatchResult

# Load environment variables
load_dotenv()

class EmailAutomationSystem:
    """
    Main email automation system that orchestrates the entire process.
    """
    
    def __init__(self, config_dir: str = 'config'):
        """
        Initialize the email automation system.
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = config_dir
        self.gmail_client = None
        self.response_matcher = None
        self.logger = self._setup_logging()
        
        # Load configuration from environment
        self.credentials_path = os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials.json')
        self.token_path = os.getenv('GMAIL_TOKEN_PATH', 'token.json')
        self.staff_email = os.getenv('STAFF_EMAIL', '')
        self.company_name = os.getenv('COMPANY_NAME', 'Your Company')
        self.debug_mode = os.getenv('DEBUG', 'false').lower() == 'true'
        
        # Statistics tracking
        self.stats = {
            'emails_processed': 0,
            'drafts_created': 0,
            'patterns_matched': 0,
            'errors': 0,
            'last_run': None
        }
    
    def _setup_logging(self) -> logging.Logger:
        """
        Set up logging configuration.
        
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger('email_automation')
        logger.setLevel(logging.INFO if not self.debug_mode else logging.DEBUG)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        file_handler = logging.FileHandler('logs/email_automation.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def initialize(self) -> bool:
        """
        Initialize all components of the automation system.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        self.logger.info("Initializing Email Automation System...")
        
        try:
            # Initialize Gmail client
            self.gmail_client = GmailClient(
                credentials_path=self.credentials_path,
                token_path=self.token_path
            )
            
            if not self.gmail_client.authenticate():
                self.logger.error("Failed to authenticate with Gmail")
                return False
            
            # Initialize response matcher
            patterns_config = os.path.join(self.config_dir, 'email_patterns.yaml')
            self.response_matcher = ResponseMatcher(config_path=patterns_config)
            
            if not self.response_matcher.patterns:
                self.logger.error("No email patterns loaded")
                return False
            
            self.logger.info("Email Automation System initialized successfully")
            self.logger.info(f"Loaded {len(self.response_matcher.patterns)} response patterns")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize system: {e}")
            return False
    
    def process_emails(self, max_emails: int = None) -> Dict:
        """
        Process unread emails and create draft replies.
        
        Args:
            max_emails: Maximum number of emails to process (uses config default if None)
            
        Returns:
            Dictionary with processing results
        """
        if not self.gmail_client or not self.response_matcher:
            self.logger.error("System not properly initialized")
            return self._get_empty_results()
        
        # Use configured max emails if not specified
        if max_emails is None:
            max_emails = self.response_matcher.settings.get('max_emails_per_batch', 10)
        
        self.logger.info(f"Starting email processing (max: {max_emails} emails)")
        
        results = {
            'processed': 0,
            'drafts_created': 0,
            'patterns_matched': 0,
            'skipped': 0,
            'errors': 0,
            'details': []
        }
        
        try:
            # Get unread emails (excluding those already processed)
            query = 'is:unread -label:Auto-Processed'
            emails = self.gmail_client.get_unread_emails(query=query, max_results=max_emails)
            
            self.logger.info(f"Found {len(emails)} unread emails to process")
            
            for email in emails:
                try:
                    result = self._process_single_email(email)
                    results['details'].append(result)
                    
                    # Update counters
                    results['processed'] += 1
                    if result['draft_created']:
                        results['drafts_created'] += 1
                    if result['pattern_matched']:
                        results['patterns_matched'] += 1
                    if result['skipped']:
                        results['skipped'] += 1
                        
                except Exception as e:
                    self.logger.error(f"Error processing email {email.get('id', 'unknown')}: {e}")
                    results['errors'] += 1
                    results['details'].append({
                        'email_id': email.get('id', 'unknown'),
                        'subject': email.get('subject', 'unknown'),
                        'error': str(e),
                        'draft_created': False,
                        'pattern_matched': False,
                        'skipped': False
                    })
            
            # Update global statistics
            self.stats['emails_processed'] += results['processed']
            self.stats['drafts_created'] += results['drafts_created']
            self.stats['patterns_matched'] += results['patterns_matched']
            self.stats['errors'] += results['errors']
            self.stats['last_run'] = datetime.now().isoformat()
            
            self.logger.info(f"Processing complete. Results: {results}")
            
        except Exception as e:
            self.logger.error(f"Error during email processing: {e}")
            results['errors'] += 1
        
        return results
    
    def _process_single_email(self, email: Dict) -> Dict:
        """
        Process a single email and create draft reply if pattern matches.
        
        Args:
            email: Email data dictionary
            
        Returns:
            Dictionary with processing result for this email
        """
        email_id = email.get('id', 'unknown')
        subject = email.get('subject', 'No Subject')
        sender = email.get('sender', 'Unknown Sender')
        
        self.logger.debug(f"Processing email: {subject} from {sender}")
        
        result = {
            'email_id': email_id,
            'subject': subject,
            'sender': sender,
            'pattern_matched': False,
            'pattern_id': None,
            'confidence_score': 0.0,
            'draft_created': False,
            'draft_id': None,
            'skipped': False,
            'error': None
        }
        
        try:
            # Skip emails from the staff email (avoid auto-responding to ourselves)
            if self.staff_email and self.staff_email.lower() in sender.lower():
                self.logger.debug(f"Skipping email from staff address: {sender}")
                result['skipped'] = True
                return result
            
            # Analyze email against patterns
            match = self.response_matcher.analyze_email(email)
            
            if match:
                result['pattern_matched'] = True
                result['pattern_id'] = match.pattern_id
                result['confidence_score'] = match.confidence_score
                
                self.logger.info(
                    f"Email matched pattern '{match.pattern_id}' "
                    f"(confidence: {match.confidence_score:.2f})"
                )
                
                # Customize response template
                custom_fields = {
                    'company_name': self.company_name
                }
                
                response_text = self.response_matcher.customize_response(
                    match, email, custom_fields
                )
                
                # Create draft reply
                draft_id = self.gmail_client.create_draft_reply(email, response_text)
                
                if draft_id:
                    result['draft_created'] = True
                    result['draft_id'] = draft_id
                    self.logger.info(f"Created draft reply with ID: {draft_id}")
                else:
                    result['error'] = "Failed to create draft reply"
                    self.logger.error("Failed to create draft reply")
            else:
                self.logger.debug("No pattern matched for this email")
            
            # Mark email as processed regardless of whether we created a draft
            self.gmail_client.mark_email_as_processed(email_id)
            
        except Exception as e:
            result['error'] = str(e)
            self.logger.error(f"Error processing email {email_id}: {e}")
        
        return result
    
    def _get_empty_results(self) -> Dict:
        """
        Get empty results dictionary for error cases.
        
        Returns:
            Empty results dictionary
        """
        return {
            'processed': 0,
            'drafts_created': 0,
            'patterns_matched': 0,
            'skipped': 0,
            'errors': 1,
            'details': []
        }
    
    def run_once(self) -> Dict:
        """
        Run the automation once and return results.
        
        Returns:
            Dictionary with processing results
        """
        self.logger.info("Running email automation (single execution)")
        
        if not self.initialize():
            return self._get_empty_results()
        
        return self.process_emails()
    
    def run_scheduled(self, interval_minutes: int = None) -> None:
        """
        Run the automation on a schedule.
        
        Args:
            interval_minutes: Check interval in minutes (uses config default if None)
        """
        if interval_minutes is None:
            interval_minutes = self.response_matcher.settings.get('check_interval_minutes', 30)
        
        self.logger.info(f"Starting scheduled email automation (every {interval_minutes} minutes)")
        
        if not self.initialize():
            self.logger.error("Failed to initialize system for scheduled execution")
            return
        
        # Schedule the job
        schedule.every(interval_minutes).minutes.do(self._scheduled_job)
        
        # Run immediately once
        self._scheduled_job()
        
        # Keep running
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            self.logger.info("Scheduled automation stopped by user")
        except Exception as e:
            self.logger.error(f"Error in scheduled execution: {e}")
    
    def _scheduled_job(self) -> None:
        """
        Job function for scheduled execution.
        """
        try:
            results = self.process_emails()
            self.logger.info(f"Scheduled run completed: {results}")
        except Exception as e:
            self.logger.error(f"Error in scheduled job: {e}")
    
    def get_statistics(self) -> Dict:
        """
        Get automation statistics.
        
        Returns:
            Dictionary with statistics
        """
        return {
            **self.stats,
            'pattern_stats': self.response_matcher.get_pattern_stats() if self.response_matcher else {},
            'system_status': 'initialized' if self.gmail_client and self.response_matcher else 'not_initialized'
        }
    
    def test_configuration(self) -> Dict:
        """
        Test the configuration and connectivity.
        
        Returns:
            Dictionary with test results
        """
        results = {
            'gmail_auth': False,
            'patterns_loaded': False,
            'config_valid': False,
            'total_patterns': 0,
            'errors': []
        }
        
        try:
            # Test Gmail authentication
            if self.initialize():
                results['gmail_auth'] = True
                results['patterns_loaded'] = len(self.response_matcher.patterns) > 0
                results['total_patterns'] = len(self.response_matcher.patterns)
                results['config_valid'] = True
            else:
                results['errors'].append("Failed to initialize system")
                
        except Exception as e:
            results['errors'].append(f"Configuration test error: {e}")
        
        return results


def main():
    """
    Main entry point for the email automation system.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Email Automation System')
    parser.add_argument('--run-once', action='store_true', 
                       help='Run automation once and exit')
    parser.add_argument('--schedule', type=int, metavar='MINUTES',
                       help='Run on schedule (specify interval in minutes)')
    parser.add_argument('--test', action='store_true',
                       help='Test configuration and exit')
    parser.add_argument('--stats', action='store_true',
                       help='Show statistics and exit')
    parser.add_argument('--max-emails', type=int, metavar='N',
                       help='Maximum number of emails to process')
    parser.add_argument('--config-dir', default='config',
                       help='Configuration directory path')
    
    args = parser.parse_args()
    
    # Create automation system
    automation = EmailAutomationSystem(config_dir=args.config_dir)
    
    if args.test:
        # Test configuration
        print("Testing configuration...")
        results = automation.test_configuration()
        print(f"Results: {results}")
        sys.exit(0 if results['config_valid'] else 1)
    
    if args.stats:
        # Show statistics
        if automation.initialize():
            stats = automation.get_statistics()
            print(f"Statistics: {stats}")
        else:
            print("Failed to initialize system")
        sys.exit(0)
    
    if args.run_once:
        # Run once
        results = automation.run_once()
        print(f"Results: {results}")
        sys.exit(0 if results['errors'] == 0 else 1)
    
    if args.schedule:
        # Run on schedule
        automation.run_scheduled(interval_minutes=args.schedule)
    else:
        # Default: run once
        results = automation.run_once()
        print(f"Results: {results}")
        sys.exit(0 if results['errors'] == 0 else 1)


if __name__ == '__main__':
    main()