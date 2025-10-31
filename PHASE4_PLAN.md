# Phase 4 Execution Plan - Remaining Files

**Phase:** 4 of 7
**Target:** 13 remaining files
**Estimated Time:** 4-6 hours
**Priority:** HIGH

---

## Overview

Phase 4 completes the SSOT refactoring by addressing:
1. Data loaders and simulation files
2. Remaining analysis and comparison files
3. Core algorithm files (multiresolution_uha_encoder.py)
4. Missing REFACTORED notices from Phase 2

---

## Group 1: Data Loaders & Simulation (3 files)

### 1. kids1000_data_loader.py
**Estimated time:** 30-45 min
**Expected constants:**
- Survey metadata (area, redshift bins)
- S8 values
- File paths

**Pattern:**
```python
from config.surveys import KIDS_1000  # Full survey config
from config.constants import KIDS_S8
```

### 2. create_simulated_des_data.py
**Estimated time:** 30-45 min
**Expected constants:**
- DES S8 values
- Cosmological parameters
- Redshift bin definitions

### 3. create_simulated_hsc_data.py
**Estimated time:** 30-45 min
**Expected constants:**
- HSC S8 values
- Cosmological parameters
- Redshift bin definitions

**Batch strategy:** All 3 similar, refactor consecutively

---

## Group 2: Analysis Files (5 files)

### 4. compare_kids_des_cross_validation.py
**Estimated time:** 45-60 min
**Expected constants:**
- Survey S8 values (KIDS, DES)
- Planck comparison values
- Correction formulas

**Similar to:** compare_three_surveys.py (already refactored)

### 5. multiresolution_endpoint.py
**Estimated time:** 30-45 min
**Expected constants:**
- API configuration (already in config.api)
- Resolution schedules
- Default parameters

**Note:** Likely minimal changes (API config already centralized)

### 6. multiresolution_uha_encoder.py ⚠️ CRITICAL
**Estimated time:** 1-2 hours
**Complexity:** HIGH
**Expected constants:**
- Physical constants (c, R_H)
- Resolution bit schedules
- Convergence thresholds
- Mathematical constants

**Key considerations:**
- Core algorithm file - most critical
- Must preserve exact numerical behavior
- Comprehensive testing required
- May have many hardcoded parameters

**Testing:**
- Verify output unchanged
- Check all resolution schedules
- Validate epistemic distance calculations

### 7. test_implementation.py
**Estimated time:** 30-45 min
**Expected constants:**
- Test expectations (keep as local)
- Physical constants for calculations
- Validation thresholds

**Similar to:** verify_analysis.py (Phase 3)

### 8. trgb_anchor_spec_corrected.py
**Estimated time:** 30-45 min
**Expected constants:**
- TRGB H0 values
- Anchor specifications
- Distance scale parameters

**Similar to:** trgb_validation.py (Phase 3)

---

## Group 3: Add Missing REFACTORED Notices (2 files)

### 9. des_y3_real_analysis.py
**Estimated time:** 5 min
**Action:** Add REFACTORED notice to docstring

**Current status:** Refactored in Phase 2, missing docstring update

### 10. hsc_y3_real_analysis.py
**Estimated time:** 5 min
**Action:** Add REFACTORED notice to docstring

**Current status:** Refactored in Phase 2, missing docstring update

**Note:** Quick fix, bundle into single commit

---

## Execution Strategy

### Session 1: Data Loaders (1-1.5 hours)
1. Scan all 3 files for constants
2. Refactor kids1000_data_loader.py
3. Refactor create_simulated_des_data.py
4. Refactor create_simulated_hsc_data.py
5. Test all 3 compilations
6. Commit: "Refactor data loaders and simulation files (Phase 4, files 4-6)"

### Session 2: Analysis Files Part 1 (1-1.5 hours)
1. compare_kids_des_cross_validation.py
2. test_implementation.py
3. trgb_anchor_spec_corrected.py
4. Test compilation
5. Commit: "Refactor analysis comparison and test files (Phase 4, files 7-9)"

### Session 3: Core Algorithm (1-2 hours) ⚠️ CRITICAL
1. **Backup:** Save any existing encoder results
2. Read multiresolution_uha_encoder.py thoroughly
3. Identify all hardcoded constants
4. Refactor carefully (preserve exact behavior)
5. **Test extensively:**
   - Compilation
   - Run test cases
   - Verify numerical outputs unchanged
6. Commit: "Refactor core UHA encoder algorithm (Phase 4, file 10) ⚠️ CRITICAL"

### Session 4: Endpoint & Cleanup (30 min)
1. multiresolution_endpoint.py (likely minimal)
2. Add REFACTORED notices to Phase 2 files
3. Commit: "Refactor endpoint and add missing REFACTORED notices (Phase 4, files 11-13)"

