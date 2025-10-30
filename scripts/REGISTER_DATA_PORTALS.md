# Data Portal Registration Guide

**Purpose**: Access real DES-Y3 and HSC-Y3 correlation function data for proper cross-validation.

---

## DES-Y3 Data Access

### Step 1: Register for DES Data Portal

1. **Go to**: https://des.ncsa.illinois.edu/easaccess/
2. **Click**: "Register" or "Create Account"
3. **Fill in**:
   - Name
   - Email (institutional email preferred)
   - Institution
   - Research purpose: "Cosmological analysis - weak lensing systematics"
4. **Submit** registration
5. **Wait**: 1-7 days for approval (usually 1-2 days)

### Step 2: Navigate to Y3 Data

Once approved:
1. **Login**: https://des.ncsa.illinois.edu/releases/
2. **Navigate to**: Y3A2 Gold Release
3. **Section**: Weak Lensing → 2-Point Correlation Functions
4. **Files to download**:
   - `2pt_NG_final_2ptunblind_02_26_21_wnz.fits` (main 2pt file)
   - `DES_Y3_covariance_2pt.fits` (covariance matrix)
   - `DES_Y3_nz_source.fits` (redshift distributions)

### Step 3: Alternative - Check Public Links

Try these first (may work without registration):
```bash
# Check Zenodo
https://zenodo.org/search?q=DES+Y3+cosmic+shear

# Check GitHub
https://github.com/des-science/Y3-3x2pt-methods

# Direct DESDM
https://des.ncsa.illinois.edu/releases/y3a2/
```

### Step 4: Fallback - Contact DES Team

If portal access fails:
- **Email**: des-data@fnal.gov
- **Subject**: "Request for Y3 2pt correlation function FITS files"
- **Body**:
```
Dear DES Data Team,

I am conducting research on weak lensing systematic errors and would like to access
the DES Y3 cosmic shear 2-point correlation functions (ξ+ and ξ-) for cross-validation
with KiDS-1000 and HSC-Y3 data.

Could you please provide access to:
1. 2pt correlation function FITS file (ξ+, ξ-)
2. Covariance matrix
3. Redshift distributions (n(z))

Reference paper: Abbott et al. 2022, PRD 105, 023520

Thank you,
[Your Name]
[Your Institution]
```

---

## HSC-Y3 Data Access

### Step 1: Register for HSC Data Portal

1. **Go to**: https://hsc-release.mtk.nao.ac.jp/
2. **Click**: "User Registration"
3. **Fill in**:
   - Name
   - Email
   - Institution
   - Research area: "Cosmology - Weak Gravitational Lensing"
4. **Accept** terms and conditions
5. **Submit** - Usually instant or <24 hour approval

### Step 2: Navigate to Cosmic Shear Data

Once approved:
1. **Login**: https://hsc-release.mtk.nao.ac.jp/datasearch/
2. **Navigate to**: Science Products → Weak Lensing
3. **Look for**:
   - PDR3 cosmic shear catalogs
   - Y3 correlation functions
   - COSEBIs data products

### Step 3: Check Paper Supplements

HSC papers often include data files:
1. **Li et al. 2022**: https://iopscience.iop.org/article/10.3847/1538-4357/ac5ea0
   - Check "Data behind the Figures"
   - Look for supplementary FITS/ASCII files

2. **Dalal et al. 2023**: https://journals.aps.org/prd/abstract/10.1103/PhysRevD.108.123519
   - May have correlation function tables

### Step 4: HSC-Y1 Fallback (Definitely Public)

If Y3 not immediately available, use Y1 first:
1. **Paper**: Hikage et al. 2019, PASJ 71, 43
2. **Data**: https://hsc.mtk.nao.ac.jp/ssp/survey/
3. **Look for**: First-year cosmic shear data products

### Step 5: Fallback - Contact HSC Team

If portal access fails:
- **Email**: hsc_helpdesk@naoj.org
- **Subject**: "Request for PDR3/Y3 cosmic shear correlation functions"
- **Body**:
```
Dear HSC Data Team,

I am researching weak lensing systematic errors and need access to HSC Y3/PDR3
cosmic shear 2-point correlation functions for cross-validation with KiDS-1000
and DES-Y3 surveys.

Could you please provide or direct me to:
1. ξ+(θ) and ξ-(θ) correlation functions for Y3
2. Tomographic bin definitions
3. Covariance matrix
4. Effective redshifts

Reference papers:
- Li et al. 2022, ApJ 929, 152
- Dalal et al. 2023, PRD 108, 123519

Thank you,
[Your Name]
[Your Institution]
```

---

## Expected Data Files

### DES-Y3
- **Main file**: `2pt_NG_final_2ptunblind_02_26_21_wnz.fits` (~50-100 MB)
- **Contains**:
  - `xip` extension: ξ+ correlation function
  - `xim` extension: ξ- correlation function
  - `covmat` extension: Full covariance matrix
  - `nz_source` extension: Redshift distributions
- **Structure**: BIN1, BIN2, ANGBIN, VALUE, ANG columns
- **Bins**: 4 tomographic bins (z = 0.2-1.05)

### HSC-Y3
- **Main file**: `hsc_y3_cosmic_shear_xipm.fits` or `.dat` (~20-50 MB)
- **Contains**:
  - ξ+ and ξ- for each bin pair
  - Angular scales (θ in arcminutes)
  - Covariance matrix
- **Format**: May be FITS or ASCII tables
- **Bins**: 4 tomographic bins (z = 0.3-1.5)

---

## Verification Checklist

After downloading, verify:

- [ ] Files are not corrupted (check file sizes)
- [ ] FITS files open with astropy: `fits.open(filename)`
- [ ] Expected extensions present
- [ ] Number of measurements matches expectations:
  - DES: ~160 measurements (4 bins × ~20 angles × 2)
  - HSC: ~144 measurements (4 bins × ~18 angles × 2)
- [ ] Correlation values reasonable: 10^-6 < ξ± < 10^-2
- [ ] Angular scales reasonable: 2-250 arcminutes

---

## Timeline Estimate

- **DES registration**: 1-7 days (usually 1-2 days)
- **HSC registration**: <24 hours (often instant)
- **Data download**: <5 minutes per survey
- **Total time**: 1-7 days depending on approval speed

---

## What to Do While Waiting

1. **Test with simulated data**: Create synthetic ξ± for testing parsers
2. **Prepare parser code**: Write structure assuming FITS format
3. **Study KiDS structure**: Use as template for DES/HSC parsers
4. **Check publications**: Look for data tables in paper appendices

---

## Status Tracking

Create `/root/private_multiresolution/DATA_ACCESS_LOG.md`:

```markdown
# Data Access Status Log

## DES-Y3
- [ ] Registration submitted: [DATE]
- [ ] Registration approved: [DATE]
- [ ] Data downloaded: [DATE]
- [ ] Data verified: [DATE]
- **Files obtained**:
- **Source URL**:

## HSC-Y3
- [ ] Registration submitted: [DATE]
- [ ] Registration approved: [DATE]
- [ ] Data downloaded: [DATE]
- [ ] Data verified: [DATE]
- **Files obtained**:
- **Source URL**:
```

---

## Next Steps After Data Access

1. Run `/root/private_multiresolution/scripts/download_des_y3.sh`
2. Run `/root/private_multiresolution/scripts/download_hsc_y3.sh`
3. Verify with `parse_des_y3_data.py` and `parse_hsc_y3_data.py`
4. Proceed with real cross-validation analysis

---

**Last Updated**: 2025-10-30
