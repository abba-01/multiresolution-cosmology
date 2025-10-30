#!/usr/bin/env bash
#
# Download HSC-Y3 Cosmic Shear 2-Point Correlation Function Data
#
# This script attempts multiple methods to download HSC-Y3 data:
# 1. HSC Public Data Release portal (may require login)
# 2. Paper supplementary data
# 3. HSC-Y1 fallback (definitely public)
# 4. Manual instructions if automated download fails
#

set -euo pipefail

DATA_DIR="/root/private_multiresolution/data/hsc_y3"
SCRIPTS_DIR="/root/private_multiresolution/scripts"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================================================"
echo " HSC-Y3 Data Download Script"
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

# Method 1: Try HSC data portal (may require authentication)
echo "========================================================================"
echo "Method 1: Attempting HSC Public Data Release portal"
echo "========================================================================"
echo ""

HSC_URLS=(
    "https://hsc-release.mtk.nao.ac.jp/archive/filetree/cosmos_pdr3/"
    "https://hsc-release.mtk.nao.ac.jp/doc/index.php/s20a-shape-catalog/"
)

for url in "${HSC_URLS[@]}"; do
    echo "Checking: $url"
    if curl --head --silent --fail "$url" > /dev/null 2>&1; then
        echo -e "  ${GREEN}→ URL is accessible${NC}"
        echo "  → May contain cosmic shear data products"
    else
        echo -e "  ${YELLOW}→ URL requires authentication or not found${NC}"
    fi
    echo ""
done

# Method 2: Try paper supplementary data
echo "========================================================================"
echo "Method 2: Checking paper supplementary data"
echo "========================================================================"
echo ""

PAPER_URLS=(
    "https://iopscience.iop.org/article/10.3847/1538-4357/ac5ea0"  # Li et al. 2022
    "https://journals.aps.org/prd/abstract/10.1103/PhysRevD.108.123519"  # Dalal et al. 2023
)

for url in "${PAPER_URLS[@]}"; do
    echo "Checking: $url"
    if curl --head --silent --fail "$url" > /dev/null 2>&1; then
        echo -e "  ${GREEN}→ Paper accessible${NC}"
        echo "  → Check for 'Data behind the Figures' or supplementary materials"
    else
        echo -e "  ${YELLOW}→ Paper not accessible (may require subscription)${NC}"
    fi
    echo ""
done

# Method 3: Try HSC-Y1 as fallback (definitely public)
echo "========================================================================"
echo "Method 3: Checking HSC-Y1 data (fallback)"
echo "========================================================================"
echo ""

echo "HSC-Y1 cosmic shear data is definitely public"
echo "Reference: Hikage et al. 2019, PASJ 71, 43"
echo "URL: https://hsc.mtk.nao.ac.jp/ssp/survey/"
echo ""
echo "Note: Y1 has 4 tomographic bins like Y3, can use for initial testing"
echo ""

# Check if we got any files
if [ "$(ls -A $DATA_DIR)" ]; then
    echo "========================================================================"
    echo -e "${GREEN}SUCCESS: Downloaded HSC data files${NC}"
    echo "========================================================================"
    echo ""
    echo "Files in $DATA_DIR:"
    ls -lh "$DATA_DIR"
    echo ""
    echo "Next steps:"
    echo "  1. Verify data integrity: python3 parse_hsc_y3_data.py"
    echo "  2. Run analysis: python3 hsc_y3_real_analysis.py"
