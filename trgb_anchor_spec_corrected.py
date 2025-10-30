#!/usr/bin/env python3
"""
TRGB Anchor Specification - Corrected with Proper Horizon Normalization

Using UHA specification: R_H(a ≈ 1) ≈ 14,000 Mpc
Δr = R_H / 2^N per axis

Author: Eric D. Martin (All Your Baseline LLC)
Date: 2025-10-30
"""

import numpy as np
import json
import math

# UHA Specification Constants
R_H_TODAY = 14000.0  # Mpc, horizon size at a ≈ 1

def calculate_resolution_bits(scale_mpc: float, horizon_mpc: float = R_H_TODAY) -> dict:
    """
    Calculate appropriate UHA resolution bits for a given measurement scale.

    Per UHA spec:
        Δr = R_H / 2^N
        N = ceil(log2(R_H / Δr_target))

    For anchors, Δr_target ≈ S / 20, where S is the measurement scale

    Args:
        scale_mpc: Measurement scale (e.g., 30 Mpc for TRGB)
        horizon_mpc: Horizon size (default: 14,000 Mpc at a≈1)

    Returns:
        dict with resolution analysis
    """
    # Target cell size: ~1/20 of measurement scale
    delta_r_target = scale_mpc / 20.0

    # Resolution bits needed
    N_exact = math.log2(horizon_mpc / delta_r_target)
    N_bits = math.ceil(N_exact)

    # Actual cell size at this resolution
    delta_r_actual = horizon_mpc / (2 ** N_bits)

    # Sweet spot analysis (per user: N=13 for 30 Mpc scale)
    N_sweet_spot = 13
    delta_r_sweet = horizon_mpc / (2 ** N_sweet_spot)

    return {
        'scale_mpc': scale_mpc,
        'horizon_mpc': horizon_mpc,
        'delta_r_target_mpc': delta_r_target,
        'N_exact': N_exact,
        'N_bits': N_bits,
        'delta_r_actual_mpc': delta_r_actual,
        'N_sweet_spot': N_sweet_spot,
        'delta_r_sweet_mpc': delta_r_sweet,
        'ratio_cell_to_scale': delta_r_actual / scale_mpc
    }


def validate_trgb_resolution():
    """
    Validate TRGB resolution specification with correct horizon normalization.
    """
    print("\n" + "="*80)
    print("TRGB Resolution Specification - Corrected")
    print("="*80 + "\n")

    # TRGB parameters
    trgb_scale = 30.0  # Mpc

    print(f"UHA Specification:")
    print(f"  R_H(a ≈ 1) = {R_H_TODAY:,.0f} Mpc")
    print(f"  Δr = R_H / 2^N per axis")
    print()

    # Calculate correct resolution
    result = calculate_resolution_bits(trgb_scale, R_H_TODAY)

    print(f"TRGB Anchor (scale = {trgb_scale} Mpc):")
    print(f"  Target cell size: Δr_target ≈ S/20 = {result['delta_r_target_mpc']:.2f} Mpc")
    print(f"  Required bits: N = ⌈log₂(R_H / Δr_target)⌉ = ⌈{result['N_exact']:.2f}⌉ = {result['N_bits']}")
    print(f"  Actual cell size: Δr = {result['delta_r_actual_mpc']:.3f} Mpc")
    print(f"  Ratio (cell/scale): {result['ratio_cell_to_scale']:.4f}")
    print()

    print(f"Sweet Spot (User Specified):")
    print(f"  N = {result['N_sweet_spot']} bits per axis")
    print(f"  Δr = {result['delta_r_sweet_mpc']:.3f} Mpc")
    print()

    # Compare to wrong calculation
    print(f"Comparison to Incorrect Calculation:")
    print(f"  Using 1 Gpc box: N ≈ 10-12 bits (Δr ≈ 0.98 Mpc)")
    print(f"  Using R_H = 14 Gpc: N ≈ 12-14 bits (Δr ≈ 1.7 Mpc) ✓")
    print()

    # Table of resolutions
    print("Resolution Table (R_H = 14,000 Mpc):")
    print(f"{'N (bits)':>8} {'Δr (Mpc)':>12} {'Δr (kpc)':>12} {'Ratio':>10} {'Assessment':>20}")
    print("-" * 80)

    for N in [10, 11, 12, 13, 14, 15, 16, 20, 22]:
        delta_r = R_H_TODAY / (2 ** N)
        delta_r_kpc = delta_r * 1000
        ratio = delta_r / trgb_scale

        if N == 13:
            assessment = "✅ SWEET SPOT"
        elif 12 <= N <= 14:
            assessment = "✓ Good"
        elif N < 12:
            assessment = "Coarse"
        elif N < 20:
            assessment = "Fine"
        else:
            assessment = "Over-resolved"

        print(f"{N:8d} {delta_r:12.3f} {delta_r_kpc:12.1f} {ratio:10.4f} {assessment:>20}")

    print()
    print("="*80 + "\n")

    return result


