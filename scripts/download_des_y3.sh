#!/usr/bin/env bash
#
# Download DES-Y3 Cosmic Shear 2-Point Correlation Function Data
#
# This script attempts multiple methods to download DES-Y3 data:
# 1. Direct download from NCSA (if public)
# 2. Zenodo archive (if uploaded)
# 3. GitHub repository (if available)
# 4. Manual instructions if automated download fails
#

set -euo pipefail

DATA_DIR="/root/private_multiresolution/data/des_y3"
SCRIPTS_DIR="/root/private_multiresolution/scripts"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================================================"
echo " DES-Y3 Data Download Script"
echo "========================================================================"
echo ""
echo "Target directory: $DATA_DIR"
echo ""

# Ensure data directory exists
mkdir -p "$DATA_DIR"

# Function to check if file was downloaded successfully
check_download() {
    local file="$1"
    local min_size="$2"

    if [ -f "$file" ]; then
        local size=$(stat --format=%s "$file" 2>/dev/null || echo "0")
        if [ "$size" -gt "$min_size" ]; then
            echo -e "${GREEN}✓ Successfully downloaded: $(basename $file) (${size} bytes)${NC}"
            return 0
        else
            echo -e "${RED}✗ Downloaded file too small: $(basename $file) (${size} bytes < ${min_size})${NC}"
            rm -f "$file"
            return 1
        fi
    else
        echo -e "${RED}✗ File not found: $(basename $file)${NC}"
        return 1
    fi
}

# Method 1: Try direct NCSA download
echo "========================================================================"
echo "Method 1: Attempting direct download from DES NCSA portal"
echo "========================================================================"
echo ""

NCSA_URLS=(
    "https://des.ncsa.illinois.edu/releases/y3a2/Y3_mastercat_02_26_21_gridspec512.h5"
    "https://des.ncsa.illinois.edu/releases/y3a2/2pt_NG_final_2ptunblind_02_26_21_wnz.fits"
    "https://des.ncsa.illinois.edu/releases/y3a2/DES_Y3_covariance_2pt.fits"
)

success=false
for url in "${NCSA_URLS[@]}"; do
    filename=$(basename "$url")
    echo "Trying: $url"

    if wget --spider "$url" 2>&1 | grep -q '200 OK'; then
        echo "  → URL is accessible, downloading..."
        wget -O "$DATA_DIR/$filename" "$url" && success=true
        check_download "$DATA_DIR/$filename" 1000000 # At least 1MB
    elif curl --head --silent --fail "$url" > /dev/null 2>&1; then
        echo "  → URL is accessible (via curl), downloading..."
        curl -L -o "$DATA_DIR/$filename" "$url" && success=true
        check_download "$DATA_DIR/$filename" 1000000
    else
        echo -e "  ${YELLOW}→ URL not accessible (may require authentication)${NC}"
    fi
    echo ""
done

# Method 2: Try Zenodo
echo "========================================================================"
echo "Method 2: Searching Zenodo for DES-Y3 data"
echo "========================================================================"
echo ""

# Known Zenodo records for DES Y3 (add actual DOIs when found)
ZENODO_RECORDS=(
    "10.5281/zenodo.XXXXX"  # Placeholder - check https://zenodo.org/search?q=DES+Y3
)

echo "Note: Zenodo links may need to be updated with actual DES-Y3 DOIs"
echo "Check: https://zenodo.org/search?q=DES+Y3+cosmic+shear"
echo ""

# Method 3: Check GitHub
echo "========================================================================"
echo "Method 3: Checking DES GitHub repositories"
echo "========================================================================"
echo ""

GITHUB_REPOS=(
    "https://github.com/des-science/Y3-3x2pt-methods"
    "https://github.com/des-science/Y3-catalogs"
)

