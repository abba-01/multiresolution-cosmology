# START HERE - Claude Code Quick Reference

**READ THIS FILE FIRST IN EVERY SESSION**

---

## Critical Information

### Repository Context
- **GitHub:** https://github.com/abba-01/multiresolution-cosmology
- **Local Path:** /root/private_multiresolution/
- **Server Access:** SSH to got.gitgap.org (keys configured)
- **Live API:** https://got.gitgap.org/v1/

### Current Status
- **Overall Status:** PRODUCTION READY (see REPOSITORY_STATUS.md for details)
- **Last Major Milestone:** SSOT refactoring 100% complete (Oct 30)
- **Test Pass Rate:** 97.5% (77/79 tests)

---

## IMPORTANT RULES

### ❌ DO NOT DO THESE THINGS
1. **DO NOT create random standalone scripts** - Use existing architecture
2. **DO NOT delete files without explicit permission** - Ask first
3. **DO NOT make tarballs without cryptographic sealing** - Use api_cryptographic_proof_system.py
4. **DO NOT create public release files without proper review** - This is IP-sensitive
5. **DO NOT assume what user wants** - Ask clarifying questions

### ✅ DO THESE THINGS
1. **READ REPOSITORY_STATUS.md** - Get full project status
2. **USE existing tools** - api_cryptographic_proof_system.py, proof system
3. **CHECK git status** - Understand what's tracked/untracked
4. **ASK before big actions** - Especially anything public-facing
5. **REFERENCE this file** - Keep it updated with new learnings

---

## Key Files to Know About

### Status & Documentation
- **REPOSITORY_STATUS.md** - Comprehensive project status (READ THIS SECOND)
- **COMPLETE_ANALYSIS_SUMMARY.md** - Full scientific analysis
- **PUBLICATION_TASKS_COMPLETE_SUMMARY.md** - Publication readiness
- **NEXT_STEPS_PLAN.md** - Roadmap

### Cryptographic Proof System (IMPORTANT!)
- **api_cryptographic_proof_system.py** - Proper cryptographic sealing tool
- **proof_out/** - Directory with sealed proofs
- **API_CRYPTOGRAPHIC_PROOF_README.md** - How the proof system works

### Core Implementation
- **multiresolution_uha_encoder.py** - PATENT-PROTECTED (never expose)
- **config/** - SSOT configuration (centralized constants)

### Protection Status
- **UHA_PROTECTION_STATUS_2025-10-31.md** - What's protected vs public
- **.gitignore** - Shows what must never be committed

---

## IP Protection Rules

### NEVER Expose These
- UHA encoding algorithm (multiresolution_uha_encoder.py)
- UHA addresses/codes in plain text
- Morton coordinates or spatial indices
- Proprietary tensor calibration data

### ALWAYS Include in Public Releases
- API references (https://got.gitgap.org/v1)
- Sanitized scientific results
- Documentation of methods (not implementation)
- Cryptographic proof/verification

---

## Common Tasks & How To Do Them

### Creating a Public Release
1. Read UHA_PROTECTION_STATUS_2025-10-31.md first
2. Use existing sanitization approach (remove UHA codes)
3. Add API references to all result files
4. Use api_cryptographic_proof_system.py to seal
5. Ask user before finalizing

### Working with Git
```bash
git status  # Always check first
# Coordinate with user before commits
```

### Accessing Server
```bash
ssh root@got.gitgap.org
# Keys are configured, should work directly
```

---

## Quick Architecture Overview

### Configuration (SSOT - Single Source of Truth)
```
config/
├── constants.py      # Cosmological constants (Planck, SH0ES, etc.)
├── surveys.py        # Survey metadata (KiDS, DES, HSC)
├── corrections.py    # Systematic correction formulas
├── api.py           # API endpoints
└── resolution.py    # Resolution schedules
```

### Analysis Scripts
- Survey-specific: kids1000_real_analysis.py, des_y3_real_analysis.py, etc.
- Validation: test_implementation.py, test_physical_validation.py
- Cross-validation: compare_three_surveys.py, joint_lambda_cdm_fit.py

### Results
- JSON files in root (kids1000_real_analysis_results.json, etc.)
- Cryptographic proofs in proof_out/

---

## User's Goals

### What They're Working Towards
- Public release of results (without exposing UHA implementation)
- ArXiv paper submission
- Proving cosmological tensions can be resolved without new physics
- Maintaining patent protection on UHA encoding system

### Key Results They've Achieved
- H₀ tension: 5.0σ → 1.2σ (76% reduction)
- S₈ tension: 2.6σ → 2.1σ (21% reduction)
- Cross-survey validation across KiDS/DES/HSC (consistent pattern)
- Joint ΛCDM fit: χ²/dof = 1.81, p = 0.093

---

## When User Says Common Things

### "organize results for public download"
- They want: Sanitized results (no UHA addresses) + API references
- Use: Their existing proof system for sealing
- Check: UHA_PROTECTION_STATUS_2025-10-31.md for what to include
- Ask: Where they want it (GitHub release? Server upload? Zenodo?)

### "check what's on got.gitgap.org"
- Use: SSH access (ssh root@got.gitgap.org)
- Check: /var/www/, /opt/uha_service/, deployed endpoints

### "create a release"
- Read: PUBLICATION_TASKS_COMPLETE_SUMMARY.md first
- Use: api_cryptographic_proof_system.py
- Coordinate: What goes in, what stays private

---

## Update This File

When you learn something important that would help in future sessions:
1. Add it to the appropriate section
2. Keep it concise
3. Focus on "what I wish I'd known at the start"

---

**Last Updated:** 2025-10-31
**By:** Claude Code
**Purpose:** Stop relearning everything in every session!
