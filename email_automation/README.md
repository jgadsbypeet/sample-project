# Email Automation System

An intelligent email automation system that connects to Gmail, analyzes incoming emails using pre-approved response patterns, and automatically creates draft replies for staff review.

## Features

- **Gmail Integration**: Secure OAuth2 authentication with Gmail API
- **Pattern Matching**: Intelligent email analysis using keyword-based patterns
- **Pre-approved Responses**: Configurable response templates for common inquiries
- **Draft Creation**: Automatically creates draft replies for staff review
- **Scheduling**: Run automation on a schedule or manually
- **Logging**: Comprehensive logging and statistics tracking
- **Safety First**: Creates drafts only - staff always reviews before sending

## Quick Start

### Prerequisites

- Python 3.7 or higher
- Gmail account with API access
- Google Cloud Platform project with Gmail API enabled

### Installation

1. **Clone or download the email automation system**
   ```bash
   cd email_automation
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Gmail API credentials** (see [Gmail API Setup](#gmail-api-setup))

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Test the configuration**
   ```bash
   python email_automation.py --test
   ```

6. **Run the automation**
   ```bash
   python email_automation.py --run-once
   ```

## Gmail API Setup

### Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

### Step 2: Create OAuth2 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Desktop application"
4. Name your client (e.g., "Email Automation")
5. Download the JSON file and save it as `credentials.json` in the email_automation directory

### Step 3: Configure OAuth Consent Screen

1. Go to "APIs & Services" > "OAuth consent screen"
2. Choose "External" (unless you have a Google Workspace account)
3. Fill in required fields:
   - App name: "Email Automation"
   - User support email: Your email
   - Developer contact: Your email
4. Add scopes (Gmail API scopes will be requested during first run)
5. Add your email as a test user

## Configuration

### Environment Variables (.env)

Create a `.env` file based on `.env.example`:

```env
# Gmail API Configuration
GMAIL_CREDENTIALS_PATH=credentials.json
GMAIL_TOKEN_PATH=token.json

# Email Configuration
STAFF_EMAIL=your.email@company.com
COMPANY_NAME=Your Company Name

# Debug mode (optional)
DEBUG=false
```

### Email Patterns (config/email_patterns.yaml)

The system comes with pre-configured patterns for common email types:

- **General Inquiries**: Questions and information requests
- **Support Requests**: Technical issues and problems
- **Pricing Inquiries**: Cost and quote requests
- **Appointment Requests**: Meeting scheduling
- **Complaints/Feedback**: Customer concerns
- **Partnership Inquiries**: Business collaboration requests

#### Adding Custom Patterns

Edit `config/email_patterns.yaml` to add new patterns:

```yaml
email_patterns:
  - pattern_id: "custom_pattern"
    keywords: ["keyword1", "keyword2", "keyword3"]
    subject_keywords: ["subject_keyword"]
    response_template: |
      Your custom response template here.
      
      Use placeholders like {sender_name} for personalization.
      
      Best regards,
      Your Team
```

#### Available Template Variables

- `{sender_name}`: Extracted sender name
- `{original_subject}`: Original email subject
- `{current_date}`: Current date
- `{company_name}`: Your company name (from .env)

#### Configuration Settings

```yaml
settings:
  confidence_threshold: 0.6    # Minimum confidence to create draft (0.0-1.0)
  max_emails_per_batch: 10     # Maximum emails to process at once
  check_interval_minutes: 30   # Default scheduling interval
  draft_label: "Auto-Draft"    # Label for auto-generated drafts
```

## Usage

### Command Line Options

```bash
# Run once and exit
python email_automation.py --run-once

# Run on schedule (every 30 minutes)
python email_automation.py --schedule 30

# Test configuration
python email_automation.py --test

# Show statistics
python email_automation.py --stats

# Process maximum 5 emails
python email_automation.py --run-once --max-emails 5

# Use custom config directory
python email_automation.py --run-once --config-dir /path/to/config
```

### First Run

When you run the automation for the first time:

1. A browser window will open for Gmail authentication
2. Sign in with your Gmail account
3. Grant permission to the application
4. The system will save authentication tokens for future use

### Monitoring

The system creates several indicators in Gmail:

- **Auto-Processed**: Label applied to emails that have been analyzed
- **Auto-Draft**: Label applied to automatically created drafts
- **Logs**: Check `logs/email_automation.log` for detailed operation logs

## How It Works

### Email Processing Flow

1. **Connect to Gmail**: Authenticate using OAuth2
2. **Fetch Unread Emails**: Get emails that haven't been processed
3. **Analyze Content**: Match email text against configured patterns
4. **Generate Response**: Use matched pattern to create personalized response
5. **Create Draft**: Save response as draft in Gmail
6. **Mark as Processed**: Apply label to prevent reprocessing

### Pattern Matching Algorithm

The system uses a weighted scoring algorithm:

1. **Keyword Matching**: Checks email body and subject for pattern keywords
2. **Subject Weight**: Subject matches are weighted 2x higher
3. **Confidence Score**: Calculates overall match confidence (0.0-1.0)
4. **Threshold Check**: Only creates drafts if confidence meets threshold

### Safety Features

- **Draft Only**: Never sends emails automatically
- **Staff Review**: All responses require manual review
- **Skip Self**: Ignores emails from configured staff address
- **Processing Labels**: Prevents duplicate processing
- **Error Handling**: Comprehensive error logging and recovery

## Customization

### Adding New Response Patterns

1. Edit `config/email_patterns.yaml`
2. Add new pattern with unique `pattern_id`
3. Define relevant keywords for matching
4. Create appropriate response template
5. Test with `--test` option

### Modifying Response Templates

Templates support basic variable substitution:

```yaml
response_template: |
  Dear {sender_name},
  
  Thank you for contacting {company_name} on {current_date}.
  
  Regarding your inquiry about "{original_subject}", we will review
  your request and respond within 24 hours.
  
  Best regards,
  Customer Service Team
