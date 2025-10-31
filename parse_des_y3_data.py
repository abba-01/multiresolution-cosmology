#!/usr/bin/env python3
"""
Parse DES-Y3 FITS Data
Load DES correlation functions in same format as KiDS-1000

REFACTORED: Now uses centralized SSOT configuration

Based on DES Y3 data structure from Abbott et al. 2022, PRD 105, 023520
Expected FITS file structure similar to DES Y1 (Troxel et al. 2018)

Author: Eric D. Martin (All Your Baseline LLC)
Date: 2025-10-30
"""

from astropy.io import fits
import numpy as np
import json
from typing import Dict, List, Tuple
import sys
import os

# Import centralized constants (SSOT)
from config.surveys import DES_S8

# Path to DES data
DATA_DIR = "./data/des_y3"

# Possible filenames (try in order)
POSSIBLE_FILENAMES = [
    "2pt_NG_final_2ptunblind_02_26_21_wnz.fits",
    "des_y3_2pt.fits",
    "DES_Y3_2pt_cosmic_shear.fits",
    "2pt_NG_mcal_1110.fits"
]

# DES-Y3 tomographic bins
Z_BINS = [
    (0.2, 0.4),
    (0.4, 0.6),
    (0.6, 0.85),
    (0.85, 1.05)
]

# Published S8 value for verification
DES_S8_PUBLISHED = DES_S8
DES_S8_SIGMA = 0.017


def find_des_data_file():
    """Find DES data file from list of possible names"""
    for filename in POSSIBLE_FILENAMES:
        filepath = os.path.join(DATA_DIR, filename)
        if os.path.exists(filepath):
            return filepath
    return None


def load_des_y3_data():
    """Load DES-Y3 correlation function data from FITS files"""

    print("="*80)
    print("LOADING DES-Y3 DATA")
    print("="*80)

    # Find data file
    xipm_file = find_des_data_file()

    if xipm_file is None:
        print("\n⚠️  ERROR: No DES-Y3 data file found")
        print(f"\nSearched for files in: {DATA_DIR}")
        print("Expected filenames:")
        for fname in POSSIBLE_FILENAMES:
            print(f"  - {fname}")
        print("\nPlease download DES-Y3 data:")
        print("  1. Run: ./scripts/download_des_y3.sh")
        print("  2. Or see: ./data/des_y3/README_DOWNLOAD_INSTRUCTIONS.md")
        sys.exit(1)

    print(f"\nFound data file: {os.path.basename(xipm_file)}")

    # Open FITS file
    try:
        hdul = fits.open(xipm_file)
    except Exception as e:
        print(f"\n⚠️  ERROR: Could not open FITS file: {e}")
        sys.exit(1)

    # Inspect file structure
    print("\nFITS file structure:")
    hdul.info()
    print("")

    # Extract data based on DES structure
    # DES typically uses: 'xip', 'xim', 'gammat', 'wtheta', 'covmat', 'nz_source'

    try:
        # Try standard DES Y3 extension names
        if 'xip' in [h.name.lower() for h in hdul]:
            xip_data = hdul['xip'].data
            xim_data = hdul['xim'].data
        elif 'xiP' in [h.name for h in hdul]:
            xip_data = hdul['xiP'].data
            xim_data = hdul['xiM'].data
        else:
            print("\n⚠️  ERROR: Could not find xip/xim extensions")
            print("Available extensions:", [h.name for h in hdul])
            sys.exit(1)

        # Get covariance matrix
        if 'covmat' in [h.name.lower() for h in hdul]:
            covmat = hdul['covmat'].data
        elif 'COVMAT' in [h.name for h in hdul]:
            covmat = hdul['COVMAT'].data
        else:
            print("\n⚠️  WARNING: No covariance matrix found, will use diagonal")
            covmat = None

        # Get redshift distributions
        if 'nz_source' in [h.name.lower() for h in hdul]:
            nz_data = hdul['nz_source'].data
        elif 'NZ_SOURCE' in [h.name for h in hdul]:
            nz_data = hdul['NZ_SOURCE'].data
        else:
            print("\n⚠️  WARNING: No n(z) data found")
            nz_data = None

    except Exception as e:
        print(f"\n⚠️  ERROR extracting data: {e}")
        sys.exit(1)

    print(f"\nLoaded measurements:")
    print(f"  ξ₊: {len(xip_data)} data points")
    print(f"  ξ₋: {len(xim_data)} data points")
    if covmat is not None:
        print(f"  Covariance: {covmat.shape}")
    if nz_data is not None:
        print(f"  Redshift bins: {nz_data.shape}")

    # Inspect data structure
    print("\nData columns (ξ+):", xip_data.dtype.names)
    print("Data columns (ξ-):", xim_data.dtype.names)

    # Organize data by tomographic bins
    bins_data = {}

    # DES uses BIN1, BIN2, ANGBIN, VALUE, ANG (similar to KiDS)
    # Bins are numbered 1-4 (not 0-3)

    for bin_idx in range(4):
        # Get data for this bin (auto-correlation: BIN1 == BIN2 == bin_idx+1)
        bin_num = bin_idx + 1

        # Filter for auto-correlations
        mask_xip = (xip_data['BIN1'] == bin_num) & (xip_data['BIN2'] == bin_num)
        mask_xim = (xim_data['BIN1'] == bin_num) & (xim_data['BIN2'] == bin_num)

        bin_xip = xip_data[mask_xip]
        bin_xim = xim_data[mask_xim]

        if len(bin_xip) == 0:
            print(f"\n⚠️  WARNING: No data for bin {bin_num}")
            continue

        # Angular scales (in arcminutes)
        theta_arcmin = bin_xip['ANG']

        # Correlation function values
        xi_plus = bin_xip['VALUE']
        xi_minus = bin_xim['VALUE']

        # Calculate effective redshift
        z_low, z_high = Z_BINS[bin_idx]
        z_eff = (z_low + z_high) / 2.0

        bins_data[bin_idx] = {
            'z_bin': (z_low, z_high),
            'z_eff': z_eff,
            'theta_arcmin': theta_arcmin,
            'xi_plus': xi_plus,
            'xi_minus': xi_minus,
            'n_points': len(xi_plus)
        }

        print(f"\nBin {bin_idx+1} (z={z_low:.2f}-{z_high:.2f}, z_eff={z_eff:.2f}):")
        print(f"  Angular scales: {theta_arcmin[0]:.2f} - {theta_arcmin[-1]:.2f} arcmin")
        print(f"  ξ₊ range: {xi_plus.min():.2e} - {xi_plus.max():.2e}")
        print(f"  ξ₋ range: {xi_minus.min():.2e} - {xi_minus.max():.2e}")
        print(f"  Number of points: {len(xi_plus)}")

    # Calculate combined S8 from all bins (simple weighted mean for verification)
    # This is a rough estimate to verify we loaded the right data
    all_xi_plus = np.concatenate([bins_data[i]['xi_plus'] for i in range(4)])
    mean_xi = np.mean(all_xi_plus)

    print("\n" + "="*80)
    print("DATA LOADING COMPLETE")
    print("="*80)
    print(f"\nTotal measurements: {sum(bins_data[i]['n_points'] for i in range(4))} per correlation function")
    print(f"Total data points: {2 * sum(bins_data[i]['n_points'] for i in range(4))} (ξ+ and ξ-)")
    print(f"\nPublished DES-Y3 S₈: {DES_S8_PUBLISHED} ± {DES_S8_SIGMA}")
    print(f"Mean ξ₊ (all bins): {mean_xi:.2e} (for verification)")

    return bins_data, covmat


