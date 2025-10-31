#!/usr/bin/env python3
"""
Parse HSC-Y3 Data
Load HSC correlation functions (FITS or ASCII format)

REFACTORED: Now uses centralized SSOT configuration

Based on HSC Y3 data structure from:
- Li et al. 2022, ApJ 929, 152
- Dalal et al. 2023, PRD 108, 123519
- Hikage et al. 2019, PASJ 71, 43 (Y1)

Author: Eric D. Martin (All Your Baseline LLC)
Date: 2025-10-30
"""

from astropy.io import fits, ascii
import numpy as np
import json
from typing import Dict, List, Tuple
import sys
import os
import glob

# Import centralized constants (SSOT)
from config.surveys import HSC_S8

# Path to HSC data
DATA_DIR = "./data/hsc_y3"

# Possible filenames (try in order)
POSSIBLE_FILENAMES = [
    "hsc_y3_cosmic_shear_xipm.fits",
    "hsc_y3_2pt.fits",
    "hsc_pdr3_cosmic_shear.fits",
    "hsc_y3_xip.dat",  # ASCII format
    "hsc_y1_cosmic_shear_xipm.fits"  # Fallback to Y1
]

# HSC-Y3 tomographic bins
Z_BINS = [
    (0.3, 0.6),
    (0.6, 0.9),
    (0.9, 1.2),
    (1.2, 1.5)
]

# Published S8 value for verification
HSC_S8_PUBLISHED = HSC_S8
HSC_S8_SIGMA = 0.033


def find_hsc_data_file():
    """Find HSC data file from list of possible names"""
    # Try FITS files first
    for filename in POSSIBLE_FILENAMES:
        if filename.endswith('.fits'):
            filepath = os.path.join(DATA_DIR, filename)
            if os.path.exists(filepath):
                return filepath, 'fits'

    # Try ASCII files
    for filename in POSSIBLE_FILENAMES:
        if filename.endswith('.dat') or filename.endswith('.txt'):
            filepath = os.path.join(DATA_DIR, filename)
            if os.path.exists(filepath):
                return filepath, 'ascii'

    # Try wildcards
    fits_files = glob.glob(os.path.join(DATA_DIR, "*.fits"))
    if fits_files:
        return fits_files[0], 'fits'

    dat_files = glob.glob(os.path.join(DATA_DIR, "*.dat"))
    if dat_files:
        return dat_files[0], 'ascii'

    return None, None


