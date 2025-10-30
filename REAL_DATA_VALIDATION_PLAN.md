# Real Data Validation Plan
## Multi-Resolution S₈ Tension Resolution

**Status**: Ready for implementation
**Priority**: High-yield minimal validation suite
**Timeline**: Critical path to publication

---

## 1. Real Survey Data Validation

### 1.1 Target Surveys
**KiDS-1000** (Kuijken et al. 2019; Asgari et al. 2021)
- Coverage: 1000 deg²
- Redshift range: 0.1 < z < 1.2 (5 tomographic bins)
- S₈ = 0.759 ± 0.024 (cosmic shear)
- Data: COSEBIs, band powers
- URL: http://kids.strw.leidenuniv.nl/DR4/

**DES-Y3** (Abbott et al. 2022)
- Coverage: 4143 deg²
- Redshift range: 0.2 < z < 1.05 (4 bins)
- S₈ = 0.776 ± 0.017 (3x2pt)
- Data: ξ₊, ξ₋, w(θ), γₜ
- URL: https://des.ncsa.illinois.edu/releases/y3a2

**HSC-Y3** (Li et al. 2023)
- Coverage: 416 deg²
- Redshift range: 0.3 < z < 1.5 (4 bins)
- S₈ = 0.763 ± 0.020 (cosmic shear)
- Data: ξ₊, ξ₋
- URL: https://hsc-release.mtk.nao.ac.jp/

### 1.2 Implementation Strategy
```python
# Bin-by-bin multi-resolution refinement
for survey in [KiDS, DES, HSC]:
    for z_bin in survey.tomographic_bins:
        # Match UHA resolution to angular scale
        theta_arcmin = survey.theta_range
        z_eff = z_bin.z_effective
        scale_mpc = theta_to_comoving(theta_arcmin, z_eff)
        N_bits = calculate_resolution_bits(scale_mpc)

        # Run refinement at matched resolution
        delta_T = compute_epistemic_distance(
            planck_chain, lensing_chain, N_bits
        )

        # Track systematic correction by scale
        systematics[z_bin][N_bits] = delta_T
```

### 1.3 Expected Results
| Survey | Initial S₈ | Final S₈ | Tension (initial → final) |
|--------|-----------|----------|---------------------------|
| KiDS-1000 | 0.759 | 0.795 | 2.9σ → 1.5σ |
| DES-Y3 | 0.776 | 0.803 | 2.3σ → 1.2σ |
| HSC-Y3 | 0.763 | 0.798 | 2.7σ → 1.4σ |

**Validation Criteria**:
- ✅ All surveys converge to S₈ ≈ 0.80 ± 0.02
- ✅ ΔT < 0.15 for all redshift bins
- ✅ Resolution bits follow scale-matching: N ≈ 13 + 3·log₂(z_eff)

---

## 2. Model Profiling

### 2.1 Intrinsic Alignment Models

**TATT Model** (Troxel et al. 2023)
```python
# Tidal Alignment and Tidal Torquing
P_IA(k, z) = C1 * ρ_crit * Ω_m / D(z) * [
    (1 + z)^η_IA * b_TA * P_δδ(k, z) +  # Tidal alignment
    b_TT * k² * P_δδ(k, z)                # Tidal torquing
]

# Expected impact on S₈ at different resolutions
# N=20 (10 Mpc): ΔS₈ ~ +0.015 (tidal alignment dominates)
# N=24 (1 Mpc): ΔS₈ ~ +0.008 (tidal torquing)
```

**NLA Model** (Baseline comparison)
```python
# Non-Linear Alignment (Hirata & Seljak 2004)
P_IA(k, z) = -A_IA * C1 * ρ_crit * Ω_m / D(z) * P_δδ(k, z)

# Expected: TATT should show better ΔT convergence
# due to scale-dependent tidal torquing term
```

### 2.2 Photo-z Calibration Schemes

**Split Prior Approach**:
```python
# Test sensitivity to photo-z scatter
for calibration in ['COSMOS', 'DEEP2', 'VVDS']:
    # Refit Δz bias per tomographic bin
    bias_params = fit_photoz_bias(calibration)

    # Run multi-resolution refinement
    S8_corrected = apply_refinement(lensing_chain, bias_params)

    # Check ΔT convergence
    assert delta_T < 0.15, f"{calibration} failed convergence"
```

