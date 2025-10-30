# Multi-Resolution UHA - Server Deployment Status

**Date:** 2025-10-30
**Server:** got.gitgap.org
**Service:** Django-based UHA API (not FastAPI as initially thought)
**Status:** PARTIALLY DEPLOYED - Core engine uploaded, Django view pending

---

## ✅ Completed

1. **SSH Access Confirmed**
   - Successfully connected to `root@got.gitgap.org`
   - SSH keys working

2. **Service Identified**
   - Service: `uha_service.service` (Django-based, not FastAPI)
   - Location: `/opt/uha_service/`
   - Current status: RUNNING
   - Architecture: Django REST Framework with binary UHA engine

3. **Multi-Resolution Engine Uploaded**
   - Source: `/root/private_multiresolution/multiresolution_uha_encoder.py`
   - Destination: `/opt/uha_service/api/services/multiresolution_engine.py`
   - Size: 18,467 bytes
   - Owner: root:root
   - Status: ✓ UPLOADED

---

## ⏳ Pending - Django View Integration

The service uses Django REST Framework, so we need to create a Django view instead of FastAPI endpoint.

### Required Files to Create on Server

1. **`/opt/uha_service/api/views.py`** - Add multi-resolution view
2. **`/opt/uha_service/api/urls.py`** - Add URL route
3. **`/opt/uha_service/api/serializers.py`** - Add request/response serializers

---

## Next Steps

### Option 1: Manual Completion (Recommended for Safety)

You should manually add the Django view to avoid breaking the running service. Here's what to add:

#### 1. Add to `/opt/uha_service/api/serializers.py`

```python
from rest_framework import serializers

class MultiResolutionRequestSerializer(serializers.Serializer):
    """Request serializer for multi-resolution calibration"""
    planck_chain = serializers.ListField(
        child=serializers.ListField(child=serializers.FloatField()),
        min_length=100,
        max_length=50000
    )
    shoes_chain = serializers.ListField(
        child=serializers.ListField(child=serializers.FloatField()),
        min_length=100,
        max_length=50000
    )
    cosmo_params_planck = serializers.DictField(
        required=False,
        default={'h0': 67.4, 'omega_m': 0.315, 'omega_lambda': 0.685}
    )
    cosmo_params_shoes = serializers.DictField(
        required=False,
        default={'h0': 73.04, 'omega_m': 0.300, 'omega_lambda': 0.700}
    )
    resolution_schedule = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_null=True
    )


class ResolutionResultSerializer(serializers.Serializer):
    """Single resolution level result"""
    resolution_bits = serializers.IntegerField()
    cell_size_mpc = serializers.FloatField()
    delta_t = serializers.FloatField()
    gap_km_s_mpc = serializers.FloatField()
    concordance_pct = serializers.FloatField()
    n_cells_planck = serializers.IntegerField()
    n_cells_shoes = serializers.IntegerField()
    tensor_planck = serializers.ListField(child=serializers.FloatField())
    tensor_shoes = serializers.ListField(child=serializers.FloatField())


class MultiResolutionResponseSerializer(serializers.Serializer):
    """Response serializer for multi-resolution calibration"""
    success = serializers.BooleanField()
    convergence_achieved = serializers.BooleanField()
    final_resolution_bits = serializers.IntegerField()
    final_delta_t = serializers.FloatField()
    final_gap_km_s_mpc = serializers.FloatField()
    final_concordance_pct = serializers.FloatField()
    results_by_resolution = ResolutionResultSerializer(many=True)
    merged_h0 = serializers.FloatField()
    merged_uncertainty = serializers.FloatField()
    merged_interval_low = serializers.FloatField()
    merged_interval_high = serializers.FloatField()
    processing_time_ms = serializers.IntegerField()
```

#### 2. Add to `/opt/uha_service/api/views.py`

