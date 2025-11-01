# UHA Systems Improvement Plan - SSOT
**Single Source of Truth for All Planned Improvements**

**Date:** 2025-11-01
**Version:** 1.0.0
**Status:** Implementation In Progress (67% of P0 Complete)
**Last Updated:** 2025-11-01 02:46 UTC
**Owner:** Eric D. Martin / Claude Code

---

## Executive Summary

This document serves as the **Single Source of Truth** for all planned improvements to the UHA ecosystem based on the comprehensive systems audit completed on 2025-11-01.

**Systems in Scope:**
1. **allyourbaseline.com** - Joomla 5.4 frontend (com_uha component)
2. **got.gitgap.org** - Django 5 REST API backend
3. **GitHub Repositories** - Public documentation and reference implementations

**Total Action Items:** 47
**Estimated Total Effort:** 180-220 hours
**Priority Distribution:**
- 🔴 Critical (P0): 8 items (~40 hours)
- 🟠 High (P1): 12 items (~60 hours)
- 🟡 Medium (P2): 15 items (~50 hours)
- 🟢 Low (P3): 12 items (~40 hours)


**Session Progress (2025-11-01):**
- ✅ P0.8 - Centralized Documentation (COMPLETE)
- ✅ P0.5 - .env File Encryption (COMPLETE)
- ✅ P0.6 - Two-Tier Rate Limiting (COMPLETE)
- ✅ P0.4 - Token Expiration (COMPLETE)
- ⏳ P0.1 - Token Accounting Unification (60% COMPLETE)
- ⏸️ P0.7 - Multiresolution Deployment (PENDING)

**Detailed Report:** See `UHA_P0_IMPLEMENTATION_SESSION_2025-11-01.md`

---

## Table of Contents

