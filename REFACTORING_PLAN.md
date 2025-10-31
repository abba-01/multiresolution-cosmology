# SSOT Refactoring Plan - Phases 2-7

**Project:** Multi-Resolution Cosmological Analysis Codebase
**Goal:** Eliminate all hardcoded constants, implement Single Source of Truth
**Started:** 2025-10-30
**Current Phase:** 2 (of 7)

---

## Overview

### Progress Summary

| Phase | Status | Files | LOC | Effort | Completion |
|-------|--------|-------|-----|--------|------------|
| **Phase 1** | ✅ COMPLETE | 17 | 4,200 | 2.5 days | 100% |
| **Phase 2** | 🔄 NEXT | 6 | 3,000 | 2 days | 0% |
| **Phase 3** | ⏳ Pending | 9 | 2,500 | 2 days | 0% |
| **Phase 4** | ⏳ Pending | 5 | 1,500 | 1 day | 0% |
| **Phase 5** | ⏳ Pending | 3 | 1,000 | 1 day | 0% |
| **Phase 6** | ⏳ Pending | 5 | 2,000 | 1 day | 0% |
| **Phase 7** | ⏳ Pending | - | - | 2 days | 0% |
| **TOTAL** | 25% | 45 | 14,200 | 10-12 days | 25% |

---

## Phase 1: Foundation ✅ COMPLETE

**Completed:** 2025-10-30

### Deliverables

- [x] config/constants.py (194 LOC)
- [x] config/surveys.py (290 LOC)
- [x] config/resolution.py (280 LOC)
- [x] config/corrections.py (240 LOC)
- [x] config/api.py (260 LOC)
- [x] utils/cosmology.py (330 LOC)
- [x] utils/validation.py (450 LOC)
- [x] utils/corrections.py (370 LOC)
- [x] compare_three_surveys.py (refactored)
- [x] SSOT_SUMMARY.md
- [x] CONFIG_MIGRATION.md
- [x] .env.example
- [x] config.yaml
- [x] Deleted duplicate: joomla/.../api_cryptographic_proof_system.py

### Results

- All modules tested and working
- First production file refactored successfully
- Zero breaking changes
- Test improvements (1 additional test passing)

---

## Phase 2: Core Analysis Files 🔄 NEXT

**Target:** 6 files, ~3,000 LOC
**Estimated effort:** 2 days
**Priority:** HIGH

### Files to Refactor

#### 1. api_cryptographic_proof_system.py ⭐ HIGHEST PRIORITY

**LOC:** 645
**Complexity:** HIGH
**Dependencies:** Many hardcoded values

**Hardcoded values to replace:**
- API endpoints (→ config.api)
- Cosmological constants (→ config.constants)
- Survey metadata (→ config.surveys)
- Resolution schedules (→ config.resolution)
- Correction formulas (→ config.corrections)

**Key functions needing refactoring:**
- `request_api_key()` - Use config.api.UserConfig
- `encode_with_uha_api()` - Use config.api endpoints
- Survey data loading - Use config.surveys
- Correction calculations - Use utils.corrections

**Testing requirements:**
- ⚠️ CRITICAL: Cryptographic proofs must remain identical
- Verify SHA3-512 hashes unchanged
- Test with all three surveys
- Validate API interactions

**Estimated time:** 4-6 hours

---

#### 2. kids1000_real_analysis.py

**LOC:** ~350
**Complexity:** MEDIUM
**Dependencies:** Survey metadata, corrections

**Hardcoded values to replace:**
```python
# Current hardcoded values
KIDS_S8 = 0.759  # → config.surveys.KIDS_S8
KIDS_S8_SIGMA = 0.024  # → config.surveys.KIDS_S8_SIGMA
PLANCK_H0 = 67.36  # → config.constants.PLANCK_H0
# ... etc
```

**Refactoring steps:**
1. Add imports from config.constants, config.surveys
2. Replace hardcoded cosmological constants
3. Use KIDS_1000 metadata object
4. Replace manual correction calculations with utils.corrections
5. Test against existing output (kids1000_real_analysis_results.json)

**Estimated time:** 2-3 hours

---

#### 3. des_y3_real_analysis.py

**LOC:** ~350
**Complexity:** MEDIUM
**Dependencies:** Survey metadata, corrections

**Similar to kids1000_real_analysis.py:**
- Replace DES-specific hardcoded values with config.surveys.DES_Y3
- Use centralized correction functions
- Verify against des_y3_real_analysis_results.json

**Estimated time:** 2-3 hours

---

#### 4. hsc_y3_real_analysis.py

