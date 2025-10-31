"""
Input Validation Utilities
===========================

Centralized validation functions for coordinates, parameters, and data.
Consolidates validation logic previously duplicated across files.

Author: Eric D. Martin
Date: 2025-10-30
License: MIT
"""

import numpy as np
from typing import Dict, List, Optional, Any

# Use absolute imports for better compatibility
try:
    from config.constants import HORIZON_SIZE_TODAY_MPC
    from config.resolution import MIN_RESOLUTION_BITS, MAX_RESOLUTION_BITS
except ImportError:
    # Fallback for relative imports when used as submodule
    from ..config.constants import HORIZON_SIZE_TODAY_MPC
    from ..config.resolution import MIN_RESOLUTION_BITS, MAX_RESOLUTION_BITS


# ============================================================================
# Custom Exceptions
# ============================================================================

class ValidationError(ValueError):
    """Base exception for validation errors."""
    pass


class CoordinateValidationError(ValidationError):
    """Raised when astronomical coordinates are invalid."""
    pass


class ParameterValidationError(ValidationError):
    """Raised when parameters are out of valid range."""
    pass


class ResolutionValidationError(ValidationError):
    """Raised when resolution parameters are invalid."""
    pass


# ============================================================================
# Celestial Coordinate Validation
# ============================================================================

def validate_right_ascension(ra_deg: float) -> None:
    """
    Validate right ascension coordinate.

    Args:
        ra_deg: Right ascension in degrees

    Raises:
        CoordinateValidationError: If RA is invalid

    Valid range: [0, 360)
    """
    if not (0 <= ra_deg < 360):
        raise CoordinateValidationError(
            f"Right ascension must be in [0, 360), got {ra_deg}°"
        )

    if np.isnan(ra_deg) or np.isinf(ra_deg):
        raise CoordinateValidationError(
            f"Right ascension is NaN or infinite: {ra_deg}"
        )


def validate_declination(dec_deg: float) -> None:
    """
    Validate declination coordinate.

    Args:
        dec_deg: Declination in degrees

    Raises:
        CoordinateValidationError: If Dec is invalid

    Valid range: [-90, 90]
    """
    if not (-90 <= dec_deg <= 90):
        raise CoordinateValidationError(
            f"Declination must be in [-90, 90], got {dec_deg}°"
        )

    if np.isnan(dec_deg) or np.isinf(dec_deg):
        raise CoordinateValidationError(
            f"Declination is NaN or infinite: {dec_deg}"
        )


def validate_distance(distance_mpc: float, max_distance: Optional[float] = None) -> None:
    """
    Validate comoving distance.

    Args:
        distance_mpc: Comoving distance in Mpc
        max_distance: Maximum allowed distance (default: horizon size)

    Raises:
        CoordinateValidationError: If distance is invalid
    """
    if max_distance is None:
        max_distance = HORIZON_SIZE_TODAY_MPC

    if distance_mpc <= 0:
        raise CoordinateValidationError(
            f"Distance must be positive, got {distance_mpc} Mpc"
        )

    if distance_mpc > max_distance:
        raise CoordinateValidationError(
            f"Distance {distance_mpc} Mpc exceeds maximum {max_distance} Mpc"
        )

    if np.isnan(distance_mpc) or np.isinf(distance_mpc):
        raise CoordinateValidationError(
            f"Distance is NaN or infinite: {distance_mpc}"
        )


def validate_celestial_coordinates(
    ra_deg: float,
    dec_deg: float,
    distance_mpc: float,
    max_distance: Optional[float] = None
) -> None:
    """
    Validate complete celestial coordinate triplet.

    Args:
        ra_deg: Right ascension in degrees
        dec_deg: Declination in degrees
        distance_mpc: Comoving distance in Mpc
        max_distance: Maximum allowed distance

    Raises:
        CoordinateValidationError: If any coordinate is invalid
    """
    validate_right_ascension(ra_deg)
    validate_declination(dec_deg)
    validate_distance(distance_mpc, max_distance)


