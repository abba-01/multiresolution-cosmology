# Email Configuration for UHA API Token Delivery

**Purpose**: Enable automatic email delivery of API tokens when users request them via the web form or API.

**Server**: got.gitgap.org
**Service**: uha_service (Django)
**Status**: Code ready, SMTP credentials needed

---

## Current Status

✅ Token generation: WORKING
✅ Database storage: ACTIVE
✅ Web form integration: COMPLETE
⚠️  Email delivery: **DISABLED** (commented out in code)

**Issue**: The `send_mail()` call in `/opt/uha_service/api/views.py` is commented out (line ~641), so users only see tokens on screen and don't receive them via email.

---

## Setup Instructions

### Option 1: Gmail SMTP (Simple, Free)

**1. Add Django Settings**

SSH to server and edit settings:
```bash
ssh root@got.gitgap.org
cd /opt/uha_service
nano uha_service/settings.py
```

Add at the end of file:
```python
# Email Configuration - Gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # CHANGE THIS
EMAIL_HOST_PASSWORD = 'your-app-password'   # CHANGE THIS (use app password, not regular password)
DEFAULT_FROM_EMAIL = 'UHA API <noreply@allyourbaseline.com>'
```

**2. Get Gmail App Password**

1. Go to: https://myaccount.google.com/apppasswords
2. Create new app password named "UHA Service"
3. Copy the 16-character password
4. Use that password in `EMAIL_HOST_PASSWORD` above

**3. Uncomment send_mail() Call**

Edit the views file:
```bash
nano api/views.py
```

Find line ~641 (in `RequestTokenView.post()`):
```python
# TODO: Send email notification
# send_mail(
#     subject='UHA API Token - Access Granted',
#     message=f'Your API token: {token.token}\n\nEndpoint: https://got.gitgap.org/v1/merge/multiresolution/',
#     from_email='noreply@aybllc.org',
#     recipient_list=[data['email']],
#     fail_silently=True
# )
```

Uncomment it (remove the `#`):
```python
# Send email notification
send_mail(
    subject='UHA API Token - Access Granted',
    message=f'Your API token: {token.token}\n\nEndpoint: https://got.gitgap.org/v1/merge/multiresolution/',
    from_email='noreply@aybllc.org',
    recipient_list=[data['email']],
    fail_silently=True
)
```

**4. Restart Service**

```bash
systemctl restart uha_service
journalctl -u uha_service -f  # Watch logs
```

---

### Option 2: SendGrid (Professional, Free Tier)

**1. Get SendGrid API Key**

1. Sign up: https://signup.sendgrid.com/
2. Create API key: Settings → API Keys → Create API Key
3. Select "Full Access"
4. Copy the key (starts with `SG.`)

**2. Install SendGrid Python Library**

```bash
ssh root@got.gitgap.org
cd /opt/uha_service
source venv/bin/activate
pip install sendgrid
```

**3. Add Django Settings**

```python
# Email Configuration - SendGrid
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'  # Literal string "apikey"
EMAIL_HOST_PASSWORD = 'SG.your_api_key_here'  # CHANGE THIS
DEFAULT_FROM_EMAIL = 'UHA API <noreply@allyourbaseline.com>'
```

**4. Uncomment send_mail() and Restart**

Same as Option 1 above.

**Free Tier**: 100 emails/day (sufficient for testing)

---

### Option 3: Custom SMTP Server

If you have your own SMTP server:

```python
# Email Configuration - Custom
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.your-domain.com'  # CHANGE THIS
EMAIL_PORT = 587  # or 465 for SSL
EMAIL_USE_TLS = True  # or EMAIL_USE_SSL = True for port 465
EMAIL_HOST_USER = 'notifications@your-domain.com'  # CHANGE THIS
EMAIL_HOST_PASSWORD = 'your-password'  # CHANGE THIS
DEFAULT_FROM_EMAIL = 'UHA API <noreply@allyourbaseline.com>'
```

---

## Testing Email Delivery

After configuration, test it:

**Method 1: Request Token via API**
```bash
curl -X POST https://got.gitgap.org/api/request-token \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "institution": "Test University",
    "email": "your-test-email@gmail.com",
    "access_tier": "academic",
    "use_case": "Testing email delivery",
    "daily_limit": 100
  }'
```

**Method 2: Use Web Form**

Visit: https://tot.allyourbaseline.com/multiresolution-uha-api

Fill out the form with your test email.

**Expected Result**:
- Token displayed on screen ✓
- Email received within 1 minute ✓
- Email contains token and endpoint URL ✓

**Check Logs**:
```bash
ssh root@got.gitgap.org
journalctl -u uha_service -f | grep -i email
```

---

## Email Template Enhancement (Optional)

For a better email, update the message in `api/views.py`:

```python
send_mail(
    subject='UHA API Token - Access Granted',
    message=f'''
Hello {data['name']},

Your UHA API token has been generated:

TOKEN: {token.token}

ENDPOINT: https://got.gitgap.org/v1/merge/multiresolution/

USAGE EXAMPLE:
  import requests
  response = requests.post(
      'https://got.gitgap.org/uha/encode',
      json={{'resolution_bits': 32, ...}},
      headers={{'Authorization': 'Bearer {token.token}'}}
  )

DAILY LIMIT: {data.get('daily_limit', 1000)} API calls
ACCESS TIER: {data['access_tier']}

Documentation: https://github.com/abba-01/multiresolution-cosmology

Questions? Reply to this email.

---
UHA Multi-Resolution Encoding Service
https://allyourbaseline.com
''',
    from_email='UHA API <noreply@allyourbaseline.com>',
    recipient_list=[data['email']],
    fail_silently=False  # Change to False to see errors
)
```

---

## Troubleshooting

### Emails Not Sending

**1. Check Django logs**:
```bash
ssh root@got.gitgap.org
journalctl -u uha_service -f
```

**2. Test SMTP connection**:
```bash
python manage.py shell
```
```python
from django.core.mail import send_mail
send_mail(
    'Test Email',
    'This is a test',
    'noreply@allyourbaseline.com',
    ['your-email@gmail.com'],
    fail_silently=False
)
```

**3. Common Issues**:
- Gmail: Need app password, not regular password
- SendGrid: Must use literal string "apikey" as username
- Firewall: Port 587 must be open outbound
- From address: Some SMTP servers require verified sender

**4. Enable verbose error logging**:

In `views.py`, change:
```python
fail_silently=True  # Suppresses errors
```
to:
```python
fail_silently=False  # Shows errors in logs
```

---

## Security Notes

⚠️ **Never commit SMTP credentials to git**

The settings.py file with credentials should NOT be in version control.

**Best practice**: Use environment variables:

```python
import os

EMAIL_HOST_USER = os.environ.get('SMTP_USER')
EMAIL_HOST_PASSWORD = os.environ.get('SMTP_PASSWORD')
```

Then set on server:
```bash
export SMTP_USER="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
```

---

## Quick Start Script

Use the automated script:
```bash
cd /root/private_multiresolution
./scripts/enable_email_notifications.sh
```

(First edit the script to add your SMTP credentials)

---

## Summary

**Current**: Tokens displayed on screen only
**After setup**: Tokens also sent via email
**Time**: 5-10 minutes
**Cost**: Free (Gmail or SendGrid free tier)
**Benefit**: Users can't lose their tokens

---

**Last Updated**: 2025-10-30
**Status**: Template ready, awaiting SMTP credentials