### Session 5: Documentation (30 min)
1. Create PHASE4_COMPLETE.md
2. Update progress metrics
3. Git tag: phase4-complete
4. Final commit

---

## Critical File: multiresolution_uha_encoder.py

### Pre-Refactoring Checklist
- [ ] Read entire file
- [ ] Understand all algorithms
- [ ] Identify all hardcoded constants
- [ ] Map each constant to config source
- [ ] Create backup of any test outputs
- [ ] Plan testing strategy

### Expected Constants
- `c = 299792.458` or `3e5` → `SPEED_OF_LIGHT_KM_S`
- `R_H = 14000.0` → `HORIZON_SIZE_TODAY_MPC`
- Resolution schedules (may need config.resolution)
- Convergence thresholds
- Iteration limits

### Testing Strategy
1. **Before refactoring:** Run encoder and save outputs
2. **After refactoring:** Run encoder with same inputs
3. **Verify:** Outputs match to numerical precision
4. **If different:** Investigate (may be acceptable if improved)

---

## Common Patterns

### Pattern 1: Survey Metadata
```python
# OLD
survey_area = 1000.0  # deg^2
S8 = 0.759

# NEW
from config.surveys import KIDS_1000
survey_area = KIDS_1000['coverage_deg2']
S8 = KIDS_1000['S8_measured']
```

### Pattern 2: Physical Constants
```python
# OLD
c = 299792.458  # km/s
R_H = 14000.0  # Mpc

# NEW
from config.constants import SPEED_OF_LIGHT_KM_S, HORIZON_SIZE_TODAY_MPC
c = SPEED_OF_LIGHT_KM_S
R_H = HORIZON_SIZE_TODAY_MPC
```

### Pattern 3: Algorithm Parameters
```python
# OLD
MAX_ITERATIONS = 100
CONVERGENCE_THRESHOLD = 0.001

# NEW - Decision point:
# If used across files → centralize to config.constants
# If file-specific → keep as local constant
MAX_ITERATIONS = 100  # Algorithm-specific parameter
```

---

## Risk Management

| Risk | Mitigation |
|------|------------|
| Core algorithm behavior changes | Backup outputs, extensive testing |
| Constants are actually tunable parameters | Document decision, keep as local if file-specific |
| Breaking existing workflows | Test compilation + run tests before committing |
| Missing dependencies | Check imports resolve before committing |

---

## Verification Checklist (Per File)

- [ ] Backup any existing result files
- [ ] Identify all hardcoded constants
- [ ] Map constants to config modules
- [ ] Refactor imports and constants
- [ ] Test compilation: `python3 -m py_compile <file>`
- [ ] Check imports resolve
- [ ] Run file if quick/possible
- [ ] Verify outputs unchanged (if applicable)
- [ ] Add REFACTORED notice to docstring
- [ ] Commit

---

## Success Criteria

### Per-File Success
- ✅ File compiles without errors
- ✅ Imports resolve correctly
- ✅ Hardcoded cosmological constants eliminated
- ✅ Algorithm behavior unchanged (where applicable)
- ✅ Docstring updated

### Phase Success
- ✅ All remaining files refactored (13 files)
- ✅ All files compile
- ✅ Core algorithm (multiresolution_uha_encoder.py) verified
- ✅ Comprehensive documentation (PHASE4_COMPLETE.md)
- ✅ Git tag created (phase4-complete)
- ✅ No breaking changes
- ✅ 100% of Python files refactored

---

## After Phase 4

**Progress:** 30/30 files complete (100%) 🎉
**Achievement:** Complete SSOT refactoring across entire codebase
**Remaining:** Documentation updates, final testing, publication prep

---

## Estimated Timeline

### Optimistic (3-4 hours)
- Hour 1: Data loaders + simulation (3 files)
- Hour 2: Analysis files (3 files)
- Hour 3: Core algorithm + endpoint (2 files)
- Hour 4: Cleanup + documentation

### Realistic (4-6 hours)
- Session 1 (1.5h): Data loaders
- Session 2 (1.5h): Analysis files
- Session 3 (2h): Core algorithm (careful testing)
- Session 4 (1h): Endpoint + cleanup + docs

### Pessimistic (1 day)
- Extra time for core algorithm testing
- Discovering complex dependencies
- Need for additional config modules

---

## Ready to Execute

**Status:** ✅ PLAN COMPLETE
**Next action:** Execute Group 1 (Data loaders & simulation files)

---

**Created:** 2025-10-30
**Author:** Claude Code + Eric D. Martin
**Version:** 1.0
