import os
import pickle
import base64
import email
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/gmail.modify'
]

class GmailClient:
    def __init__(self, credentials_path: str = 'credentials.json', token_path: str = 'token.json'):
        """
        Initialize Gmail client with OAuth2 authentication.
        
        Args:
            credentials_path: Path to the OAuth2 credentials JSON file
            token_path: Path to store/load the OAuth2 token
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None
        self.logger = logging.getLogger(__name__)
        
    def authenticate(self) -> bool:
        """
        Authenticate with Gmail API using OAuth2.
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        creds = None
        
        # Load existing token if available
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    self.logger.info("Token refreshed successfully")
                except Exception as e:
                    self.logger.error(f"Token refresh failed: {e}")
                    creds = None
            
            if not creds:
                if not os.path.exists(self.credentials_path):
                    self.logger.error(f"Credentials file not found: {self.credentials_path}")
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
                
            # Save the credentials for the next run
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
                
        try:
            self.service = build('gmail', 'v1', credentials=creds)
            self.logger.info("Gmail service authenticated successfully")
            return True
        except HttpError as error:
            self.logger.error(f"An error occurred during authentication: {error}")
            return False
    
    def get_unread_emails(self, query: str = 'is:unread', max_results: int = 10) -> List[Dict]:
        """
        Retrieve unread emails from Gmail.
        
        Args:
            query: Gmail search query (default: 'is:unread')
            max_results: Maximum number of emails to retrieve
            
        Returns:
            List of email dictionaries containing id, subject, sender, body, etc.
        """
        if not self.service:
            self.logger.error("Gmail service not authenticated")
            return []
            
        emails = []
        
        try:
            # Search for emails matching the query
            results = self.service.users().messages().list(
                userId='me', q=query, maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            for message in messages:
                email_data = self._get_email_details(message['id'])
                if email_data:
                    emails.append(email_data)
                    
        except HttpError as error:
            self.logger.error(f"An error occurred while fetching emails: {error}")
            
        return emails
    
    def _get_email_details(self, message_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific email.
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            Dictionary containing email details or None if error
        """
        try:
            message = self.service.users().messages().get(
                userId='me', id=message_id, format='full'
            ).execute()
            
            headers = message['payload'].get('headers', [])
            
            # Extract headers
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
            to = next((h['value'] for h in headers if h['name'] == 'To'), '')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
            
            # Extract email body
            body = self._extract_email_body(message['payload'])
            
            return {
                'id': message_id,
                'thread_id': message['threadId'],
                'subject': subject,
                'sender': sender,
                'to': to,
                'date': date,
                'body': body,
                'snippet': message.get('snippet', ''),
                'label_ids': message.get('labelIds', [])
            }
            
        except HttpError as error:
            self.logger.error(f"An error occurred while getting email details: {error}")
            return None
    
    def _extract_email_body(self, payload: Dict) -> str:
        """
        Extract text body from email payload.
        
        Args:
            payload: Email payload from Gmail API
            
        Returns:
            String containing email body text
        """
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                    break
                elif part['mimeType'] == 'text/html':
                    # Fallback to HTML if plain text not available
                    data = part['body']['data']
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            if payload['mimeType'] == 'text/plain':
                data = payload['body']['data']
                body = base64.urlsafe_b64decode(data).decode('utf-8')
            elif payload['mimeType'] == 'text/html':
                data = payload['body']['data']
                body = base64.urlsafe_b64decode(data).decode('utf-8')
                
        return body
    
    def create_draft_reply(self, original_email: Dict, reply_body: str, 
                          subject_prefix: str = "Re: ") -> Optional[str]:
        """
        Create a draft reply to an email.
        
        Args:
            original_email: Original email dictionary
            reply_body: Body text for the reply
            subject_prefix: Prefix for reply subject
            
        Returns:
            Draft ID if successful, None otherwise
        """
        if not self.service:
            self.logger.error("Gmail service not authenticated")
            return None
            
        try:
            # Prepare reply subject
            original_subject = original_email.get('subject', '')
            if not original_subject.startswith('Re:'):
                reply_subject = f"{subject_prefix}{original_subject}"
            else:
                reply_subject = original_subject
            
            # Create email message
            message = email.message.EmailMessage()
            message['To'] = original_email['sender']
            message['Subject'] = reply_subject
            message['In-Reply-To'] = original_email['id']
            message['References'] = original_email['id']
            message.set_content(reply_body)
            
            # Create draft
            draft_body = {
                'message': {
                    'raw': base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8'),
                    'threadId': original_email['thread_id']
                }
            }
            
            draft = self.service.users().drafts().create(
                userId='me', body=draft_body
            ).execute()
            
            draft_id = draft['id']
            self.logger.info(f"Draft created successfully with ID: {draft_id}")
            
            # Apply label to mark as auto-generated draft
            self._apply_label_to_draft(draft_id, 'Auto-Draft')
            
            return draft_id
            
        except HttpError as error:
            self.logger.error(f"An error occurred while creating draft: {error}")
            return None
    
    def _apply_label_to_draft(self, draft_id: str, label_name: str) -> bool:
        """
        Apply a label to a draft email.
        
        Args:
            draft_id: Gmail draft ID
            label_name: Name of the label to apply
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get or create label
            label_id = self._get_or_create_label(label_name)
            if not label_id:
                return False
                
            # Get the draft to find the message ID
            draft = self.service.users().drafts().get(
                userId='me', id=draft_id
            ).execute()
            
            message_id = draft['message']['id']
            
            # Apply label to the message
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'addLabelIds': [label_id]}
            ).execute()
            
            return True
            
        except HttpError as error:
            self.logger.error(f"An error occurred while applying label: {error}")
            return False
    
    def _get_or_create_label(self, label_name: str) -> Optional[str]:
        """
        Get existing label or create new one.
        
        Args:
            label_name: Name of the label
            
        Returns:
            Label ID if successful, None otherwise
        """
        try:
            # Get existing labels
            labels = self.service.users().labels().list(userId='me').execute()
            
            # Check if label already exists
            for label in labels.get('labels', []):
                if label['name'] == label_name:
                    return label['id']
            
            # Create new label if it doesn't exist
            label_object = {
                'name': label_name,
                'labelListVisibility': 'labelShow',
                'messageListVisibility': 'show'
            }
            
            created_label = self.service.users().labels().create(
                userId='me', body=label_object
            ).execute()
            
            return created_label['id']
            
        except HttpError as error:
            self.logger.error(f"An error occurred while managing label: {error}")
            return None
    
    def mark_email_as_processed(self, email_id: str) -> bool:
        """
        Mark an email as processed by applying a custom label.
        
        Args:
            email_id: Gmail message ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get or create 'Processed' label
            label_id = self._get_or_create_label('Auto-Processed')
            if not label_id:
                return False
                
            # Apply label to the message
            self.service.users().messages().modify(
                userId='me',
                id=email_id,
                body={'addLabelIds': [label_id]}
            ).execute()
            
            self.logger.info(f"Email {email_id} marked as processed")
            return True
            
        except HttpError as error:
            self.logger.error(f"An error occurred while marking email as processed: {error}")
            return False