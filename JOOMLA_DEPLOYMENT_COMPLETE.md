# Joomla Article Deployment - COMPLETE

**Date:** 2025-10-30
**Site:** tot.allyourbaseline.com
**Status:** ✅ LIVE

---

## Deployment Summary

### Files Deployed

1. **HTML Demo Page**
   - Source: `/root/private_multiresolution/multiresolution_demo_page.html`
   - Destination: `/home/allyb/public_html/multiresolution-uha.html`
   - Size: 22KB
   - Direct URL: https://tot.allyourbaseline.com/multiresolution-uha.html

2. **Joomla Article**
   - ID: 1
   - Title: "Multi-Resolution UHA Tensor Calibration"
   - Alias: `multiresolution-uha-api`
   - State: Published (1)
   - Category: 2 (default)
   - URL: https://tot.allyourbaseline.com/multiresolution-uha-api

3. **Main Menu Item**
   - ID: 121
   - Title: "Multi-Resolution UHA API"
   - Alias: `multiresolution-uha-api`
   - Type: component (com_content)
   - Published: Yes
   - Link: `index.php?option=com_content&view=article&id=1`

---

## Features Deployed

### 1. Professional Letter Section
- Introduces the multi-resolution UHA method
- Explains the breakthrough discovery
- Patent protection notice (US 63/902,536)
- Key features list
- Professional signature from Dr. Eric D. Martin

### 2. API Token Request Form
- Full name input
- Institution input
- Email address input
- Access tier selection:
  - Academic (Free for peer-reviewed publications)
  - Commercial ($5,000/year)
  - Enterprise (Contact for pricing)
- Research use case description
- Daily API call limit selector
- Token generation (currently mock - ready for backend integration)

### 3. Live Interactive Simulation
- Configurable Planck/SH0ES sample sizes
- Three resolution schedule options:
  - Fast: [8, 16, 24, 32]
  - Standard: [8, 12, 16, 20, 24, 28, 32] (default)
  - Fine: [8-32 in steps of 2]
- Real-time simulation output in terminal style
- Shows:
  - Progressive convergence through resolution scales
  - Δ_T (epistemic distance) decreasing
  - H₀ gap narrowing
  - Concordance percentage increasing
  - Final merged H₀ value with uncertainty

### 4. Responsive Design
- Two-column layout (letter | API form)
- Full-width simulation section below
- Beautiful gradient backgrounds
- Mobile-friendly (switches to single column on small screens)
- Professional typography
- Smooth animations

---

## Access URLs

### Main Article (via Joomla)
```
https://tot.allyourbaseline.com/multiresolution-uha-api
```
- Embedded iframe with the full demo
- Joomla header/footer/menu
- Integrated with site navigation

### Direct HTML (Standalone)
```
https://tot.allyourbaseline.com/multiresolution-uha.html
```
- Full-page experience
- No Joomla wrapper
- Recommended for best experience

---

## Database Records

### Article Record (kdfux_content)
```sql
SELECT * FROM kdfux_content WHERE id = 1;
```

Fields:
- `id`: 1
- `title`: "Multi-Resolution UHA Tensor Calibration"
- `alias`: "multiresolution-uha-api"
- `state`: 1 (published)
- `catid`: 2 (default category)
- `access`: 1 (public)
- `language`: * (all languages)
- `introtext`: Summary paragraph
- `fulltext`: Iframe embed + direct link

### Menu Record (kdfux_menu)
```sql
SELECT * FROM kdfux_menu WHERE id = 121;
```

Fields:
- `id`: 121
- `menutype`: "mainmenu"
- `title`: "Multi-Resolution UHA API"
- `alias`: "multiresolution-uha-api"
- `link`: "index.php?option=com_content&view=article&id=1"
- `type`: "component"
- `published`: 1
- `access`: 1 (public)

---

## Next Steps to Connect Backend

### 1. Create Token Generation Endpoint

Currently, the form generates mock tokens. To connect to real backend:

**Option A: Django REST API on got.gitgap.org**

Create `/opt/uha_service/api/views.py` endpoint:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import ServiceToken

@api_view(['POST'])
def request_token(request):
    data = request.data

    # Create token
    token = ServiceToken.objects.create(
        observer=f"{data['name']} ({data['institution']})",
        permissions="read,write",
        is_active=True,
        daily_limit=data.get('daily_limit', 100),
        notes=f"Tier: {data['access_tier']}, Use case: {data['use_case']}"
    )

    # Send email
    send_mail(
        subject='UHA API Token - Access Granted',
        message=f'Your token: {token.token}',
        from_email='support@aybllc.org',
        recipient_list=[data['email']]
    )

    return Response({
        'success': True,
        'token': token.token,
        'endpoint': 'https://got.gitgap.org/v1/merge/multiresolution/',
        'daily_limit': token.daily_limit
    })
