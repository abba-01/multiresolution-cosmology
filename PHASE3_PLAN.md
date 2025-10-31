# Phase 3 Execution Plan - Validation Files

**Phase:** 3 of 7
**Target:** 9 validation/test files
**Estimated LOC:** ~2,500 lines
**Estimated Effort:** 2 days (4-6 hours active work)
**Priority:** MEDIUM

---

## Overview

Phase 3 focuses on validation, testing, and verification files. These ensure scientific correctness but are less critical than core analysis files (Phase 2).

**Strategy:** Group similar files and refactor in batches

---

## Files to Refactor (9 total)

### Group 1: TRGB Files (2 files, ~850 LOC)

#### 1. trgb_validation.py
**LOC:** ~400
**Priority:** MEDIUM
**Estimated time:** 1-1.5 hours

**Expected hardcoded values:**
- TRGB_H0 = 69.8 → config.constants.TRGB_H0
- Planck H0/cosmology → config.constants
- Distance calculations → utils.cosmology
- Validation thresholds → document or config

**Pattern:**
```python
from config.constants import TRGB_H0, PLANCK_H0, PLANCK_OMEGA_M
```

#### 2. trgb_real_data_analysis.py
**LOC:** ~450
**Priority:** MEDIUM
**Estimated time:** 1-1.5 hours

**Expected hardcoded values:**
- Similar to trgb_validation.py
- TRGB anchor calibration values
- Systematic corrections

**Batch refactoring:** Can be done together with trgb_validation.py

---

### Group 2: Test/Validation Files (4 files, ~1,200 LOC)

#### 3. test_physical_validation.py
**LOC:** ~400
**Priority:** LOW
**Estimated time:** 45-60 min

**Expected hardcoded values:**
- Physical constraints (c, R_H, H0 range)
- Test thresholds
- Validation criteria

**Pattern:**
```python
from config.constants import SPEED_OF_LIGHT_KM_S, HORIZON_SIZE_TODAY_MPC
```

#### 4. real_data_validation.py
**LOC:** ~350
**Priority:** MEDIUM
**Estimated time:** 45-60 min

**Expected hardcoded values:**
- Survey S8 values for validation
- Cosmological parameters
- Acceptance criteria

#### 5. validate_consistency_test.py
**LOC:** ~250
**Priority:** LOW
**Estimated time:** 30-45 min

**Expected hardcoded values:**
- Consistency thresholds
- Survey metadata
- Pattern matching criteria

#### 6. verify_analysis.py
**LOC:** ~200
**Priority:** LOW
**Estimated time:** 30-45 min

**Expected hardcoded values:**
- Verification thresholds
- Expected values for comparison
- Tolerance levels

**Batch strategy:** All 4 files similar pattern, can refactor consecutively

---

### Group 3: Analysis/Comparison Files (3 files, ~750 LOC)

#### 7. simulated_cross_survey_validation.py
**LOC:** ~300
**Priority:** MEDIUM
**Estimated time:** 45-60 min

**Expected hardcoded values:**
- Survey S8 values
- Redshift bins
- Correction formulas
- Simulation parameters

**Note:** Similar to compare_three_surveys.py (already refactored)

#### 8. joint_lambda_cdm_fit.py
**LOC:** ~250
**Priority:** MEDIUM
**Estimated time:** 45-60 min

**Expected hardcoded values:**
- ΛCDM parameters (Ωm, ΩΛ, H0)
- Survey data
- Fitting constraints

**Pattern:**
```python
from config.constants import PLANCK_OMEGA_M, PLANCK_OMEGA_LAMBDA, PLANCK_H0
```

#### 9. check_published_values.py
**LOC:** ~200
**Priority:** LOW
**Estimated time:** 30-45 min

**Expected hardcoded values:**
- Published survey values → config.surveys
- Literature references → document in config
- Comparison tolerances

---

## Execution Strategy

### Day 1: Groups 1 & 2 (6 files, ~2,050 LOC)

