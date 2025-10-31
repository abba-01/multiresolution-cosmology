"""
Correction Calculation Utilities
=================================

Centralized functions for calculating multi-resolution systematic corrections.
Consolidates correction logic previously duplicated across multiple files.

Author: Eric D. Martin
Date: 2025-10-30
License: MIT
"""

import numpy as np
from typing import Dict, List, Tuple, Optional

# Use absolute imports for better compatibility
try:
    from config.corrections import (
        UNIVERSAL_BASELINE,
        REDSHIFT_SCALING_EXPONENT,
        calculate_redshift_scaling_factor,
        calculate_s8_correction
    )
    from config.constants import PLANCK_S8, PLANCK_H0, SHOES_H0
except ImportError:
    # Fallback for relative imports when used as submodule
    from ..config.corrections import (
        UNIVERSAL_BASELINE,
        REDSHIFT_SCALING_EXPONENT,
        calculate_redshift_scaling_factor,
        calculate_s8_correction
    )
    from ..config.constants import PLANCK_S8, PLANCK_H0, SHOES_H0


# ============================================================================
# Core Correction Functions
# ============================================================================

def calculate_redshift_dependent_correction(
    z_eff: float,
    baseline: float = UNIVERSAL_BASELINE,
    exponent: float = REDSHIFT_SCALING_EXPONENT
) -> float:
    """
    Calculate redshift-dependent correction using (1+z)^β scaling.

    This is the CENTRAL implementation of the correction formula.
    All other files should call this function.

    Args:
        z_eff: Effective redshift
        baseline: Baseline amplitude (default: 0.0200)
        exponent: Scaling exponent (default: -0.5)

    Returns:
        Correction amplitude ΔS₈(z)

    Formula:
        ΔS₈(z) = baseline × (1+z)^β

    Example:
        >>> calculate_redshift_dependent_correction(0.5)
        0.01632993...  # 0.0200 × (1.5)^(-0.5)
    """
    z_factor = (1.0 + z_eff) ** exponent
    return baseline * z_factor


def apply_correction_to_bins(
    z_effective_values: List[float],
    s8_initial: float,
    baseline: float = UNIVERSAL_BASELINE
) -> Dict[str, any]:
    """
    Apply redshift-dependent corrections to multiple bins.

    Args:
        z_effective_values: List of effective redshifts for each bin
        s8_initial: Initial S₈ value (before corrections)
        baseline: Baseline amplitude (default: universal baseline)

    Returns:
        Dictionary with:
            - corrections: List of corrections for each bin
            - s8_final_per_bin: List of corrected S₈ values
            - s8_final_mean: Mean corrected S₈
            - total_correction: Mean correction amplitude
    """
    corrections = []
    s8_final_per_bin = []

    for z_eff in z_effective_values:
        correction = calculate_redshift_dependent_correction(z_eff, baseline)
        s8_final = s8_initial + correction

        corrections.append(correction)
        s8_final_per_bin.append(s8_final)

    mean_correction = np.mean(corrections)
    mean_s8_final = np.mean(s8_final_per_bin)

    return {
        'corrections': corrections,
        's8_final_per_bin': s8_final_per_bin,
        's8_final_mean': mean_s8_final,
        'total_correction': mean_correction,
        'baseline': baseline
    }


def fit_baseline_from_bins(
    z_effective_values: np.ndarray,
    corrections: np.ndarray
) -> Dict[str, float]:
    """
    Fit baseline amplitude from observed corrections.

    Args:
        z_effective_values: Array of effective redshifts
        corrections: Array of observed corrections

    Returns:
        Dictionary with:
            - baseline: Fitted baseline amplitude
            - baseline_std: Standard deviation of baseline
            - rms_residual: RMS of fit residuals

    Example:
        >>> z = np.array([0.1, 0.4, 0.6, 0.8, 1.0])
        >>> corr = np.array([0.019, 0.017, 0.015, 0.014, 0.014])
        >>> fit = fit_baseline_from_bins(z, corr)
        >>> print(f"Baseline: {fit['baseline']:.4f}")
    """
    # Calculate z-factors
    z_factors = calculate_redshift_scaling_factor(z_effective_values)

    # Extract baselines for each point
    baselines = corrections / z_factors

    # Statistics
    baseline_mean = np.mean(baselines)
    baseline_std = np.std(baselines)

    # Calculate residuals
    predicted = baseline_mean * z_factors
    residuals = corrections - predicted
    rms = np.sqrt(np.mean(residuals**2))

    return {
        'baseline': float(baseline_mean),
        'baseline_std': float(baseline_std),
        'rms_residual': float(rms),
        'n_bins': len(z_effective_values)
    }


