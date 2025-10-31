"""
Multi-Resolution UHA Encoding Endpoint
=======================================

NEW API endpoint for /v1/merge/multiresolution

REFACTORED: Now uses centralized SSOT configuration

This keeps the multi-resolution implementation server-side (proprietary),
exposing only an API interface for researchers.

Deploy to: /got/uha-api-service/app/multiresolution.py

Author: Eric D. Martin (All Your Baseline LLC)
Date: 2025-10-30
"""

from typing import List, Dict, Optional, Tuple
from pydantic import BaseModel, Field
import numpy as np

# Import centralized constants (SSOT)
from config.constants import PLANCK_H0, PLANCK_OMEGA_M, PLANCK_OMEGA_LAMBDA, SHOES_H0


# ============================================================================
# Request/Response Models
# ============================================================================

class MultiResolutionRequest(BaseModel):
    """Request for multi-resolution tensor calibration."""

    planck_chain: List[List[float]] = Field(
        ...,
        description="Planck MCMC chain [[H0, Omega_m, ...], ...]",
        min_items=100,
        max_items=50000
    )

    shoes_chain: List[List[float]] = Field(
        ...,
        description="SH0ES MCMC chain [[H0, ra, dec, dist, ...], ...]",
        min_items=100,
        max_items=50000
    )

    cosmo_params_planck: Dict[str, float] = Field(
        default={'h0': PLANCK_H0, 'omega_m': PLANCK_OMEGA_M, 'omega_lambda': PLANCK_OMEGA_LAMBDA},
        description="Planck cosmological parameters"
    )

    cosmo_params_shoes: Dict[str, float] = Field(
        default={'h0': SHOES_H0, 'omega_m': 0.300, 'omega_lambda': 0.700},
        description="SH0ES cosmological parameters"
    )

    resolution_schedule: Optional[List[int]] = Field(
        default=None,
        description="Custom resolution schedule (bits per dimension). Default: [8, 12, 16, 20, 24, 28, 32]"
    )


class ResolutionResult(BaseModel):
    """Results at a single resolution level."""

    resolution_bits: int
    cell_size_mpc: float
    delta_t: float
    gap_km_s_mpc: float
    concordance_pct: float
    n_cells_planck: int
    n_cells_shoes: int
    tensor_planck: List[float]
    tensor_shoes: List[float]


class MultiResolutionResponse(BaseModel):
    """Response from multi-resolution calibration."""

    success: bool
    convergence_achieved: bool
    final_resolution_bits: int
    final_delta_t: float
    final_gap_km_s_mpc: float
    final_concordance_pct: float

    results_by_resolution: List[ResolutionResult]

    merged_h0: float
    merged_uncertainty: float
    merged_interval_low: float
    merged_interval_high: float

    processing_time_ms: int


# ============================================================================
# Core Implementation (Proprietary)
# ============================================================================

def multiresolution_tensor_calibration(
    planck_chain: np.ndarray,
    shoes_chain: np.ndarray,
    cosmo_params_planck: dict,
    cosmo_params_shoes: dict,
    resolution_schedule: List[int] = None
) -> Tuple[bool, Dict]:
    """
    Perform multi-resolution tensor calibration.

    PROPRIETARY IMPLEMENTATION
    This function contains the patented multi-resolution algorithm.

    Args:
        planck_chain: Planck MCMC samples
        shoes_chain: SH0ES MCMC samples
        cosmo_params_planck: Planck cosmology
        cosmo_params_shoes: SH0ES cosmology
        resolution_schedule: Bits per dimension at each level

    Returns:
        Tuple of (converged, results_dict)
    """
    if resolution_schedule is None:
        resolution_schedule = [8, 12, 16, 20, 24, 28, 32]

    results = []
    converged = False

    # Import proprietary implementation
    # (In actual deployment, this would be a compiled binary)
    from .multiresolution_core import (
        encode_uha_batch,
        compute_spatial_distribution,
        extract_tensor_from_spatial,
        compute_epistemic_distance
    )

    for res_bits in resolution_schedule:
        # Encode chains at current resolution
        uha_planck = encode_uha_batch(
            planck_chain,
            morton_bits=res_bits,
            cosmo_params=cosmo_params_planck
        )

        uha_shoes = encode_uha_batch(
            shoes_chain,
            morton_bits=res_bits,
            cosmo_params=cosmo_params_shoes
        )

        # Compute spatial distributions
        spatial_planck = compute_spatial_distribution(uha_planck, res_bits)
        spatial_shoes = compute_spatial_distribution(uha_shoes, res_bits)

        # Extract tensors
        tensor_planck = extract_tensor_from_spatial(
            spatial_planck, planck_chain, method='cmb'
        )
        tensor_shoes = extract_tensor_from_spatial(
            spatial_shoes, shoes_chain, method='shoes'
        )

        # Compute metrics
        delta_t = compute_epistemic_distance(
            tensor_planck, tensor_shoes, res_bits
        )

        # Merge H0 values with epistemic correction
        h0_planck = np.mean(planck_chain[:, 0])
        h0_shoes = np.mean(shoes_chain[:, 0])

        # Apply epistemic distance as correction factor
        epistemic_correction = delta_t * abs(h0_planck - h0_shoes)
        merged_h0 = (h0_planck + h0_shoes) / 2.0
        merged_unc = epistemic_correction / 2.0

        gap = abs(h0_planck - h0_shoes)
        concordance = max(0, (1 - gap / 6.0) * 100)  # Simple concordance metric

        cell_size = 1000.0 / (2 ** res_bits)

        results.append({
            'resolution_bits': res_bits,
            'cell_size_mpc': cell_size,
            'delta_t': delta_t,
            'gap_km_s_mpc': gap,
            'concordance_pct': concordance,
            'n_cells_planck': spatial_planck.n_cells,
            'n_cells_shoes': spatial_shoes.n_cells,
            'tensor_planck': tensor_planck.to_array().tolist(),
            'tensor_shoes': tensor_shoes.to_array().tolist(),
            'merged_h0': merged_h0,
            'merged_uncertainty': merged_unc
        })

        # Check convergence
        if delta_t < 0.15 and concordance > 95.0:
            converged = True
            break

    return converged, {
        'results': results,
        'final': results[-1] if results else None
    }


