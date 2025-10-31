#!/usr/bin/env python3
"""
Create Simulated HSC-Y3 Data
For cross-validation testing while awaiting real data access

REFACTORED: Now uses centralized SSOT configuration

Based on:
- Published HSC-Y3 S₈ (from centralized config)
- 4 tomographic bins (z = 0.3-1.5)

Author: Eric D. Martin (All Your Baseline LLC)
Date: 2025-10-30
"""

import numpy as np
import json

# Import centralized constants (SSOT)
from config.surveys import HSC_S8

# HSC-Y3 configuration
HSC_S8_PUBLISHED = HSC_S8
HSC_S8_SIGMA = 0.033

# Tomographic bins (z ranges)
Z_BINS = [
    (0.3, 0.6),
    (0.6, 0.9),
    (0.9, 1.2),
    (1.2, 1.5)
]

# Angular scales - HSC typically uses wider range
THETA_MIN = 2.0
THETA_MAX = 300.0
N_THETA_BINS = 18


def generate_correlation_function(theta_arcmin, z_eff, S8=None):
    """
    Generate realistic HSC cosmic shear correlation function.

    Args:
        theta_arcmin: Angular scales in arcminutes
        z_eff: Effective redshift
        S8: Structure growth parameter (defaults to HSC published value)

    Returns:
        (xi_plus, xi_minus)
    """
    if S8 is None:
        S8 = HSC_S8_PUBLISHED

    theta_norm = theta_arcmin / 10.0
    amplitude = (S8 / 0.8)**2 * (1 + z_eff)**0.5 * 1e-3

    # ξ+ (E-mode)
    xi_plus = amplitude * (theta_norm**(-0.8)) * np.exp(-theta_norm / 30.0)

    # ξ- (B-mode)
    xi_minus = amplitude * 0.3 * (theta_norm**(-0.6)) * np.exp(-theta_norm / 40.0)

    # Add noise
    noise_level = amplitude * 0.05
    xi_plus += np.random.normal(0, noise_level, size=len(theta_arcmin))
    xi_minus += np.random.normal(0, noise_level, size=len(theta_arcmin))
    xi_minus *= np.random.choice([-1, 1], size=len(theta_arcmin))

    return xi_plus, xi_minus


def create_simulated_hsc_data():
    """Create simulated HSC-Y3 data"""

    print("="*80)
    print("CREATING SIMULATED HSC-Y3 DATA")
    print("="*80)

    theta_arcmin = np.logspace(
        np.log10(THETA_MIN),
        np.log10(THETA_MAX),
        N_THETA_BINS
    )

    print(f"\nAngular scales: {THETA_MIN:.1f} - {THETA_MAX:.1f} arcmin")
    print(f"Number of bins: {N_THETA_BINS}")
    print(f"Target S₈: {HSC_S8_PUBLISHED} ± {HSC_S8_SIGMA}")

    bins_data = {}

    for bin_idx, (z_low, z_high) in enumerate(Z_BINS):
        z_eff = (z_low + z_high) / 2.0

        xi_plus, xi_minus = generate_correlation_function(
            theta_arcmin, z_eff, S8=HSC_S8_PUBLISHED
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
        'survey': 'HSC-Y3',
        'reference': 'Dalal et al. 2023, PRD 108, 123519',
        'data_type': 'SIMULATED',
        'note': 'Simulated data for cross-validation. Replace with real data when available.',
        'n_bins': len(bins_data),
        'published_S8': HSC_S8_PUBLISHED,
        'published_S8_sigma': HSC_S8_SIGMA,
        'bins': bins_data
    }

    output_file = "hsc_y3_parsed.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n{'='*80}")
    print(f"✅ Simulated data saved to: {output_file}")
    print(f"{'='*80}")

    print(f"\nTotal measurements: {N_THETA_BINS} per bin")
    print(f"Total data points: {2 * N_THETA_BINS * len(Z_BINS)} (ξ+ and ξ-)")
    print(f"\n⚠️  Replace with real HSC-Y3 data for publication")


if __name__ == '__main__':
    np.random.seed(43)  # Different seed from DES
    create_simulated_hsc_data()

    print("""
================================================================================
NEXT STEPS
================================================================================

1. Run HSC-Y3 analysis with h32:
   python3 hsc_y3_real_analysis.py

2. Compare all three surveys:
   python3 compare_three_surveys.py

================================================================================
""")