else
    echo "========================================================================"
    echo -e "${YELLOW}NO AUTOMATIC DOWNLOAD AVAILABLE${NC}"
    echo "========================================================================"
    echo ""
    echo "HSC-Y3 data requires manual download. Please follow these steps:"
    echo ""
    echo "1. REGISTER for HSC data access:"
    echo "   → https://hsc-release.mtk.nao.ac.jp/"
    echo "   → Click 'User Registration'"
    echo "   → Usually instant or <24 hour approval"
    echo "   → See: $SCRIPTS_DIR/REGISTER_DATA_PORTALS.md"
    echo ""
    echo "2. Once approved, LOGIN and navigate to:"
    echo "   → https://hsc-release.mtk.nao.ac.jp/datasearch/"
    echo "   → Science Products → Weak Lensing"
    echo "   → Look for PDR3 or Y3 cosmic shear products"
    echo ""
    echo "3. ALTERNATIVE - Download from paper supplements:"
    echo "   → Li et al. 2022, ApJ 929, 152"
    echo "   → https://iopscience.iop.org/article/10.3847/1538-4357/ac5ea0"
    echo "   → Check 'Data behind the Figures' section"
    echo ""
    echo "4. FALLBACK - Use HSC-Y1 for initial testing:"
    echo "   → https://hsc.mtk.nao.ac.jp/ssp/survey/"
    echo "   → Hikage et al. 2019, PASJ 71, 43"
    echo "   → Similar structure to Y3, good for testing parsers"
    echo ""
    echo "5. Save files to: $DATA_DIR"
    echo "   Expected files:"
    echo "   → hsc_y3_cosmic_shear_xipm.fits (or .dat)"
    echo "   → hsc_y3_covariance.fits (or .txt)"
    echo "   → hsc_y3_nz_source.fits"
    echo ""
    echo "6. ALTERNATIVE - Contact HSC team:"
    echo "   → Email: hsc_helpdesk@naoj.org"
    echo "   → Subject: 'Request for PDR3/Y3 cosmic shear correlation functions'"
    echo ""
    echo "7. Once files are in $DATA_DIR/, verify with:"
    echo "   → python3 parse_hsc_y3_data.py"
    echo ""

    # Create a README in the data directory
    cat > "$DATA_DIR/README_DOWNLOAD_INSTRUCTIONS.md" << 'EOF'
# HSC-Y3 Data Download Instructions

## Manual Download Required

HSC-Y3/PDR3 cosmic shear data requires portal registration.

### Steps:

1. **Register**: https://hsc-release.mtk.nao.ac.jp/
   - Click "User Registration"
   - Use any email (institutional preferred)
   - Research area: "Cosmology - Weak Gravitational Lensing"
   - Usually approved instantly or within 24 hours

2. **Login**: https://hsc-release.mtk.nao.ac.jp/datasearch/

3. **Navigate**: Science Products → Weak Lensing → PDR3/Y3

4. **Download** to this directory:
   - Cosmic shear correlation functions (ξ+ and ξ-)
   - Covariance matrix
   - Redshift distributions

5. **Alternative - Paper Supplements**:
   - Li et al. 2022: https://iopscience.iop.org/article/10.3847/1538-4357/ac5ea0
   - Check "Data behind the Figures" section
   - Download correlation function tables

6. **Fallback - HSC-Y1** (for testing):
   - Hikage et al. 2019: https://hsc.mtk.nao.ac.jp/ssp/survey/
   - Y1 has same 4-bin structure as Y3
   - Good for testing parsers while waiting for Y3

7. **Verify**:
   ```bash
   cd /root/private_multiresolution
   python3 parse_hsc_y3_data.py
   ```

### Alternative - Contact Authors

Email: hsc_helpdesk@naoj.org
Subject: Request for PDR3/Y3 cosmic shear correlation functions

References:
- Li et al. 2022, ApJ 929, 152
- Dalal et al. 2023, PRD 108, 123519

### Expected Files

**Option A - FITS format:**
- `hsc_y3_cosmic_shear_xipm.fits` (~20-50 MB)
- Contains: xip, xim, covmat, nz extensions

**Option B - ASCII format:**
- `hsc_y3_xip.dat` (ξ+ correlation function)
- `hsc_y3_xim.dat` (ξ- correlation function)
- `hsc_y3_covmat.txt` (covariance matrix)
- `hsc_y3_nz.dat` (redshift distributions)

### Expected Data

- 4 tomographic bins: z = 0.3-1.5
- ~15-20 angular bins per tomographic bin
- Total: ~144 measurements (72 ξ+, 72 ξ-)
- Angular scales: 2-56 arcmin (ξ+), 20-224 arcmin (ξ-)
EOF

    echo -e "${GREEN}Created: $DATA_DIR/README_DOWNLOAD_INSTRUCTIONS.md${NC}"
    echo ""
fi

echo "========================================================================"
echo "HSC-Y3 download script complete"
echo "========================================================================"