```

### Adjusting Matching Sensitivity

Modify the `confidence_threshold` in `config/email_patterns.yaml`:

- **0.3-0.5**: More sensitive (creates more drafts, some may be incorrect)
- **0.6-0.7**: Balanced (recommended)
- **0.8-1.0**: Conservative (only very clear matches)

## Troubleshooting

### Common Issues

**Authentication Error**
```
Error: Failed to authenticate with Gmail
```
- Ensure `credentials.json` is in the correct location
- Check that Gmail API is enabled in Google Cloud Console
- Verify OAuth consent screen is configured

**No Patterns Loaded**
```
Error: No email patterns loaded
```
- Check that `config/email_patterns.yaml` exists and is valid YAML
- Verify file permissions
- Check logs for YAML parsing errors

**Permission Denied**
```
Error: Insufficient authentication scopes
```
- Delete `token.json` and re-authenticate
- Ensure all required scopes are granted during authentication

**No Emails Found**
```
Found 0 unread emails to process
```
- Check that there are unread emails in the account
- Verify the Gmail query is correct
- Check for existing "Auto-Processed" labels

### Debug Mode

Enable debug logging in `.env`:
```env
DEBUG=true
```

This provides detailed information about:
- Email content analysis
- Pattern matching scores
- API requests and responses
- Processing decisions

### Testing Patterns

Test specific patterns against sample emails:

```python
from response_matcher import ResponseMatcher

matcher = ResponseMatcher()
test_email = {
    'subject': 'Pricing inquiry',
    'body': 'I would like to know your pricing for services',
    'sender': 'customer@example.com'
}

results = matcher.test_pattern_match(test_email)
print(results)
```

## Scheduling and Automation

### Running as a Service

For production deployment, consider running as a system service:

#### Linux (systemd)

Create `/etc/systemd/system/email-automation.service`:

```ini
[Unit]
Description=Email Automation Service
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/email_automation
ExecStart=/usr/bin/python3 email_automation.py --schedule 30
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable email-automation
sudo systemctl start email-automation
```

#### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., every 30 minutes)
4. Set action to run: `python email_automation.py --schedule 30`

### Cron Job (Alternative)

Add to crontab for periodic execution:
```bash
# Run every 30 minutes
*/30 * * * * cd /path/to/email_automation && python email_automation.py --run-once
```

## Security Considerations

### Credentials Storage

- **Never commit `credentials.json` or `token.json` to version control**
- Store credentials securely on the server
- Use environment variables for sensitive configuration
- Regularly rotate OAuth tokens

### Access Control

- Use a dedicated Gmail account for automation (recommended)
- Limit API scopes to minimum required permissions
- Monitor API usage in Google Cloud Console
- Enable 2FA on the Gmail account

### Data Privacy

- Logs may contain email metadata (subjects, senders)
- Implement log rotation and retention policies
- Consider encryption for log files
- Comply with relevant privacy regulations (GDPR, etc.)

## API Rate Limits

Gmail API has usage quotas:

- **Daily quota**: 1,000,000,000 quota units per day
- **Per-user rate limit**: 250 quota units per user per second

The automation system is designed to work within these limits:
- Processes emails in small batches
- Uses efficient API calls
- Implements appropriate delays

## Support and Maintenance

### Monitoring

- Check logs regularly: `tail -f logs/email_automation.log`
- Monitor statistics: `python email_automation.py --stats`
- Set up alerts for authentication failures
- Track draft creation rates

### Updates

- Keep dependencies updated: `pip install -r requirements.txt --upgrade`
- Review and update response patterns periodically
- Monitor Gmail API changes and deprecations
- Test configuration after updates: `python email_automation.py --test`

### Backup

Backup important files:
- `config/email_patterns.yaml`
- `.env` (without committing to version control)
- `credentials.json` (securely)
- Log files for analysis

## License

This email automation system is provided as-is for educational and business use. Please ensure compliance with Gmail API Terms of Service and applicable privacy regulations.

## Contributing

To contribute improvements:
1. Test thoroughly with your configuration
2. Update documentation if needed
3. Follow existing code style and patterns
4. Consider backward compatibility