# ============================================================================
# Resolution Parameter Validation
# ============================================================================

def validate_resolution_bits(resolution_bits: int) -> None:
    """
    Validate UHA resolution bits.

    Args:
        resolution_bits: Bits per dimension

    Raises:
        ResolutionValidationError: If resolution is invalid

    Valid range: [8, 32]
    """
    if not isinstance(resolution_bits, (int, np.integer)):
        raise ResolutionValidationError(
            f"Resolution bits must be an integer, got {type(resolution_bits)}"
        )

    if not (MIN_RESOLUTION_BITS <= resolution_bits <= MAX_RESOLUTION_BITS):
        raise ResolutionValidationError(
            f"Resolution bits must be in [{MIN_RESOLUTION_BITS}, {MAX_RESOLUTION_BITS}], "
            f"got {resolution_bits}"
        )


def validate_scale_factor(scale_factor: float) -> None:
    """
    Validate cosmic scale factor.

    Args:
        scale_factor: Scale factor a

    Raises:
        ParameterValidationError: If scale factor is invalid

    Valid range: (0, 1]
    Note: a=1 corresponds to today (z=0)
    """
    if not (0 < scale_factor <= 1.0):
        raise ParameterValidationError(
            f"Scale factor must be in (0, 1], got {scale_factor}"
        )

    if np.isnan(scale_factor) or np.isinf(scale_factor):
        raise ParameterValidationError(
            f"Scale factor is NaN or infinite: {scale_factor}"
        )


def validate_redshift(z: float, max_z: float = 10.0) -> None:
    """
    Validate redshift.

    Args:
        z: Redshift
        max_z: Maximum allowed redshift (default: 10)

    Raises:
        ParameterValidationError: If redshift is invalid

    Valid range: [0, max_z]
    """
    if z < 0:
        raise ParameterValidationError(
            f"Redshift must be non-negative, got {z}"
        )

    if z > max_z:
        raise ParameterValidationError(
            f"Redshift {z} exceeds maximum {max_z}"
        )

    if np.isnan(z) or np.isinf(z):
        raise ParameterValidationError(
            f"Redshift is NaN or infinite: {z}"
        )


# ============================================================================
# Cosmological Parameter Validation
# ============================================================================

def validate_hubble_constant(h0: float) -> None:
    """
    Validate Hubble constant.

    Args:
        h0: Hubble constant in km/s/Mpc

    Raises:
        ParameterValidationError: If H0 is invalid

    Reasonable range: [40, 100] km/s/Mpc
    """
    if not (40 < h0 < 100):
        raise ParameterValidationError(
            f"Hubble constant {h0} km/s/Mpc is outside reasonable range [40, 100]"
        )

    if np.isnan(h0) or np.isinf(h0):
        raise ParameterValidationError(
            f"Hubble constant is NaN or infinite: {h0}"
        )


def validate_omega_parameter(omega: float, parameter_name: str = "Omega") -> None:
    """
    Validate density parameter.

    Args:
        omega: Density parameter
        parameter_name: Name for error messages

    Raises:
        ParameterValidationError: If Omega is invalid

    Valid range: (0, 1)
    """
    if not (0 < omega < 1):
        raise ParameterValidationError(
            f"{parameter_name} = {omega} must be in (0, 1)"
        )

    if np.isnan(omega) or np.isinf(omega):
        raise ParameterValidationError(
            f"{parameter_name} is NaN or infinite: {omega}"
        )