**Expected**:
- Δz uncertainty: σ(Δz) ~ 0.02 per bin
- Impact on S₈: ΔS₈ ~ 0.01 (comparable to N=16 correction)
- ΔT should converge regardless of prior choice

### 2.3 Shear Calibration Methods

**Self-Calibration** (KiDS, HSC)
```python
# Metacalibration: Response-based (DES)
m_metacal = measure_response_to_shear(galaxy_ensemble)

# Self-calibration: Image simulation (KiDS/HSC)
m_selfcal = calibrate_from_simulations(galaxy_ensemble)

# Expected difference: Δm ~ 0.01 → ΔS₈ ~ 0.009
# Both should converge to same S₈ after multi-resolution correction
```

---

## 3. BAO/CMB-Lensing Cross-Anchors

### 3.1 BAO Anchors (N ≈ 10-11 bits)

**BOSS/eBOSS** (Alam et al. 2021)
- Scale: r_d = 147.09 ± 0.26 Mpc (sound horizon)
- Resolution: N = 11 bits → Δr = 6.8 Mpc ≈ r_d / 22 ✅
- Redshift range: 0.2 < z < 2.2

```python
# BAO cross-validation
r_d = 147.09  # Mpc
z_effective = [0.38, 0.51, 0.70, 1.48, 2.33]  # BOSS/eBOSS

for z in z_effective:
    scale_mpc = r_d * (1 + z)  # Comoving BAO scale
    N_bits = 10 + int(np.log2(1 + z))  # 10-12 bits

    # Check ΔT at BAO scale
    delta_T_bao = compute_epistemic_distance(
        planck_chain, bao_chain, N_bits
    )

    # Expected: ΔT ~ 0.05-0.10 (better than lensing)
    assert delta_T_bao < 0.15
```

### 3.2 CMB Lensing

**Planck Lensing** (Planck Collaboration 2020)
- S₈ = 0.832 ± 0.013 (consistent with primary CMB)
- Angular scales: 40 < ℓ < 400
- Resolution: N ≈ 8-12 bits (large scales)

**DES-Y3 CMB Lensing** (Abbott et al. 2022)
- Combined with galaxy lensing: S₈ = 0.812 ± 0.008
- Expected: ΔT should be small (both CMB-derived)

```python
# CMB lensing cross-check
planck_lensing = load_planck_lensing_chain()
des_lensing = load_des_y3_lensing_chain()

# These should have ΔT < 0.10 even at N=8
# (Both measure same large-scale potential)
delta_T_cmbxcmb = compute_epistemic_distance(
    planck_lensing, des_lensing, N_bits=8
)

print(f"CMB lensing self-consistency: ΔT = {delta_T_cmbxcmb:.3f}")
```

---

## 4. Baryon Systematics Validation

### 4.1 Compare to Hydrodynamic Simulations

**OWLS** (van Daalen et al. 2011)
- AGN feedback models: REF, AGN_8.0, AGN_8.5
- Suppression: 5-15% at k ~ 1 h/Mpc
- Redshift evolution: ∝ (1+z)^(-1.5)

**EAGLE** (Schaye et al. 2015)
- Calibrated to galaxy properties
- Baryon suppression: ~10% at k = 1 h/Mpc
- Scale-dependent: minimal at k < 0.1, maximal at k ~ 10

**Illustris-TNG** (Pillepich et al. 2018)
- Most recent, best calibrated
- Suppression: 8 ± 3% at k = 1 h/Mpc (z=0)

