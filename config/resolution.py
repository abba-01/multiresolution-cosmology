"""
UHA Resolution Schedules and Parameters
========================================

Single source of truth for UHA encoding resolution configurations,
schedules, and related parameters.

Author: Eric D. Martin
Date: 2025-10-30
License: MIT
"""

from typing import List, Dict
import numpy as np


# ============================================================================
# Resolution Bit Ranges
# ============================================================================

# Minimum and maximum allowed resolution bits per dimension
MIN_RESOLUTION_BITS = 8   # Coarsest: ~54.7 Mpc cells
MAX_RESOLUTION_BITS = 32  # Finest: ~3.3 pc cells

# Default resolution for simple analyses
DEFAULT_RESOLUTION_BITS = 21  # ~6.7 kpc cells


# ============================================================================
# Standard Resolution Schedules
# ============================================================================

# Full multi-resolution schedule (8 levels)
# Spans from supercluster scales (54.7 Mpc) to stellar neighborhood (3.3 pc)
RESOLUTION_SCHEDULE_FULL = [8, 12, 16, 20, 24, 28, 32]

# Short schedule for faster analyses (5 levels)
# Stops at ~0.84 kpc, sufficient for most systematic corrections
RESOLUTION_SCHEDULE_SHORT = [8, 12, 16, 20, 24]

# Conservative schedule (6 levels)
# Stops at ~52 pc, avoids potential instabilities at highest resolution
RESOLUTION_SCHEDULE_CONSERVATIVE = [8, 12, 16, 20, 24, 28]

# Aggressive schedule with finer steps
RESOLUTION_SCHEDULE_AGGRESSIVE = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]

# Coarse schedule for quick testing
RESOLUTION_SCHEDULE_COARSE = [8, 16, 24, 32]

# Default schedule
DEFAULT_RESOLUTION_SCHEDULE = RESOLUTION_SCHEDULE_FULL


# ============================================================================
# Resolution-to-Scale Mapping
# ============================================================================

def resolution_to_cell_size(resolution_bits: int, horizon_mpc: float = 14000.0) -> float:
    """
    Calculate cell size in Mpc for a given resolution.

    Args:
        resolution_bits: Number of bits per dimension (8-32)
        horizon_mpc: Horizon size in Mpc (default: 14000)

    Returns:
        Cell size in Mpc

    Formula:
        Δr = R_H / 2^N per axis
    """
    return horizon_mpc / (2 ** resolution_bits)


def cell_size_to_resolution(cell_size_mpc: float, horizon_mpc: float = 14000.0) -> int:
    """
    Calculate required resolution bits for a target cell size.

    Args:
        cell_size_mpc: Desired cell size in Mpc
        horizon_mpc: Horizon size in Mpc (default: 14000)

    Returns:
        Resolution bits (rounded up to integer)

    Formula:
        N = ⌈log₂(R_H / Δr_target)⌉
    """
    n_exact = np.log2(horizon_mpc / cell_size_mpc)
    n_bits = int(np.ceil(n_exact))
    return max(MIN_RESOLUTION_BITS, min(MAX_RESOLUTION_BITS, n_bits))


def physical_scale_to_resolution(scale_mpc: float, oversampling: int = 20) -> int:
    """
    Calculate required resolution for a given physical scale.

    The resolution is chosen such that the cell size is ~1/oversampling
    of the physical scale of interest.

    Args:
        scale_mpc: Physical scale in Mpc
        oversampling: Number of cells per scale (default: 20)

    Returns:
        Resolution bits

    Example:
        For a 10 Mpc feature with oversampling=20:
        target cell size = 10/20 = 0.5 Mpc
        N = ⌈log₂(14000 / 0.5)⌉ = 15 bits
    """
    target_cell_size = scale_mpc / oversampling
    return cell_size_to_resolution(target_cell_size)


# ============================================================================
# Pre-computed Cell Sizes
# ============================================================================

# Cell sizes for standard resolution levels (in Mpc)
CELL_SIZES_MPC = {
    8:  resolution_to_cell_size(8),   # 54.6875 Mpc
    12: resolution_to_cell_size(12),  # 3.4180 Mpc
    16: resolution_to_cell_size(16),  # 0.2136 Mpc
    20: resolution_to_cell_size(20),  # 13.4 kpc (0.0134 Mpc)
    24: resolution_to_cell_size(24),  # 0.84 kpc (0.000839 Mpc)
    28: resolution_to_cell_size(28),  # 52.5 pc (0.0000525 Mpc)
    32: resolution_to_cell_size(32),  # 3.28 pc (0.00000328 Mpc)
}

# Cell sizes in parsecs for convenience
CELL_SIZES_PC = {
    bits: size_mpc * 1e6 for bits, size_mpc in CELL_SIZES_MPC.items()
}

# Cell sizes in kiloparsecs for convenience
CELL_SIZES_KPC = {
    bits: size_mpc * 1e3 for bits, size_mpc in CELL_SIZES_MPC.items()
}


# ============================================================================
# Physical Scale Categories
# ============================================================================

