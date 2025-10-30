# How to Use the Multi-Resolution UHA Endpoint

**Endpoint:** `https://got.gitgap.org/v1/merge/multiresolution/`
**Status:** ✅ LIVE
**Auth:** Token required

---

## Quick Start

### Step 1: Get an API Token

First, create an API token on the server:

```bash
ssh root@got.gitgap.org
cd /opt/uha_service
source venv/bin/activate
python manage.py shell
```

Then in the Python shell:

```python
from api.models import ServiceToken

# Create a token
token = ServiceToken.objects.create(
    observer="your_name_or_institution",
    permissions="read,write",
    is_active=True,
    daily_limit=1000,  # Adjust as needed
    notes="Multi-resolution testing"
)

print(f"Your token: {token.token}")
# Copy this token - you'll need it!
```

Save the token somewhere secure.

---

## Step 2: Prepare Your Data

You need two MCMC chains in the format:

**Planck chain:** `[[H0, Omega_m, ...], [H0, Omega_m, ...], ...]`
**SH0ES chain:** `[[H0, ra, dec, distance, ...], [H0, ra, dec, distance, ...], ...]`

### Example: Generate Test Data

```python
import numpy as np

# Mock Planck MCMC chain (1000 samples)
planck_chain = np.column_stack([
    np.random.normal(67.4, 0.5, 1000),   # H0
    np.random.normal(0.315, 0.005, 1000) # Omega_m
])

# Mock SH0ES MCMC chain (1000 samples)
shoes_chain = np.column_stack([
    np.random.normal(73.04, 1.04, 1000),  # H0
    np.random.uniform(0, 360, 1000),      # RA (degrees)
    np.random.uniform(-90, 90, 1000),     # Dec (degrees)
    np.random.uniform(10, 200, 1000)      # Distance (Mpc)
])

# Convert to lists for JSON
planck_list = planck_chain.tolist()
shoes_list = shoes_chain.tolist()
```

---

## Step 3: Call the API

### Python Example (Recommended)

```python
import requests
import numpy as np

# Your API token
API_TOKEN = "your_token_from_step1"

# Prepare your chains (use real data here)
planck_chain = np.random.normal(67.4, 0.5, (1000, 2))  # Replace with real data
shoes_chain = np.random.normal(73.04, 1.04, (1000, 4))  # Replace with real data

# Build request
payload = {
    "planck_chain": planck_chain.tolist(),
    "shoes_chain": shoes_chain.tolist(),
    "cosmo_params_planck": {
        "h0": 67.4,
        "omega_m": 0.315,
        "omega_lambda": 0.685
    },
    "cosmo_params_shoes": {
        "h0": 73.04,
        "omega_m": 0.300,
        "omega_lambda": 0.700
    },
    "resolution_schedule": [8, 12, 16, 20, 24, 28, 32]  # Optional
}

# Call API
response = requests.post(
    'https://got.gitgap.org/v1/merge/multiresolution/',
    json=payload,
    headers={
        'Authorization': f'Token {API_TOKEN}',
        'Content-Type': 'application/json'
    },
    timeout=60  # Allow time for computation
)

# Check result
if response.status_code == 200:
    result = response.json()

    print("=" * 60)
    print("Multi-Resolution Tensor Calibration Results")
    print("=" * 60)
    print(f"Success: {result['success']}")
    print(f"Convergence: {result['convergence_achieved']}")
    print(f"Final Resolution: {result['final_resolution_bits']} bits")
    print(f"Final Δ_T: {result['final_delta_t']:.4f}")
    print(f"Final Gap: {result['final_gap_km_s_mpc']:.2f} km/s/Mpc")
    print(f"Concordance: {result['final_concordance_pct']:.1f}%")
    print()
    print(f"Merged H₀: {result['merged_h0']:.2f} ± {result['merged_uncertainty']:.2f} km/s/Mpc")
    print(f"Interval: [{result['merged_interval_low']:.2f}, {result['merged_interval_high']:.2f}]")
    print()
    print("Resolution Progression:")
    for res in result['results_by_resolution']:
        print(f"  {res['resolution_bits']:2d}-bit: "
              f"Δ_T={res['delta_t']:.4f}, "
              f"Gap={res.get('gap_km_s_mpc', 0):.2f} km/s/Mpc, "
              f"Cells=(P:{res['n_cells_planck']}, S:{res['n_cells_shoes']})")
else:
    print(f"Error {response.status_code}: {response.text}")
```

### cURL Example

```bash
# Set your token
export API_TOKEN="your_token_here"

# Make request (with small test data)
curl -X POST https://got.gitgap.org/v1/merge/multiresolution/ \
  -H "Authorization: Token $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "planck_chain": [
      [67.4, 0.315],
      [67.3, 0.316],
      [67.5, 0.314]
    ],
    "shoes_chain": [
      [73.04, 180.0, 45.0, 100.0],
      [73.1, 181.0, 44.5, 99.5],
      [73.0, 179.5, 45.5, 100.5]
    ],
    "resolution_schedule": [8, 12, 16]
  }'
```