def validate_cosmology_dict(cosmo: Dict[str, float], require_flat: bool = True) -> None:
    """
    Validate cosmology parameter dictionary.

    Args:
        cosmo: Dictionary with 'h0', 'omega_m', 'omega_lambda'
        require_flat: If True, enforce flat universe constraint

    Raises:
        ParameterValidationError: If parameters are invalid
    """
    # Check required keys
    required_keys = ['h0', 'omega_m', 'omega_lambda']
    for key in required_keys:
        if key not in cosmo:
            raise ParameterValidationError(f"Missing required parameter: {key}")

    # Validate individual parameters
    validate_hubble_constant(cosmo['h0'])
    validate_omega_parameter(cosmo['omega_m'], 'Omega_m')
    validate_omega_parameter(cosmo['omega_lambda'], 'Omega_lambda')

    # Check flat universe constraint
    if require_flat:
        total = cosmo['omega_m'] + cosmo['omega_lambda']
        if abs(total - 1.0) > 0.01:
            raise ParameterValidationError(
                f"Flat universe required: Omega_m + Omega_lambda = {total:.4f} ≠ 1.0"
            )


# ============================================================================
# Array and Data Validation
# ============================================================================

def validate_array_size(arr: np.ndarray, max_size: int, name: str = "array") -> None:
    """
    Validate array size to prevent memory issues.

    Args:
        arr: Numpy array to validate
        max_size: Maximum allowed number of elements
        name: Array name for error messages

    Raises:
        ValidationError: If array is too large
    """
    size = arr.size if hasattr(arr, 'size') else len(arr)

    if size > max_size:
        raise ValidationError(
            f"{name} size {size} exceeds maximum {max_size}. "
            "This may indicate a DoS attempt or memory issue."
        )


def validate_array_finite(arr: np.ndarray, name: str = "array") -> None:
    """
    Validate that array contains only finite values.

    Args:
        arr: Numpy array to validate
        name: Array name for error messages

    Raises:
        ValidationError: If array contains NaN or inf
    """
    if not np.all(np.isfinite(arr)):
        n_nan = np.sum(np.isnan(arr))
        n_inf = np.sum(np.isinf(arr))
        raise ValidationError(
            f"{name} contains non-finite values: {n_nan} NaN, {n_inf} inf"
        )


def validate_positive_array(arr: np.ndarray, name: str = "array") -> None:
    """
    Validate that array contains only positive values.

    Args:
        arr: Numpy array to validate
        name: Array name for error messages

    Raises:
        ValidationError: If array contains non-positive values
    """
    if not np.all(arr > 0):
        n_negative = np.sum(arr <= 0)
        raise ValidationError(
            f"{name} contains {n_negative} non-positive values"
        )


def validate_array_range(
    arr: np.ndarray,
    min_val: float,
    max_val: float,
    name: str = "array"
) -> None:
    """
    Validate that array values are within specified range.

    Args:
        arr: Numpy array to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        name: Array name for error messages

    Raises:
        ValidationError: If any values are outside range
    """
    if np.any(arr < min_val) or np.any(arr > max_val):
        actual_min = np.min(arr)
        actual_max = np.max(arr)
        raise ValidationError(
            f"{name} values must be in [{min_val}, {max_val}], "
            f"got range [{actual_min}, {actual_max}]"
        )


# ============================================================================
# Survey Data Validation
# ============================================================================

def validate_redshift_bins(z_bins: List[tuple]) -> None:
    """
    Validate redshift bin structure.

    Args:
        z_bins: List of (z_min, z_max) tuples

    Raises:
        ValidationError: If bins are invalid
    """
    if not z_bins:
        raise ValidationError("Redshift bins cannot be empty")

    for i, (z_min, z_max) in enumerate(z_bins):
        if z_min >= z_max:
            raise ValidationError(
                f"Bin {i}: z_min ({z_min}) must be < z_max ({z_max})"
            )

        validate_redshift(z_min)
        validate_redshift(z_max)


def validate_measurement_uncertainty(value: float, sigma: float, name: str = "measurement") -> None:
    """
    Validate measurement and its uncertainty.

    Args:
        value: Measured value
        sigma: Uncertainty (1-sigma)
        name: Measurement name for error messages

    Raises:
        ValidationError: If uncertainty is invalid
    """
    if sigma <= 0:
        raise ValidationError(
            f"{name} uncertainty must be positive, got {sigma}"
        )

    if sigma > abs(value):
        raise ValidationError(
            f"{name} uncertainty ({sigma}) is larger than value ({value}). "
            "This may indicate a problem."
        )

    if np.isnan(value) or np.isnan(sigma):
        raise ValidationError(
            f"{name} or uncertainty contains NaN"
        )