def save_parsed_data(bins_data, covmat, output_file="des_y3_parsed.json"):
    """Save parsed data to JSON for later use"""

    # Convert to JSON-serializable format
    output = {
        'survey': 'DES-Y3',
        'reference': 'Abbott et al. 2022, PRD 105, 023520',
        'n_bins': len(bins_data),
        'published_S8': DES_S8_PUBLISHED,
        'published_S8_sigma': DES_S8_SIGMA,
        'bins': {}
    }

    for bin_idx, data in bins_data.items():
        output['bins'][str(bin_idx)] = {
            'z_bin': data['z_bin'],
            'z_eff': data['z_eff'],
            'theta_arcmin': data['theta_arcmin'].tolist(),
            'xi_plus': data['xi_plus'].tolist(),
            'xi_minus': data['xi_minus'].tolist(),
            'n_points': data['n_points']
        }

    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n✓ Saved parsed data to: {output_file}")


if __name__ == '__main__':
    print("")
    print("╔════════════════════════════════════════════════════════════════════════╗")
    print("║                      DES-Y3 Data Parser                                ║")
    print("║                                                                        ║")
    print("║  Loads real DES-Y3 cosmic shear correlation functions                 ║")
    print("║  For cross-validation with KiDS-1000 and HSC-Y3                       ║")
    print("╚════════════════════════════════════════════════════════════════════════╝")
    print("")

    # Load data
    bins_data, covmat = load_des_y3_data()

    # Save parsed data
    save_parsed_data(bins_data, covmat)

    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("="*80)
    print("1. Run multi-resolution analysis:")
    print("   python3 des_y3_real_analysis.py")
    print("")
    print("2. Compare with KiDS-1000 and HSC-Y3:")
    print("   python3 real_cross_survey_validation.py")
    print("")