def load_hsc_fits_format(filepath):
    """Load HSC data from FITS file"""

    print(f"Loading FITS file: {os.path.basename(filepath)}")

    hdul = fits.open(filepath)

    # Inspect structure
    print("\nFITS file structure:")
    hdul.info()
    print("")

    # HSC may use different extension naming conventions
    # Try common patterns

    bins_data = {}

    try:
        # Pattern 1: Similar to KiDS/DES (xip, xim extensions)
        if 'xip' in [h.name.lower() for h in hdul]:
            xip_data = hdul['xip'].data
            xim_data = hdul['xim'].data

            print("Using xip/xim extension structure")
            print(f"Columns: {xip_data.dtype.names}")

            # Parse similar to DES
            for bin_idx in range(4):
                bin_num = bin_idx + 1
                mask_xip = (xip_data['BIN1'] == bin_num) & (xip_data['BIN2'] == bin_num)
                mask_xim = (xim_data['BIN1'] == bin_num) & (xim_data['BIN2'] == bin_num)

                bin_xip = xip_data[mask_xip]
                bin_xim = xim_data[mask_xim]

                if len(bin_xip) == 0:
                    continue

                z_low, z_high = Z_BINS[bin_idx]
                z_eff = (z_low + z_high) / 2.0

                bins_data[bin_idx] = {
                    'z_bin': (z_low, z_high),
                    'z_eff': z_eff,
                    'theta_arcmin': bin_xip['ANG'],
                    'xi_plus': bin_xip['VALUE'],
                    'xi_minus': bin_xim['VALUE'],
                    'n_points': len(bin_xip)
                }

        # Pattern 2: Separate tables for each bin
        elif any('bin' in h.name.lower() for h in hdul):
            print("Using per-bin table structure")

            for bin_idx in range(4):
                # Look for extension names like 'BIN1', 'bin_1', etc.
                possible_names = [f'BIN{bin_idx+1}', f'bin{bin_idx+1}', f'bin_{bin_idx+1}']

                ext_data = None
                for name in possible_names:
                    if name in [h.name for h in hdul] or name.lower() in [h.name.lower() for h in hdul]:
                        ext_data = hdul[name].data if name in [h.name for h in hdul] else hdul[name.lower()].data
                        break

                if ext_data is None:
                    continue

                z_low, z_high = Z_BINS[bin_idx]
                z_eff = (z_low + z_high) / 2.0

                # Extract data (column names may vary)
                if 'theta' in ext_data.dtype.names:
                    theta = ext_data['theta']
                elif 'THETA' in ext_data.dtype.names:
                    theta = ext_data['THETA']
                elif 'ANG' in ext_data.dtype.names:
                    theta = ext_data['ANG']
                else:
                    theta = np.arange(len(ext_data))  # Fallback

                # Try to find xip/xim columns
                xip_col = None
                xim_col = None
                for col in ext_data.dtype.names:
                    if 'xip' in col.lower() or 'xi_plus' in col.lower():
                        xip_col = col
                    if 'xim' in col.lower() or 'xi_minus' in col.lower():
                        xim_col = col

                if xip_col and xim_col:
                    bins_data[bin_idx] = {
                        'z_bin': (z_low, z_high),
                        'z_eff': z_eff,
                        'theta_arcmin': theta,
                        'xi_plus': ext_data[xip_col],
                        'xi_minus': ext_data[xim_col],
                        'n_points': len(theta)
                    }

        # Pattern 3: Single table with all data
        elif len(hdul) > 1:
            print("Using single table structure")
            main_data = hdul[1].data
            print(f"Columns: {main_data.dtype.names}")

            # This would need customization based on actual HSC format
            # For now, provide diagnostic output
            print("\n⚠️  Please inspect FITS structure and adapt parser")
            print("Available columns:", main_data.dtype.names)

    except Exception as e:
        print(f"\n⚠️  ERROR parsing FITS: {e}")

    # Try to get covariance
    covmat = None
    if 'covmat' in [h.name.lower() for h in hdul]:
        covmat = hdul['covmat'].data
    elif 'COVMAT' in [h.name for h in hdul]:
        covmat = hdul['COVMAT'].data

    return bins_data, covmat


def load_hsc_ascii_format(filepath):
    """Load HSC data from ASCII file"""

    print(f"Loading ASCII file: {os.path.basename(filepath)}")

    try:
        data = ascii.read(filepath)
        print(f"\nColumns: {data.colnames}")
        print(f"Rows: {len(data)}")

        # ASCII format typically has structure:
        # theta_arcmin  xip_bin1  xim_bin1  xip_bin2  xim_bin2  ...

        bins_data = {}

        for bin_idx in range(4):
            # Look for columns like 'xip_bin1', 'xip_1', 'xip_11' (auto-correlation)
            xip_cols = [col for col in data.colnames if 'xip' in col.lower() and (f'{bin_idx+1}' in col or f'bin{bin_idx+1}' in col)]
            xim_cols = [col for col in data.colnames if 'xim' in col.lower() and (f'{bin_idx+1}' in col or f'bin{bin_idx+1}' in col)]

            if not xip_cols or not xim_cols:
                # Try auto-correlation notation: xip_11, xip_22, etc.
                xip_cols = [col for col in data.colnames if f'xip_{bin_idx+1}{bin_idx+1}' in col.lower()]
                xim_cols = [col for col in data.colnames if f'xim_{bin_idx+1}{bin_idx+1}' in col.lower()]

            if xip_cols and xim_cols:
                # Get angular scales
                theta_col = [col for col in data.colnames if 'theta' in col.lower()][0]

                z_low, z_high = Z_BINS[bin_idx]
                z_eff = (z_low + z_high) / 2.0

                bins_data[bin_idx] = {
                    'z_bin': (z_low, z_high),
                    'z_eff': z_eff,
                    'theta_arcmin': np.array(data[theta_col]),
                    'xi_plus': np.array(data[xip_cols[0]]),
                    'xi_minus': np.array(data[xim_cols[0]]),
                    'n_points': len(data)
                }

        # Try to find covariance file
        covmat_file = filepath.replace('.dat', '_covmat.txt').replace('.txt', '_covmat.txt')
        if os.path.exists(covmat_file):
            covmat = np.loadtxt(covmat_file)
        else:
            covmat = None

        return bins_data, covmat

    except Exception as e:
        print(f"\n⚠️  ERROR parsing ASCII: {e}")
        return {}, None