**Note:** The cURL example uses minimal data (3 samples) for testing. Real usage requires 100+ samples.

---

## Step 4: Interpret Results

### Response Structure

```json
{
  "success": true,
  "convergence_achieved": true,
  "final_resolution_bits": 32,
  "final_delta_t": 0.0512,
  "final_gap_km_s_mpc": 0.01,
  "final_concordance_pct": 99.8,

  "results_by_resolution": [
    {
      "resolution_bits": 8,
      "cell_size_mpc": 3.90625,
      "delta_t": 1.20,
      "gap_km_s_mpc": 5.42,
      "concordance_pct": 10.0,
      "n_cells_planck": 245,
      "n_cells_shoes": 189,
      "tensor_planck": [0.95, 0.01, -0.02, -0.05],
      "tensor_shoes": [0.78, 0.02, -0.05, 0.50]
    },
    {
      "resolution_bits": 12,
      "cell_size_mpc": 0.244,
      "delta_t": 0.85,
      ...
    },
    ...
  ],

  "merged_h0": 70.22,
  "merged_uncertainty": 0.05,
  "merged_interval_low": 70.17,
  "merged_interval_high": 70.27,
  "processing_time_ms": 4523
}
```

### Key Metrics

- **`convergence_achieved`**: Did the algorithm converge? (Δ_T < 0.15)
- **`final_delta_t`**: Epistemic distance between observer tensors (lower = better)
- **`final_gap_km_s_mpc`**: Remaining H₀ discrepancy
- **`final_concordance_pct`**: How well the measurements agree (higher = better)
- **`merged_h0`**: Final merged Hubble constant
- **`results_by_resolution`**: Progression through spatial scales

### What Good Results Look Like

✅ **Successful Convergence:**
- `convergence_achieved: true`
- `final_delta_t < 0.15`
- `final_concordance_pct > 95%`
- `final_gap_km_s_mpc < 0.5`

⚠️ **Partial Success:**
- `convergence_achieved: false`
- `final_delta_t: 0.2 - 0.5`
- `final_concordance_pct: 70-95%`

❌ **No Convergence:**
- `final_delta_t > 0.6`
- `final_concordance_pct < 70%`
- May need more samples or different resolution schedule

---

## Complete Working Example

```python
#!/usr/bin/env python3
"""
Complete example: Multi-resolution UHA API usage
"""

import requests
import numpy as np
import json

# Configuration
API_TOKEN = "your_token_here"  # Get from Step 1
API_URL = "https://got.gitgap.org/v1/merge/multiresolution/"

def generate_realistic_planck_chain(n_samples=10000):
    """Generate realistic Planck-like MCMC chain"""
    # Correlation between H0 and Omega_m
    h0_base = np.random.normal(67.4, 0.5, n_samples)
    omega_m = 0.315 + 0.6 * (h0_base - 67.4) / 0.5 * 0.005
    omega_m += np.random.normal(0, 0.002, n_samples)

    return np.column_stack([h0_base, omega_m])

def generate_realistic_shoes_chain(n_samples=5000):
    """Generate realistic SH0ES-like MCMC chain"""
    h0 = np.random.normal(73.04, 1.04, n_samples)
    ra = np.random.uniform(0, 360, n_samples)
    dec = np.random.uniform(-90, 90, n_samples)
    distance = np.random.lognormal(np.log(50), 0.5, n_samples)

    return np.column_stack([h0, ra, dec, distance])

def call_multiresolution_api(planck_chain, shoes_chain, token):
    """Call the multi-resolution API"""

    payload = {
        "planck_chain": planck_chain.tolist(),
        "shoes_chain": shoes_chain.tolist(),
        "cosmo_params_planck": {
            "h0": 67.4,
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

    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }

    print("Calling API...")
    print(f"Planck samples: {len(planck_chain)}")
    print(f"SH0ES samples: {len(shoes_chain)}")

    response = requests.post(API_URL, json=payload, headers=headers, timeout=120)

    return response

def main():
    print("=" * 70)
    print("Multi-Resolution Hubble Tension Calibration")
    print("=" * 70)
    print()

    # Generate chains
    print("Generating MCMC chains...")
    planck = generate_realistic_planck_chain(1000)  # Start with 1000 for testing
    shoes = generate_realistic_shoes_chain(500)
    print(f"✓ Planck chain: {planck.shape}")
    print(f"✓ SH0ES chain: {shoes.shape}")
    print()

    # Call API
    response = call_multiresolution_api(planck, shoes, API_TOKEN)

    # Process response
    if response.status_code == 200:
        result = response.json()

        print("=" * 70)
        print("RESULTS")
        print("=" * 70)
        print()

        # Summary
        print(f"Success: {result['success']}")
        print(f"Convergence: {'✓ YES' if result['convergence_achieved'] else '✗ NO'}")
        print(f"Processing time: {result['processing_time_ms']/1000:.2f}s")
        print()

        # Final metrics
        print("Final Metrics:")
        print(f"  Resolution: {result['final_resolution_bits']} bits")
        print(f"  Δ_T (epistemic distance): {result['final_delta_t']:.4f}")
        print(f"  Gap: {result['final_gap_km_s_mpc']:.2f} km/s/Mpc")
        print(f"  Concordance: {result['final_concordance_pct']:.1f}%")
        print()

        # Merged H0
        print("Merged Hubble Constant:")
        print(f"  H₀ = {result['merged_h0']:.2f} ± {result['merged_uncertainty']:.2f} km/s/Mpc")
        print(f"  95% CI: [{result['merged_interval_low']:.2f}, {result['merged_interval_high']:.2f}]")
        print()

        # Resolution progression
        print("Resolution Progression:")
        print(f"{'Bits':<6} {'Cell Size (Mpc)':<18} {'Δ_T':<8} {'Gap (km/s/Mpc)':<16} {'Cells (P/S)'}")
        print("-" * 70)

        for res in result['results_by_resolution']:
            print(f"{res['resolution_bits']:<6} "
                  f"{res['cell_size_mpc']:<18.6f} "
                  f"{res['delta_t']:<8.4f} "
                  f"{res.get('gap_km_s_mpc', 0):<16.2f} "
                  f"{res['n_cells_planck']}/{res['n_cells_shoes']}")

        # Save results
        with open('multiresolution_results.json', 'w') as f:
            json.dump(result, f, indent=2)
        print()
        print("✓ Results saved to: multiresolution_results.json")

    elif response.status_code == 401:
        print("✗ Authentication failed - check your API token")
    elif response.status_code == 400:
        print(f"✗ Bad request: {response.json()}")
    else:
        print(f"✗ Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    main()
```