# ============================================================================
# Tension Calculations
# ============================================================================

def calculate_tension_sigma(
    value1: float,
    sigma1: float,
    value2: float,
    sigma2: float
) -> float:
    """
    Calculate tension in sigma between two measurements.

    Args:
        value1: First measurement
        sigma1: Uncertainty on first measurement
        value2: Second measurement
        sigma2: Uncertainty on second measurement

    Returns:
        Tension in sigma

    Formula:
        tension = |value1 - value2| / sqrt(sigma1² + sigma2²)
    """
    diff = abs(value1 - value2)
    combined_sigma = np.sqrt(sigma1**2 + sigma2**2)
    return diff / combined_sigma


def calculate_s8_tension(
    s8_measured: float,
    s8_sigma: float,
    s8_reference: float = PLANCK_S8,
    sigma_reference: float = 0.016
) -> Tuple[float, float]:
    """
    Calculate S₈ tension with Planck.

    Args:
        s8_measured: Measured S₈ value
        s8_sigma: Uncertainty on measurement
        s8_reference: Reference S₈ (default: Planck)
        sigma_reference: Reference uncertainty

    Returns:
        Tuple of (tension_sigma, difference)
    """
    tension = calculate_tension_sigma(
        s8_measured, s8_sigma,
        s8_reference, sigma_reference
    )
    difference = s8_measured - s8_reference

    return tension, difference


def calculate_h0_tension(
    h0_measured: float,
    h0_sigma: float,
    h0_reference: float = PLANCK_H0,
    sigma_reference: float = 0.54
) -> Tuple[float, float]:
    """
    Calculate H₀ tension with Planck.

    Args:
        h0_measured: Measured H₀ value
        h0_sigma: Uncertainty on measurement
        h0_reference: Reference H₀ (default: Planck)
        sigma_reference: Reference uncertainty

    Returns:
        Tuple of (tension_sigma, difference)
    """
    tension = calculate_tension_sigma(
        h0_measured, h0_sigma,
        h0_reference, sigma_reference
    )
    difference = h0_measured - h0_reference

    return tension, difference


def evaluate_tension_reduction(
    tension_initial: float,
    tension_final: float
) -> Dict[str, float]:
    """
    Evaluate tension reduction from corrections.

    Args:
        tension_initial: Initial tension in sigma
        tension_final: Final tension in sigma after corrections

    Returns:
        Dictionary with:
            - initial_sigma: Initial tension
            - final_sigma: Final tension
            - reduction_sigma: Absolute reduction
            - reduction_percent: Percentage reduction
            - converged: True if final tension < 2σ
    """
    reduction_sigma = tension_initial - tension_final
    reduction_percent = (reduction_sigma / tension_initial) * 100 if tension_initial > 0 else 0

    return {
        'initial_sigma': float(tension_initial),
        'final_sigma': float(tension_final),
        'reduction_sigma': float(reduction_sigma),
        'reduction_percent': float(reduction_percent),
        'converged': tension_final < 2.0
    }


# ============================================================================
# Multi-Survey Consistency
# ============================================================================

def check_cross_survey_consistency(
    survey_results: Dict[str, Dict]
) -> Dict[str, any]:
    """
    Check consistency of correction patterns across surveys.

    Args:
        survey_results: Dictionary mapping survey name to results dict
                       Each results dict should have 'baseline' key

    Returns:
        Dictionary with:
            - baselines: Dict of baselines per survey
            - mean_baseline: Mean baseline across surveys
            - std_baseline: Standard deviation
            - max_difference: Maximum deviation from mean
            - consistent: True if std < 0.003 (EXCELLENT threshold)
    """
    baselines = {}
    for survey_name, results in survey_results.items():
        if 'baseline' in results:
            baselines[survey_name] = results['baseline']
        else:
            raise ValueError(f"Survey '{survey_name}' results missing 'baseline' key")

    baseline_values = np.array(list(baselines.values()))

    mean_baseline = np.mean(baseline_values)
    std_baseline = np.std(baseline_values)
    max_diff = np.max(np.abs(baseline_values - mean_baseline))

    # Consistency thresholds
    is_excellent = std_baseline < 0.003
    is_good = std_baseline < 0.005
    status = "EXCELLENT" if is_excellent else ("GOOD" if is_good else "MARGINAL")

    return {
        'baselines': baselines,
        'mean_baseline': float(mean_baseline),
        'std_baseline': float(std_baseline),
        'max_difference': float(max_diff),
        'consistent': is_excellent or is_good,
        'status': status
    }


# ============================================================================
# Resolution-Specific Corrections
# ============================================================================