def load_hsc_y3_data():
    """Load HSC-Y3 correlation function data"""

    print("="*80)
    print("LOADING HSC-Y3 DATA")
    print("="*80)

    # Find data file
    filepath, file_format = find_hsc_data_file()

    if filepath is None:
        print("\n⚠️  ERROR: No HSC-Y3 data file found")
        print(f"\nSearched for files in: {DATA_DIR}")
        print("Expected filenames:")
        for fname in POSSIBLE_FILENAMES:
            print(f"  - {fname}")
        print("\nPlease download HSC-Y3 data:")
        print("  1. Run: ./scripts/download_hsc_y3.sh")
        print("  2. Or see: ./data/hsc_y3/README_DOWNLOAD_INSTRUCTIONS.md")
        sys.exit(1)

    print(f"\nFound data file: {os.path.basename(filepath)}")
    print(f"Format: {file_format.upper()}")
    print("")

    # Load based on format
    if file_format == 'fits':
        bins_data, covmat = load_hsc_fits_format(filepath)
    elif file_format == 'ascii':
        bins_data, covmat = load_hsc_ascii_format(filepath)
    else:
        print(f"\n⚠️  ERROR: Unknown format: {file_format}")
        sys.exit(1)

    if not bins_data:
        print("\n⚠️  ERROR: No data was loaded")
        sys.exit(1)

    # Print summary
    for bin_idx, data in bins_data.items():
        print(f"\nBin {bin_idx+1} (z={data['z_bin'][0]:.2f}-{data['z_bin'][1]:.2f}, z_eff={data['z_eff']:.2f}):")
        print(f"  Angular scales: {data['theta_arcmin'][0]:.2f} - {data['theta_arcmin'][-1]:.2f} arcmin")
        print(f"  ξ₊ range: {data['xi_plus'].min():.2e} - {data['xi_plus'].max():.2e}")
        print(f"  ξ₋ range: {data['xi_minus'].min():.2e} - {data['xi_minus'].max():.2e}")
        print(f"  Number of points: {data['n_points']}")

    # Calculate mean for verification
    all_xi_plus = np.concatenate([bins_data[i]['xi_plus'] for i in range(len(bins_data))])
    mean_xi = np.mean(all_xi_plus)

    print("\n" + "="*80)
    print("DATA LOADING COMPLETE")
    print("="*80)
    print(f"\nTotal measurements: {sum(bins_data[i]['n_points'] for i in range(len(bins_data)))} per correlation function")
    print(f"Total data points: {2 * sum(bins_data[i]['n_points'] for i in range(len(bins_data)))} (ξ+ and ξ-)")
    print(f"\nPublished HSC-Y3 S₈: {HSC_S8_PUBLISHED} ± {HSC_S8_SIGMA}")
    print(f"Mean ξ₊ (all bins): {mean_xi:.2e} (for verification)")

    return bins_data, covmat


def save_parsed_data(bins_data, covmat, output_file="hsc_y3_parsed.json"):
    """Save parsed data to JSON for later use"""

    output = {
        'survey': 'HSC-Y3',
        'reference': 'Li et al. 2022, ApJ 929, 152',
        'n_bins': len(bins_data),
        'published_S8': HSC_S8_PUBLISHED,
        'published_S8_sigma': HSC_S8_SIGMA,
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
    print("║                      HSC-Y3 Data Parser                                ║")
    print("║                                                                        ║")
    print("║  Loads real HSC-Y3 cosmic shear correlation functions                 ║")
    print("║  For cross-validation with KiDS-1000 and DES-Y3                       ║")
    print("╚════════════════════════════════════════════════════════════════════════╝")
    print("")

    # Load data
    bins_data, covmat = load_hsc_y3_data()

    # Save parsed data
    save_parsed_data(bins_data, covmat)

    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("="*80)
    print("1. Run multi-resolution analysis:")
    print("   python3 hsc_y3_real_analysis.py")
    print("")
    print("2. Compare with KiDS-1000 and DES-Y3:")
    print("   python3 real_cross_survey_validation.py")
    print("")