### 4.2 Validation Strategy
```python
# Load baryonification model predictions
bcm_model = load_bcm_model(A_baryon=3.13)  # Schneider+ 2019
owls_model = load_owls_model(feedback='AGN_8.0')
eagle_model = load_eagle_suppression()
illustris_model = load_tng_suppression()

# Our N=24 prediction: +5% correction to S₈
our_correction_pct = 5.0  # ΔS₈ = +0.034 on base of 0.766

# Compare to simulation predictions at k ~ 1 h/Mpc
k_target = 1.0  # h/Mpc (corresponds to ~1 Mpc scales, N=24)

bcm_suppression = bcm_model.P_ratio(k_target)       # ~10%
owls_suppression = owls_model.P_ratio(k_target)     # ~12%
eagle_suppression = eagle_model.P_ratio(k_target)   # ~10%
illustris_suppression = illustris_model.P_ratio(k_target)  # ~8%

# Check: our S₈ correction is ~half of power suppression
# (S₈ ∝ σ₈ ∝ √P, so 10% in P → 5% in S₈)
expected_S8_correction = np.mean([
    np.sqrt(1 + bcm_suppression/100) - 1,
    np.sqrt(1 + owls_suppression/100) - 1,
    np.sqrt(1 + eagle_suppression/100) - 1,
    np.sqrt(1 + illustris_suppression/100) - 1
]) * 100

print(f"Our correction: {our_correction_pct:.1f}%")
print(f"Simulations predict: {expected_S8_correction:.1f}%")
assert abs(our_correction_pct - expected_S8_correction) < 2.0
```

### 4.3 Sanity Checks
- ✅ Correction should be scale-dependent (not constant offset)
- ✅ At N=12 (100 Mpc): minimal baryonic correction (< 1%)
- ✅ At N=20 (10 Mpc): moderate correction (~3%)
- ✅ At N=24 (1 Mpc): maximum correction (~5%)
- ⚠️ At N=28 (100 kpc): should NOT improve further (stellar physics, not cosmology)

---

## 5. Null Tests & Leakage Detection

### 5.1 E/B-Mode Decomposition
```python
# B-modes should be zero in cosmic shear (GR prediction)
# If method "improves" ΔT when fed B-modes → LEAK DETECTED

def test_b_mode_null():
    """Test that B-modes do not spuriously reduce ΔT"""
    # Load real survey B-mode spectrum (should be noise)
    C_ell_B = load_b_mode_power_spectrum(survey='DES-Y3')

    # Run multi-resolution refinement on B-modes
    delta_T_B = compute_epistemic_distance_from_b_modes(C_ell_B)

    # B-modes should NOT converge
    assert delta_T_B > 0.25, "B-mode leak detected!"

    # E/B ratio should be large
    C_ell_E = load_e_mode_power_spectrum(survey='DES-Y3')
    eb_ratio = np.median(C_ell_E / np.maximum(C_ell_B, 1e-10))
    assert eb_ratio > 100, "E/B contamination detected"
```

### 5.2 Star/PSF Residual Maps
```python
def test_psf_residual_null():
    """Test that PSF residuals do not reduce ΔT"""
    # Load star-star correlation functions
    xi_star = load_star_correlations(survey='KiDS-1000')

    # These should be uncorrelated with dark matter
    # Run multi-resolution on star field
    delta_T_stars = compute_epistemic_distance_from_stars(xi_star)

    # Should NOT improve
    assert delta_T_stars > 0.30, "PSF systematics leak detected!"
```

### 5.3 Mask/Mode Coupling Tests
```python
def test_mask_coupling():
    """Test that survey mask does not create spurious ΔT reduction"""
    # Generate random field with survey mask applied
    random_map = generate_random_field() * survey_mask

    # Compute pseudo-Cℓ
    C_ell_masked = compute_pseudo_cl(random_map)

    # Apply mode coupling correction
    C_ell_corrected = apply_mode_coupling_matrix(C_ell_masked)

    # Run refinement on corrected vs uncorrected
    delta_T_before = compute_delta_T(C_ell_masked)
    delta_T_after = compute_delta_T(C_ell_corrected)

    # Should be insensitive to mask correction
    assert abs(delta_T_before - delta_T_after) < 0.05
```

---

## 6. Schedule Robustness

### 6.1 Randomized Resolution Order
```python
def test_schedule_invariance():
    """Test that result is independent of resolution order"""

    base_schedule = [8, 12, 16, 20, 24]
    n_permutations = 100

    results = []
    for i in range(n_permutations):
        # Randomize order (keep 8 first, 24 last)
        middle = [12, 16, 20]
        np.random.shuffle(middle)
        schedule = [8] + middle + [24]

        # Run refinement
        S8_final = run_refinement_with_schedule(schedule)
        results.append(S8_final)

    # Check variance
    S8_mean = np.mean(results)
    S8_std = np.std(results)

    print(f"S₈ final: {S8_mean:.3f} ± {S8_std:.3f}")
    assert S8_std < 0.01, "Schedule order dependence detected!"
```

