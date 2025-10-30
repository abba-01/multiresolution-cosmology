# DES Y3 Data - What We Need vs What You Found

## ✅ What You Found: Y3 Gold Catalog

**URL**: https://des.ncsa.illinois.edu/releases/y3a2/
**Contents**: Galaxy catalog with:
- Object positions (RA, DEC)
- Magnitudes in grizY bands
- Star/galaxy classification
- Photo-z estimates
- ~690 million objects

**Good for**: Making galaxy catalogs, measuring correlation functions yourself

**Problem**: We need the **already-computed 2-point correlation functions**, not raw galaxy catalogs

---

## ❌ What We Actually Need: Y3 Cosmology Products

### The File We're Looking For

**Filename**: `2pt_NG_final_2ptunblind_02_26_21_wnz.fits` (or similar)

**Contents**:
- ξ+(θ) correlation functions (cosmic shear)
- ξ-(θ) correlation functions (cosmic shear)
- γt(θ) galaxy-galaxy lensing
- w(θ) galaxy clustering
- Covariance matrices
- Redshift distributions

**Reference Paper**: Abbott et al. 2022, PRD 105, 023520
- "Dark Energy Survey Year 3 results: Cosmological constraints from galaxy clustering and weak lensing"

---

## Where to Find DES Y3 2pt Data

### Option 1: DES Cosmology Data Products Page

Look for a section like:
- "Y3 Cosmology Products"
- "Y3 3×2pt Analysis"
- "Y3 Weak Lensing Products"
- "Y3 2-Point Correlation Functions"

This should be separate from the Gold catalog.

### Option 2: Direct Links to Try

```bash
# Try these URLs (may require login):
https://des.ncsa.illinois.edu/releases/y3a2/Y3key-cosmology-products/

# Or check the main Y3 page for a cosmology section:
https://des.ncsa.illinois.edu/releases/y3a2/

# Look for links to:
# - "3x2pt data vectors"
# - "2pt correlation functions"
# - "Cosmic shear measurements"
```

### Option 3: GitHub Repository

The DES Y3 3×2pt analysis team may have published data:

```bash
# Check:
https://github.com/des-science/Y3-3x2pt-methods
https://github.com/des-science/cosmology-y3

# Look for:
# - data_vectors/ directory
# - 2pt_* files
# - README with data links
```

### Option 4: Zenodo Archive

Paper supplementary data on Zenodo:

```bash
# Search:
https://zenodo.org/search?q=DES+Y3+cosmology+2pt

# Look for DOI from Abbott et al. 2022 paper
# Paper often includes "Data Availability" section with Zenodo links
```

### Option 5: Paper Supplementary Materials

Check the Physical Review D paper directly:

```bash
# Paper URL:
https://journals.aps.org/prd/abstract/10.1103/PhysRevD.105.023520

# Look for:
# - "Supplemental Material" link
# - "Data availability" section
# - Links to data files
```

---

## What the 2pt FITS File Should Contain

Once you find the right file, it should have these extensions:

```
2pt_NG_*.fits:
├── xip          # ξ+ (E-mode cosmic shear)
│   ├── BIN1     # Source bin i
│   ├── BIN2     # Source bin j
│   ├── ANGBIN   # Angular bin index
│   ├── VALUE    # ξ+ value
│   └── ANG      # θ in arcminutes
├── xim          # ξ- (B-mode cosmic shear)
│   └── (same structure as xip)
├── gammat       # Galaxy-galaxy lensing (optional)
├── wtheta       # Galaxy clustering (optional)
├── covmat       # Full covariance matrix
└── nz_source    # Redshift distributions
    ├── Z_MID    # Redshift bin centers
    ├── BIN1     # n(z) for bin 1
    ├── BIN2     # n(z) for bin 2
    └── ...
```

---

## Quick Check: Do You Have the Right File?

**If the FITS file is ~50-100 MB** → Probably correct (2pt functions)
**If the FITS file is >1 GB** → Wrong file (galaxy catalog)

**If file has extensions named**:
- `xip`, `xim`, `gammat`, `wtheta`, `covmat` → ✓ CORRECT
- `ALPHAWIN_J2000`, `DELTAWIN_J2000`, `MAG_AUTO` → ✗ WRONG (catalog)

---

## How to Navigate DES Portal

1. **Login** to https://des.ncsa.illinois.edu/releases/

2. **Navigate**:
   ```
   Y3A2 Release
   └── Weak Lensing / Cosmology Products
       └── 2-Point Correlation Functions
           └── Download: 2pt_NG_final_*.fits
   ```

3. **Alternatives** if not obvious:
   - Look for "Science Products" section
   - Look for "3×2pt Analysis" page
   - Check sidebar menu for "Cosmology"
   - Search portal for "2pt" or "correlation"

---

## Comparison Table

| Data Product | Gold Catalog | 2pt Correlation Functions |
|-------------|--------------|---------------------------|
| **File size** | GB-scale | ~50-100 MB |
| **Number of objects** | ~690 million | ~160 measurements |
| **Contains** | Galaxy positions, mags | ξ±(θ) values |
| **Use case** | Build catalogs | Cosmology constraints |
| **What we need** | ❌ No | ✅ YES |

---

## If You Can't Find 2pt Data

### Contact DES Directly

**Email**: des-data@fnal.gov

**Subject**: Request for Y3 2-point correlation function FITS files

**Body**:
```
Dear DES Data Team,

I am conducting research on weak lensing systematic corrections and need
access to the DES Y3 cosmic shear 2-point correlation functions (ξ+ and ξ-)
for cross-validation with KiDS-1000 and HSC-Y3 data.

I have access to the Y3 Gold catalog, but I specifically need the 2pt
correlation function data products from the cosmology analysis.

Reference paper: Abbott et al. 2022, PRD 105, 023520

Could you please provide:
1. Download link or location for 2pt_NG_*.fits file
2. Or direct me to the correct section of the DES portal

Thank you,
[Your Name]
```

---

## Alternative: Download from Paper Authors

Contact the lead authors of Abbott et al. 2022:
- Elisabeth Krause (Arizona)
- Michael Troxel (Duke)
- They may provide direct download links

---

## For Now

While searching for the 2pt data:

1. **Register for DES portal** (if not done): https://des.ncsa.illinois.edu/easaccess/
2. **Search portal** for "cosmology" or "2pt" or "weak lensing"
3. **Check GitHub repos** linked above
4. **Email DES team** with template above

The Gold catalog is useful for many things, but for our cross-validation we
specifically need the pre-computed 2-point correlation functions from the
cosmology analysis.

---

**Status**: Still looking for 2pt correlation functions
**Next**: Search DES portal for cosmology/2pt products section
