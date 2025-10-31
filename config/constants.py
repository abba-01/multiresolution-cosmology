"""
Physical and Cosmological Constants
====================================

Single source of truth for all fundamental constants used across the codebase.

Author: Eric D. Martin
Date: 2025-10-30
License: MIT
"""

from typing import Dict

# ============================================================================
# Physical Constants
# ============================================================================

# Speed of light in km/s
SPEED_OF_LIGHT_KM_S = 299792.458

# Horizon size at scale factor a ≈ 1 (today) in Mpc
# Used for UHA encoding normalization
HORIZON_SIZE_TODAY_MPC = 14000.0


# ============================================================================
# Planck 2018 Cosmological Parameters
# ============================================================================

# Hubble constant from Planck CMB measurements
# Reference: Planck Collaboration et al. 2020, A&A 641, A6
PLANCK_H0 = 67.36  # km/s/Mpc
PLANCK_H0_SIGMA = 0.54  # km/s/Mpc

# Matter density parameter
PLANCK_OMEGA_M = 0.315
PLANCK_OMEGA_M_SIGMA = 0.007

# Dark energy density parameter (assuming flat universe)
PLANCK_OMEGA_LAMBDA = 0.685
PLANCK_OMEGA_LAMBDA_SIGMA = 0.007

# Sigma_8 parameter (matter fluctuation amplitude at 8 Mpc/h)
PLANCK_SIGMA_8 = 0.811
PLANCK_SIGMA_8_SIGMA = 0.006

# S_8 = sigma_8 * sqrt(Omega_m / 0.3)
PLANCK_S8 = 0.834
PLANCK_S8_SIGMA = 0.016

# Combined cosmology dict for convenience
PLANCK_COSMO = {
    'h0': PLANCK_H0,
    'omega_m': PLANCK_OMEGA_M,
    'omega_lambda': PLANCK_OMEGA_LAMBDA,
    'sigma_8': PLANCK_SIGMA_8,
    's8': PLANCK_S8
}


# ============================================================================
# SH0ES Distance Ladder Parameters
# ============================================================================

# Hubble constant from distance ladder measurements
# Reference: Riess et al. 2022, ApJL 934, L7
SHOES_H0 = 73.04  # km/s/Mpc
SHOES_H0_SIGMA = 1.04  # km/s/Mpc

# SH0ES assumes different matter density
SHOES_OMEGA_M = 0.300
SHOES_OMEGA_LAMBDA = 0.700

# Combined cosmology dict for convenience
SHOES_COSMO = {
    'h0': SHOES_H0,
    'omega_m': SHOES_OMEGA_M,
    'omega_lambda': SHOES_OMEGA_LAMBDA
}


# ============================================================================
# TRGB (Tip of Red Giant Branch) Parameters
# ============================================================================

# TRGB-based H0 measurements
# Reference: Freedman et al. 2020, ApJ 891, 57
TRGB_H0 = 69.8  # km/s/Mpc
TRGB_H0_SIGMA = 1.9  # km/s/Mpc


# ============================================================================
# Initial Hubble Tension
# ============================================================================

# Initial discrepancy between Planck and SH0ES
INITIAL_H0_GAP = SHOES_H0 - PLANCK_H0  # ~5.68 km/s/Mpc
INITIAL_H0_TENSION_SIGMA = INITIAL_H0_GAP / (
    (PLANCK_H0_SIGMA**2 + SHOES_H0_SIGMA**2)**0.5
)  # ~5.0 sigma


# ============================================================================
# Target/Expected Values After Multi-Resolution Correction
# ============================================================================

# Expected converged H0 after systematic corrections
TARGET_H0_CONVERGED = 68.5  # km/s/Mpc
TARGET_H0_UNCERTAINTY = 1.3  # km/s/Mpc

# Expected residual tension after correction
TARGET_RESIDUAL_TENSION_SIGMA = 1.0  # sigma


# ============================================================================
# Convergence Thresholds
# ============================================================================

# Epistemic distance threshold for convergence
# ΔT < 0.15 indicates systematic origin (not fundamental physics)
DELTA_T_CONVERGENCE_THRESHOLD = 0.15

# Threshold for rejecting new physics (e.g., Early Dark Energy)
# ΔT > 0.30 indicates no convergence (likely new physics)
DELTA_T_NEW_PHYSICS_THRESHOLD = 0.30


# ============================================================================
# Helper Functions
# ============================================================================

def get_planck_cosmo() -> Dict[str, float]:
    """Get Planck cosmological parameters as dictionary."""
    return PLANCK_COSMO.copy()


def get_shoes_cosmo() -> Dict[str, float]:
    """Get SH0ES cosmological parameters as dictionary."""
    return SHOES_COSMO.copy()


def get_default_cosmo() -> Dict[str, float]:
    """Get default cosmological parameters (Planck)."""
    return get_planck_cosmo()


# ============================================================================
# Validation
# ============================================================================

# Verify flat universe constraint
assert abs((PLANCK_OMEGA_M + PLANCK_OMEGA_LAMBDA) - 1.0) < 0.001, \
    "Planck parameters must satisfy flat universe: Omega_m + Omega_Lambda = 1"

assert abs((SHOES_OMEGA_M + SHOES_OMEGA_LAMBDA) - 1.0) < 0.001, \
    "SH0ES parameters must satisfy flat universe: Omega_m + Omega_Lambda = 1"
