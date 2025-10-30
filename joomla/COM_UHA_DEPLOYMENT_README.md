# com_uha Joomla Component - Deployment Guide

**Component**: Universal Horizon Address (UHA) API Management
**Version**: 1.0.0
**Date**: 2025-10-30
**Target**: tot.allyourbaseline.com (143.198.225.109)

---

## 📦 What's Included

### Core Structure:
- ✅ Component manifest (`uha.xml`)
- ✅ Database schema (4 tables + config)
- ✅ ApiHelper.php (Django API proxy - security layer)
- ✅ ACL permissions (access.xml)
- ✅ Configuration options (config.xml)
- ✅ Language files (English)
- ✅ Service provider (Joomla 4/5 DI)
- ✅ Cryptographic proof script bundled

### Features Implemented:
- API token request system (proxied to Django)
- User-token mapping database
- Usage tracking infrastructure
- Documentation system structure
- Proof execution framework
- ACL-based permissions

### Features Pending (Phase 2):
- Full controllers & views (dashboard, token list, etc.)
- Frontend UI templates
- Admin UI templates
- JavaScript interactions
- Charts/visualizations

---

## 🚀 Quick Deployment

### Step 1: Package Component

```bash
cd /root/private_multiresolution/joomla/
zip -r com_uha_v1.0.0.zip com_uha/ \
  -x "com_uha/{site,admin,media}/*" \
  -x "com_uha/.DS_Store" \
  -x "com_uha/*~"
```

### Step 2: Upload to Server

```bash
scp com_uha_v1.0.0.zip root@tot.allyourbaseline.com:/tmp/
```

### Step 3: Install via Joomla

1. **Access Joomla Admin**:
   - URL: https://tot.allyourbaseline.com/administrator
   - Login with admin credentials

2. **Install Extension**:
   - Navigate to: System → Extensions → Install
   - Click "Upload Package File"
   - Select: `/tmp/com_uha_v1.0.0.zip`
   - Click "Upload & Install"

3. **Verify Installation**:
   - Navigate to: Components → UHA
   - Check database tables:
     ```sql
     SHOW TABLES LIKE '%uha%';
     ```

### Step 4: Configure

1. Navigate to: Components → UHA → Options
2. Set Django API Endpoint: `https://got.gitgap.org/api`
3. Set API Timeout: 30 seconds
4. Enable auto-approve for academic tier
5. Save & Close

---

## 🗄️ Database Tables Created

The component will automatically create these tables:

```
kdfux_uha_user_tokens     - User-token mapping
kdfux_uha_usage_cache     - Cached usage statistics
kdfux_uha_docs            - Documentation pages
kdfux_uha_proof_logs      - Proof execution logs
kdfux_uha_config          - Component configuration
```

Check after installation:
```sql
SELECT * FROM kdfux_uha_config;
```

---

## 🔐 Security Architecture

### API Proxy Pattern:
```
Frontend JS
    ↓
Joomla PHP (ApiHelper.php)
    ↓ HTTPS (server-side)
Django API (got.gitgap.org)
    ↓
PostgreSQL
```

**Benefits**:
- Django endpoint URL never exposed to browser
- All requests authenticated via Joomla session
- Rate limiting can be added in PHP layer
- Request logging in Joomla
- User permissions enforced via ACL

### ApiHelper Methods:
- `requestToken($userData)` - Request new token from Django
- `getUsageStats($token)` - Get token usage from Django
- `executeProof($token, $data)` - Run cryptographic proof
- `validateToken($token)` - Check if token is valid

---

## 👥 Access Control (ACL)

### Default Permissions:

| Action | Public | Registered | Admin |
|--------|--------|------------|-------|
| View Docs | ✅ | ✅ | ✅ |
| Request Token | ❌ | ✅ | ✅ |
| View Own Token | ❌ | ✅ | ✅ |
| View All Tokens | ❌ | ❌ | ✅ |
| Approve Tokens | ❌ | ❌ | ✅ |
| Execute Proofs | ❌ | ✅ | ✅ |

**Configuration**: System → Global Configuration → Permissions → UHA

---

## 🔧 Configuration Options

### API Settings:
- **Django API Endpoint**: Base URL for Django backend
- **API Timeout**: Request timeout in seconds
- **Cache Duration**: How long to cache API responses

### Token Settings:
- **Auto-Approve Academic**: Auto-approve .edu emails
- **Academic Domains**: List of academic email domains
- **Default Limits**: Daily API call limits per tier