for repo in "${GITHUB_REPOS[@]}"; do
    echo "Checking: $repo"
    if curl --head --silent --fail "$repo" > /dev/null 2>&1; then
        echo -e "  ${GREEN}→ Repository exists${NC}"
        echo "  → Check for data releases or data files"
    else
        echo -e "  ${YELLOW}→ Repository not found or not public${NC}"
    fi
    echo ""
done

# Check if we got any files
if [ "$(ls -A $DATA_DIR)" ]; then
    echo "========================================================================"
    echo -e "${GREEN}SUCCESS: Downloaded DES-Y3 data files${NC}"
    echo "========================================================================"
    echo ""
    echo "Files in $DATA_DIR:"
    ls -lh "$DATA_DIR"
    echo ""
    echo "Next steps:"
    echo "  1. Verify data integrity: python3 parse_des_y3_data.py"
    echo "  2. Run analysis: python3 des_y3_real_analysis.py"
else
    echo "========================================================================"
    echo -e "${YELLOW}NO AUTOMATIC DOWNLOAD AVAILABLE${NC}"
    echo "========================================================================"
    echo ""
    echo "DES-Y3 data requires manual download. Please follow these steps:"
    echo ""
    echo "1. REGISTER for DES data access:"
    echo "   → https://des.ncsa.illinois.edu/easaccess/"
    echo "   → See: $SCRIPTS_DIR/REGISTER_DATA_PORTALS.md"
    echo ""
    echo "2. Once approved, LOGIN and navigate to:"
    echo "   → https://des.ncsa.illinois.edu/releases/y3a2/"
    echo "   → Weak Lensing → 2-Point Correlation Functions"
    echo ""
    echo "3. Download these files to $DATA_DIR:"
    echo "   → 2pt_NG_final_2ptunblind_02_26_21_wnz.fits"
    echo "   → DES_Y3_covariance_2pt.fits (if separate)"
    echo "   → DES_Y3_nz_source.fits"
    echo ""
    echo "4. ALTERNATIVE - Contact DES team:"
    echo "   → Email: des-data@fnal.gov"
    echo "   → Subject: 'Request for Y3 2pt correlation function FITS files'"
    echo ""
    echo "5. Once files are in $DATA_DIR/, verify with:"
    echo "   → python3 parse_des_y3_data.py"
    echo ""

    # Create a README in the data directory
    cat > "$DATA_DIR/README_DOWNLOAD_INSTRUCTIONS.md" << 'EOF'
# DES-Y3 Data Download Instructions

## Manual Download Required

DES-Y3 cosmic shear data requires portal authentication.

### Steps:

1. **Register**: https://des.ncsa.illinois.edu/easaccess/
   - Use institutional email
   - Research purpose: "Weak lensing systematic analysis"
   - Wait 1-7 days for approval

2. **Login**: https://des.ncsa.illinois.edu/releases/

3. **Navigate**: Y3A2 Gold → Weak Lensing → 2pt Correlation Functions

4. **Download** to this directory:
   - `2pt_NG_final_2ptunblind_02_26_21_wnz.fits`
   - `DES_Y3_covariance_2pt.fits`
   - `DES_Y3_nz_source.fits`

5. **Verify**:
   ```bash
   cd /root/private_multiresolution
   python3 parse_des_y3_data.py
   ```

### Alternative - Contact Authors

Email: des-data@fnal.gov
Subject: Request for Y3 2pt correlation function FITS files

Reference: Abbott et al. 2022, PRD 105, 023520

### Expected Files

- Main 2pt file: ~50-100 MB
- Contains: xip, xim, covmat, nz_source extensions
- 4 tomographic bins, ~20 angular bins each
- Total: ~160 measurements (80 ξ+, 80 ξ-)
EOF

    echo -e "${GREEN}Created: $DATA_DIR/README_DOWNLOAD_INSTRUCTIONS.md${NC}"
    echo ""
fi

echo "========================================================================"
echo "DES-Y3 download script complete"
echo "========================================================================"