**LOC:** ~350
**Complexity:** MEDIUM
**Dependencies:** Survey metadata, corrections

**Similar to kids1000_real_analysis.py:**
- Replace HSC-specific hardcoded values with config.surveys.HSC_Y3
- Use centralized correction functions
- Verify against hsc_y3_real_analysis_results.json

**Estimated time:** 2-3 hours

---

#### 5. s8_tension_resolution.py

**LOC:** ~450
**Complexity:** HIGH
**Dependencies:** Constants, surveys, corrections

**Hardcoded values to replace:**
- Planck S₈ values (→ config.constants)
- Survey S₈ values (→ config.surveys)
- Tension calculation formulas (→ utils.corrections.calculate_tension_sigma)
- Correction patterns (→ config.corrections)

**Key functions:**
- Tension calculations → use utils.corrections
- Multi-survey comparisons → use config.surveys
- Resolution sweeps → use config.resolution

**Testing:**
- Verify s8_tension_results.json unchanged
- Check tension values match expected

**Estimated time:** 3-4 hours

---

#### 6. s8_multiresolution_refinement.py

**LOC:** ~500
**Complexity:** HIGH
**Dependencies:** Constants, surveys, resolution, corrections

**Similar to s8_tension_resolution.py plus:**
- Resolution schedule iteration (→ config.resolution)
- Multi-resolution convergence checks
- Baseline fitting across resolutions

**Testing:**
- Verify s8_multiresolution_results.json unchanged
- Check convergence metrics

**Estimated time:** 3-4 hours

---

### Phase 2 Checklist

**Pre-refactoring:**
- [ ] Read and understand each file's logic
- [ ] Identify all hardcoded constants
- [ ] Map constants to config modules
- [ ] Identify duplicate calculations

**During refactoring:**
- [ ] Add appropriate imports
- [ ] Replace constants one at a time
- [ ] Replace duplicate functions with utils calls
- [ ] Update docstrings and comments
- [ ] Test after each major change

**Post-refactoring:**
- [ ] Run refactored file and capture output
- [ ] Compare with original output JSON files
- [ ] Verify all tests still pass
- [ ] Check for any new dependencies
- [ ] Update documentation

**Commit strategy:**
- Option A: Commit after each file (6 commits)
- Option B: Commit logical groups (2-3 commits)
- Option C: Single commit for entire phase (1 commit)

**Recommended:** Option B (commit related files together)

---

## Phase 3: Validation Files

**Target:** 9 files, ~2,500 LOC
**Estimated effort:** 2 days
**Priority:** MEDIUM

### Files to Refactor

1. **trgb_validation.py** (~400 LOC)
   - TRGB-specific constants
   - Validation logic
   - Distance calculations

2. **trgb_real_data_analysis.py** (~450 LOC)
   - TRGB anchor calibration
   - H₀ calculations
   - Systematic corrections

3. **test_physical_validation.py** (~400 LOC)
   - Physical constraints
   - Validation functions
   - Test assertions

4. **real_data_validation.py** (~350 LOC)
   - Real data loading
   - Validation pipeline
   - Result verification

5. **validate_consistency_test.py** (~250 LOC)
   - Cross-survey consistency
   - Pattern matching
   - Statistical tests

6. **verify_analysis.py** (~200 LOC)
   - Analysis verification
   - Result checking
   - Reproducibility tests

7. **simulated_cross_survey_validation.py** (~300 LOC)
   - Simulated data generation
   - Cross-validation
   - Pattern verification

8. **joint_lambda_cdm_fit.py** (~250 LOC)
   - ΛCDM model fitting
   - Parameter constraints
   - Joint analysis

9. **check_published_values.py** (~200 LOC)
   - Published value comparison
   - Consistency checks
   - Literature references

### Common Patterns

All these files likely need:
- config.constants (Planck, SH0ES, TRGB)
- config.surveys (survey metadata)
- utils.validation (validation functions)
- utils.corrections (correction calculations)

### Phase 3 Strategy

**Group 1: TRGB files** (trgb_validation.py, trgb_real_data_analysis.py)
- Refactor together (similar structure)
- Focus on TRGB_H0 constant
- Estimated: 4-5 hours

**Group 2: Test/validation files** (test_physical_validation.py, real_data_validation.py, validate_consistency_test.py, verify_analysis.py)
- Refactor together (validation focus)
- Estimated: 4-5 hours

**Group 3: Analysis files** (simulated_cross_survey_validation.py, joint_lambda_cdm_fit.py, check_published_values.py)
- Refactor together (analysis focus)
- Estimated: 3-4 hours

