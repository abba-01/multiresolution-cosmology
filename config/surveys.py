"""
Weak Lensing Survey Metadata
=============================

Single source of truth for all published survey results, specifications,
and metadata.

References:
- KiDS-1000: Asgari et al. 2021, A&A 645, A104
- DES-Y3: Abbott et al. 2022, PRD 105, 023520
- HSC-Y3: Hikage et al. 2019, PASJ 71, 43 / Li et al. 2023

Author: Eric D. Martin
Date: 2025-10-30
License: MIT
"""

from typing import List, Tuple, Dict
from dataclasses import dataclass


# ============================================================================
# Survey Data Classes
# ============================================================================

@dataclass
class SurveyMetadata:
    """Metadata for a weak lensing survey."""
    name: str
    full_name: str
    telescope: str
    location: str
    area_deg2: float
    n_bins: int
    z_bins: List[Tuple[float, float]]
    z_effective: List[float]
    S8_measured: float
    S8_sigma: float
    reference: str
    data_url: str
    data_release: str


# ============================================================================
# KiDS-1000 Survey
# ============================================================================

KIDS_NAME = "KiDS-1000"
KIDS_FULL_NAME = "Kilo-Degree Survey - 1000 square degrees"
KIDS_TELESCOPE = "VST"
KIDS_LOCATION = "ESO Paranal, Chile"
KIDS_AREA_DEG2 = 1000.0
KIDS_N_BINS = 5

# Tomographic redshift bins
KIDS_Z_BINS = [
    (0.1, 0.3),
    (0.3, 0.5),
    (0.5, 0.7),
    (0.7, 0.9),
    (0.9, 1.2)
]

# Effective redshifts for each bin
KIDS_Z_EFFECTIVE = [0.1, 0.4, 0.6, 0.8, 1.0]

# Published S_8 result
KIDS_S8 = 0.759
KIDS_S8_SIGMA = 0.024

# Reference and data access
KIDS_REFERENCE = "Asgari et al. 2021, A&A 645, A104"
KIDS_DATA_URL = "http://kids.strw.leidenuniv.nl/DR4/"
KIDS_DATA_RELEASE = "DR4"
KIDS_DATA_DIR = "./data/kids1000/KiDS1000_cosmis_shear_data_release/data_fits"

# Complete metadata object
KIDS_1000 = SurveyMetadata(
    name=KIDS_NAME,
    full_name=KIDS_FULL_NAME,
    telescope=KIDS_TELESCOPE,
    location=KIDS_LOCATION,
    area_deg2=KIDS_AREA_DEG2,
    n_bins=KIDS_N_BINS,
    z_bins=KIDS_Z_BINS,
    z_effective=KIDS_Z_EFFECTIVE,
    S8_measured=KIDS_S8,
    S8_sigma=KIDS_S8_SIGMA,
    reference=KIDS_REFERENCE,
    data_url=KIDS_DATA_URL,
    data_release=KIDS_DATA_RELEASE
)


# ============================================================================
# DES-Y3 Survey
# ============================================================================

DES_NAME = "DES-Y3"
DES_FULL_NAME = "Dark Energy Survey - Year 3"
DES_TELESCOPE = "Blanco 4m"
DES_LOCATION = "CTIO, Chile"
DES_AREA_DEG2 = 4143.0  # 4100 often quoted, 4143 precise
DES_N_BINS = 4

# Tomographic redshift bins
DES_Z_BINS = [
    (0.2, 0.43),
    (0.43, 0.63),
    (0.63, 0.90),
    (0.90, 1.05)
]

# Effective redshifts for each bin
DES_Z_EFFECTIVE = [0.3, 0.5, 0.7, 0.95]

# Published S_8 result
DES_S8 = 0.776
DES_S8_SIGMA = 0.017

# Reference and data access
DES_REFERENCE = "Abbott et al. 2022, PRD 105, 023520"
DES_DATA_URL = "https://des.ncsa.illinois.edu/releases/y3a2"
DES_DATA_RELEASE = "Y3A2"
DES_DATA_DIR = "./data/des_y3"

# Alternative redshift bin definitions (source vs lens samples)
DES_Z_BINS_SOURCE = DES_Z_BINS  # Source galaxy bins for cosmic shear
DES_Z_BINS_LENS = [
    (0.20, 0.40),
    (0.40, 0.60),
    (0.60, 0.85),
    (0.85, 1.05)
]  # Lens galaxy bins for galaxy-galaxy lensing

# Complete metadata object
DES_Y3 = SurveyMetadata(
    name=DES_NAME,
    full_name=DES_FULL_NAME,
    telescope=DES_TELESCOPE,
    location=DES_LOCATION,
    area_deg2=DES_AREA_DEG2,
    n_bins=DES_N_BINS,
    z_bins=DES_Z_BINS,
    z_effective=DES_Z_EFFECTIVE,
    S8_measured=DES_S8,
    S8_sigma=DES_S8_SIGMA,
    reference=DES_REFERENCE,
    data_url=DES_DATA_URL,
    data_release=DES_DATA_RELEASE
)