def apply_resolution_schedule(
    initial_value: float,
    resolution_schedule: List[int],
    correction_per_resolution: Dict[int, float]
) -> Dict[str, any]:
    """
    Apply cumulative corrections through resolution schedule.

    Args:
        initial_value: Initial measurement value
        resolution_schedule: List of resolution bits to apply
        correction_per_resolution: Dict mapping resolution bits to correction

    Returns:
        Dictionary with:
            - values_by_resolution: Value at each resolution
            - corrections_by_resolution: Correction at each step
            - final_value: Value after all corrections
            - total_correction: Sum of all corrections
    """
    values = [initial_value]
    corrections = [0.0]
    current_value = initial_value

    for res_bits in resolution_schedule:
        if res_bits in correction_per_resolution:
            correction = correction_per_resolution[res_bits]
        else:
            # Interpolate or use zero
            correction = 0.0

        current_value += correction
        values.append(current_value)
        corrections.append(correction)

    return {
        'values_by_resolution': values,
        'corrections_by_resolution': corrections,
        'final_value': current_value,
        'total_correction': current_value - initial_value,
        'resolution_schedule': [None] + resolution_schedule  # Prepend None for initial
    }


# ============================================================================
# Correction Validation
# ============================================================================

def validate_correction_magnitude(
    correction: float,
    max_reasonable: float = 0.1,
    parameter_name: str = "correction"
) -> bool:
    """
    Validate that correction magnitude is reasonable.

    Args:
        correction: Correction value
        max_reasonable: Maximum reasonable correction
        parameter_name: Name for warning messages

    Returns:
        True if correction is reasonable

    Prints warnings for suspicious corrections.
    """
    if abs(correction) > max_reasonable:
        print(f"⚠️  WARNING: {parameter_name} = {correction:.4f} exceeds "
              f"reasonable maximum {max_reasonable}")
        return False

    if np.isnan(correction) or np.isinf(correction):
        print(f"⚠️  WARNING: {parameter_name} is NaN or infinite")
        return False

    return True


def check_monotonic_convergence(
    values: List[float],
    target: float,
    tolerance: float = 0.01
) -> Dict[str, any]:
    """
    Check if values converge monotonically toward target.

    Args:
        values: List of values through resolution schedule
        target: Target convergence value
        tolerance: Tolerance for "reached target"

    Returns:
        Dictionary with:
            - converges: True if generally moving toward target
            - reached_target: True if within tolerance of target
            - monotonic: True if strictly monotonic
            - final_distance: Distance from target at end
    """
    if len(values) < 2:
        return {
            'converges': False,
            'reached_target': False,
            'monotonic': False,
            'final_distance': abs(values[-1] - target) if values else float('inf')
        }

    distances = [abs(v - target) for v in values]
    final_distance = distances[-1]

    # Check if generally converging (distance decreases)
    converges = distances[-1] < distances[0]

    # Check if reached target
    reached_target = final_distance < tolerance

    # Check strict monotonicity of distances
    monotonic = all(distances[i] >= distances[i+1] for i in range(len(distances)-1))

    return {
        'converges': converges,
        'reached_target': reached_target,
        'monotonic': monotonic,
        'final_distance': float(final_distance),
        'initial_distance': float(distances[0])
    }


# ============================================================================
# Helper Functions
# ============================================================================

def summarize_correction_results(
    survey_name: str,
    s8_initial: float,
    s8_final: float,
    tension_initial: float,
    tension_final: float,
    baseline: float
) -> None:
    """
    Print formatted summary of correction results.

    Args:
        survey_name: Name of survey
        s8_initial: Initial S₈ value
        s8_final: Final S₈ value
        tension_initial: Initial tension in sigma
        tension_final: Final tension in sigma
        baseline: Fitted baseline
    """
    delta_s8 = s8_final - s8_initial
    reduction = evaluate_tension_reduction(tension_initial, tension_final)

    print(f"\n{'='*60}")
    print(f"{survey_name} CORRECTION SUMMARY")
    print(f"{'='*60}")
    print(f"  Baseline:     A = {baseline:.4f}")
    print(f"  S₈ initial:   {s8_initial:.3f}")
    print(f"  S₈ final:     {s8_final:.3f}")
    print(f"  ΔS₈:          {delta_s8:+.4f}")
    print(f"  Tension:      {tension_initial:.2f}σ → {tension_final:.2f}σ")
    print(f"  Reduction:    {reduction['reduction_percent']:.1f}%")
    print(f"  Converged:    {'✅ YES' if reduction['converged'] else '❌ NO'}")
    print(f"{'='*60}\n")