```

Add to `urls.py`:
```python
path('api/request-token', request_token, name='request_token'),
```

**Option B: Joomla PHP Component**

Create `/home/allyb/public_html/components/com_uha/api_token.php`:

```php
<?php
// Handle token request
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = json_decode(file_get_contents('php://input'), true);

    // Generate token
    $token = 'uha_' . bin2hex(random_bytes(16));

    // Store in database
    $db = JFactory::getDbo();
    $query = $db->getQuery(true);
    $query->insert('#__uha_tokens')
        ->columns(['token', 'observer', 'email', 'tier', 'daily_limit'])
        ->values($db->quote($token) . ',' .
                 $db->quote($data['name']) . ',' .
                 $db->quote($data['email']) . ',' .
                 $db->quote($data['access_tier']) . ',' .
                 (int)$data['daily_limit']);
    $db->setQuery($query);
    $db->execute();

    // Send email
    $mailer = JFactory::getMailer();
    $mailer->addRecipient($data['email']);
    $mailer->setSubject('UHA API Token');
    $mailer->setBody("Your token: $token");
    $mailer->send();

    // Return response
    header('Content-Type: application/json');
    echo json_encode([
        'success' => true,
        'token' => $token,
        'endpoint' => 'https://got.gitgap.org/v1/merge/multiresolution/'
    ]);
}
?>
```

### 2. Update JavaScript in HTML

Edit `/home/allyb/public_html/multiresolution-uha.html` line ~330:

```javascript
const response = await fetch('https://got.gitgap.org/api/request-token', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(formData)
});

const result = await response.json();

if (result.success) {
    responseBox.className = 'response-box success';
    responseBox.innerHTML = `
        <h3>✓ API Token Generated Successfully!</h3>
        <p><strong>Your API Token:</strong></p>
        <p style="font-family: monospace; background: #fff; padding: 10px; border-radius: 5px;">${result.token}</p>
        <p><strong>Endpoint:</strong> ${result.endpoint}</p>
        <p><strong>Daily Limit:</strong> ${result.daily_limit} calls</p>
    `;
}
```

### 3. Create Database Table for Tokens (if using Joomla)

```sql
CREATE TABLE kdfux_uha_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    token VARCHAR(255) NOT NULL UNIQUE,
    observer VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    institution VARCHAR(255),
    tier ENUM('academic', 'commercial', 'enterprise') NOT NULL,
    daily_limit INT DEFAULT 100,
    is_active TINYINT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used TIMESTAMP NULL,
    use_count INT DEFAULT 0,
    notes TEXT,
    INDEX idx_token (token),
    INDEX idx_email (email),
    INDEX idx_active (is_active)
);
```

---

## Maintenance

### Update Article Content

```bash
ssh root@tot.allyourbaseline.com
mysql -u allyb_allyb -p'*cx?w.GHWj@ab5gA' allyb_ase

UPDATE kdfux_content
SET fulltext = 'NEW CONTENT HERE'
WHERE id = 1;
```

### Update HTML Demo

```bash
# On local machine
scp /root/private_multiresolution/multiresolution_demo_page.html \
    root@tot.allyourbaseline.com:/home/allyb/public_html/multiresolution-uha.html

# On server
ssh root@tot.allyourbaseline.com
chown allyb:allyb /home/allyb/public_html/multiresolution-uha.html
```

### Unpublish Article

```sql
UPDATE kdfux_content SET state = 0 WHERE id = 1;
```

### Unpublish Menu Item

```sql
UPDATE kdfux_menu SET published = 0 WHERE id = 121;
```

---

## Testing Checklist

- [x] HTML file uploaded and accessible
- [x] Article created in Joomla database
- [x] Menu item created in main menu
- [x] Article marked as published
- [x] Menu item marked as published
- [ ] Test token request form with real backend
- [ ] Test simulation runner
- [ ] Test on mobile devices
- [ ] Test iframe embed in article
- [ ] Verify email notifications work

---

## Support

For issues or questions:
- **Joomla Admin**: https://tot.allyourbaseline.com/administrator/
- **Database Access**: MySQL via SSH
- **File Access**: SSH to /home/allyb/public_html/

---

## Summary

✅ **Complete deployment successful!**

The Multi-Resolution UHA API demo page is now live on tot.allyourbaseline.com with:

1. **Full-featured demo page** with letter, API form, and simulation
2. **Joomla article** integrated into site navigation
3. **Main menu item** for easy access
4. **Ready for backend integration** to generate real tokens

**URLs:**
- Article: https://tot.allyourbaseline.com/multiresolution-uha-api
- Direct: https://tot.allyourbaseline.com/multiresolution-uha.html

All files are in place and the system is ready for use!