# Map resolution bits to physical scale categories
SCALE_CATEGORIES = {
    8:  "Supercluster",      # ~55 Mpc
    12: "Cluster",           # ~3.4 Mpc
    16: "Group",             # ~214 kpc
    20: "Galaxy",            # ~13 kpc
    24: "Subgalactic",       # ~840 pc
    28: "Stellar cluster",   # ~52 pc
    32: "Stellar neighborhood"  # ~3.3 pc
}


# ============================================================================
# Systematic Corrections by Scale
# ============================================================================

# Expected systematic effects at each resolution level
SYSTEMATIC_EFFECTS = {
    8:  "None (cosmological scales)",
    12: "Peculiar velocities, bulk flows",
    16: "Large-scale structure, bulk flows",
    20: "Metallicity gradients, galaxy peculiar velocities",
    24: "Dust extinction, reddening, stellar populations",
    28: "Population mixing, local extinction variations",
    32: "Individual stellar properties, local environment"
}


# ============================================================================
# Schedule Selection Helper
# ============================================================================

def get_resolution_schedule(mode: str = 'full') -> List[int]:
    """
    Get a resolution schedule by name.

    Args:
        mode: Schedule mode. Options:
            - 'full': Full 8-level schedule [8,12,16,20,24,28,32]
            - 'short': 5-level schedule [8,12,16,20,24]
            - 'conservative': 6-level schedule [8,12,16,20,24,28]
            - 'aggressive': Fine-grained schedule with 2-bit steps
            - 'coarse': Quick 4-level schedule [8,16,24,32]

    Returns:
        List of resolution bits

    Raises:
        ValueError: If mode not recognized
    """
    schedules = {
        'full': RESOLUTION_SCHEDULE_FULL,
        'short': RESOLUTION_SCHEDULE_SHORT,
        'conservative': RESOLUTION_SCHEDULE_CONSERVATIVE,
        'aggressive': RESOLUTION_SCHEDULE_AGGRESSIVE,
        'coarse': RESOLUTION_SCHEDULE_COARSE,
        'default': DEFAULT_RESOLUTION_SCHEDULE
    }

    mode_lower = mode.lower()
    if mode_lower not in schedules:
        raise ValueError(
            f"Unknown resolution schedule: {mode}. "
            f"Valid options: {', '.join(schedules.keys())}"
        )

    return schedules[mode_lower].copy()


def validate_resolution_schedule(schedule: List[int]) -> None:
    """
    Validate a resolution schedule.

    Args:
        schedule: List of resolution bits

    Raises:
        ValueError: If schedule is invalid
    """
    if not schedule:
        raise ValueError("Resolution schedule cannot be empty")

    for bits in schedule:
        if not MIN_RESOLUTION_BITS <= bits <= MAX_RESOLUTION_BITS:
            raise ValueError(
                f"Resolution {bits} bits out of valid range "
                f"[{MIN_RESOLUTION_BITS}, {MAX_RESOLUTION_BITS}]"
            )

    # Check for monotonically increasing
    if schedule != sorted(schedule):
        raise ValueError(
            "Resolution schedule must be monotonically increasing"
        )


# ============================================================================
# Resolution Information
# ============================================================================

def get_resolution_info(resolution_bits: int) -> Dict:
    """
    Get comprehensive information about a resolution level.

    Args:
        resolution_bits: Resolution in bits per dimension

    Returns:
        Dictionary with resolution information
    """
    return {
        'bits': resolution_bits,
        'cell_size_mpc': resolution_to_cell_size(resolution_bits),
        'cell_size_kpc': resolution_to_cell_size(resolution_bits) * 1e3,
        'cell_size_pc': resolution_to_cell_size(resolution_bits) * 1e6,
        'scale_category': SCALE_CATEGORIES.get(resolution_bits, "Custom"),
        'systematic_effects': SYSTEMATIC_EFFECTS.get(resolution_bits, "Unknown"),
        'total_cells_per_axis': 2 ** resolution_bits,
        'total_morton_bits': 3 * resolution_bits
    }


def print_resolution_schedule(schedule: List[int]) -> None:
    """
    Print formatted information about a resolution schedule.

    Args:
        schedule: List of resolution bits
    """
    print(f"\nResolution Schedule: {schedule}")
    print(f"{'='*80}")
    print(f"{'Bits':<6} {'Cell Size':<20} {'Scale':<20} {'Systematics'}")
    print(f"{'-'*80}")

    for bits in schedule:
        info = get_resolution_info(bits)
        cell_size_str = f"{info['cell_size_pc']:.1f} pc" if bits >= 20 else f"{info['cell_size_mpc']:.2f} Mpc"
        print(
            f"{bits:<6} {cell_size_str:<20} {info['scale_category']:<20} "
            f"{info['systematic_effects']}"
        )
    print(f"{'='*80}\n")


# ============================================================================
# Validation
# ============================================================================

# Verify all standard schedules are valid
for schedule_name, schedule in [
    ('FULL', RESOLUTION_SCHEDULE_FULL),
    ('SHORT', RESOLUTION_SCHEDULE_SHORT),
    ('CONSERVATIVE', RESOLUTION_SCHEDULE_CONSERVATIVE),
    ('AGGRESSIVE', RESOLUTION_SCHEDULE_AGGRESSIVE),
    ('COARSE', RESOLUTION_SCHEDULE_COARSE)
]:
    validate_resolution_schedule(schedule)
