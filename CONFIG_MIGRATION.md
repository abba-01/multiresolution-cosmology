# Configuration Migration Guide
## Single Source of Truth (SSOT) Refactoring

**Date:** 2025-10-30
**Status:** ✅ Phase 1-2 Complete, Phase 3 In Progress

---

## Overview

The multi-resolution cosmological analysis codebase has been refactored to implement **Single Source of Truth (SSOT)** principles. This migration eliminates ~150 hardcoded values scattered across 30+ files and consolidates them into centralized configuration modules.

---

## What Changed

### Before Refactoring

**Problems:**
- Cosmological constants (H₀, Ωm, S₈) duplicated in 15-20 files each
- Survey metadata (KiDS, DES, HSC) hardcoded in 12-14 files per survey
- Resolution schedules repeated in 13+ files
- Correction formulas duplicated in 10+ files
- Complete file duplication (`api_cryptographic_proof_system.py` × 2)
- Magic numbers without documentation
- Inconsistent values across files (maintenance nightmare)

**Example:**
```python
# OLD CODE - Hardcoded in 20+ files
PLANCK_H0 = 67.36  # Duplicated everywhere!
PLANCK_OMEGA_M = 0.315
```

### After Refactoring

**Solution:**
All constants, parameters, and metadata are now in centralized modules:

```python
# NEW CODE - Single source of truth
from config.constants import PLANCK_H0, PLANCK_OMEGA_M
from config.surveys import KIDS_1000, DES_Y3, HSC_Y3
from config.resolution import RESOLUTION_SCHEDULE_FULL
from utils.cosmology import calculate_angular_diameter_distance
```

---

## New Directory Structure

```
private_multiresolution/
├── config/                          # Configuration modules (SSOT)
│   ├── __init__.py
│   ├── constants.py                 # Physical/cosmological constants
│   ├── surveys.py                   # Survey metadata (KiDS, DES, HSC)
│   ├── resolution.py                # Resolution schedules & parameters
│   ├── corrections.py               # Correction formulas & calibration
│   └── api.py                       # API configuration & endpoints
│
├── utils/                           # Utility functions
│   ├── __init__.py
│   ├── cosmology.py                 # Cosmological calculations
│   ├── validation.py                # Input validation
│   └── corrections.py               # Correction calculations
│
├── .env.example                     # Environment variable template
├── config.yaml                      # Configuration file template
└── CONFIG_MIGRATION.md              # This file
```

---

## Module Reference

### 1. `config/constants.py`

**Purpose:** Physical and cosmological constants

**Exports:**
```python
# Physical constants
SPEED_OF_LIGHT_KM_S = 299792.458
HORIZON_SIZE_TODAY_MPC = 14000.0

# Planck 2018
PLANCK_H0 = 67.36  # km/s/Mpc
PLANCK_OMEGA_M = 0.315
PLANCK_OMEGA_LAMBDA = 0.685
PLANCK_S8 = 0.834
PLANCK_S8_SIGMA = 0.016

# SH0ES
SHOES_H0 = 73.04  # km/s/Mpc

# TRGB
TRGB_H0 = 69.8  # km/s/Mpc

# Convergence thresholds
DELTA_T_CONVERGENCE_THRESHOLD = 0.15
```

**Replaces:** ~40 hardcoded values in 18+ files

---

### 2. `config/surveys.py`

**Purpose:** Weak lensing survey metadata

**Exports:**
```python
# Survey objects
KIDS_1000   # SurveyMetadata with all KiDS properties
DES_Y3      # SurveyMetadata with all DES properties
HSC_Y3      # SurveyMetadata with all HSC properties

# Survey constants
KIDS_S8 = 0.759
KIDS_S8_SIGMA = 0.024
KIDS_Z_BINS = [(0.1, 0.3), (0.3, 0.5), ...]

DES_S8 = 0.776
DES_S8_SIGMA = 0.017
DES_Z_BINS = [(0.2, 0.43), (0.43, 0.63), ...]

HSC_S8 = 0.780
HSC_S8_SIGMA = 0.033
HSC_Z_BINS = [(0.3, 0.6), (0.6, 0.9), ...]

# Helper functions
get_survey(name: str) -> SurveyMetadata
get_survey_s8_values() -> Dict
```

**Replaces:** ~60 hardcoded values in 13+ files per survey

---

### 3. `config/resolution.py`

**Purpose:** UHA resolution schedules and parameters