---

## Phase 4: Parser Files

**Target:** 5 files, ~1,500 LOC
**Estimated effort:** 1 day
**Priority:** MEDIUM

### Files to Refactor

1. **parse_kids_real_data.py** (~300 LOC)
2. **parse_des_y3_data.py** (~400 LOC)
3. **parse_hsc_y3_data.py** (~400 LOC)
4. **kids1000_data_loader.py** (~250 LOC)
5. **create_simulated_des_data.py** (~150 LOC)

### Common Patterns

- Data file paths
- Survey metadata
- Redshift bin definitions
- Column mappings

### Strategy

Parsers are straightforward:
- Replace hardcoded paths with config
- Use survey metadata objects
- Verify parsed output unchanged

Estimated: 6-8 hours total

---

## Phase 5: Cross-Validation Files

**Target:** 3 files, ~1,000 LOC
**Estimated effort:** 1 day
**Priority:** MEDIUM

### Files to Refactor

1. **compare_kids_des_cross_validation.py** (~300 LOC)
   - Already have compare_three_surveys.py as template
   - Similar structure

2. **multiresolution_endpoint.py** (~350 LOC)
   - API endpoint configuration
   - Resolution handling
   - Request/response logic

3. **multiresolution_uha_encoder.py** (~350 LOC)
   - UHA encoding parameters
   - Resolution mapping
   - Coordinate handling

### Strategy

- Use compare_three_surveys.py as reference
- Most patterns already solved in Phase 1

Estimated: 6-8 hours total

---

## Phase 6: Test Files

**Target:** 5 files, ~2,000 LOC
**Estimated effort:** 1 day
**Priority:** LOW

### Files to Refactor

1. **test_implementation.py** (~850 LOC)
   - Large test battery
   - Many hardcoded test values
   - Systematic testing

2. **Remaining test files** (~1,150 LOC)
   - Various test scripts
   - Validation tests
   - Integration tests

### Strategy

Tests are lower priority:
- Can refactor after main code
- May keep some hardcoded values for test clarity
- Focus on test data consistency

Estimated: 6-8 hours total

---

## Phase 7: Testing & Documentation

**Target:** Comprehensive testing and docs
**Estimated effort:** 2 days
**Priority:** HIGH (for completion)

### Tasks

#### Unit Tests (Day 1)

1. **Config module tests**
   - [ ] Test all constants load correctly
   - [ ] Test survey metadata completeness
   - [ ] Test resolution mappings
   - [ ] Test correction formulas
   - [ ] Test API configuration

2. **Utils module tests**
   - [ ] Test cosmology calculations
   - [ ] Test validation functions
   - [ ] Test correction utilities
   - [ ] Test edge cases
   - [ ] Test error handling

#### Integration Tests (Day 1)

3. **Cross-module tests**
   - [ ] Test imports from multiple files
   - [ ] Test circular dependency absence
   - [ ] Test configuration overrides
   - [ ] Test environment variable handling

4. **Regression tests**
   - [ ] Compare all output JSON files
   - [ ] Verify scientific results unchanged
   - [ ] Check cryptographic hashes
   - [ ] Validate test pass rates

#### Documentation (Day 2)

5. **API documentation**
   - [ ] Generate module documentation
   - [ ] Document all public functions
   - [ ] Create usage examples
   - [ ] Add docstring completeness check

6. **User documentation**
   - [ ] Update main README.md
   - [ ] Create quick start guide
   - [ ] Document configuration options
   - [ ] Add troubleshooting guide

7. **Developer documentation**
   - [ ] Update CONFIG_MIGRATION.md
   - [ ] Document best practices
   - [ ] Add contribution guidelines
   - [ ] Create architectural overview

#### CI/CD (Day 2)

8. **Continuous integration**
   - [ ] Add GitHub Actions workflow
   - [ ] Run tests on all commits
   - [ ] Check for hardcoded constants (grep audit)
   - [ ] Validate import structure
   - [ ] Generate coverage reports

9. **Code quality**
   - [ ] Add linting (pylint/flake8)
   - [ ] Add type checking (mypy)
   - [ ] Add formatting (black)
   - [ ] Add docstring checking

---

## Risk Management

### Known Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Breaking cryptographic proofs | CRITICAL | LOW | Extensive testing, hash verification |
| Output changes | HIGH | MEDIUM | Compare all JSON outputs before/after |
| Import circular dependencies | MEDIUM | LOW | Careful module design (already done) |
| Test failures | MEDIUM | MEDIUM | Run tests after each refactor |
| Performance degradation | LOW | LOW | Profile if issues arise |