# ============================================================================
# Configuration Validation
# ============================================================================

def validate_resolution_schedule(schedule: List[int]) -> None:
    """
    Validate resolution schedule.

    Args:
        schedule: List of resolution bits

    Raises:
        ResolutionValidationError: If schedule is invalid
    """
    if not schedule:
        raise ResolutionValidationError("Resolution schedule cannot be empty")

    # Validate each resolution
    for bits in schedule:
        validate_resolution_bits(bits)

    # Check monotonically increasing
    if schedule != sorted(schedule):
        raise ResolutionValidationError(
            f"Resolution schedule must be monotonically increasing, got {schedule}"
        )

    # Check for duplicates
    if len(schedule) != len(set(schedule)):
        raise ResolutionValidationError(
            f"Resolution schedule contains duplicates: {schedule}"
        )


def validate_convergence_threshold(threshold: float) -> None:
    """
    Validate convergence threshold (ΔT).

    Args:
        threshold: Convergence threshold

    Raises:
        ValidationError: If threshold is invalid

    Typical range: [0.05, 0.30]
    """
    if not (0 < threshold < 1.0):
        raise ValidationError(
            f"Convergence threshold must be in (0, 1), got {threshold}"
        )

    if threshold < 0.01:
        raise ValidationError(
            f"Convergence threshold {threshold} is unrealistically small"
        )

    if threshold > 0.5:
        raise ValidationError(
            f"Convergence threshold {threshold} is too large (no convergence expected)"
        )


# ============================================================================
# High-Level Validation
# ============================================================================

def validate_uha_encoding_inputs(
    ra_deg: float,
    dec_deg: float,
    distance_mpc: float,
    resolution_bits: int,
    scale_factor: float,
    cosmo_params: Dict[str, float]
) -> None:
    """
    Validate all inputs for UHA encoding.

    Args:
        ra_deg: Right ascension in degrees
        dec_deg: Declination in degrees
        distance_mpc: Comoving distance in Mpc
        resolution_bits: Resolution in bits per dimension
        scale_factor: Cosmic scale factor
        cosmo_params: Cosmology parameter dictionary

    Raises:
        ValidationError: If any input is invalid
    """
    validate_celestial_coordinates(ra_deg, dec_deg, distance_mpc)
    validate_resolution_bits(resolution_bits)
    validate_scale_factor(scale_factor)
    validate_cosmology_dict(cosmo_params)


def validate_api_request_size(data: Any, max_size_mb: float = 10.0) -> None:
    """
    Validate API request/response size.

    Args:
        data: Data object (list, dict, etc.)
        max_size_mb: Maximum size in megabytes

    Raises:
        ValidationError: If data is too large
    """
    import sys

    size_bytes = sys.getsizeof(data)
    size_mb = size_bytes / (1024 * 1024)

    if size_mb > max_size_mb:
        raise ValidationError(
            f"Data size {size_mb:.2f} MB exceeds maximum {max_size_mb} MB"
        )


# ============================================================================
# Validation Helper
# ============================================================================

def validate_all_or_none(*values, names: Optional[List[str]] = None) -> None:
    """
    Validate that either all values are provided or none are.

    Args:
        *values: Values to check
        names: Optional names for error messages

    Raises:
        ValidationError: If some but not all values are None
    """
    none_count = sum(v is None for v in values)

    if none_count not in (0, len(values)):
        if names:
            provided = [name for name, val in zip(names, values) if val is not None]
            missing = [name for name, val in zip(names, values) if val is None]
            raise ValidationError(
                f"Either provide all or none: provided={provided}, missing={missing}"
            )
        else:
            raise ValidationError(
                f"Either provide all values or none: {none_count}/{len(values)} are None"
            )