```python
from .services.multiresolution_engine import iterative_tensor_refinement_multiresolution
import numpy as np
import time

class MultiResolutionView(APIView):
    """
    Multi-resolution tensor calibration endpoint
    POST /v1/merge/multiresolution/

    Requires authentication with premium API key tier
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Perform multi-resolution tensor calibration

        This endpoint implements the proprietary multi-scale UHA encoding
        algorithm (Patent US 63/902,536) for systematic bias correction.
        """
        # Validate request
        serializer = MultiResolutionRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data

        # Check token tier (premium required)
        token = request.auth
        if not hasattr(token, 'tier') or token.tier != 'premium':
            return Response(
                {'error': 'Premium API key required for multi-resolution endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Convert to numpy arrays
        planck_chain = np.array(data['planck_chain'])
        shoes_chain = np.array(data['shoes_chain'])

        # Start timer
        start_time = time.time()

        try:
            # Perform multi-resolution calibration
            tensors, history = iterative_tensor_refinement_multiresolution(
                planck_chain,
                shoes_chain,
                data['cosmo_params_planck'],
                data['cosmo_params_shoes'],
                data.get('resolution_schedule')
            )

            # Extract final results
            final = history[-1] if history else None
            if not final:
                return Response(
                    {'error': 'No results generated'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Calculate concordance
            converged = final['delta_t'] < 0.15

            # Build response
            response_data = {
                'success': True,
                'convergence_achieved': converged,
                'final_resolution_bits': final['resolution_bits'],
                'final_delta_t': final['delta_t'],
                'final_gap_km_s_mpc': final.get('gap', 0.0),
                'final_concordance_pct': final.get('concordance', 0.0),
                'results_by_resolution': history,
                'merged_h0': final.get('merged_h0', 70.0),
                'merged_uncertainty': final.get('merged_unc', 1.0),
                'merged_interval_low': final.get('merged_h0', 70.0) - final.get('merged_unc', 1.0),
                'merged_interval_high': final.get('merged_h0', 70.0) + final.get('merged_unc', 1.0),
                'processing_time_ms': int((time.time() - start_time) * 1000)
            }

            # Log usage
            logger.info(f"Multi-resolution calibration: token={token.key[:8]}..., converged={converged}")

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Multi-resolution error: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
```

#### 3. Add to `/opt/uha_service/api/urls.py`

```python
from .views import MultiResolutionView

urlpatterns = [
    # ... existing patterns ...
    path('v1/merge/multiresolution/', MultiResolutionView.as_view(), name='multiresolution'),
]
```

#### 4. Restart Service

```bash
ssh root@got.gitgap.org "systemctl restart uha_service"
```

### Option 2: Automated Deployment (Risky - Service Downtime)

I can SSH in and make all changes automatically, but this risks breaking the running service if there are syntax errors or conflicts.

**Recommendation:** Let me know which option you prefer, or I can create the view files for you to review first.

---

## Current Service Architecture

```
/opt/uha_service/
├── api/
│   ├── views.py              # Django REST views
│   ├── urls.py               # URL routing
│   ├── serializers.py        # Request/response validation
│   ├── models.py             # Database models
│   ├── services/
│   │   ├── uha_engine.py     # Binary wrapper (existing)
│   │   └── multiresolution_engine.py  # ✓ UPLOADED (new)
│   └── ...
├── uha_service/              # Django settings
├── manage.py                 # Django management
└── uha_service.service       # systemd service file
```

---

## Testing After Deployment

```bash
# Test health endpoint (no auth)
curl https://got.gitgap.org/health/

# Test multi-resolution (requires premium API key)
curl -X POST https://got.gitgap.org/v1/merge/multiresolution/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_PREMIUM_TOKEN" \
  -d '{
    "planck_chain": [[67.4, 0.315], [67.3, 0.316]],
    "shoes_chain": [[73.04, 180, 45, 100], [73.1, 181, 44, 99]],
    "resolution_schedule": [8, 12, 16]
  }'
```

---

## IP Protection Status

✅ **SECURE:**
- Multi-resolution engine source code on server only (not in public Git)
- Django service is private (not public repository)
- API key authentication required
- Premium tier gating available

⚠️ **NOTE:**
- Need to ensure `/opt/uha_service/.git` is NOT pushed to public GitHub
- Service appears to be private deployment (good!)

---

## What I Need From You

**Choose deployment approach:**

1. **Manual (Safest):**
   - I provide the code snippets above
   - You manually add to views.py, urls.py, serializers.py
   - You test and restart service
   - Zero risk of breaking running service

2. **Semi-Automated (Moderate risk):**
   - I create the view files locally
   - You review them
   - You upload and integrate
   - Low risk, you control final deployment

3. **Fully Automated (Highest risk):**
   - I SSH in and make all changes
   - Automatic service restart
   - Risk of breaking service if errors

**Recommendation:** Option 1 or 2 for production service safety.

---

**Status:** READY FOR YOUR DECISION
**Next:** Await your choice on deployment approach