# ============================================================================
# HSC-Y3 Survey
# ============================================================================

HSC_NAME = "HSC-Y3"
HSC_FULL_NAME = "Hyper Suprime-Cam Survey - Year 3"
HSC_TELESCOPE = "Subaru 8.2m"
HSC_LOCATION = "Mauna Kea, Hawaii"
HSC_AREA_DEG2 = 416.0
HSC_N_BINS = 4

# Tomographic redshift bins
HSC_Z_BINS = [
    (0.3, 0.6),
    (0.6, 0.9),
    (0.9, 1.2),
    (1.2, 1.5)
]

# Effective redshifts for each bin
HSC_Z_EFFECTIVE = [0.4, 0.75, 1.1, 1.35]

# Published S_8 result
# Note: HSC has reported different values; using cosmic shear only
HSC_S8 = 0.780  # Cosmic shear only (Li et al. 2023)
HSC_S8_SIGMA = 0.033  # Conservative uncertainty

# Alternative values from Hikage et al. 2019
HSC_S8_HIKAGE = 0.763
HSC_S8_SIGMA_HIKAGE = 0.020

# Reference and data access
HSC_REFERENCE = "Hikage et al. 2019, PASJ 71, 43; Li et al. 2023"
HSC_DATA_URL = "https://hsc-release.mtk.nao.ac.jp/"
HSC_DATA_RELEASE = "PDR3"
HSC_DATA_DIR = "./data/hsc_y3"

# Complete metadata object
HSC_Y3 = SurveyMetadata(
    name=HSC_NAME,
    full_name=HSC_FULL_NAME,
    telescope=HSC_TELESCOPE,
    location=HSC_LOCATION,
    area_deg2=HSC_AREA_DEG2,
    n_bins=HSC_N_BINS,
    z_bins=HSC_Z_BINS,
    z_effective=HSC_Z_EFFECTIVE,
    S8_measured=HSC_S8,
    S8_sigma=HSC_S8_SIGMA,
    reference=HSC_REFERENCE,
    data_url=HSC_DATA_URL,
    data_release=HSC_DATA_RELEASE
)


# ============================================================================
# All Surveys Registry
# ============================================================================

ALL_SURVEYS = {
    'kids': KIDS_1000,
    'des': DES_Y3,
    'hsc': HSC_Y3
}

SURVEY_NAMES = ['kids', 'des', 'hsc']


# ============================================================================
# Helper Functions
# ============================================================================

def get_survey(name: str) -> SurveyMetadata:
    """
    Get survey metadata by name.

    Args:
        name: Survey name ('kids', 'des', or 'hsc')

    Returns:
        SurveyMetadata object

    Raises:
        ValueError: If survey name not recognized
    """
    name_lower = name.lower()

    if name_lower in ALL_SURVEYS:
        return ALL_SURVEYS[name_lower]

    # Try matching against full names
    for survey in ALL_SURVEYS.values():
        if name.upper() in survey.name.upper():
            return survey

    raise ValueError(
        f"Unknown survey: {name}. "
        f"Valid options: {', '.join(SURVEY_NAMES)}"
    )


def get_survey_s8_values() -> Dict[str, Tuple[float, float]]:
    """
    Get all survey S8 measurements.

    Returns:
        Dictionary mapping survey name to (S8, sigma_S8)
    """
    return {
        'kids': (KIDS_S8, KIDS_S8_SIGMA),
        'des': (DES_S8, DES_S8_SIGMA),
        'hsc': (HSC_S8, HSC_S8_SIGMA)
    }


def get_survey_z_ranges() -> Dict[str, Tuple[float, float]]:
    """
    Get redshift ranges for all surveys.

    Returns:
        Dictionary mapping survey name to (z_min, z_max)
    """
    return {
        'kids': (0.1, 1.2),
        'des': (0.2, 1.05),
        'hsc': (0.3, 1.5)
    }


# ============================================================================
# Validation
# ============================================================================

# Verify all surveys have consistent structure
for name, survey in ALL_SURVEYS.items():
    assert len(survey.z_bins) == survey.n_bins, \
        f"{survey.name}: Number of z_bins must match n_bins"
    assert len(survey.z_effective) == survey.n_bins, \
        f"{survey.name}: Number of z_effective must match n_bins"
    assert survey.S8_sigma > 0, \
        f"{survey.name}: S8_sigma must be positive"
    assert survey.area_deg2 > 0, \
        f"{survey.name}: area_deg2 must be positive"
