"""
Multi-Resolution Correction Parameters
=======================================

Single source of truth for systematic correction formulas, calibration
constants, and correction patterns.

Author: Eric D. Martin
Date: 2025-10-30
License: MIT
"""

from typing import Dict
import numpy as np


# ============================================================================
# Universal Correction Patterns
# ============================================================================

# Universal baseline correction amplitude
# Pattern: ΔS₈(z) = A × (1+z)^(-0.5)
# This is the SINGLE SOURCE for this critical parameter
UNIVERSAL_BASELINE = 0.0200  # Amplitude A

# Redshift scaling exponent
# (1+z)^β where β = -0.5
REDSHIFT_SCALING_EXPONENT = -0.5

# Correction formula string for documentation
CORRECTION_FORMULA = "ΔS₈(z) = 0.0200 × (1+z)^(-0.5)"
CORRECTION_FORMULA_GENERAL = "ΔS₈(z) = A × (1+z)^β"


# ============================================================================
# Calibration Constants at Specific Redshifts
# ============================================================================

# Baseline correction at z = 0.2
# Used for calibration and validation
BASELINE_CORRECTION_Z02 = 0.018

# Baseline correction at z = 0.0 (today)
BASELINE_CORRECTION_Z00 = UNIVERSAL_BASELINE  # (1+0)^(-0.5) = 1.0

# Baseline correction at z = 1.0
BASELINE_CORRECTION_Z10 = UNIVERSAL_BASELINE * (1.0 + 1.0)**REDSHIFT_SCALING_EXPONENT  # ~0.0141


# ============================================================================
# Resolution-Specific Corrections
# ============================================================================

# Correction increments at each resolution level
# These are APPROXIMATE values - actual corrections depend on data
CORRECTION_BY_RESOLUTION = {
    8:  0.000,   # No correction at coarsest scale (cosmological)
    12: 0.009,   # Shear calibration, photo-z errors
    16: 0.019,   # Intrinsic alignments begin
    20: 0.029,   # Intrinsic alignments dominant
    24: 0.034,   # Baryonic feedback effects
    28: 0.036,   # Population mixing
    32: 0.037    # Local variations (asymptotic)
}

# Cumulative corrections up to each resolution
CUMULATIVE_CORRECTION_BY_RESOLUTION = {
    8:  0.000,
    12: 0.009,
    16: 0.028,  # 0.000 + 0.009 + 0.019
    20: 0.057,  # + 0.029
    24: 0.091,  # + 0.034
    28: 0.127,  # + 0.036
    32: 0.164   # + 0.037 (not typically used, S8 specific)
}


# ============================================================================
# H0 Correction Parameters
# ============================================================================

# Total H0 correction from multi-resolution analysis
# SH0ES 73.04 → Converged 68.5 km/s/Mpc
TOTAL_H0_CORRECTION = -4.54  # km/s/Mpc

# H0 corrections by resolution level (approximate)
H0_CORRECTION_BY_RESOLUTION = {
    8:  0.0,    # No correction at cosmological scales
    12: -0.8,   # Peculiar velocities
    16: -1.5,   # Bulk flows
    20: -1.2,   # Metallicity gradients
    24: -0.6,   # Dust, reddening
    28: -0.3,   # Population mixing
    32: -0.1    # Local extinction
}


# ============================================================================
# Systematic Categories and Corrections
# ============================================================================

# Systematic effects by physical origin
SYSTEMATIC_CORRECTIONS = {
    'shear_calibration': {
        'delta_s8': 0.009,
        'resolution_bits': 12,
        'description': 'Shape measurement bias corrections'
    },
    'photo_z': {
        'delta_s8': 0.010,
        'resolution_bits': 12,
        'description': 'Photometric redshift uncertainties'
    },
    'intrinsic_alignments': {
        'delta_s8': 0.029,
        'resolution_bits': 20,
        'description': 'Galaxy intrinsic alignment contamination'
    },
    'baryonic_feedback': {
        'delta_s8': 0.034,
        'resolution_bits': 24,
        'description': 'Baryonic effects on matter power spectrum'
    },
    'peculiar_velocities': {
        'delta_h0': -0.8,
        'resolution_bits': 12,
        'description': 'Local peculiar velocity field'
    },
    'bulk_flows': {
        'delta_h0': -1.5,
        'resolution_bits': 16,
        'description': 'Large-scale coherent flows'
    },
    'metallicity': {
        'delta_h0': -1.2,
        'resolution_bits': 20,
        'description': 'Metallicity gradient effects on Cepheids'
    },
    'dust_extinction': {
        'delta_h0': -0.6,
        'resolution_bits': 24,
        'description': 'Dust reddening corrections'
    }
}


# ============================================================================
# Convergence Criteria
# ============================================================================

# Maximum allowed correction per resolution step
# Larger jumps may indicate numerical instability
MAX_CORRECTION_PER_STEP_S8 = 0.015
MAX_CORRECTION_PER_STEP_H0 = 2.0  # km/s/Mpc

# Expected total correction ranges
EXPECTED_TOTAL_S8_CORRECTION_MIN = 0.020
EXPECTED_TOTAL_S8_CORRECTION_MAX = 0.070