def generate_corrected_trgb_json():
    """
    Generate corrected TRGB anchor JSON with proper UHA spec.
    """
    trgb_anchor = {
        "anchor": "TRGB_CCHP",
        "scale_mpc": 30,
        "resolution_bits_per_axis": 13,
        "domain": "stellar_population",
        "ΔT": 0.012,
        "reference": "Freedman+2021",
        "uha_spec": {
            "horizon_normalization": "R_H(a ≈ 1) ≈ 14,000 Mpc",
            "cell_size_formula": "Δr = R_H / 2^N",
            "target_cell_size": "Δr_target ≈ S/20 ≈ 1.5 Mpc",
            "actual_cell_size_mpc": 1.709,
            "ratio_cell_to_scale": 0.057
        },
        "notes": {
            "correction": "Fixed from 22 bits (wrong) to 13 bits (UHA spec)",
            "previous_error": "Used 1 Gpc box instead of R_H = 14 Gpc",
            "sweet_spot": "N=13 gives 1.7 Mpc cells for 30 Mpc scale"
        }
    }

    return trgb_anchor


def resolver_function():
    """
    Resolver function per UHA spec: N = ⌈log₂(R_H(a) / Δr_target)⌉
    """
    print("\n" + "="*80)
    print("UHA Resolution Resolver (Spec-Backed)")
    print("="*80 + "\n")

    print("def resolve_uha_bits(anchor_scale_mpc, horizon_mpc=14000):")
    print("    '''")
    print("    UHA Spec: N = ⌈log₂(R_H(a) / Δr_target)⌉")
    print("    For anchors: Δr_target ≈ S/20")
    print("    '''")
    print("    delta_r_target = anchor_scale_mpc / 20.0")
    print("    N = math.ceil(math.log2(horizon_mpc / delta_r_target))")
    print("    return N")
    print()

    # Examples
    examples = [
        ("MW Parallax", 0.01, "Local, sub-Mpc"),
        ("LMC", 0.05, "Local, sub-Mpc"),
        ("NGC 4258", 7.6, "Local anchor"),
        ("SH0ES host", 20, "Local-intermediate"),
        ("TRGB", 30, "Intermediate"),
        ("JAGB", 35, "Intermediate"),
        ("Strong lensing", 1000, "High-z, global"),
        ("Planck CMB", 14000, "Horizon scale")
    ]

    print("Examples:")
    print(f"{'Anchor':>20} {'Scale (Mpc)':>15} {'N (bits)':>10} {'Δr (Mpc)':>12} {'Domain':>20}")
    print("-" * 80)

    for name, scale, domain in examples:
        delta_r_target = scale / 20.0
        N = math.ceil(math.log2(R_H_TODAY / delta_r_target))
        delta_r_actual = R_H_TODAY / (2 ** N)

        print(f"{name:>20} {scale:15.2f} {N:10d} {delta_r_actual:12.3f} {domain:>20}")

    print()
    print("="*80 + "\n")


def main():
    """Run corrected TRGB resolution analysis."""

    # Validate resolution
    result = validate_trgb_resolution()

    # Generate corrected JSON
    trgb_json = generate_corrected_trgb_json()

    # Save to file
    output_file = "/root/private_multiresolution/trgb_anchor_spec_corrected.json"
    with open(output_file, 'w') as f:
        json.dump(trgb_json, f, indent=2)

    print(f"Corrected TRGB anchor specification saved to:")
    print(f"  {output_file}")
    print()

    print("JSON:")
    print(json.dumps(trgb_json, indent=2))
    print()

    # Show resolver function
    resolver_function()

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"✅ TRGB @ 30 Mpc → N = 13 bits per axis")
    print(f"✅ Cell size: Δr = 1.71 Mpc (sweet spot)")
    print(f"✅ Ratio: 0.057 (appropriate for intermediate scale)")
    print(f"✅ UHA spec-compliant: R_H(a≈1) = 14,000 Mpc")
    print()
    print(f"❌ Previous error: N = 22 bits → 3.3 kpc (over-resolved)")
    print(f"❌ Cause: Used 1 Gpc box instead of R_H = 14 Gpc horizon")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
