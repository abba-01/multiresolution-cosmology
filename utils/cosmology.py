"""
Cosmological Calculation Utilities
===================================

Centralized cosmological distance calculations and transformations.
Consolidates repeated logic from multiple files.

Author: Eric D. Martin
Date: 2025-10-30
License: MIT
"""

import numpy as np
from typing import Dict, Tuple, Optional

# Use absolute imports for better compatibility
try:
    from config.constants import SPEED_OF_LIGHT_KM_S
except ImportError:
    # Fallback for relative imports when used as submodule
    from ..config.constants import SPEED_OF_LIGHT_KM_S


# ============================================================================
# Distance Calculations
# ============================================================================

def calculate_hubble_distance(h0: float) -> float:
    """
    Calculate Hubble distance D_H = c / H0.

    Args:
        h0: Hubble constant in km/s/Mpc

    Returns:
        Hubble distance in Mpc

    Example:
        >>> calculate_hubble_distance(67.36)
        4451.93...  # Mpc
    """
    return SPEED_OF_LIGHT_KM_S / h0


def calculate_angular_diameter_distance(
    z: float,
    h0: float,
    omega_m: float,
    omega_lambda: Optional[float] = None
) -> float:
    """
    Calculate angular diameter distance for a flat universe.

    This uses a simplified approximation suitable for z < 2.
    For precise calculations, use astropy.cosmology.

    Args:
        z: Redshift
        h0: Hubble constant in km/s/Mpc
        omega_m: Matter density parameter
        omega_lambda: Dark energy density (default: 1 - omega_m for flat universe)

    Returns:
        Angular diameter distance in Mpc

    Formula (approximation for flat ΛCDM):
        D_A(z) ≈ D_H × z / (1+z) × [1 + 0.5 × Ω_m × z]

    Note:
        This is an approximation. For high precision or z > 2, use proper integration.
    """
    if omega_lambda is None:
        omega_lambda = 1.0 - omega_m

    # Verify flat universe
    if abs(omega_m + omega_lambda - 1.0) > 0.01:
        raise ValueError(
            f"omega_m ({omega_m}) + omega_lambda ({omega_lambda}) != 1.0. "
            "Non-flat universes not supported in this approximation."
        )

    # Hubble distance
    d_h = calculate_hubble_distance(h0)

    # Simplified angular diameter distance
    # This approximation is good to ~5% for z < 1, ~10% for z < 2
    d_a_approx = d_h * z / (1 + z) * (1 + 0.5 * omega_m * z)

    return d_a_approx


def calculate_comoving_distance(
    z: float,
    h0: float,
    omega_m: float,
    omega_lambda: Optional[float] = None
) -> float:
    """
    Calculate comoving distance for a flat universe.

    Args:
        z: Redshift
        h0: Hubble constant in km/s/Mpc
        omega_m: Matter density parameter
        omega_lambda: Dark energy density (default: 1 - omega_m)

    Returns:
        Comoving distance in Mpc

    Formula:
        D_C(z) = D_A(z) × (1 + z)
    """
    d_a = calculate_angular_diameter_distance(z, h0, omega_m, omega_lambda)
    return d_a * (1 + z)


def calculate_luminosity_distance(
    z: float,
    h0: float,
    omega_m: float,
    omega_lambda: Optional[float] = None
) -> float:
    """
    Calculate luminosity distance for a flat universe.

    Args:
        z: Redshift
        h0: Hubble constant in km/s/Mpc
        omega_m: Matter density parameter
        omega_lambda: Dark energy density (default: 1 - omega_m)

    Returns:
        Luminosity distance in Mpc

    Formula:
        D_L(z) = D_A(z) × (1 + z)²
    """
    d_a = calculate_angular_diameter_distance(z, h0, omega_m, omega_lambda)
    return d_a * (1 + z) ** 2


# ============================================================================
# Angular to Physical Scale Conversions
# ============================================================================

def angular_to_comoving_scale(
    theta_arcmin: float,
    z_eff: float,
    h0: float = 67.36,
    omega_m: float = 0.315
) -> float:
    """
    Convert angular scale to comoving scale.

    Args:
        theta_arcmin: Angular scale in arcminutes
        z_eff: Effective redshift
        h0: Hubble constant in km/s/Mpc (default: Planck)
        omega_m: Matter density (default: Planck)

    Returns:
        Comoving scale in Mpc

    Formula:
        θ [rad] = Δr [Mpc] / D_A(z)
        => Δr = θ × D_A(z) × (1 + z)  # Convert to comoving
    """
    # Convert to radians
    theta_rad = theta_arcmin * np.pi / 180.0 / 60.0

    # Angular diameter distance
    d_a = calculate_angular_diameter_distance(z_eff, h0, omega_m)

    # Comoving scale
    scale_mpc = theta_rad * d_a * (1 + z_eff)

    return scale_mpc


def comoving_to_angular_scale(
    scale_mpc: float,
    z_eff: float,
    h0: float = 67.36,
    omega_m: float = 0.315
) -> float:
    """
    Convert comoving scale to angular scale.

    Args:
        scale_mpc: Comoving scale in Mpc
        z_eff: Effective redshift
        h0: Hubble constant in km/s/Mpc (default: Planck)
        omega_m: Matter density (default: Planck)

    Returns:
        Angular scale in arcminutes
    """
    # Angular diameter distance
    d_a = calculate_angular_diameter_distance(z_eff, h0, omega_m)

    # Physical scale at redshift z
    scale_physical = scale_mpc / (1 + z_eff)

    # Angular scale in radians
    theta_rad = scale_physical / d_a

    # Convert to arcminutes
    theta_arcmin = theta_rad * 180.0 / np.pi * 60.0

    return theta_arcmin