**Exports:**
```python
# Resolution schedules
RESOLUTION_SCHEDULE_FULL = [8, 12, 16, 20, 24, 28, 32]
RESOLUTION_SCHEDULE_SHORT = [8, 12, 16, 20, 24]
RESOLUTION_SCHEDULE_CONSERVATIVE = [8, 12, 16, 20, 24, 28]

# Resolution info
MIN_RESOLUTION_BITS = 8
MAX_RESOLUTION_BITS = 32

# Helper functions
resolution_to_cell_size(bits: int) -> float
cell_size_to_resolution(size_mpc: float) -> int
get_resolution_schedule(mode: str) -> List[int]
```

**Replaces:** ~30 hardcoded schedule definitions in 13+ files

---

### 4. `config/corrections.py`

**Purpose:** Systematic correction formulas and parameters

**Exports:**
```python
# Universal correction pattern
UNIVERSAL_BASELINE = 0.0200
REDSHIFT_SCALING_EXPONENT = -0.5

# Formula: ΔS₈(z) = 0.0200 × (1+z)^(-0.5)
calculate_s8_correction(z: float) -> float
calculate_redshift_scaling_factor(z: float) -> float

# Resolution-specific corrections
CORRECTION_BY_RESOLUTION = {8: 0.0, 12: 0.009, ...}
H0_CORRECTION_BY_RESOLUTION = {8: 0.0, 12: -0.8, ...}
```

**Replaces:** ~15 hardcoded formula implementations in 10+ files

---

### 5. `config/api.py`

**Purpose:** API configuration and authentication

**Exports:**
```python
# API endpoints
API_BASE_URL = "https://got.gitgap.org"
TOKEN_ENDPOINT = f"{API_BASE_URL}/api/request-token"
UHA_ENCODE_ENDPOINT = f"{API_BASE_URL}/uha/encode"

# Rate limiting
API_KEY_REQUEST_INTERVAL_SECONDS = 60

# Timeouts
CONNECTION_TIMEOUT_SECONDS = 30

# User configuration (from environment)
UserConfig.from_env()
```

**Replaces:** Hardcoded API config in 2 files + duplicates

---

### 6. `utils/cosmology.py`

**Purpose:** Cosmological calculation functions

**Exports:**
```python
calculate_angular_diameter_distance(z, h0, omega_m) -> float
calculate_comoving_distance(z, h0, omega_m) -> float
angular_to_comoving_scale(theta_arcmin, z, h0, omega_m) -> float
radec_distance_to_cartesian(ra, dec, dist) -> Tuple[x, y, z]
redshift_to_scale_factor(z) -> float
```

**Replaces:** ~5 duplicate implementations in different files

---

### 7. `utils/validation.py`

**Purpose:** Input validation functions

**Exports:**
```python
validate_celestial_coordinates(ra, dec, dist) -> None
validate_resolution_bits(bits) -> None
validate_cosmology_dict(cosmo, require_flat=True) -> None
validate_array_size(arr, max_size, name) -> None
```

**Replaces:** Scattered validation logic across files

---

### 8. `utils/corrections.py`

**Purpose:** Correction calculation utilities

**Exports:**
```python
calculate_redshift_dependent_correction(z, baseline) -> float
apply_correction_to_bins(z_values, s8_initial) -> Dict
fit_baseline_from_bins(z_values, corrections) -> Dict
check_cross_survey_consistency(survey_results) -> Dict
calculate_tension_sigma(val1, sig1, val2, sig2) -> float
```

**Replaces:** Duplicate correction logic in 10+ files

---

## Migration Example

### Example 1: Survey Metadata

**Before:**
```python
# kids1000_real_analysis.py (OLD)
KIDS_S8 = 0.759  # ❌ Hardcoded
KIDS_S8_SIGMA = 0.024  # ❌ Hardcoded
KIDS_REFERENCE = "Asgari et al. 2021, A&A 645, A104"  # ❌ Hardcoded
```

**After:**
```python
# kids1000_real_analysis.py (NEW)
from config.surveys import KIDS_1000, KIDS_S8, KIDS_S8_SIGMA

# Access survey metadata
print(f"Survey: {KIDS_1000.name}")
print(f"S8: {KIDS_S8} ± {KIDS_S8_SIGMA}")
print(f"Reference: {KIDS_1000.reference}")
```

### Example 2: Redshift Scaling

**Before:**
```python
# compare_three_surveys.py (OLD)
z_factors = (1 + z_effs)**(-0.5)  # ❌ Hardcoded exponent
baselines = corrections / z_factors
```

**After:**
```python
# compare_three_surveys.py (NEW)
from config.corrections import calculate_redshift_scaling_factor, REDSHIFT_SCALING_EXPONENT

z_factors = calculate_redshift_scaling_factor(z_effs, REDSHIFT_SCALING_EXPONENT)
baselines = corrections / z_factors
```

### Example 3: Cosmological Calculations