# ============================================================================
# FastAPI Endpoint Handler
# ============================================================================

def perform_multiresolution_merge(request: MultiResolutionRequest) -> MultiResolutionResponse:
    """
    API endpoint handler for multi-resolution merge.

    This is the public interface. Implementation details are proprietary.
    """
    import time
    start_time = time.time()

    # Convert to numpy arrays
    planck_chain = np.array(request.planck_chain)
    shoes_chain = np.array(request.shoes_chain)

    # Perform multi-resolution calibration
    converged, results_dict = multiresolution_tensor_calibration(
        planck_chain,
        shoes_chain,
        request.cosmo_params_planck,
        request.cosmo_params_shoes,
        request.resolution_schedule
    )

    processing_time_ms = int((time.time() - start_time) * 1000)

    # Extract final results
    final = results_dict['final']

    # Build response
    return MultiResolutionResponse(
        success=True,
        convergence_achieved=converged,
        final_resolution_bits=final['resolution_bits'],
        final_delta_t=final['delta_t'],
        final_gap_km_s_mpc=final['gap_km_s_mpc'],
        final_concordance_pct=final['concordance_pct'],
        results_by_resolution=[
            ResolutionResult(**r) for r in results_dict['results']
        ],
        merged_h0=final['merged_h0'],
        merged_uncertainty=final['merged_uncertainty'],
        merged_interval_low=final['merged_h0'] - final['merged_uncertainty'],
        merged_interval_high=final['merged_h0'] + final['merged_uncertainty'],
        processing_time_ms=processing_time_ms
    )


# ============================================================================
# Add to main.py
# ============================================================================

"""
Add this to /got/uha-api-service/app/main.py:

from .multiresolution import perform_multiresolution_merge, MultiResolutionRequest, MultiResolutionResponse

@app.post("/v1/merge/multiresolution", response_model=MultiResolutionResponse, tags=["Merge"])
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def multiresolution_merge(
    request: Request,
    merge_request: MultiResolutionRequest,
    key_info: dict = Depends(get_api_key)
):
    '''
    Multi-resolution tensor calibration for Hubble tension resolution

    Performs progressive refinement through spatial resolution hierarchy,
    capturing systematic biases from local (<1 Mpc) to global (>100 Mpc) scales.

    **Requires:** Premium API key tier (contact support@aybllc.org)

    **Example:**
    ```json
    {
      "planck_chain": [[67.36, 0.315, ...], ...],
      "shoes_chain": [[73.04, 180.0, 45.0, 100.0, ...], ...],
      "resolution_schedule": [8, 12, 16, 20, 24, 28, 32]
    }
    ```
    '''
    return perform_multiresolution_merge(merge_request)
"""


# ============================================================================
# Client Example (Public)
# ============================================================================

"""
Example client usage (researchers can use this):

```python
import requests
import numpy as np

# Generate or load your MCMC chains
planck_chain = generate_planck_chain(n=10000)  # Your data
shoes_chain = generate_shoes_chain(n=5000)     # Your data

# Prepare request
payload = {
    "planck_chain": planck_chain.tolist(),
    "shoes_chain": shoes_chain.tolist(),
    "cosmo_params_planck": {
        "h0": 67.36,
        "omega_m": 0.315,
        "omega_lambda": 0.685
    },
    "cosmo_params_shoes": {
        "h0": 73.04,
        "omega_m": 0.300,
        "omega_lambda": 0.700
    },
    "resolution_schedule": [8, 12, 16, 20, 24, 28, 32]
}

# Call API
response = requests.post(
    'https://got.gitgap.org/v1/merge/multiresolution',
    json=payload,
    headers={'X-API-Key': 'your_premium_key_here'}
)

result = response.json()

# Extract results
print(f"Convergence achieved: {result['convergence_achieved']}")
print(f"Final Δ_T: {result['final_delta_t']:.4f}")
print(f"Final gap: {result['final_gap_km_s_mpc']:.2f} km/s/Mpc")
print(f"Concordance: {result['final_concordance_pct']:.1f}%")
print(f"Merged H0: {result['merged_h0']:.2f} ± {result['merged_uncertainty']:.2f}")

# View progression through resolutions
for res_result in result['results_by_resolution']:
    print(f"  {res_result['resolution_bits']}-bit: Δ_T={res_result['delta_t']:.4f}")
```
"""