# ============================================================================
# Coordinate Transformations
# ============================================================================

def radec_distance_to_cartesian(
    ra_deg: float,
    dec_deg: float,
    distance_mpc: float
) -> Tuple[float, float, float]:
    """
    Convert (RA, Dec, distance) to Cartesian coordinates.

    Args:
        ra_deg: Right ascension in degrees
        dec_deg: Declination in degrees
        distance_mpc: Comoving distance in Mpc

    Returns:
        Tuple (x, y, z) in Mpc

    Coordinate system:
        - x-axis points toward RA=0°, Dec=0°
        - y-axis points toward RA=90°, Dec=0°
        - z-axis points toward Dec=90° (North pole)
    """
    # Convert to radians
    ra_rad = np.radians(ra_deg)
    dec_rad = np.radians(dec_deg)

    # Spherical to Cartesian
    x = distance_mpc * np.cos(dec_rad) * np.cos(ra_rad)
    y = distance_mpc * np.cos(dec_rad) * np.sin(ra_rad)
    z = distance_mpc * np.sin(dec_rad)

    return x, y, z


def cartesian_to_radec_distance(
    x: float,
    y: float,
    z: float
) -> Tuple[float, float, float]:
    """
    Convert Cartesian coordinates to (RA, Dec, distance).

    Args:
        x, y, z: Cartesian coordinates in Mpc

    Returns:
        Tuple (ra_deg, dec_deg, distance_mpc)
    """
    # Distance
    distance_mpc = np.sqrt(x**2 + y**2 + z**2)

    # Declination
    dec_rad = np.arcsin(z / distance_mpc)
    dec_deg = np.degrees(dec_rad)

    # Right ascension
    ra_rad = np.arctan2(y, x)
    ra_deg = np.degrees(ra_rad)

    # Ensure RA is in [0, 360)
    if ra_deg < 0:
        ra_deg += 360.0

    return ra_deg, dec_deg, distance_mpc


# ============================================================================
# Scale Factor and Redshift Conversions
# ============================================================================

def redshift_to_scale_factor(z: float) -> float:
    """
    Convert redshift to scale factor.

    Args:
        z: Redshift

    Returns:
        Scale factor a = 1/(1+z)
    """
    return 1.0 / (1.0 + z)


def scale_factor_to_redshift(a: float) -> float:
    """
    Convert scale factor to redshift.

    Args:
        a: Scale factor (0 < a <= 1)

    Returns:
        Redshift z = (1/a) - 1

    Raises:
        ValueError: If a <= 0 or a > 1
    """
    if a <= 0 or a > 1:
        raise ValueError(f"Scale factor must be in (0, 1], got {a}")

    return (1.0 / a) - 1.0


# ============================================================================
# Cosmology Dictionaries
# ============================================================================

def create_cosmo_dict(
    h0: float,
    omega_m: float,
    omega_lambda: Optional[float] = None,
    sigma_8: Optional[float] = None,
    s8: Optional[float] = None
) -> Dict[str, float]:
    """
    Create a standardized cosmology dictionary.

    Args:
        h0: Hubble constant in km/s/Mpc
        omega_m: Matter density parameter
        omega_lambda: Dark energy density (default: 1 - omega_m)
        sigma_8: Matter fluctuation amplitude (optional)
        s8: S8 parameter (optional)

    Returns:
        Dictionary with cosmological parameters
    """
    if omega_lambda is None:
        omega_lambda = 1.0 - omega_m

    cosmo = {
        'h0': h0,
        'omega_m': omega_m,
        'omega_lambda': omega_lambda
    }

    if sigma_8 is not None:
        cosmo['sigma_8'] = sigma_8

    if s8 is not None:
        cosmo['s8'] = s8

    return cosmo


# ============================================================================
# Validation Helpers
# ============================================================================

def validate_cosmology_parameters(cosmo: Dict[str, float], flat_only: bool = True) -> None:
    """
    Validate cosmological parameters.

    Args:
        cosmo: Dictionary with h0, omega_m, omega_lambda
        flat_only: If True, enforce flat universe constraint

    Raises:
        ValueError: If parameters are invalid
    """
    required_keys = ['h0', 'omega_m', 'omega_lambda']
    for key in required_keys:
        if key not in cosmo:
            raise ValueError(f"Missing required parameter: {key}")

    h0 = cosmo['h0']
    omega_m = cosmo['omega_m']
    omega_lambda = cosmo['omega_lambda']

    # Validate ranges
    if not (40 < h0 < 100):
        raise ValueError(f"H0 = {h0} km/s/Mpc is outside reasonable range [40, 100]")

    if not (0 < omega_m < 1):
        raise ValueError(f"Omega_m = {omega_m} must be in (0, 1)")

    if not (0 < omega_lambda < 1):
        raise ValueError(f"Omega_lambda = {omega_lambda} must be in (0, 1)")

    # Check flat universe if required
    if flat_only:
        total = omega_m + omega_lambda
        if abs(total - 1.0) > 0.01:
            raise ValueError(
                f"Flat universe required: Omega_m + Omega_lambda = {total} != 1.0"
            )
