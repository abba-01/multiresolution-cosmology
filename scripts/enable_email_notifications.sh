#!/bin/bash
# Enable Email Notifications for UHA API Token Delivery
# Run this script AFTER adding SMTP credentials to Django settings.py

set -e  # Exit on error

echo "================================"
echo "Enable Email Notifications"
echo "================================"
echo ""

# Check if we can SSH to server
echo "Testing SSH connection to got.gitgap.org..."
if ! ssh -o ConnectTimeout=5 root@got.gitgap.org "echo 'Connected successfully'" 2>/dev/null; then
    echo "❌ ERROR: Cannot connect to got.gitgap.org"
    echo "   Make sure you have SSH access configured"
    exit 1
fi
echo "✓ SSH connection OK"
echo ""

# Verify settings.py has email config
echo "Checking for email configuration in settings.py..."
if ssh root@got.gitgap.org "grep -q 'EMAIL_HOST_USER' /opt/uha_service/uha_service/settings.py" 2>/dev/null; then
    echo "✓ Email configuration found in settings.py"
else
    echo "⚠️  WARNING: No EMAIL_HOST_USER found in settings.py"
    echo ""
    echo "Please add email configuration first!"
    echo "See: EMAIL_CONFIG_TEMPLATE.md"
    echo ""
    echo "Example:"
    echo "  EMAIL_HOST = 'smtp.gmail.com'"
    echo "  EMAIL_HOST_USER = 'your-email@gmail.com'"
    echo "  EMAIL_HOST_PASSWORD = 'your-app-password'"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
echo ""

# Backup views.py before modifying
echo "Creating backup of views.py..."
ssh root@got.gitgap.org "cp /opt/uha_service/api/views.py /opt/uha_service/api/views.py.backup" 2>/dev/null
echo "✓ Backup created: /opt/uha_service/api/views.py.backup"
echo ""

# Uncomment the send_mail() block
echo "Uncommenting send_mail() in views.py..."

# This finds the commented-out send_mail block and uncomments it
ssh root@got.gitgap.org "sed -i '/^# *TODO: Send email notification/,/^# *)/s/^# \?//' /opt/uha_service/api/views.py" 2>/dev/null

echo "✓ send_mail() uncommented"
echo ""

# Verify the change
echo "Verifying changes..."
if ssh root@got.gitgap.org "grep -q '^[^#]*send_mail(' /opt/uha_service/api/views.py" 2>/dev/null; then
    echo "✓ send_mail() is now active (not commented)"
else
    echo "⚠️  WARNING: Could not verify send_mail() was uncommented"
    echo "   You may need to manually edit /opt/uha_service/api/views.py"
fi
echo ""

# Restart the service
echo "Restarting uha_service..."
ssh root@got.gitgap.org "systemctl restart uha_service" 2>/dev/null
sleep 2
echo "✓ Service restarted"
echo ""

# Check service status
echo "Checking service status..."
if ssh root@got.gitgap.org "systemctl is-active uha_service" 2>/dev/null | grep -q "active"; then
    echo "✓ uha_service is ACTIVE"
else
    echo "❌ ERROR: uha_service failed to start"
    echo ""
    echo "Check logs:"
    echo "  ssh root@got.gitgap.org 'journalctl -u uha_service -n 50'"
    exit 1
fi
echo ""

echo "================================"
echo "✅ EMAIL NOTIFICATIONS ENABLED"
echo "================================"
echo ""
echo "Test it:"
echo "  1. Visit: https://tot.allyourbaseline.com/multiresolution-uha-api"
echo "  2. Request a token with your email"
echo "  3. Check your inbox (may take 1-2 minutes)"
echo ""
echo "Or test via API:"
echo "  curl -X POST https://got.gitgap.org/api/request-token \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"name\":\"Test\",\"institution\":\"Test\",\"email\":\"your@email.com\",\"access_tier\":\"academic\",\"use_case\":\"Test\",\"daily_limit\":100}'"
echo ""
echo "Watch logs:"
echo "  ssh root@got.gitgap.org 'journalctl -u uha_service -f | grep -i email'"
echo ""
echo "If emails not arriving, check:"
echo "  - SMTP credentials in settings.py"
echo "  - Firewall allows port 587 outbound"
echo "  - Gmail app password (not regular password)"
echo ""
echo "To rollback:"
echo "  ssh root@got.gitgap.org 'cp /opt/uha_service/api/views.py.backup /opt/uha_service/api/views.py && systemctl restart uha_service'"
echo ""