**Morning (3 hours):**
1. ✅ TRGB files (trgb_validation.py, trgb_real_data_analysis.py)
   - Backup existing results
   - Refactor both files
   - Test compilation
   - Commit: "Refactor TRGB validation files to use SSOT (Phase 3, files 1-2/9)"

**Afternoon (3 hours):**
2. ✅ Test/validation files (4 files)
   - test_physical_validation.py
   - real_data_validation.py
   - validate_consistency_test.py
   - verify_analysis.py
   - Batch refactor (similar pattern)
   - Test all 4
   - Commit: "Refactor validation/test files to use SSOT (Phase 3, files 3-6/9)"

### Day 2: Group 3 (3 files, ~750 LOC)

**Morning (2-3 hours):**
3. ✅ Analysis/comparison files
   - simulated_cross_survey_validation.py
   - joint_lambda_cdm_fit.py
   - check_published_values.py
   - Refactor all 3
   - Test compilation
   - Commit: "Refactor analysis comparison files to use SSOT (Phase 3, files 7-9/9)"

**Afternoon (1-2 hours):**
4. ✅ Phase 3 completion
   - Create PHASE3_COMPLETE.md
   - Verify all outputs
   - Git tag: phase3-complete
   - Final commit: "Complete Phase 3 - All validation files refactored"

---

## Common Patterns

### Pattern 1: Cosmological Constants

```python
# OLD
PLANCK_H0 = 67.36
PLANCK_OMEGA_M = 0.315
TRGB_H0 = 69.8

# NEW
from config.constants import PLANCK_H0, PLANCK_OMEGA_M, TRGB_H0
```

### Pattern 2: Survey Values

```python
# OLD
KIDS_S8 = 0.759
DES_S8 = 0.776

# NEW
from config.surveys import KIDS_S8, DES_S8
```

### Pattern 3: Physical Constants

```python
# OLD
c = 299792.458  # km/s
R_H = 14000.0  # Mpc

# NEW
from config.constants import SPEED_OF_LIGHT_KM_S, HORIZON_SIZE_TODAY_MPC
c = SPEED_OF_LIGHT_KM_S
R_H = HORIZON_SIZE_TODAY_MPC
```

### Pattern 4: Test Thresholds

```python
# OLD
TOLERANCE = 0.001  # Hardcoded

# NEW
# Option A: Keep as local constant (if test-specific)
TOLERANCE = 0.001  # Test-specific threshold

# Option B: Move to config if used elsewhere
from config.validation import NUMERICAL_TOLERANCE
```

**Decision:** Keep test-specific thresholds as local constants (not worth centralizing)

---

## Verification Checklist (Per File)

Before committing each file:

- [ ] Backup existing output/results if they exist
- [ ] Identify all hardcoded cosmological constants
- [ ] Replace with imports from config modules
- [ ] Test compilation: `python3 -m py_compile <file>`
- [ ] Run file (if quick) and verify output format
- [ ] Check diff to ensure only constants changed
- [ ] Update docstring with "REFACTORED" notice
- [ ] Verify imports are organized and clear

---

## Expected Challenges

### Challenge 1: Test-Specific Values

