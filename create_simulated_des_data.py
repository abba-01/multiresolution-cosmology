#!/usr/bin/env python3
"""
Create Simulated DES-Y3 Data
For cross-validation testing while awaiting real data access

Based on:
- Published DES-Y3 S₈ = 0.776 ± 0.017
- Expected correlation function shape
- 4 tomographic bins matching DES-Y3 structure
"""

import numpy as np
import json


# DES-Y3 configuration
DES_S8_PUBLISHED = 0.776
DES_S8_SIGMA = 0.017

# Tomographic bins (z ranges)
Z_BINS = [
    (0.2, 0.4),
    (0.4, 0.6),
    (0.6, 0.85),
    (0.85, 1.05)
]

# Angular scales (arcminutes) - typical for DES
THETA_MIN = 2.5
THETA_MAX = 250.0
N_THETA_BINS = 20


def generate_correlation_function(theta_arcmin, z_eff, S8=0.776):
    """
    Generate realistic-looking cosmic shear correlation function.

    ξ+(θ) has general shape:
    - Positive at small θ (few arcmin)
    - Decreases with θ
    - Can go negative at large θ

    Args:
        theta_arcmin: Angular scales in arcminutes
        z_eff: Effective redshift
        S8: Structure growth parameter

    Returns:
        (xi_plus, xi_minus)
    """

    # Convert to dimensionless scale
    theta_norm = theta_arcmin / 10.0  # Normalize to 10 arcmin

    # ξ+ model: power law with exponential cutoff
    # Amplitude scales with S8^2 and redshift
    amplitude = (S8 / 0.8)**2 * (1 + z_eff)**0.5 * 1e-3

    # ξ+ (E-mode): positive at small scales, decreases
    xi_plus = amplitude * (theta_norm**(-0.8)) * np.exp(-theta_norm / 30.0)

    # ξ- (B-mode should be ~0, but small-scale systematics):
    # Smaller amplitude, different slope
    xi_minus = amplitude * 0.3 * (theta_norm**(-0.6)) * np.exp(-theta_norm / 40.0)

    # Add realistic noise
    noise_level = amplitude * 0.05
    xi_plus += np.random.normal(0, noise_level, size=len(theta_arcmin))
    xi_minus += np.random.normal(0, noise_level, size=len(theta_arcmin))

    # ξ- can be positive or negative (should average ~0 for no systematics)
    xi_minus *= np.random.choice([-1, 1], size=len(theta_arcmin))

    return xi_plus, xi_minus


def create_simulated_des_data():
    """Create simulated DES-Y3 data matching published structure"""

    print("="*80)
    print("CREATING SIMULATED DES-Y3 DATA")
    print("="*80)

    # Angular scales (log-spaced)
    theta_arcmin = np.logspace(
        np.log10(THETA_MIN),
        np.log10(THETA_MAX),
        N_THETA_BINS
    )

    print(f"\nAngular scales: {THETA_MIN:.1f} - {THETA_MAX:.1f} arcmin")
    print(f"Number of bins: {N_THETA_BINS}")
    print(f"Target S₈: {DES_S8_PUBLISHED} ± {DES_S8_SIGMA}")

    bins_data = {}

    for bin_idx, (z_low, z_high) in enumerate(Z_BINS):
        z_eff = (z_low + z_high) / 2.0

        # Generate correlation functions
        xi_plus, xi_minus = generate_correlation_function(
            theta_arcmin, z_eff, S8=DES_S8_PUBLISHED
        )

        bins_data[bin_idx] = {
            'z_bin': (z_low, z_high),
            'z_eff': z_eff,
            'theta_arcmin': theta_arcmin.tolist(),
            'xi_plus': xi_plus.tolist(),
            'xi_minus': xi_minus.tolist(),
            'n_points': len(theta_arcmin)
        }

        print(f"\nBin {bin_idx} (z={z_low:.2f}-{z_high:.2f}, z_eff={z_eff:.2f}):")
        print(f"  ξ₊ range: {xi_plus.min():.2e} - {xi_plus.max():.2e}")
        print(f"  ξ₋ range: {xi_minus.min():.2e} - {xi_minus.max():.2e}")
        print(f"  Number of points: {len(theta_arcmin)}")

    # Save to JSON
    output = {
        'survey': 'DES-Y3',
        'reference': 'Abbott et al. 2022, PRD 105, 023520',
        'data_type': 'SIMULATED',
        'note': 'Simulated data for cross-validation testing. Replace with real FITS data when available.',
        'n_bins': len(bins_data),
        'published_S8': DES_S8_PUBLISHED,
        'published_S8_sigma': DES_S8_SIGMA,
        'bins': bins_data
    }

    output_file = "des_y3_parsed.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n{'='*80}")
    print(f"✅ Simulated data saved to: {output_file}")
    print(f"{'='*80}")

    print(f"\nTotal measurements: {N_THETA_BINS} per bin")
    print(f"Total data points: {2 * N_THETA_BINS * len(Z_BINS)} (ξ+ and ξ-)")
    print(f"\nThis simulated data can be used for:")
    print("  1. Testing the analysis pipeline")
    print("  2. Cross-validation with KiDS-1000 pattern")
    print("  3. Demonstrating h32 resolution analysis")
    print("\n⚠️  Replace with real DES-Y3 FITS data for publication")


if __name__ == '__main__':
    np.random.seed(42)  # Reproducible results
    create_simulated_des_data()

    print("""
================================================================================
NEXT STEPS
================================================================================

1. Run DES-Y3 analysis with h32:
   python3 des_y3_real_analysis.py

2. Compare with KiDS-1000 pattern

3. When real DES data is available:
   - Run: python3 parse_des_y3_data.py
   - This will overwrite des_y3_parsed.json with real data
   - Re-run: python3 des_y3_real_analysis.py

================================================================================
""")