---

## Advanced Usage

### Custom Resolution Schedule

You can customize which resolutions to test:

```python
# Fast (fewer resolutions)
"resolution_schedule": [8, 16, 24, 32]

# Standard (default)
"resolution_schedule": [8, 12, 16, 20, 24, 28, 32]

# Very fine (more resolutions)
"resolution_schedule": [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]
```

### Batch Processing

Process multiple chain pairs:

```python
chains_to_process = [
    (planck_chain1, shoes_chain1, "Run 1"),
    (planck_chain2, shoes_chain2, "Run 2"),
    (planck_chain3, shoes_chain3, "Run 3"),
]

for planck, shoes, label in chains_to_process:
    print(f"\nProcessing: {label}")
    response = call_multiresolution_api(planck, shoes, API_TOKEN)
    # ... process response
```

---

## Troubleshooting

### Error: "Authentication credentials were not provided"

**Solution:** Make sure you're sending the Authorization header:
```python
headers={'Authorization': f'Token {YOUR_TOKEN}'}
```

### Error: "Planck chain must have at least 100 samples"

**Solution:** Your chains are too small. Minimum 100 samples required:
```python
planck_chain = generate_chain(n_samples=100)  # At least 100
```

### Error: "Planck chain cannot exceed 50,000 samples"

**Solution:** Chains too large. Downsample:
```python
if len(planck_chain) > 50000:
    indices = np.random.choice(len(planck_chain), 50000, replace=False)
    planck_chain = planck_chain[indices]
```

### Timeout Errors

**Solution:** Increase timeout or reduce chain size:
```python
response = requests.post(..., timeout=180)  # 3 minutes
```

### Service Unreachable

**Check server status:**
```bash
ssh root@got.gitgap.org "systemctl status uha_service"
```

---

## For Publication

When referencing this method in papers:

```latex
Systematic bias correction was performed using the multi-resolution
Universal Horizon Address (UHA) tensor calibration method
\citep{Martin2025_UHA}. The implementation is available via
authenticated API access at \url{https://got.gitgap.org/v1/merge/multiresolution/}.
Contact the authors for API credentials.

The method employs progressive spatial refinement from coarse (8-bit)
to fine (32-bit) Morton encoding precision, capturing systematic biases
from local ($<1$ Mpc) to global ($>100$ Mpc) scales \citep{Martin2025_UHA_Patent}.
```

**Citation:**
```
Martin, E.D. (2025). Multi-Resolution Universal Horizon Address System
for Cosmological Systematic Bias Correction. Patent US 63/902,536.
```

---

## Support

**Questions?** Contact: support@aybllc.org

**Bug reports:** Include:
- Your API token (first 8 characters only)
- Error message
- Chain sizes
- Timestamp

**Need more quota?** Email with:
- Your observer name
- Current daily limit
- Requested limit
- Use case description

---

## Next Steps

1. **Get your API token** (Step 1 above)
2. **Test with small data** (100-1000 samples)
3. **Run with real chains** (10,000+ samples)
4. **Analyze results**
5. **Include in publication**

**The multi-resolution endpoint is ready to use!** 🚀