### Notifications:
- **Email Notifications**: Enable/disable email alerts
- **Admin Email**: Where to send new request notifications

### Proof Runner:
- **Enable Proof Runner**: Allow web-based proof execution
- **Script Path**: Path to api_cryptographic_proof_system.py
- **Max Execution Time**: Timeout for proof runs

---

## 📝 Next Steps (Phase 2 Development)

### Priority 1: Admin Interface
Create full admin controllers and views:
```
admin/src/Controller/TokensController.php
admin/src/Model/TokensModel.php
admin/src/View/Tokens/HtmlView.php
admin/tmpl/tokens/default.php
```

### Priority 2: Frontend Dashboard
Create user dashboard:
```
site/src/Controller/DashboardController.php
site/src/Model/DashboardModel.php
site/src/View/Dashboard/HtmlView.php
site/tmpl/dashboard/default.php
```

### Priority 3: Token Request Form
Integrate existing HTML form or rebuild in Joomla:
```
site/src/Controller/TokenController.php
site/src/Model/TokenModel.php
site/forms/token_request.xml
site/tmpl/token/request.php
```

### Priority 4: Proof Runner UI
Web interface for proof execution:
```
site/src/Controller/ProofController.php
site/tmpl/proof/form.php
site/tmpl/proof/results.php
media/js/proof-runner.js
```

---

## 🧪 Testing Checklist

After installation, test:

- [ ] Component appears in Components menu
- [ ] Database tables created successfully
- [ ] Configuration page loads (Options button)
- [ ] ACL permissions set correctly
- [ ] ApiHelper can connect to Django
- [ ] Language strings display correctly

**Test Database**:
```sql
-- Check config
SELECT * FROM kdfux_uha_config;

-- Test insert
INSERT INTO kdfux_uha_user_tokens
  (user_id, token, access_tier, status, request_date)
VALUES
  (100, 'test_token_12345', 'academic', 'approved', NOW());

-- Verify
SELECT * FROM kdfux_uha_user_tokens;
```

---

## 🔗 Integration Points

### Existing Systems:
1. **Django Backend**: https://got.gitgap.org/api
   - Token generation: `/request-token`
   - Token validation: `/token/validate`
   - Usage stats: `/token/usage`

2. **HTML Form**: https://tot.allyourbaseline.com/multiresolution-uha.html
   - Currently functional
   - Can be integrated or replaced

3. **Joomla User System**:
   - Use existing registration
   - Link users to tokens via user_id
   - ACL permissions

### Future Integrations:
- uha.allyourbaseline.com subdomain
- Email notification system (Django)
- Usage analytics dashboard
- Billing system (for commercial tier)

---

## 📊 Component Status

### ✅ Completed (Phase 1):
- Core structure & manifest
- Database schema
- API proxy layer (security)
- ACL permissions
- Configuration options
- Language files
- Service provider (DI)

### ⏳ Pending (Phase 2):
- Full controllers & models
- Admin UI (token management)
- Frontend UI (user dashboard)
- JavaScript interactions
- Documentation browser
- Proof runner UI

### 🎯 Current State:
**MVP (Minimum Viable Product)** - Component will install successfully and create database structure. UI components need to be added for full functionality.

---

## 🆘 Troubleshooting

### Installation Fails:
```bash
# Check Joomla error log
tail -f /home/allyb/public_html/administrator/logs/error.php

# Check database
mysql -u allyb_allyb -p allyb_ase
SHOW TABLES LIKE '%uha%';
```

### API Connection Issues:
```php
// Test ApiHelper
use AllYourBaseline\Component\Uha\Site\Helper\ApiHelper;
$endpoint = ApiHelper::getEndpoint();
echo $endpoint; // Should show: https://got.gitgap.org/api
```

### Permission Denied:
```bash
# Check file permissions
chown -R allyb:allyb /home/allyb/public_html/components/com_uha/
chmod -R 755 /home/allyb/public_html/components/com_uha/
```

---

## 📞 Support

- **Repository**: https://github.com/abba-01/multiresolution-cosmology
- **Documentation**: https://allyourbaseline.com/multiresolution-uha-api
- **Email**: support@aybllc.org

---

**Created**: 2025-10-30
**Author**: Dr. Eric D. Martin (via Claude Code)
**License**: Proprietary - All Your Baseline LLC
