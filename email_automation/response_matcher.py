import re
import yaml
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

@dataclass
class EmailPattern:
    """Data class for email patterns and responses."""
    pattern_id: str
    keywords: List[str]
    subject_keywords: List[str]
    response_template: str

@dataclass
class MatchResult:
    """Data class for pattern matching results."""
    pattern_id: str
    confidence_score: float
    response_template: str
    matched_keywords: List[str]

class ResponseMatcher:
    """
    Email response matching system that analyzes incoming emails
    and matches them with pre-approved response templates.
    """
    
    def __init__(self, config_path: str = 'config/email_patterns.yaml'):
        """
        Initialize the response matcher with configuration.
        
        Args:
            config_path: Path to the email patterns configuration file
        """
        self.config_path = config_path
        self.patterns: List[EmailPattern] = []
        self.settings = {}
        self.logger = logging.getLogger(__name__)
        
        self.load_config()
    
    def load_config(self) -> bool:
        """
        Load email patterns and settings from configuration file.
        
        Returns:
            bool: True if config loaded successfully, False otherwise
        """
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
            
            # Load patterns
            self.patterns = []
            for pattern_data in config.get('email_patterns', []):
                pattern = EmailPattern(
                    pattern_id=pattern_data['pattern_id'],
                    keywords=pattern_data['keywords'],
                    subject_keywords=pattern_data.get('subject_keywords', []),
                    response_template=pattern_data['response_template']
                )
                self.patterns.append(pattern)
            
            # Load settings
            self.settings = config.get('settings', {})
            
            self.logger.info(f"Loaded {len(self.patterns)} email patterns from config")
            return True
            
        except FileNotFoundError:
            self.logger.error(f"Configuration file not found: {self.config_path}")
            return False
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing configuration file: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error loading config: {e}")
            return False
    
    def analyze_email(self, email_data: Dict) -> Optional[MatchResult]:
        """
        Analyze an email and find the best matching response pattern.
        
        Args:
            email_data: Dictionary containing email information (subject, body, etc.)
            
        Returns:
            MatchResult if a good match is found, None otherwise
        """
        if not email_data:
            return None
            
        subject = email_data.get('subject', '').lower()
        body = email_data.get('body', '').lower()
        snippet = email_data.get('snippet', '').lower()
        
        # Combine all text for analysis
        email_text = f"{subject} {body} {snippet}"
        
        best_match = None
        highest_score = 0.0
        
        for pattern in self.patterns:
            score, matched_keywords = self._calculate_match_score(
                email_text, subject, pattern
            )
            
            if score > highest_score:
                highest_score = score
                best_match = MatchResult(
                    pattern_id=pattern.pattern_id,
                    confidence_score=score,
                    response_template=pattern.response_template,
                    matched_keywords=matched_keywords
                )
        
        # Check if confidence meets threshold
        confidence_threshold = self.settings.get('confidence_threshold', 0.6)
        if best_match and best_match.confidence_score >= confidence_threshold:
            self.logger.info(
                f"Email matched pattern '{best_match.pattern_id}' "
                f"with confidence {best_match.confidence_score:.2f}"
            )
            return best_match
        else:
            self.logger.info(
                f"No pattern matched with sufficient confidence. "
                f"Best score: {highest_score:.2f}, threshold: {confidence_threshold}"
            )
            return None
    
    def _calculate_match_score(self, email_text: str, subject: str, 
                              pattern: EmailPattern) -> Tuple[float, List[str]]:
        """
        Calculate matching score for a given pattern against email text.
        
        Args:
            email_text: Combined email text (subject + body + snippet)
            subject: Email subject line
            pattern: EmailPattern to match against
            
        Returns:
            Tuple of (confidence_score, matched_keywords)
        """
        matched_keywords = []
        
        # Check body/content keywords
        body_matches = 0
        for keyword in pattern.keywords:
            # Use word boundaries to avoid partial matches
            keyword_pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if re.search(keyword_pattern, email_text):
                body_matches += 1
                matched_keywords.append(keyword)
        
        # Check subject keywords (weighted higher)
        subject_matches = 0
        for keyword in pattern.subject_keywords:
            keyword_pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if re.search(keyword_pattern, subject):
                subject_matches += 1
                matched_keywords.append(f"subject:{keyword}")
        
        # Calculate weighted score
        if len(pattern.keywords) > 0:
            body_score = body_matches / len(pattern.keywords)
        else:
            body_score = 0
            
        if len(pattern.subject_keywords) > 0:
            subject_score = subject_matches / len(pattern.subject_keywords)
        else:
            subject_score = 0
        
        # Weight subject matches higher (2x) as they're typically more indicative
        total_score = (body_score + (subject_score * 2)) / 3
        
        return total_score, matched_keywords
    
    def customize_response(self, match_result: MatchResult, email_data: Dict, 
                          custom_fields: Optional[Dict] = None) -> str:
        """
        Customize the response template with dynamic content.
        
        Args:
            match_result: The matched pattern result
            email_data: Original email data
            custom_fields: Additional fields for template customization
            
        Returns:
            Customized response text
        """
        response = match_result.response_template
        
        # Extract sender name from email
        sender = email_data.get('sender', '')
        sender_name = self._extract_sender_name(sender)
        
        # Basic template variables
        template_vars = {
            'sender_name': sender_name,
            'original_subject': email_data.get('subject', ''),
            'current_date': self._get_current_date(),
            'matched_keywords': ', '.join(match_result.matched_keywords[:3])  # First 3 keywords
        }
        
        # Add custom fields if provided
        if custom_fields:
            template_vars.update(custom_fields)
        
        # Simple template substitution
        # Note: For production use, consider using a proper template engine like Jinja2
        for var_name, var_value in template_vars.items():
            placeholder = f"{{{var_name}}}"
            if placeholder in response:
                response = response.replace(placeholder, str(var_value))
        
        return response
    
    def _extract_sender_name(self, sender_email: str) -> str:
        """
        Extract sender name from email address.
        
        Args:
            sender_email: Full sender email string (e.g., "John Doe <john@example.com>")
            
        Returns:
            Extracted name or 'Customer' as fallback
        """
        if not sender_email:
            return "Customer"
        
        # Try to extract name from "Name <email>" format
        name_match = re.match(r'^(.*?)\s*<.*?>$', sender_email.strip())
        if name_match:
            name = name_match.group(1).strip().strip('"\'')
            if name:
                return name
        
        # If no name found, try to use part of email
        email_match = re.search(r'<?([\w\.-]+)@[\w\.-]+>?', sender_email)
        if email_match:
            username = email_match.group(1)
            # Capitalize first letter
            return username.replace('.', ' ').replace('_', ' ').title()
        
        return "Customer"
    
    def _get_current_date(self) -> str:
        """
        Get current date in a readable format.
        
        Returns:
            Formatted date string
        """
        from datetime import datetime
        return datetime.now().strftime("%B %d, %Y")
    
    def get_pattern_stats(self) -> Dict:
        """
        Get statistics about loaded patterns.
        
        Returns:
            Dictionary with pattern statistics
        """
        return {
            'total_patterns': len(self.patterns),
            'pattern_ids': [p.pattern_id for p in self.patterns],
            'confidence_threshold': self.settings.get('confidence_threshold', 0.6),
            'max_emails_per_batch': self.settings.get('max_emails_per_batch', 10)
        }
    
    def test_pattern_match(self, test_email: Dict, pattern_id: str = None) -> Dict:
        """
        Test email against patterns for debugging purposes.
        
        Args:
            test_email: Test email data
            pattern_id: Specific pattern to test (optional)
            
        Returns:
            Dictionary with test results
        """
        results = {}
        
        if pattern_id:
            # Test specific pattern
            pattern = next((p for p in self.patterns if p.pattern_id == pattern_id), None)
            if pattern:
                subject = test_email.get('subject', '').lower()
                body = test_email.get('body', '').lower()
                snippet = test_email.get('snippet', '').lower()
                email_text = f"{subject} {body} {snippet}"
                
                score, matched_keywords = self._calculate_match_score(
                    email_text, subject, pattern
                )
                
                results[pattern_id] = {
                    'score': score,
                    'matched_keywords': matched_keywords,
                    'meets_threshold': score >= self.settings.get('confidence_threshold', 0.6)
                }
        else:
            # Test all patterns
            for pattern in self.patterns:
                subject = test_email.get('subject', '').lower()
                body = test_email.get('body', '').lower()
                snippet = test_email.get('snippet', '').lower()
                email_text = f"{subject} {body} {snippet}"
                
                score, matched_keywords = self._calculate_match_score(
                    email_text, subject, pattern
                )
                
                results[pattern.pattern_id] = {
                    'score': score,
                    'matched_keywords': matched_keywords,
                    'meets_threshold': score >= self.settings.get('confidence_threshold', 0.6)
                }
        
        return results