### 6.2 Resolution Granularity Test
```python
def test_fine_schedule():
    """Test with finer resolution steps"""

    # Coarse schedule (current)
    coarse = [8, 12, 16, 20, 24]
    S8_coarse = run_refinement_with_schedule(coarse)

    # Fine schedule (every 2 bits)
    fine = [8, 10, 12, 14, 16, 18, 20, 22, 24]
    S8_fine = run_refinement_with_schedule(fine)

    # Results should agree within uncertainty
    assert abs(S8_coarse - S8_fine) < 0.015
```

---

## 7. Neutrino Mass Sensitivity

### 7.1 Σm_ν Prior Test
```python
def test_neutrino_mass_prior():
    """Test that ΔT convergence persists with different neutrino mass"""

    # Minimal mass (normal hierarchy)
    m_nu_min = 0.06  # eV
    S8_min, deltaT_min = run_refinement(m_nu=m_nu_min)

    # Moderate mass
    m_nu_mod = 0.12  # eV (KiDS+Planck preference)
    S8_mod, deltaT_mod = run_refinement(m_nu=m_nu_mod)

    # High mass (excluded by Planck alone)
    m_nu_high = 0.20  # eV
    S8_high, deltaT_high = run_refinement(m_nu=m_nu_high)

    # All should converge (ΔT < 0.15)
    assert deltaT_min < 0.15
    assert deltaT_mod < 0.15
    assert deltaT_high < 0.15

    # S₈ should shift slightly (expected ~1σ difference)
    # S₈ anti-correlated with Σm_ν
    assert S8_min > S8_mod > S8_high

    # Check magnitude: ΔS₈ ~ 0.015 per 0.06 eV
    dS8_dm = (S8_min - S8_mod) / (m_nu_min - m_nu_mod)
    expected_slope = -0.25  # From Planck 2018

    print(f"∂S₈/∂Σm_ν = {dS8_dm:.2f} (expected: {expected_slope:.2f})")
    assert abs(dS8_dm - expected_slope) < 0.1
```

### 7.2 Free Neutrino Mass Fit
```python
def test_neutrino_mass_free():
    """Allow Σm_ν to vary freely in multi-resolution fit"""

    # Run refinement with neutrino mass as free parameter
    result = run_refinement_free_mnu()

    S8_final = result['S8']
    m_nu_final = result['m_nu']
    deltaT_final = result['delta_T']

    # Should still converge
    assert deltaT_final < 0.15

    # S₈ and m_ν should decorrelate after refinement
    correlation = compute_correlation(result['chain'], ['S8', 'm_nu'])

    print(f"S₈-Σm_ν correlation: {correlation:.3f}")
    # Expected: |ρ| < 0.3 (reduced from ~0.7 before correction)
```

---

## 8. Reproducibility Infrastructure

### 8.1 SHA-256 Run Identifiers
```python
import hashlib
import json

def generate_run_id(config: dict) -> str:
    """Generate SHA-256 hash for reproducibility"""
    # Canonicalize configuration
    config_str = json.dumps(config, sort_keys=True)

    # Hash
    run_id = hashlib.sha256(config_str.encode()).hexdigest()

    return run_id[:16]  # Short hash

# Example usage
config = {
    'survey': 'DES-Y3',
    'resolution_schedule': [8, 12, 16, 20, 24],
    'ia_model': 'TATT',
    'photoz_prior': 'COSMOS',
    'shear_calibration': 'metacal',
    'neutrino_mass': 0.06,
    'code_version': 'v1.0.0',
    'timestamp': '2025-10-30T12:00:00Z'
}

run_id = generate_run_id(config)
print(f"Run ID: {run_id}")  # e.g., "a3f5e9c2d4b1a7f3"
```

### 8.2 UHA API Version Hashing
```python
def get_uha_api_hash() -> str:
    """Hash UHA encoder implementation for versioning"""
    with open('multiresolution_uha_encoder.py', 'rb') as f:
        code = f.read()

    api_hash = hashlib.sha256(code).hexdigest()
    return api_hash[:16]

# Store in results
results['uha_api_version'] = get_uha_api_hash()
results['run_id'] = generate_run_id(config)
```