EXPECTED_TOTAL_H0_CORRECTION_MIN = -6.0  # km/s/Mpc
EXPECTED_TOTAL_H0_CORRECTION_MAX = -3.0  # km/s/Mpc


# ============================================================================
# Helper Functions
# ============================================================================

def calculate_redshift_scaling_factor(z: float, exponent: float = REDSHIFT_SCALING_EXPONENT) -> float:
    """
    Calculate (1+z)^β scaling factor.

    Args:
        z: Redshift
        exponent: Scaling exponent (default: -0.5)

    Returns:
        Scaling factor (1+z)^β

    Example:
        >>> calculate_redshift_scaling_factor(0.5)
        0.8164965809277261  # (1.5)^(-0.5)
    """
    return (1.0 + z) ** exponent


def calculate_s8_correction(z: float, baseline: float = UNIVERSAL_BASELINE) -> float:
    """
    Calculate S8 correction at given redshift.

    Args:
        z: Redshift
        baseline: Baseline amplitude (default: UNIVERSAL_BASELINE)

    Returns:
        ΔS₈ correction

    Formula:
        ΔS₈(z) = baseline × (1+z)^(-0.5)
    """
    return baseline * calculate_redshift_scaling_factor(z)


def validate_correction_magnitude(delta_s8: float, delta_h0: float = None) -> Dict[str, bool]:
    """
    Validate that corrections are within expected ranges.

    Args:
        delta_s8: S8 correction magnitude
        delta_h0: H0 correction magnitude (optional)

    Returns:
        Dictionary with validation results
    """
    results = {}

    # Validate S8 correction
    results['s8_in_range'] = (
        EXPECTED_TOTAL_S8_CORRECTION_MIN <= abs(delta_s8) <= EXPECTED_TOTAL_S8_CORRECTION_MAX
    )

    # Validate H0 correction if provided
    if delta_h0 is not None:
        results['h0_in_range'] = (
            EXPECTED_TOTAL_H0_CORRECTION_MIN <= delta_h0 <= EXPECTED_TOTAL_H0_CORRECTION_MAX
        )

    results['all_valid'] = all(results.values())

    return results


def get_correction_by_systematic(systematic_name: str) -> Dict:
    """
    Get correction parameters for a specific systematic effect.

    Args:
        systematic_name: Name of systematic effect

    Returns:
        Dictionary with correction information

    Raises:
        KeyError: If systematic name not found
    """
    if systematic_name not in SYSTEMATIC_CORRECTIONS:
        available = ', '.join(SYSTEMATIC_CORRECTIONS.keys())
        raise KeyError(
            f"Unknown systematic: {systematic_name}. "
            f"Available: {available}"
        )

    return SYSTEMATIC_CORRECTIONS[systematic_name].copy()


# ============================================================================
# Correction Pattern Fitting
# ============================================================================

def fit_correction_pattern(z_values: np.ndarray, corrections: np.ndarray) -> Dict:
    """
    Fit corrections to the (1+z)^β pattern and extract baseline.

    Args:
        z_values: Array of redshifts
        corrections: Array of corresponding corrections

    Returns:
        Dictionary with:
            - baseline: Fitted baseline amplitude A
            - exponent: Fitted exponent β (should be close to -0.5)
            - residuals: Fit residuals
            - rms: RMS of residuals

    Example:
        >>> z = np.array([0.1, 0.4, 0.7, 1.0])
        >>> corr = np.array([0.019, 0.017, 0.015, 0.014])
        >>> fit = fit_correction_pattern(z, corr)
        >>> print(f"Baseline: {fit['baseline']:.4f}")
    """
    # Convert to numpy arrays
    z_arr = np.asarray(z_values)
    corr_arr = np.asarray(corrections)

    # Calculate z-factors
    z_factors = calculate_redshift_scaling_factor(z_arr)

    # Extract baselines for each point
    baselines = corr_arr / z_factors

    # Statistics
    baseline_mean = np.mean(baselines)
    baseline_std = np.std(baselines)

    # Calculate residuals
    predicted = baseline_mean * z_factors
    residuals = corr_arr - predicted
    rms = np.sqrt(np.mean(residuals**2))

    return {
        'baseline': baseline_mean,
        'baseline_std': baseline_std,
        'exponent': REDSHIFT_SCALING_EXPONENT,  # Fixed by model
        'residuals': residuals,
        'rms': rms,
        'n_points': len(z_arr)
    }


# ============================================================================
# Validation
# ============================================================================

# Verify correction consistency
assert abs(BASELINE_CORRECTION_Z02 - calculate_s8_correction(0.2)) < 0.001, \
    "BASELINE_CORRECTION_Z02 inconsistent with formula"

assert TOTAL_H0_CORRECTION < 0, \
    "H0 correction should be negative (reducing SH0ES value)"

# Verify H0 corrections sum approximately
total_h0_from_components = sum(H0_CORRECTION_BY_RESOLUTION.values())
assert abs(total_h0_from_components - TOTAL_H0_CORRECTION) < 0.5, \
    f"H0 correction components ({total_h0_from_components:.2f}) " \
    f"don't sum to total ({TOTAL_H0_CORRECTION:.2f})"