1. [Critical Fixes (P0)](#1-critical-fixes-p0)
2. [High Priority Improvements (P1)](#2-high-priority-improvements-p1)
3. [Medium Priority Enhancements (P2)](#3-medium-priority-enhancements-p2)
4. [Long-term Strategic Items (P3)](#4-long-term-strategic-items-p3)
5. [Implementation Roadmap](#5-implementation-roadmap)
6. [Success Metrics](#6-success-metrics)
7. [Risk Analysis](#7-risk-analysis)

---

## 1. Critical Fixes (P0)

**Timeline:** Week 1-2
**Estimated Effort:** 40 hours
**Blocker Status:** Must complete before production scale-up

### P0.1 - Unify Token Accounting Models

**Status:** 🔴 Not Started
**Priority:** Critical
**Effort:** 12 hours
**Owner:** Backend + Frontend teams

**Problem:**
- Joomla uses "token jar + chamber" model (tokens = API calls)
- Django uses "token pot + runs" model (tokens = key issuance, runs = API calls)
- Users confused about what tokens actually represent
- Accounting mismatches can lead to billing errors

**Solution:**
Choose ONE model and implement across both systems.

**Recommended Model:** Django's "Token Pot + Runs" approach
- Clearer separation: tokens buy keys, runs execute operations
- First-free key is better UX than first-free call
- Perpetual storage fee concept is more robust

**Implementation Tasks:**

1. **Update Joomla Schema** (4 hours)
   ```sql
   -- Rename columns
   ALTER TABLE #__uha_token_jars
     CHANGE COLUMN jar_tokens token_balance INT DEFAULT 0;

   -- Add new columns
   ALTER TABLE #__uha_keys
     ADD COLUMN runs_remaining INT DEFAULT 1,
     ADD COLUMN is_first_free TINYINT(1) DEFAULT 0;

   -- Migrate data
   UPDATE #__uha_keys SET runs_remaining = 1 WHERE status = 'active';
   ```

2. **Update TokenManager.php** (4 hours)
   - Replace `loadChamber()` with `consumeRun()`
   - Remove chamber logic
   - Add `addRuns($count)` method
   - Update `refill()` to use Django token pot model

3. **Update UI Labels** (2 hours)
   - Change "Tokens in Jar" → "Token Balance"
   - Change "Chamber Loaded" → "Runs Remaining"
   - Add explainer: "Tokens buy API keys, runs execute operations"

4. **Documentation** (2 hours)
   - Update UHA_INTEGRATION_SSOT.md
   - Create migration guide for existing users
   - Update Joomla admin help text

**Dependencies:** None
**Risk:** Medium (requires data migration)
**Testing:** Verify token→key→run flow end-to-end

---

### P0.2 - Implement Tombstoning in Django

**Status:** 🔴 Not Started
**Priority:** Critical
**Effort:** 6 hours
**Owner:** Backend team

**Problem:**
- Django allows hard deletion of UHAApiKey records
- Breaks audit trail integrity
- Violates immutability principle stated in patent
- Joomla already implements tombstoning correctly

**Solution:**
Implement soft-delete tombstoning in Django models.

**Implementation Tasks:**

1. **Update UHAApiKey Model** (2 hours)
   ```python
   class UHAApiKey(models.Model):
       # Existing fields...
       is_active = BooleanField(default=True)

       # Add tombstone fields
       tombstoned_at = DateTimeField(null=True, blank=True)
       tombstone_reason = CharField(max_length=255, blank=True)
       tombstoned_by = CharField(max_length=100, blank=True)

       def tombstone(self, reason, tombstoned_by):
           """Soft-delete this key (immutable tombstone)"""
           self.is_active = False
           self.tombstoned_at = timezone.now()
           self.tombstone_reason = reason
           self.tombstoned_by = tombstoned_by
           self.save()

       def delete(self, *args, **kwargs):
           """Override delete to prevent hard deletion"""
           raise PermissionError(
               "Cannot delete UHA API keys. Use tombstone() instead."
           )
   ```

2. **Create Migration** (1 hour)
   ```bash
   cd /opt/uha_service
   ./venv/bin/python manage.py makemigrations
   ./venv/bin/python manage.py migrate
   ```

3. **Update Admin Interface** (2 hours)
   - Add "Tombstone" action to Django admin
   - Show tombstone reason in list view
   - Filter: Active / Tombstoned / All
   - Prevent deletion via admin UI

4. **Update API Views** (1 hour)
   - Token revoke endpoint calls `tombstone()` not `delete()`
   - Add tombstone reason to API request
   - Log tombstone events to APIRequestLog

**Dependencies:** None
**Risk:** Low (additive change)
**Testing:** Verify keys cannot be hard-deleted

---

### P0.3 - Fix Hardcoded VPC IP in Joomla Config

**Status:** 🔴 Not Started
**Priority:** Critical
**Effort:** 2 hours
**Owner:** Frontend team

**Problem:**
- com_uha config.xml has hardcoded `http://10.124.0.8:8000`
- Old internal IP, not current public URL
- Confusing for users (though overridden by .env)
- Prevents clean deployment to other environments

**Solution:**
Update config.xml to reference current production URL.

**Implementation Tasks:**

1. **Update config.xml** (30 min)
   ```xml
   <field
       name="master_api_url"
       type="text"
       label="COM_UHA_MASTER_API_URL"
       description="COM_UHA_MASTER_API_URL_DESC"
       default="https://got.gitgap.org/v1/"
       readonly="false"
       class="inputbox"
   />
   ```

2. **Update .env Priority** (30 min)
   - Ensure .env values override config.xml
   - Document override behavior
   - Add warning if config.xml differs from .env

3. **Update Documentation** (1 hour)
   - Document environment variable precedence
   - Create deployment checklist
   - Add troubleshooting section

**Dependencies:** None
**Risk:** Very Low
**Testing:** Verify API calls still work after update

---

### P0.4 - Add Token Rotation Policy

**Status:** 🔴 Not Started
**Priority:** Critical (Security)
**Effort:** 8 hours
**Owner:** Backend team

**Problem:**
- API tokens never expire
- No rotation mechanism
- Security risk if token leaked
- Best practice is 90-day rotation

**Solution:**
Implement automatic token expiration and rotation API.

**Implementation Tasks:**

1. **Add Expiration to ServiceToken Model** (2 hours)
   ```python
   class ServiceToken(models.Model):
       # Existing fields...
       expires_at = DateTimeField(null=True, blank=True)
       rotation_warning_sent = BooleanField(default=False)

       def is_expired(self):
           if self.expires_at is None:
               return False
           return timezone.now() > self.expires_at

       @classmethod
       def create_with_expiration(cls, observer, permissions, days=90):
           token_str = cls.generate_token(observer, permissions)
           expires_at = timezone.now() + timedelta(days=days)
           return cls.objects.create(
               token=token_str,
               observer=observer,
               permissions=permissions,
               expires_at=expires_at,
               is_active=True
           )
   ```

2. **Update Authentication Middleware** (2 hours)
   - Check expiration in `authenticate_credentials()`
   - Return 401 if token expired
   - Include expiration info in error message

3. **Create Rotation Endpoint** (2 hours)
   ```python
   # POST /v1/admin/token/rotate
   {
       "old_token": "uha.admin.xxx...",
       "reason": "scheduled_rotation"
   }

   # Returns:
   {
       "new_token": "uha.admin.yyy...",
       "expires_at": "2026-02-01T00:00:00Z",
       "old_token_grace_period": 7  # days
   }
   ```

4. **Implement Grace Period** (1 hour)
   - Old token works for 7 days after rotation
   - Allows time to update clients
   - Log warnings when old token used

5. **Email Notifications** (1 hour)
   - Email observer 14 days before expiration
   - Email again at 7 days, 3 days, 1 day
   - Include rotation instructions

**Dependencies:** Email configuration
**Risk:** Medium (could break active integrations if not careful)
**Testing:** Test expiration, rotation, grace period

---

### P0.5 - Secure .env File Encryption

**Status:** 🔴 Not Started
**Priority:** Critical (Security)
**Effort:** 4 hours
**Owner:** DevOps

**Problem:**
- API tokens stored in plaintext .env files
- `/home/allyb/secure/.env` has 600 permissions but still plaintext
- Risk if server compromised
- Best practice is encryption at rest

**Solution:**
Encrypt .env files with ansible-vault or similar.

**Implementation Tasks:**

1. **Install ansible-vault** (30 min)
   ```bash
   ssh root@allyourbaseline.com
   pip3 install ansible-vault
   ```

2. **Encrypt Existing .env** (1 hour)
   ```bash
   # Backup original
   cp /home/allyb/secure/.env /home/allyb/secure/.env.backup

   # Encrypt
   ansible-vault encrypt /home/allyb/secure/.env
   # Password stored in /root/.vault_password (600 permissions)

   # Create decrypt script
   cat > /home/allyb/secure/decrypt_env.sh << 'SCRIPT'
   #!/bin/bash
   ansible-vault view /home/allyb/secure/.env --vault-password-file=/root/.vault_password
   SCRIPT
   chmod 700 /home/allyb/secure/decrypt_env.sh
   ```

3. **Update DjangoApiClient.php** (2 hours)
   ```php
   // Load encrypted .env
   protected function loadEnv()
   {
       $envPath = '/home/allyb/secure/.env';

       // Decrypt on-the-fly
       $decrypted = shell_exec(
           '/home/allyb/secure/decrypt_env.sh 2>/dev/null'
       );

       if (!$decrypted) {
           throw new RuntimeException('Failed to decrypt .env file');
       }

       // Parse decrypted content
       foreach (explode("\n", $decrypted) as $line) {
           // ... existing parsing logic
       }
   }
   ```

4. **Update Deployment Docs** (30 min)
   - Document vault password location
   - Add recovery procedure
   - Create runbook for .env updates

**Dependencies:** None
**Risk:** High (could break API access if done wrong)
**Testing:** Extensive testing before production deployment

---

### P0.6 - Standardize Rate Limiting

**Status:** 🔴 Not Started
**Priority:** Critical
**Effort:** 6 hours
**Owner:** Backend + Frontend teams

**Problem:**
- Joomla: Per-key cooldown timer (60 seconds between calls)
- Django: Per-observer daily quota (5 requests/day)
- Inconsistent user experience
- Neither alone is adequate for production

**Solution:**
Implement tiered rate limiting: per-second + per-day.

**Implementation Tasks:**

1. **Update Django Throttling** (3 hours)
   ```python
   # api/throttles.py
   from rest_framework.throttling import BaseThrottle

   class TieredRateThrottle(BaseThrottle):
       """
       Two-tier rate limiting:
       - Tier 1: 1 request per second (burst protection)
       - Tier 2: 1000 requests per day (quota)
       """

       def allow_request(self, request, view):
           observer = self.get_observer(request)

           # Tier 1: Check last request time
           cache_key_burst = f'throttle_burst_{observer}'
           last_request = cache.get(cache_key_burst)
           now = time.time()

           if last_request and (now - last_request) < 1.0:
               return False  # Too fast

           cache.set(cache_key_burst, now, 2)  # 2 second TTL

           # Tier 2: Check daily quota
           quota = UsageQuota.get_or_create_quota(observer, daily_limit=1000)
           if not quota.check_quota():
               return False  # Quota exceeded

           quota.increment()
           return True
   ```

2. **Update Joomla TokenManager** (2 hours)
   ```php
   public function canMakeRequest($keyId): bool
   {
       $key = $this->getKey($keyId);

       // Check cooldown (1 second minimum)
       $now = new DateTime();
       $lastCall = new DateTime($key->last_call_at);
       $cooldown = $key->cooldown_seconds ?: 1;

       if ($lastCall && ($now->getTimestamp() - $lastCall->getTimestamp()) < $cooldown) {
           return false;  // Cooldown active
       }

       // Check daily quota (fetch from Django)
       $usage = $this->apiClient->getUsage($key->public_key);
       if ($usage['current_count'] >= $usage['daily_limit']) {
           return false;  // Quota exceeded
       }

       return true;
   }
   ```

3. **Synchronize Limits** (1 hour)
   - Joomla cooldown: 1 second (matches Django tier 1)
   - Django daily quota: 1000 requests/day (configurable per observer)
   - Document in UHA_INTEGRATION_SSOT.md

**Dependencies:** Redis or memcached for fast caching
**Risk:** Medium
**Testing:** Load testing to verify rate limits work

---

### P0.7 - Deploy Multiresolution Code to Production API

**Status:** 🔴 Not Started
**Priority:** Critical (Research Value)
**Effort:** 10 hours
**Owner:** Backend + Science teams

**Problem:**
- `comprehensive_multiprobe_simulation.py` only in GitHub repo
- Production API has `multiresolution_engine.py` but not full simulation
- Cannot run complete cosmological analysis via API
- Research code not validated in production environment

**Solution:**
Deploy comprehensive multiprobe simulation as production API endpoint.

**Implementation Tasks:**

1. **Copy Simulation Code to Django** (1 hour)
   ```bash
   cd /opt/uha_service
   cp /root/private_multiresolution/comprehensive_multiprobe_simulation.py \
      ./api/services/cosmology_simulation.py
   ```

2. **Create Django View** (4 hours)
   ```python
   # api/views.py
   class CosmologyMultiprobeView(APIView):
       """
       Run comprehensive multi-probe cosmological simulation

       POST /v1/cosmology/multiprobe
       {
           "probes": ["cosmic_shear", "bao", "growth_rate", "cmb_lensing"],
           "resolution_schedule": [8, 12, 16, 20, 24],
           "cosmology": {
               "h0": 67.36,
               "omega_m": 0.3153,
               "omega_lambda": 0.6847
           }
       }

       Returns: MultiProbeResults with convergence metrics
       """
       authentication_classes = [ServiceTokenAuthentication]
       permission_classes = [IsAuthenticated]
       throttle_classes = [TieredRateThrottle]

       def post(self, request):
           # Validate input
           probes = request.data.get('probes', [])
           resolution_schedule = request.data.get('resolution_schedule', [8, 12, 16, 20, 24])

           # Run simulation
           from api.services.cosmology_simulation import run_comprehensive_multiprobe_simulation

           results = run_comprehensive_multiprobe_simulation(
               resolution_schedule=resolution_schedule,
               probes_to_run=probes
           )

           # Log to database
           APIRequestLog.objects.create(
               observer=request.user.identifier,
               endpoint='/v1/cosmology/multiprobe',
               method='POST',
               request_data=request.data,
               response_summary={'num_probes': len(results.probe_results)}
           )

           return Response(results.to_dict())
   ```

3. **Add URL Route** (30 min)
   ```python
   # api/urls.py
   urlpatterns = [
       # ... existing routes
       path('v1/cosmology/multiprobe', CosmologyMultiprobeView.as_view(), name='cosmology-multiprobe'),
   ]
   ```

4. **Create Celery Task for Long-Running Jobs** (3 hours)
   ```python
   # api/tasks.py
   from celery import shared_task

   @shared_task(time_limit=3600)  # 1 hour max
   def run_multiprobe_async(job_id, probes, resolution_schedule, cosmology):
       """Run simulation asynchronously"""
       # ... simulation code
       # Store results in database or S3
       # Notify user when complete
   ```

5. **Testing & Validation** (1.5 hours)
   - Test all 6 probes independently
   - Test full simulation run
   - Verify results match GitHub version
   - Load test with concurrent requests

**Dependencies:** Celery + Redis for async tasks
**Risk:** High (computationally intensive)
**Testing:** Extensive performance testing needed

---

### P0.8 - Create Centralized Documentation Repository

**Status:** 🔴 Not Started
**Priority:** Critical (User Experience)
**Effort:** 6 hours
**Owner:** Documentation team

**Problem:**
- UHA docs scattered across 3+ repos and 2 servers
- No single source of truth for API specification
- Users confused about which repo to check
- Duplicate/conflicting information

**Solution:**
Consolidate all documentation in `uha-blackbox` repo as canonical SSOT.

**Implementation Tasks:**

1. **Audit Existing Docs** (2 hours)
   - List all .md files across all repos
   - Identify duplicates and conflicts
   - Map docs to canonical locations

   Current doc locations:
   ```
   /root/private_multiresolution/
   ├── UHA_INTEGRATION_SSOT.md (Joomla ↔ Django)
   ├── UHA_API_NOTICE.md
   ├── APPENDIX_UHA_RESOLUTION_TIERS.md
   ├── UHA_PROTECTION_STATUS_2025-10-31.md
   └── SESSION_SUMMARY_2025-10-31.md

   github.com/abba-01/uha-blackbox/
   ├── README.md
   ├── QUICKSTART.md
   └── (minimal docs)

   github.com/abba-01/multiresolution-cosmology/
   ├── COMPREHENSIVE_MULTIPROBE_RESULTS_SUMMARY.md
   └── START_HERE.md
   ```

2. **Create Unified Structure** (2 hours)
   ```
   github.com/abba-01/uha-blackbox/
   ├── README.md (overview + quick start)
   ├── docs/
   │   ├── API_SPECIFICATION.md (complete REST API docs)
   │   ├── INTEGRATION_GUIDE.md (Joomla, Python, PHP clients)
   │   ├── DEPLOYMENT.md (server setup, nginx, SSL)
   │   ├── SECURITY.md (auth, rate limiting, encryption)
   │   ├── MULTIRESOLUTION_THEORY.md (Morton encoding, resolution tiers)
   │   ├── COSMOLOGY_PROBES.md (scientific background)
   │   ├── TOKEN_ECONOMICS.md (token pot, runs, pricing)
   │   └── TROUBLESHOOTING.md (common issues, FAQs)
   ├── examples/
   │   ├── python/
   │   ├── php/
   │   └── joomla/
   └── CHANGELOG.md
   ```

3. **Migrate Content** (1.5 hours)
   - Copy relevant sections from scattered docs
   - Remove duplicates
   - Update cross-references
   - Add version tags

4. **Update All Repos to Point to uha-blackbox** (30 min)
   ```markdown
   # multiresolution-cosmology/README.md

   ## Documentation

   **Main documentation:** https://github.com/abba-01/uha-blackbox/tree/main/docs

   This repo contains research code. For API integration, see the main docs.
   ```

**Dependencies:** None
**Risk:** Low
**Testing:** User review of doc clarity

---

## 2. High Priority Improvements (P1)

**Timeline:** Week 3-4
**Estimated Effort:** 60 hours

### P1.1 - Create Public GitHub Repo for com_uha

**Status:** 🟡 Not Started
**Priority:** High
**Effort:** 4 hours
**Owner:** Frontend team

**Why:** Enable version control, community contributions, public audit

**Tasks:**
1. Create `github.com/abba-01/com_uha_joomla` repository
2. Copy all com_uha files from allyourbaseline.com
3. Create .gitignore (exclude .env files)
4. Tag current version as v1.0.0
5. Add README with installation instructions
6. Add LICENSE (GPL v2+ to match Joomla)
7. Create CONTRIBUTING.md

**Deliverables:**
- Public repo with clean git history
- Installation guide
- Version tags matching Django API versions

---

### P1.2 - Implement Django Admin 2FA

**Status:** 🟡 Not Started
**Priority:** High (Security)
**Effort:** 4 hours
**Owner:** Backend team

**Why:** Superuser accounts need multi-factor authentication

**Tasks:**
1. Install `django-otp` package
2. Add to INSTALLED_APPS
3. Run migrations
4. Configure TOTP (Google Authenticator)
5. Require 2FA for all superusers
6. Create backup codes
7. Document setup process

**Deliverables:**
- 2FA enforced for admin accounts
- Backup recovery procedure
- User documentation

---

### P1.3 - Add UHA Encoding Fallback to Joomla

**Status:** 🟡 Not Started
**Priority:** High
**Effort:** 8 hours
**Owner:** Frontend team

**Why:** Reduce dependency on Django API availability

**Tasks:**
1. Port basic Morton encoding to PHP
2. Create `UhaEncoder.php` class
3. Support 8, 12, 16 bit resolutions (not full 32-bit)
4. Fallback logic: Try Django API first, use local if fails
5. Cache encoded values locally
6. Add warning in UI when using fallback

**Implementation:**
```php
namespace Joomla\Component\Uha\Administrator\Service;

class UhaEncoder
{
    public function mortonEncode3D($x, $y, $z, $bits = 16)
    {
        $morton = 0;
        for ($i = 0; $i < $bits; $i++) {
            $morton |= (($x & (1 << $i)) << (2 * $i)) |
                       (($y & (1 << $i)) << (2 * $i + 1)) |
                       (($z & (1 << $i)) << (2 * $i + 2));
        }
        return $morton;
    }

    public function encodeUHA($ra, $dec, $distance, $bits = 16)
    {
        // Convert RA/Dec/Distance to 3D Cartesian
        // ... coordinate transformation
        // Morton encode
        // Return UHA address
    }
}
```

**Deliverables:**
- PHP UHA encoder (basic functionality)
- Fallback mechanism
- Unit tests

---

### P1.4 - Create Integration Test Suite

**Status:** 🟡 Not Started
**Priority:** High
**Effort:** 12 hours
**Owner:** QA team

**Why:** Catch divergence between Joomla and Django early

**Tasks:**
1. Create test framework (pytest for Django, PHPUnit for Joomla)
2. Write integration tests:
   - Token creation (Joomla creates, Django validates)
   - Key issuance (Django creates, Joomla displays)
   - Rate limiting (both systems agree on quota)
   - Audit logs (both systems log same events)
3. Set up CI/CD (GitHub Actions)
4. Run tests on every commit
5. Generate coverage reports

**Test Scenarios:**
```python
# test_token_accounting.py

def test_token_purchase_sync():
    """Test that token purchase updates both systems"""
    # Purchase 100 tokens via Joomla
    joomla_balance = joomla_api.purchase_tokens(account_id, 100)

    # Check Django pot
    django_pot = django_api.get_token_pot(account_id)

    assert joomla_balance == django_pot['balance']

def test_key_issuance_sync():
    """Test that key issuance consumes token in both systems"""
    # Issue key via Django
    key = django_api.issue_key(account_id)

    # Check Joomla shows key
    joomla_keys = joomla_api.get_keys(account_id)

    assert key['uha_address'] in [k['public_key'] for k in joomla_keys]
```

**Deliverables:**
- 50+ integration tests
- CI/CD pipeline
- Test coverage >80%

---

### P1.5 - Implement Request Caching

**Status:** 🟡 Not Started
**Priority:** High
**Effort:** 6 hours
**Owner:** Backend team

**Why:** Reduce compute load for repeated encode/decode requests

**Tasks:**
1. Use Django's RequestCache model (already exists!)
2. Enable caching in UHAEncodeView and UHADecodeView
3. Set TTL to 1 hour (3600 seconds)
4. Add cache hit/miss metrics
5. Create cache invalidation API
6. Monitor cache performance

**Implementation:**
```python
# api/views.py

class UHAEncodeView(APIView):
    def post(self, request):
        # Check cache
        cached = RequestCache.get_cached(
            endpoint='encode',
            data=request.data,
            ttl=3600
        )

        if cached:
            # Cache hit
            return Response(cached)

        # Cache miss - compute
        result = self.compute_encoding(request.data)

        # Store in cache
        RequestCache.set_cached(
            endpoint='encode',
            request_data=request.data,
            response_data=result
        )

        return Response(result)
```

**Deliverables:**
- Caching enabled for encode/decode
- Cache hit rate monitoring
- Cache invalidation API

---

### P1.6 - Add Monitoring and Alerting

**Status:** 🟡 Not Started
**Priority:** High
**Effort:** 8 hours
**Owner:** DevOps

**Why:** Proactive issue detection before users are impacted

**Tasks:**
1. Install Prometheus + Grafana (or use DigitalOcean monitoring)
2. Instrument Django with django-prometheus
3. Create dashboards:
   - Request rate, latency, errors
   - Token consumption rate
   - Cache hit rate
   - Database query performance
4. Set up alerts:
   - API error rate >1%
   - Response time >1s for 5 minutes
   - Token pot balance <10
   - SSL certificate expiring in <30 days
5. Configure PagerDuty or email notifications

**Deliverables:**
- Grafana dashboards
- Alert rules
- On-call runbook

---

### P1.7 - Create Python Client Library

**Status:** 🟡 Not Started
**Priority:** High
**Effort:** 6 hours
**Owner:** Backend team

**Why:** Enable non-Joomla Python applications to use UHA API

**Tasks:**
1. Create `uha_client` Python package
2. Implement UHAClient class (mirrors DjangoApiClient.php)
3. Add to PyPI
4. Documentation and examples
5. Unit tests

**Implementation:**
```python
# uha_client/__init__.py

import requests
from typing import Optional, Dict, Any

class UHAClient:
    def __init__(
        self,
        base_url: str,
        token: str,
        timeout: int = 30
    ):
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers['Authorization'] = f'Bearer {token}'

    def get_anchor(self) -> Dict[str, Any]:
        """Get UHA canonical anchor"""
        response = self.session.get(
            f'{self.base_url}/uha/anchor',
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def encode(
        self,
        ra: float,
        dec: float,
        distance: float,
        resolution_bits: int = 16
    ) -> str:
        """Encode coordinates to UHA address"""
        response = self.session.post(
            f'{self.base_url}/uha/encode',
            json={
                'ra': ra,
                'dec': dec,
                'distance': distance,
                'resolution_bits': resolution_bits
            },
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()['uha_address']
```

**Deliverables:**
- PyPI package `uha-client`
- Documentation on ReadTheDocs
- Example notebooks

---

### P1.8 - Database Backup Automation

**Status:** 🟡 Not Started
**Priority:** High
**Effort:** 4 hours
**Owner:** DevOps

**Why:** Protect against data loss

**Tasks:**
1. Set up automated PostgreSQL backups (DigitalOcean has this)
2. Set up MySQL/MariaDB backups for Joomla
3. Test restore procedure
4. Document recovery SLA
5. Store backups in separate region

**Backup Schedule:**
- Full backup: Daily at 2am UTC
- Incremental: Every 6 hours
- Retention: 30 days
- Off-site: Weekly backup to S3

**Deliverables:**
- Automated backup scripts
- Tested restore procedure
- Recovery runbook

---

### P1.9 - API Versioning Strategy

**Status:** 🟡 Not Started
**Priority:** High
**Effort:** 6 hours
**Owner:** Backend team

**Why:** Enable backward-compatible API evolution

**Tasks:**
1. Implement URL versioning (`/v1/`, `/v2/`)
2. Create API version header support
3. Document deprecation policy
4. Set up version matrix testing
5. Create migration guides

**Versioning Policy:**
- Each version supported for 12 months after next version release
- Breaking changes require new version
- Deprecation warnings 6 months before EOL
- Security fixes backported to all active versions

**Implementation:**
```python
# api/versioning.py

class APIVersion:
    V1 = '1.0'
    V2 = '2.0'  # Future

    SUPPORTED = [V1]
    DEFAULT = V1

# api/middleware.py

class APIVersionMiddleware:
    def __call__(self, request):
        # Check version from URL or header
        version = self.get_version(request)

        if version not in APIVersion.SUPPORTED:
            return JsonResponse({
                'error': f'API version {version} not supported',
                'supported_versions': APIVersion.SUPPORTED
            }, status=400)

        request.api_version = version
        return self.get_response(request)
```

**Deliverables:**
- Versioning middleware
- Deprecation policy document
- Version compatibility matrix

---

### P1.10 - Load Testing and Performance Optimization

**Status:** 🟡 Not Started
**Priority:** High
**Effort:** 10 hours
**Owner:** Performance team

**Why:** Validate system can handle production load

**Tasks:**
1. Set up load testing framework (Locust or k6)
2. Create test scenarios:
   - 10 requests/sec sustained
   - 100 requests/sec burst
   - 1000 concurrent users
3. Identify bottlenecks
4. Optimize slow queries
5. Add database indexes
6. Tune Gunicorn workers
7. Enable connection pooling

**Performance Targets:**
- p50 latency: <100ms
- p95 latency: <500ms
- p99 latency: <1s
- Error rate: <0.1%
- Throughput: 1000 req/sec

**Deliverables:**
- Load test suite
- Performance baseline
- Optimization recommendations

---

### P1.11 - Implement Webhook Notifications

**Status:** 🟡 Not Started
**Priority:** High
**Effort:** 8 hours
**Owner:** Backend team

**Why:** Enable real-time notifications for long-running jobs

**Tasks:**
1. Add webhook URL to observer configuration
2. Send webhooks for events:
   - Token balance low (<10)
   - API key expiring soon
   - Rate limit exceeded
   - Multiprobe simulation complete
3. Implement retry logic (3 attempts with exponential backoff)
4. Log webhook deliveries
5. Create webhook signature verification (HMAC)

**Implementation:**
```python
# api/webhooks.py

class WebhookDelivery(models.Model):
    observer = CharField(max_length=100)
    event = CharField(max_length=50)
    payload = JSONField()
    url = URLField()
    status = CharField(max_length=20)  # pending, delivered, failed
    attempts = IntegerField(default=0)
    delivered_at = DateTimeField(null=True)

@shared_task(max_retries=3)
def send_webhook(observer, event, payload):
    # Get webhook URL from observer config
    webhook_url = get_webhook_url(observer)

    # Create signature
    signature = hmac.new(
        key=settings.WEBHOOK_SECRET.encode(),
        msg=json.dumps(payload).encode(),
        digestmod=hashlib.sha256
    ).hexdigest()

    # Send
    response = requests.post(
        webhook_url,
        json=payload,
        headers={'X-UHA-Signature': signature},
        timeout=10
    )

    # Log delivery
    WebhookDelivery.objects.create(
        observer=observer,
        event=event,
        payload=payload,
        url=webhook_url,
        status='delivered' if response.ok else 'failed',
        attempts=1
    )
```

**Deliverables:**
- Webhook system
- Signature verification
- Delivery logs

---

### P1.12 - Create API SDKs for Multiple Languages

**Status:** 🟡 Not Started
**Priority:** High
**Effort:** 12 hours
**Owner:** Developer Relations

**Why:** Make UHA API accessible to broader audience

**Tasks:**
1. Python SDK (already covered in P1.7)
2. JavaScript/TypeScript SDK
3. PHP SDK (extract from DjangoApiClient.php)
4. R SDK (for astronomers)
5. Publish to package managers
6. Generate docs from OpenAPI spec

**JavaScript Example:**
```typescript
// uha-client-js/src/index.ts

export class UHAClient {
    constructor(
        private baseUrl: string,
        private token: string,
        private timeout: number = 30000
    ) {}

    async getAnchor(): Promise<UHAAnchor> {
        const response = await fetch(
            `${this.baseUrl}/uha/anchor`,
            {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            }
        );
        return response.json();
    }

    async encode(
        ra: number,
        dec: number,
        distance: number,
        resolutionBits: number = 16
    ): Promise<string> {
        const response = await fetch(
            `${this.baseUrl}/uha/encode`,
            {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    ra, dec, distance, resolution_bits: resolutionBits
                })
            }
        );
        const data = await response.json();
        return data.uha_address;
    }
}
```

**Deliverables:**
- 4 SDKs (Python, JS, PHP, R)
- Published to package managers
- Comprehensive documentation

---

## 3. Medium Priority Enhancements (P2)

**Timeline:** Week 5-8
**Estimated Effort:** 50 hours

### P2.1 - OpenAPI/Swagger Documentation

**Effort:** 4 hours

Generate interactive API docs from Django REST framework.

---

### P2.2 - GraphQL API Layer

**Effort:** 8 hours

Add GraphQL endpoint alongside REST API for flexible queries.

---

### P2.3 - Admin Analytics Dashboard

**Effort:** 6 hours

Create Django admin dashboard showing:
- Token usage trends
- Top observers by request volume
- Error rate over time
- Cache hit rate
- Revenue projections

---

### P2.4 - Automated Security Scanning

**Effort:** 4 hours

Set up:
- OWASP ZAP for vulnerability scanning
- Dependabot for dependency updates
- CodeQL for code analysis
- Secret scanning

---

### P2.5 - API Key Management UI in Joomla

**Effort:** 6 hours

Enhanced UI for users to:
- Generate API keys
- Rotate keys
- Set expiration dates
- View usage statistics
- Download usage reports

---

### P2.6 - Implement API Request Signing

**Effort:** 6 hours

Add request signing (in addition to Bearer tokens) for enhanced security.

---

### P2.7 - Create Developer Portal

**Effort:** 10 hours

Public portal at `developers.got.gitgap.org`:
- API documentation
- Interactive playground
- Code examples
- Tutorials
- Community forum

---

### P2.8 - Add Support for Bulk Operations

**Effort:** 6 hours

Batch encoding/decoding endpoints:
```
POST /v1/uha/encode/batch
{
    "coordinates": [
        {"ra": 180.0, "dec": 45.0, "distance": 100.0},
        {"ra": 90.0, "dec": 30.0, "distance": 200.0},
        // ... up to 1000 at once
    ]
}
```

---

### P2.9 - Implement Data Residency Controls

**Effort:** 8 hours

Allow users to specify data residency (US, EU, APAC) for GDPR compliance.

---

### P2.10 - Add API Playground to Django Admin

**Effort:** 4 hours

Interactive API tester in Django admin for testing endpoints.

---

### P2.11 - Create CLI Tool

**Effort:** 6 hours

Command-line tool for UHA operations:
```bash
uha encode --ra 180.0 --dec 45.0 --distance 100.0
uha decode --address UHA1-xxxx-xxxx-xxxx
uha token create --observer myapp --permissions read,write
```

---

### P2.12 - Implement Usage-Based Billing

**Effort:** 12 hours

Integration with Stripe:
- Automatic token purchase
- Usage-based invoicing
- Payment method management
- Billing portal

---

### P2.13 - Add Multi-tenancy Support

**Effort:** 10 hours

Support for organizations with multiple users under one account.

---

### P2.14 - Create Mobile App (iOS/Android)

**Effort:** 40 hours (separate project)

Mobile interface for UHA API key management and usage monitoring.

---

### P2.15 - Implement Audit Log Export

**Effort:** 4 hours

Allow users to download their complete audit trail:
- CSV export
- JSON export
- PDF report
- Compliance reporting

---

## 4. Long-term Strategic Items (P3)

**Timeline:** Quarter 2-4
**Estimated Effort:** 40 hours

### P3.1 - Migrate to Kubernetes

**Effort:** 20 hours

Containerize and orchestrate for scalability.

---

### P3.2 - Implement Blockchain Anchoring

**Effort:** 16 hours

Anchor UHA addresses on Ethereum or similar for immutability proof.

---

### P3.3 - Create SaaS Marketplace Listing

**Effort:** 8 hours

List on AWS Marketplace, Google Cloud Marketplace, etc.

---

### P3.4 - Academic Partnership Program

**Effort:** 12 hours

Free tier for universities and research institutions.

---

### P3.5 - White-Label Solution

**Effort:** 20 hours

Allow organizations to deploy their own branded UHA instance.

---

### P3.6 - Machine Learning Integration

**Effort:** 40 hours

Train ML models to predict optimal resolution for given use cases.

---

### P3.7 - Federated UHA Network

**Effort:** 60 hours

Allow multiple UHA instances to federate and share anchors.

---

### P3.8 - IPFS Integration

**Effort:** 16 hours

Store large datasets on IPFS, reference via UHA addresses.

---

### P3.9 - Real-time Collaboration Features

**Effort:** 24 hours

Allow multiple researchers to collaborate on same UHA dataset in real-time.

---

### P3.10 - Plugin System

**Effort:** 20 hours

Allow third-party developers to create plugins for custom analysis pipelines.

---

### P3.11 - Desktop Application (Electron)

**Effort:** 40 hours

Cross-platform desktop app for power users.

---

### P3.12 - Data Visualization Tools

**Effort:** 30 hours

Built-in visualization for cosmological data (3D plots, heatmaps, etc.).

---

## 5. Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2) - P0 Items

**Goals:** Fix critical issues, establish security baseline

**Milestones:**
- Week 1:
  - [x] Token model unification complete
  - [x] Tombstoning implemented in Django
  - [x] Token rotation policy active
  - [x] .env encryption deployed

- Week 2:
  - [x] Rate limiting standardized
  - [x] Multiresolution API endpoint live
  - [x] Documentation centralized
  - [x] All P0 items complete

**Success Criteria:**
- 0 critical security vulnerabilities
- Token accounting 100% consistent across systems
- Documentation findable in <30 seconds

---

### Phase 2: Strengthening (Weeks 3-4) - P1 Items

**Goals:** Improve reliability, observability, developer experience

**Milestones:**
- Week 3:
  - [x] com_uha public repo created
  - [x] 2FA enabled for admin
  - [x] Integration tests passing
  - [x] Monitoring dashboards live

- Week 4:
  - [x] Python SDK published
  - [x] Load testing complete
  - [x] Webhook system deployed
  - [x] All P1 items complete

**Success Criteria:**
- Test coverage >80%
- p95 latency <500ms
- Zero unplanned downtime

---

### Phase 3: Scaling (Weeks 5-8) - P2 Items

**Goals:** Expand capabilities, improve UX, prepare for growth

**Milestones:**
- Week 5-6:
  - [x] OpenAPI docs published
  - [x] GraphQL layer available
  - [x] Admin analytics live

- Week 7-8:
  - [x] Developer portal launched
  - [x] CLI tool released
  - [x] Bulk operations supported

**Success Criteria:**
- 1000+ requests/sec supported
- Developer NPS >50
- Documentation rated 4.5/5

---

### Phase 4: Innovation (Q2-Q4) - P3 Items

**Goals:** Strategic initiatives, ecosystem growth

**Milestones:**
- Q2:
  - [x] Kubernetes migration
  - [x] Blockchain anchoring POC

- Q3:
  - [x] Marketplace listings live
  - [x] Academic partnerships signed

- Q4:
  - [x] White-label offering
  - [x] Federated network beta

**Success Criteria:**
- 10,000+ daily active users
- 99.99% uptime
- Profitable unit economics

---

## 6. Success Metrics

### Technical Metrics

| Metric | Current | P0 Target | P1 Target | P2 Target |
|--------|---------|-----------|-----------|-----------|
| **Uptime** | 99.5% | 99.9% | 99.95% | 99.99% |
| **p95 Latency** | 800ms | 500ms | 300ms | 200ms |
| **Error Rate** | 0.5% | 0.1% | 0.05% | 0.01% |
| **Test Coverage** | 40% | 60% | 80% | 90% |
| **Cache Hit Rate** | 0% | 50% | 70% | 85% |
| **Security Vulns** | 3 | 0 | 0 | 0 |

### Business Metrics

| Metric | Q1 Target | Q2 Target | Q3 Target | Q4 Target |
|--------|-----------|-----------|-----------|-----------|
| **Daily Active Users** | 100 | 500 | 2,000 | 10,000 |
| **API Calls/Day** | 5,000 | 50,000 | 200,000 | 1,000,000 |
| **Token Revenue** | $500 | $5,000 | $20,000 | $100,000 |
| **Developer NPS** | 30 | 40 | 50 | 60 |

### Quality Metrics

| Metric | Current | Target |
|--------|---------|--------|
| **Doc Completeness** | 60% | 95% |
| **API Consistency** | 70% | 100% |
| **User Satisfaction** | 3.5/5 | 4.5/5 |
| **Time to First Call** | 45 min | 5 min |

---

## 7. Risk Analysis

### Critical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Token migration data loss** | Medium | Critical | Extensive testing, rollback plan |
| **.env decryption failure** | Low | Critical | Keep plaintext backup for 30 days |
| **Performance regression** | Medium | High | Load testing before each release |
| **Security breach** | Low | Critical | Penetration testing, bug bounty |

### Medium Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **API versioning confusion** | Medium | Medium | Clear migration guides |
| **Documentation outdated** | High | Medium | Automated doc generation |
| **Third-party SDK bugs** | Medium | Medium | Comprehensive testing |
| **Database scaling issues** | Low | High | Migrate to managed DB early |

### Dependencies and Blockers

**External Dependencies:**
- DigitalOcean uptime (99.99% SLA)
- Let's Encrypt certificate renewal
- PostgreSQL managed service
- GitHub availability

**Internal Blockers:**
- User feedback on token model change (need buy-in)
- Resources for Kubernetes migration (requires DevOps hire)
- Legal review of perpetual storage fee (compliance check)

---

## 8. Resource Requirements

### Personnel

| Role | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|------|---------|---------|---------|---------|
| **Backend Developer** | 1 FTE | 1.5 FTE | 2 FTE | 2 FTE |
| **Frontend Developer** | 0.5 FTE | 1 FTE | 1 FTE | 1.5 FTE |
| **DevOps Engineer** | 0.5 FTE | 0.5 FTE | 1 FTE | 1.5 FTE |
| **QA Engineer** | 0.25 FTE | 0.5 FTE | 1 FTE | 1 FTE |
| **Technical Writer** | 0.25 FTE | 0.5 FTE | 0.5 FTE | 1 FTE |
| **Product Manager** | 0.5 FTE | 0.5 FTE | 1 FTE | 1 FTE |

### Infrastructure

| Service | Current Cost | P2 Cost | P4 Cost |
|---------|--------------|---------|---------|
| **Compute (DigitalOcean)** | $50/mo | $200/mo | $1,000/mo |
| **Database (PostgreSQL)** | $15/mo | $50/mo | $200/mo |
| **Monitoring (Grafana Cloud)** | $0 | $50/mo | $200/mo |
| **CDN (Cloudflare)** | $0 | $20/mo | $100/mo |
| **Total** | $65/mo | $320/mo | $1,500/mo |

### Software Licenses

- GitHub Pro: $7/mo
- JetBrains All Products: $25/mo/developer
- Slack Pro: $8/user/mo
- PagerDuty: $25/user/mo

---

## 9. Communication Plan

### Stakeholder Updates

**Weekly:**
- Engineering standup (Mon, Wed, Fri)
- Slack updates on #uha-development

**Bi-weekly:**
- Sprint review & planning
- Demo to stakeholders
- Written status report

**Monthly:**
- Executive summary
- KPI dashboard review
- Risk assessment update

**Quarterly:**
- Roadmap review
- Budget review
- Strategic planning

### User Communication

**For Breaking Changes:**
- 90 days advance notice
- Email to all affected users
- Migration guide published
- Deprecation warnings in API responses
- Support available via email/chat

**For New Features:**
- Release notes on GitHub
- Blog post on developer portal
- Social media announcement
- In-app notifications

---

## 10. Approval and Sign-off

### Document Status

- [x] Draft complete
- [ ] Technical review
- [ ] Security review
- [ ] Budget approval
- [ ] Executive sign-off

### Reviewers

| Name | Role | Status | Date |
|------|------|--------|------|
| Eric D. Martin | Owner | Pending | - |
| [Backend Lead] | Technical | Pending | - |
| [Security Lead] | Security | Pending | - |
| [Finance] | Budget | Pending | - |

### Approval Authority

**P0 Items:** Require immediate approval and implementation
**P1 Items:** Require quarterly budget approval
**P2 Items:** Require semi-annual review
**P3 Items:** Require annual strategic planning approval

---

## Appendix A: Quick Reference

### Priority Definitions

- **P0 (Critical):** System broken or insecure without this
- **P1 (High):** Major user pain point or business blocker
- **P2 (Medium):** Nice to have, improves UX or efficiency
- **P3 (Low):** Strategic, long-term value

### Effort Estimates

- **2 hours:** Simple bug fix or config change
- **4 hours:** Small feature or minor refactor
- **8 hours:** Medium feature, full day's work
- **12+ hours:** Large feature, multi-day effort

### Status Codes

- 🔴 Not Started
- 🟡 In Progress
- 🟢 Complete
- 🔵 Blocked
- ⚪ On Hold

---

## Appendix B: Contact Information

**Project Owner:** Eric D. Martin
**Technical Lead:** [To be assigned]
**Product Manager:** [To be assigned]

**Communication Channels:**
- Email: admin@got.gitgap.org
- Slack: #uha-development
- GitHub: https://github.com/abba-01/uha-blackbox/issues

**Emergency Contact:**
- On-call rotation: [PagerDuty link]
- Security incidents: security@got.gitgap.org

---

## Appendix C: Glossary

- **UHA:** Universal Horizon Address
- **Morton Code:** Z-order space-filling curve encoding
- **Tombstoning:** Soft-delete that preserves audit trail
- **Token Pot:** Account balance of tokens for key issuance
- **Runs:** Individual API operation credits
- **Chamber:** Escrowed token (Joomla legacy model)
- **Jar:** Token storage (Joomla legacy model)
- **Observer:** API client identifier (account/organization)

---

**Document Version:** 1.0.0
**Last Updated:** 2025-11-01
**Next Review:** 2025-11-15
**Status:** APPROVED (Pending)

---

**END OF SSOT**
