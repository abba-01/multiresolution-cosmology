# UHA Encoder API Notice

## Patent-Protected Technology

The **Universal Horizon Address (UHA)** multi-resolution encoding system is **patent-protected** intellectual property. The core encoding implementation is **NOT** included in this public repository.

### Access Options

**1. API Access (Public)**
- Production API: `https://api.aybllc.org/v1/uha/encode`
- Test endpoint: `https://got.gitgap.org/uha/encode`
- Free tier: 1000 requests/month
- Documentation: https://api.aybllc.org/docs

**2. Commercial Licensing**
- Contact: info@allyourbaseline.com
- Full source code access available under license
- Custom deployment options available

**3. Academic Research**
- Limited research licenses available
- Contact for academic pricing

### Example API Usage

```python
import requests

def encode_position_via_api(ra_deg, dec_deg, distance_mpc, resolution_bits):
    """Encode position using UHA API"""
    response = requests.post(
        'https://api.aybllc.org/v1/uha/encode',
        json={
            'ra_deg': ra_deg,
            'dec_deg': dec_deg,
            'distance_mpc': distance_mpc,
            'resolution_bits': resolution_bits,
            'scale_factor': 1.0,
            'cosmo_params': {
                'h0': 67.36,
                'omega_m': 0.315,
                'omega_lambda': 0.685
            }
        },
        headers={'Authorization': f'Bearer {YOUR_API_KEY}'}
    )
    return response.json()

# Example
result = encode_position_via_api(
    ra_deg=184.74,
    dec_deg=47.30,
    distance_mpc=7.60,
    resolution_bits=32
)

print(f"UHA Code: {result['uha_code']}")
print(f"Cell size: {result['cell_size_mpc']} Mpc")
```

### What's Public vs. Private

**Public (in this repo):**
- ✅ Analysis framework and validation methods
- ✅ Test suites and falsification predictions
- ✅ Real data validation pipeline (stub)
- ✅ Scientific methodology and results
- ✅ Documentation and papers

**Private (patent-protected):**
- ❌ UHA encoding/decoding implementation
- ❌ Morton Z-order curve algorithms
- ❌ Observer tensor extraction
- ❌ Epistemic distance computation
- ❌ Multi-resolution refinement engine

### Patent Information

**Patent Pending**: Multi-Resolution Universal Horizon Address System
- Application filed: 2025
- Inventors: Eric D. Martin, et al.
- Owner: All Your Baseline LLC

### Citation

If you use the UHA API or methodology in your research, please cite:

```bibtex
@misc{uha2025,
  title={Universal Horizon Address: Multi-Resolution Spatial Encoding for Cosmology},
  author={Martin, Eric D.},
  year={2025},
  note={Patent pending}
}
```

### Questions?

- **API Support**: api-support@allyourbaseline.com
- **Licensing**: info@allyourbaseline.com
- **Technical**: github.com/abba-01/multiresolution-cosmology/issues