### 8.3 Full Provenance Tracking
```json
{
  "run_id": "a3f5e9c2d4b1a7f3",
  "uha_api_version": "f7e4d9c1a2b5e8f3",
  "timestamp": "2025-10-30T12:00:00Z",
  "config": {
    "survey": "DES-Y3",
    "resolution_schedule": [8, 12, 16, 20, 24],
    "ia_model": "TATT",
    "photoz_prior": "COSMOS",
    "shear_calibration": "metacal",
    "neutrino_mass": 0.06
  },
  "results": {
    "S8_initial": 0.776,
    "S8_final": 0.803,
    "tension_reduction": "2.3σ → 1.2σ",
    "delta_T_final": 0.014
  },
  "validation": {
    "b_mode_null": "PASS",
    "psf_residual_null": "PASS",
    "schedule_robustness": "PASS (σ = 0.008)",
    "neutrino_sensitivity": "PASS",
    "baryon_consistency": "PASS (EAGLE ± 1.2%)"
  }
}
```

---

## 9. Implementation Timeline

### Phase 1: Infrastructure (Week 1)
- [ ] Set up data download scripts for KiDS/DES/HSC
- [ ] Implement UHA API versioning and hashing
- [ ] Create provenance tracking system
- [ ] Build null test framework

### Phase 2: Core Validation (Week 2-3)
- [ ] Run bin-by-bin refinement on all three surveys
- [ ] Implement TATT IA model comparison
- [ ] Test split photo-z priors
- [ ] Compare shear calibration methods

### Phase 3: Cross-Validation (Week 4)
- [ ] BAO cross-anchor validation
- [ ] CMB lensing consistency checks
- [ ] Baryon systematics comparison
- [ ] Neutrino mass sensitivity tests

### Phase 4: Robustness & Publication (Week 5-6)
- [ ] Schedule randomization tests
- [ ] E/B mode null tests
- [ ] PSF residual validation
- [ ] Write validation paper
- [ ] Prepare data release

---

## 10. Success Criteria

### Minimal Validation (Publication-Ready)
1. ✅ All three surveys converge: ΔT < 0.15
2. ✅ Final S₈ = 0.80 ± 0.02 (all surveys)
3. ✅ Tension reduced to < 2σ (all surveys)
4. ✅ B-mode null test passes
5. ✅ Schedule order-invariant (σ < 0.01)
6. ✅ Baryon systematics consistent with simulations (< 2% difference)
7. ✅ Neutrino mass insensitive (ΔT < 0.15 for all priors)
8. ✅ Full provenance tracking in place

### Extended Validation (Strong Evidence)
1. ✅ BAO/CMB lensing cross-anchors consistent
2. ✅ TATT IA model improves convergence vs NLA
3. ✅ PSF residual null test passes
4. ✅ Results stable across photo-z calibrations
5. ✅ Shear calibration method-independent

---

## File Manifest

### Data Downloads
- `scripts/download_kids1000.sh` - KiDS-1000 data
- `scripts/download_des_y3.sh` - DES-Y3 data
- `scripts/download_hsc_y3.sh` - HSC-Y3 data

### Core Analysis
- `real_data_validation.py` - Main validation pipeline
- `survey_binning.py` - Tomographic bin handlers
- `ia_models.py` - TATT/NLA implementations
- `photoz_calibration.py` - Split prior testing

### Cross-Validation
- `bao_cross_anchor.py` - BAO validation
- `cmb_lensing_cross.py` - CMB lensing checks
- `baryon_systematics.py` - Hydro sim comparison

### Null Tests
- `null_tests.py` - E/B mode, PSF, mask tests
- `schedule_robustness.py` - Randomization tests
- `neutrino_sensitivity.py` - m_ν prior tests

### Infrastructure
- `provenance.py` - SHA-256 hashing and tracking
- `uha_versioning.py` - API version control
- `results_schema.json` - Standardized output format

---

**Priority**: Start with Phase 1 infrastructure, then run KiDS-1000 as first real-data test.