### Rollback Plan

If issues arise:
1. Git revert to last good commit
2. Fix issues in isolation
3. Re-test thoroughly
4. Commit fixed version

Each phase should be committed separately for easy rollback.

---

## Success Criteria

### Per-Phase Criteria

- [ ] All files in phase refactored
- [ ] All imports resolve correctly
- [ ] All syntax checks pass
- [ ] All existing tests pass
- [ ] Output JSON files unchanged (or documented changes)
- [ ] No hardcoded constants in refactored code
- [ ] Documentation updated
- [ ] Changes committed

### Project Completion Criteria

- [ ] All 30+ files refactored
- [ ] Zero hardcoded constants (verified by grep audit)
- [ ] 100% test pass rate maintained or improved
- [ ] All documentation complete
- [ ] CI/CD pipeline functional
- [ ] Code review completed
- [ ] Final verification passed

---

## Timeline

### Optimistic (10 days)

- Day 1-2: Phase 1 ✅ COMPLETE
- Day 3-4: Phase 2 (core analysis)
- Day 5-6: Phase 3 (validation)
- Day 7: Phase 4 (parsers)
- Day 8: Phase 5 (cross-validation)
- Day 9: Phase 6 (tests)
- Day 10: Phase 7 (testing & docs)

### Realistic (12 days)

- Day 1-2.5: Phase 1 ✅ COMPLETE
- Day 3-5: Phase 2 (core analysis, careful testing)
- Day 6-7.5: Phase 3 (validation, many files)
- Day 8: Phase 4 (parsers)
- Day 9: Phase 5 (cross-validation)
- Day 10: Phase 6 (tests)
- Day 11-12: Phase 7 (comprehensive testing & docs)

### Pessimistic (15 days)

- Add 3 days buffer for unexpected issues
- Comprehensive regression testing
- Thorough documentation review
- External code review

---

## Next Steps (Immediate)

### Start Phase 2

1. **Read api_cryptographic_proof_system.py** thoroughly
2. **Identify all hardcoded values** (make list)
3. **Plan refactoring approach** (order of changes)
4. **Create backup** of current outputs (proof hashes)
5. **Begin refactoring** systematically
6. **Test incrementally** (after each major change)
7. **Verify cryptographic proofs** unchanged
8. **Move to next file** (survey analyses)

### Tools/Commands

```bash
# Find hardcoded constants
grep -n "67.36\|0.315\|0.759\|0.776\|0.780" api_cryptographic_proof_system.py

# Test imports
python3 -c "from config.api import *; print('OK')"

# Run refactored file
python3 api_cryptographic_proof_system.py

# Compare outputs
diff api_proof_results.json api_proof_results.json.backup
```

---

## Notes

### Code Review Checklist (per file)

- [ ] All imports at top of file
- [ ] No hardcoded constants (except local variables)
- [ ] Docstrings updated
- [ ] Comments updated
- [ ] No new dependencies added
- [ ] Backward compatible
- [ ] Tests pass
- [ ] Output verified

### Refactoring Pattern (standard)

```python
# OLD
PLANCK_H0 = 67.36  # Hardcoded
result = calculate_something(PLANCK_H0)

# NEW
from config.constants import PLANCK_H0  # Centralized
result = calculate_something(PLANCK_H0)
```

### Common Replacements

| Old | New |
|-----|-----|
| `PLANCK_H0 = 67.36` | `from config.constants import PLANCK_H0` |
| `KIDS_S8 = 0.759` | `from config.surveys import KIDS_S8` |
| `schedule = [8,12,16,20,24,28,32]` | `from config.resolution import RESOLUTION_SCHEDULE_FULL` |
| `baseline = 0.0200` | `from config.corrections import UNIVERSAL_BASELINE` |
| `(1 + z)**(-0.5)` | `calculate_redshift_scaling_factor(z, REDSHIFT_SCALING_EXPONENT)` |

---

## Conclusion

Phase 1 complete and committed. Foundation solid. Ready to proceed with Phase 2 core analysis files. Critical files first (api_cryptographic_proof_system.py), then survey analyses, then tension analyses.

**Current Status:** ✅ Phase 1 complete, 🔄 Phase 2 ready to start
**Next File:** api_cryptographic_proof_system.py (645 LOC, HIGH PRIORITY)
**ETA Phase 2:** 2 days
**ETA Full Project:** 7.5-9.5 days remaining

---

**Created:** 2025-10-30
**Author:** Claude Code + Eric D. Martin
**Version:** 1.0
**Status:** Living document (update after each phase)