**Before:**
```python
# des_y3_real_analysis.py (OLD)
c = 299792.458  # ❌ Hardcoded
D_H = c / h0
D_A_approx = D_H * z_eff / (1 + z_eff) * (1 + 0.5 * omega_m * z_eff)  # ❌ Duplicate logic
```

**After:**
```python
# des_y3_real_analysis.py (NEW)
from utils.cosmology import calculate_angular_diameter_distance

D_A = calculate_angular_diameter_distance(z_eff, h0, omega_m)  # ✅ Centralized
```

---

## Files Refactored

### ✅ Completed
1. `config/constants.py` - NEW (centralized constants)
2. `config/surveys.py` - NEW (centralized survey metadata)
3. `config/resolution.py` - NEW (centralized resolution config)
4. `config/corrections.py` - NEW (centralized corrections)
5. `config/api.py` - NEW (centralized API config)
6. `utils/cosmology.py` - NEW (cosmological calculations)
7. `utils/validation.py` - NEW (validation functions)
8. `utils/corrections.py` - NEW (correction utilities)
9. `compare_three_surveys.py` - REFACTORED (uses centralized config)

### 🔄 In Progress
- `api_cryptographic_proof_system.py`
- Survey analysis files (kids, des, hsc)
- Validation files (s8, trgb, test)

### ⏳ Pending (~20 files)
- All other .py files that use hardcoded values

---

## Environment Configuration

### `.env` File Setup

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your information:
   ```bash
   # Required
   UHA_EMAIL=your.email@university.edu

   # Optional
   UHA_USER_NAME=Your Name
   UHA_INSTITUTION=Your University
   UHA_OFFLINE_MODE=True
   ```

3. **IMPORTANT:** Never commit `.env` to version control!
   ```bash
   # .gitignore
   .env
   ```

---

## Testing the Migration

### Import Test

```python
# test_config_import.py
from config.constants import PLANCK_H0, PLANCK_S8
from config.surveys import KIDS_1000, DES_Y3, HSC_Y3
from config.resolution import RESOLUTION_SCHEDULE_FULL
from utils.cosmology import calculate_angular_diameter_distance

print(f"Planck H0: {PLANCK_H0}")
print(f"KiDS S8: {KIDS_1000.S8_measured}")
print(f"Resolution schedule: {RESOLUTION_SCHEDULE_FULL}")

# Test calculation
d_a = calculate_angular_diameter_distance(0.5, PLANCK_H0, 0.315)
print(f"D_A(z=0.5): {d_a:.2f} Mpc")
```

Expected output:
```
Planck H0: 67.36
KiDS S8: 0.759
Resolution schedule: [8, 12, 16, 20, 24, 28, 32]
D_A(z=0.5): ...  Mpc
```

---

## Benefits

### ✅ Maintenance
- **Single point of modification** for any constant
- **No risk of inconsistent values** across files
- **Easy updates** when new data released

### ✅ Documentation
- All constants **documented in one place**
- Clear **references and citations**
- **Type hints** for better IDE support

### ✅ Testing
- **Centralized validation** catches errors early
- **Easy to mock** for unit tests
- **Reproducible results** guaranteed

### ✅ Security
- **Credentials in environment** variables, not code
- **No secrets in version control**
- **Configurable timeouts and limits**

---

## Breaking Changes

### For Existing Code

If you have code that directly uses hardcoded values, it will need updating:

```python
# OLD CODE - Will still work but not using SSOT
PLANCK_H0 = 67.36  # Local definition

# NEW CODE - Use centralized constant
from config.constants import PLANCK_H0
```

### For API Users

API configuration now requires environment variables:

```bash
# Before: Hardcoded in code
# After: Set in .env file
UHA_EMAIL=your.email@university.edu
```

---

## Rollback Plan

If issues arise, the refactoring can be rolled back:

1. **Git rollback:**
   ```bash
   git revert HEAD~10  # Revert last 10 commits
   ```

2. **Selective rollback:**
   - Keep config modules (they don't break anything)
   - Revert individual file changes if needed

3. **Compatibility:**
   - Old code can coexist with new config modules
   - Gradual migration supported

---

## Future Work

### Phase 3: Remaining File Refactoring (~20 files)
- `api_cryptographic_proof_system.py`
- Survey-specific analysis files
- Test and validation files

### Phase 4: Additional Improvements
- Add comprehensive unit tests for config modules
- Create integration tests
- Add CI/CD validation
- Generate API documentation

---

## Support

### Questions?
- Review code comments in config modules
- Check examples in this document
- Open GitHub issue for problems

### Contributing
When adding new constants:
1. Add to appropriate config module
2. Document with comments
3. Add validation if needed
4. Update this migration guide

---

**Status:** ✅ Phases 1-2 Complete
**Next:** Continue Phase 3 file refactoring
**Timeline:** ~10 days total estimated