**Issue:** Tests often have hardcoded expected values
**Solution:** Keep test expectations as local constants (they're testing specific scenarios)

**Example:**
```python
# KEEP THIS - test expectation
EXPECTED_S8 = 0.834  # Expected result for this test case

# REFACTOR THIS - input parameter
from config.constants import PLANCK_S8
assert calculate_s8() == EXPECTED_S8  # Test against expectation
```

### Challenge 2: Validation Thresholds

**Issue:** Many validation thresholds (tolerances, σ limits)
**Solution:** Document but don't necessarily centralize (unless used across multiple files)

### Challenge 3: Literature Values

**Issue:** Published values from papers
**Solution:** Move to config.surveys if survey-related, otherwise document in comments

---

## Success Criteria

### Per-File Success

- ✅ File compiles without errors
- ✅ Imports resolve correctly
- ✅ No hardcoded Planck/survey values remaining
- ✅ Test logic unchanged
- ✅ Docstring updated

### Phase Success

- ✅ All 9 files refactored
- ✅ All files compile
- ✅ Consistent import patterns
- ✅ Comprehensive documentation (PHASE3_COMPLETE.md)
- ✅ Git tag created (phase3-complete)
- ✅ No breaking changes

---

## Risk Management

| Risk | Mitigation |
|------|------------|
| Tests fail after refactoring | Keep test expectations as local constants |
| Validation logic breaks | Only change parameter sources, not logic |
| Performance impact | Config loaded once, negligible impact |
| Difficult to verify outputs | Compare before/after if files are quick to run |

---

## Estimated Timeline

### Optimistic (1 day)

- Hour 1-2: TRGB files
- Hour 3-4: Test/validation files
- Hour 5-6: Analysis files
- Hour 7-8: Documentation & verification

**Total:** 8 hours continuous work

### Realistic (2 days)

- Day 1 (4-5 hours): TRGB + Test/validation files (6 files)
- Day 2 (2-3 hours): Analysis files + documentation (3 files + docs)

**Total:** 6-8 hours spread over 2 days

### Pessimistic (3 days)

- Add 1 day buffer for unexpected issues
- More thorough testing
- Complex validation logic

**Total:** 3 days maximum

---

## Dependencies

### Files Needed (Already Complete)

- ✅ config/constants.py - All constants available
- ✅ config/surveys.py - Survey metadata ready
- ✅ config/corrections.py - Formulas available
- ✅ utils/cosmology.py - Calculation functions ready
- ✅ utils/validation.py - Validation functions ready
- ✅ utils/corrections.py - Correction utilities ready

**No blockers:** All dependencies from Phase 1 are complete

---

## After Phase 3

**Progress:** 16/30 files complete (53%)
**Remaining phases:** 4, 5, 6, 7
**Estimated remaining time:** 4-6 days

**Next:** Phase 4 - Parser files (easier, similar patterns)

---

## Commit Messages Template

### Group 1 (TRGB files):
```
Refactor TRGB validation files to use SSOT (Phase 3, files 1-2/9)

FILES:
- trgb_validation.py
- trgb_real_data_analysis.py

CHANGES:
- TRGB_H0 → config.constants.TRGB_H0
- Planck values → config.constants
- [Other specifics]

VERIFICATION:
- Both files compile ✅
- Imports resolve ✅
```

### Group 2 (Test files):
```
Refactor validation/test files to use SSOT (Phase 3, files 3-6/9)

FILES:
- test_physical_validation.py
- real_data_validation.py
- validate_consistency_test.py
- verify_analysis.py

CHANGES:
- Physical constants → config.constants
- Survey values → config.surveys
- Test expectations preserved as local constants

VERIFICATION:
- All 4 files compile ✅
- Test logic unchanged ✅
```

### Group 3 (Analysis files):
```
Refactor analysis comparison files to use SSOT (Phase 3, files 7-9/9)

✅ PHASE 3 COMPLETE

FILES:
- simulated_cross_survey_validation.py
- joint_lambda_cdm_fit.py
- check_published_values.py

CHANGES:
- Survey metadata → config.surveys
- ΛCDM parameters → config.constants
- Cross-validation consistent with core analysis

VERIFICATION:
- All files compile ✅
- Consistent with Phase 2 patterns ✅

PHASE 3 SUMMARY:
- 9 files refactored (~2,500 LOC)
- All validation files now use SSOT
- Cumulative: 16/30 files (53%)
```

---

## Notes

### Keep as Local Constants

Don't centralize these:
- Test-specific expected values
- File-specific tolerances
- Debug/development parameters
- One-off calculations

### Definitely Centralize

Always use config for:
- Planck 2018 parameters
- Survey S8 values
- Physical constants (c, R_H)
- Published H0 values (SHOES, TRGB)

---

## Ready to Execute

**Status:** ✅ PLAN COMPLETE
**Next action:** Begin Phase 3 execution with Group 1 (TRGB files)
**Command:** Continue with "execute phase 3"

---

**Created:** 2025-10-30
**Author:** Claude Code + Eric D. Martin
**Version:** 1.0
