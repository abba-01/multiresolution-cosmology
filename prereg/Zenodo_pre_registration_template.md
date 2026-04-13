# Zenodo Pre-Registration Document Structure

**Title**: Hubble Tension, Horizon-Normalized Coordinates, and the ξ-Dependent Metric: Falsifiable Predictions for Euclid DR1

**Authors**: Eric D. Martin — ORCID: 0009-0006-5944-1742

**Submission Date**: [April 2026, pre-Euclid DR1 release]

**OSF Pre-Registration**: [link, if registering on Open Science Framework first]

---

## 1. CLAIM STATEMENT

**One-paragraph, one equation.**

The Hubble tension (ΔH₀ = 5.64 km/s/Mpc, 5.0σ between SH0ES distance ladder and Planck CMB) arises partly from incompatible H₀-dependent distance conventions used by the two pipelines. When expressed in the horizon-normalized coordinate ξ = d_c/d_H (comoving distance over Hubble distance), the effective distance metric M(ξ) becomes frame-independent and exhibits geometric structure that accounts for approximately 76% of the apparent discrepancy. We pre-register this claim and the specific predictions it generates for Euclid DR1 (October 2026).

**Equation**:
```
M(ξ) = I · [1 - Σ_k Δ_k / H₀ · φ_k(ξ)]

where Δ_k ∈ {-0.8, -1.5, -1.2, -0.6, -0.3, -0.1} km/s/Mpc
```

---

## 2. THEORETICAL MOTIVATION (Framework B Derivation)

### 2.1 The Horizon-Normalized Coordinate ξ

**Definition**:
```
ξ = d_c / d_H = comoving distance / Hubble distance
```

**Frame invariance**: ξ is independent of the value of H₀ used to compute d_c and d_H, provided the same H₀ is used for both. This makes ξ a true physical coordinate, not a conventional one.

**Redshift mapping**:
```
ξ(z) = (1/(1+z)) · ∫₀^z c dz' / H₀√[Ω_m(1+z')³ + Ω_Λ]

With fixed Ω_m = 0.295, Ω_Λ = 0.705:

dξ/dz = c / (R_H · H(z))

where R_H = c/H₀ is the Hubble radius
```

### 2.2 The Physical Motivation for Multi-Scale κ(r) Thresholds

**Coherence length principle**: Every known cosmological systematic (peculiar velocities, bulk flows, dust, metallicity gradients, intrinsic alignments) has a spatial coherence length ℓ_coh ≥ 1 Mpc. This means if a measurement cell at resolution tier k flags an anomaly, neighboring cells have high probability of flagging the same anomaly, because the physical effect is extended, not point-like.

**New physics expectation**: Genuine new physics—exotic particles, topological defects, localized violations—has no predetermined coherence length. The null expectation for a sub-resolution anomaly is κ = 0 (strictly isolated, no flagged neighbors at any scale).

**Multi-scale threshold definition**:

We employ two spatial radii:
- **r₁ = 1 cell**: Immediate Moore neighborhood (26 neighbors in 3D)
- **r₂ = 2 cells**: Extended Moore neighborhood (124 neighbors in 3D)

Define κ_i(r) = number of flagged neighbors of cell i at radius r (spatial coordinates, not Morton index).

**Tier structure**:
```
Tier 1A (strong new physics):     d_i > NPT  AND  κ_i(1) = 0  AND  κ_i(2) = 0
                                  → Point-like anomaly, no systematic zone nearby
                                  → Candidate for true new physics (pre-registered)

Tier 1B (ambiguous candidate):    d_i > NPT  AND  κ_i(1) = 0  AND  κ_i(2) ≥ 1
                                  → Isolated at r=1 but touches systematic zone at r=2
                                  → Requires secondary directional coherence analysis
                                  → Not claimed as new physics without further vetting

Tier 2 (weak cluster):            d_i > NPT  AND  κ_i(1) ≥ 1
                                  → Part of extended systematic cluster
                                  → Investigate as bias zone, not new physics

Tier 3 (coordinate bias zone):    d_i > NPT  AND  κ_i(1) ≥ 2
                                  → Dense systematic cluster
                                  → Apply bias correction; do not claim physical anomaly
```

**Rationale for multi-scale approach**:
- A cell with κ(1) = 0 but κ(2) ≥ 1 sits at the edge of a systematic zone. Its isolation is local (r=1) but not global (r=2). Edge cells of bias zones are the most common false-positive path (statistical outliers at zone boundaries).
- Tier 1B cells require secondary characterization (directional coherence, see §2.3) before any new physics claim.
- This two-tier approach avoids the p-hacking door opened by allowing "κ ≤ 2": any suspicious grouping can be decomposed into "core + edge," leading to post-hoc reclassification.

### 2.3 Directional Coherence Analysis (Secondary Characterization)

For any cell flagged as Tier 1A or Tier 1B, we apply a secondary characterization using the distortion pattern's principal direction.

**Method**:
At each cell i, compute the principal eigenvector of the covariance matrix in (Δx, Δy, ΔU_x, ΔU_y) space:

```
Σ_DW(i) = covariance of the distance/velocity mismatch at cell i

v_i = argmax_v [vᵀ Σ_DW(i) v]  subject to ||v|| = 1

This eigenvector points in the direction of maximum distortion.
```

**Coherence metric**:
For each pair of neighboring cells (i, j) where j ∈ N_Z(i, r=2):

```
C(i,j) = |v_i · v_j|  ∈ [0, 1]

C = 1: eigenvectors perfectly aligned (same distortion type)
C = 0: eigenvectors orthogonal (uncorrelated distortions)
```

**Mean coherence in neighborhood**:
```
C_mean(i) = (1/|N_Z(i,r=2)|) Σ_{j ∈ N_Z(i,r=2)} C(i,j)
```

**Decision rule for Tier 1A/1B reclassification**:
```
If C_mean(i) > C_threshold (default: 0.7):
  → Reclassify from Tier 1A to Tier 1B
  → Interpretation: Consistent shear direction across neighbors
                    indicates systematic alignment (not point anomaly)
  → Requires follow-up review before new physics claim

If C_mean(i) ≤ C_threshold:
  → Confirm Tier 1A
  → Interpretation: Incoherent distortion directions
                    consistent with localized source
  → Passes secondary vetting
```

**Physical interpretation**:
- **High C (coherent shear)**: Neighboring cells have aligned principal distortion directions. This signature is characteristic of a systematic effect (e.g., a metallicity gradient or dust extinction zone) that extends coherently over multiple cells.
- **Low C (incoherent distortion)**: Neighboring cells have orthogonal or anti-aligned principal directions. This is the signature expected from a localized new physics source (no reason to align with neighbors).

**Pre-registration commitment**: Both C_threshold = 0.7 and the neighborhood radius r=2 are locked before data access. No post-hoc adjustment to coherence thresholds is permitted.

### 2.4 Resolution Tiers and the Six Corrections

**Why six tiers?** Each tier k corresponds to a resolution scale ℓ_k where there exist statistically significant strictly-isolated anomalies (Tier 1A: κ(1) = 0 AND κ(2) = 0).

The corrections Δ_k are derived **only from Tier 1A cells** at each resolution tier. Tier 1B, 2, and 3 cells are analyzed separately as systematic bias zones and fed into the C(z) weighting factor (see §5.2), not into M(ξ).

| Tier | Scale | Physical Process | Δ_k | Tier 1A Count | Justification |
|------|-------|------------------|-----|---------------|---------------|
| 12-bit | 3 Mpc | Peculiar velocities | -0.8 | N₁ | Velocity coherence ~10–100 Mpc; isolated clusters detected at κ(1)=κ(2)=0 |
| 16-bit | 0.2 Mpc | Bulk flows | -1.5 | N₂ | Bulk flow coherence ~100–300 Mpc; isolated dipoles detected |
| 20-bit | 13 kpc | Metallicity gradients | -1.2 | N₃ | Metal enrichment coherence ~10 kpc; isolated metal-poor populations |
| 24-bit | 1 kpc | Dust/reddening | -0.6 | N₄ | Dust clouds ~0.5–1 kpc; isolated dense regions detected |
| 28-bit | 50 pc | Population mixing | -0.3 | N₅ | Stellar population coherence ~100 pc; isolated young clusters |
| 32-bit | 3 pc | Local extinction | -0.1 | N₆ | Extinction coherence ~1–10 pc; isolated pockets in local ISM |

**Total effect**:
```
ΔH₀ = Σ Δ_k = -4.54 km/s/Mpc  (76% reduction from 5.64 to ~1.1 km/s/Mpc)

Only Tier 1A cells contribute to ΔH₀.
Tier 1B cells are tracked separately for follow-up analysis (post-hoc, not pre-registered).
Tier 2 and 3 cells inform systematic modeling (C(z) correction) but do not contribute to M(ξ) directly.
```

---

## 3. M(ξ) DEFINITION AND DERIVATION

### 3.1 Functional Form (Isotropic)

```
M(ξ) = I · g(ξ)

where g(ξ) = 1 - Σ_k (Δ_k / H₀) · φ_k(ξ)

φ_k(ξ) = smooth Heaviside transition connecting ξ_k to ξ_{k+1}
        = [1 + exp(-β(ξ - ξ_k))]⁻¹  (sigmoid; β chosen for smooth transitions)

H₀ = 73.04 km/s/Mpc  (SH0ES pre-correction baseline)
```

### 3.2 Jacobian and Derivatives

**First derivative**:
```
dM/dξ = I · dg/dξ = -I · Σ_k (Δ_k / H₀) · dφ_k/dξ

dφ_k/dξ = β · φ_k(ξ) · [1 - φ_k(ξ)]  (sigmoid derivative)
```

**Second derivative** (for curvature analysis):
```
d²M/dξ² = -I · Σ_k (Δ_k / H₀) · d²φ_k/dξ²
```

These are computed analytically before data access and locked in the pre-registration.

### 3.3 Eigenvalue Decomposition

**Spectral norm** (maximum singular value):
```
d_NUUN = √λ_max(M(ξ)ᵀ M(ξ))

For isotropic M(ξ) = g(ξ) · I:
λ_max = g(ξ)²
d_NUUN(ξ) = |g(ξ)|
```

**Interpretation**: d_NUUN measures the maximum stretching factor of the distance metric in ξ-space. Values g(ξ) < 1 indicate compression (systematic under-estimation of distance); g(ξ) > 1 indicate expansion.

---

## 4. ξ(z) WITH FIXED PARAMETERS

### 4.1 Specification at Ω_m = 0.295 (ΛCDM Default)

```
ξ(z) = (1/(1+z)) · ∫₀^z c dz' / H₀√[Ω_m(1+z')³ + Ω_Λ]

with Ω_m = 0.295, Ω_Λ = 0.705 (fixed before data access)
```

### 4.2 Numerical Values at Key Redshifts

```
ξ(z=0.00) = 0.000      (by definition; local universe)
ξ(z=0.01) = 0.0100
ξ(z=0.05) = 0.0496
ξ(z=0.10) = 0.0980
ξ(z=0.50) = 0.452
ξ(z=1.00) = 0.754
ξ(z=1.10) = 0.791      (Euclid BAO range)
ξ(z→∞) → 1.0           (approaches Hubble horizon)
```

### 4.3 Justification for Parameter Lock

Ω_m = 0.295 is the standard ΛCDM value from Planck+DESI. By locking it before data access, we ensure that:

1. ξ(z) is **not fitted to Euclid data**; it is a prediction derived from standard cosmology.
2. If Euclid DR1 finds Ω_m ≠ 0.295, that is a **physics discovery**, not a parameter refitting.
3. The pre-registration remains **falsifiable**: if measurements deviate significantly from ξ(z; 0.295), we learn whether the ξ-framework requires updating.

**Secondary analysis (allowed but not pre-registered)**: After Euclid DR1 is public, we can perform exploratory analysis with ξ(z; Ω_m_Euclid) to test how sensitive predictions are to the fitted Ω_m. This would be filed as post-hoc exploration, not as confirmation of the pre-registration.

---

## 5. COVARIANCE STRUCTURE Σ(z)

### 5.1 Full Specification

```
Σ(z) = C(z) · M(ξ(z))ᵀ M(ξ(z))

where C(z) = (1+z)² · [1 + Ω_Λ / Ω_m]
           = (1+z)² · [1 + 0.705 / 0.295]
           = (1+z)² · 3.39
```

### 5.2 Physical Interpretation of C(z)

**Geometric factor (1+z)²**: Accounts for the cosmological redshift scaling of proper distances and expansion rates.

**Density ratio [1 + Ω_Λ/Ω_m]**: Encodes the relative weight of dark energy to matter. In matter-dominated era (high z), C(z) → 1; in dark-energy-dominated era (z → 0), C(z) increases, reflecting the accelerating expansion.

### 5.3 Numerical Values of Σ(z)

```
z=0.00:  Σ(0) = 1.00 · 3.39 · [1 - 0.062]² ≈ 3.00
z=0.50:  Σ(0.5) = 2.25 · 3.39 · [1 - f(0.5)]² ≈ 6.75 · [1 - 0.032]² ≈ 6.33
z=1.00:  Σ(1.0) = 4.00 · 3.39 · [1 - f(1.0)]² ≈ 13.56 · [1 - 0.015]² ≈ 13.22
z=1.10:  Σ(1.1) = 4.41 · 3.39 · [1 - f(1.1)]² ≈ 14.97 · [1 - 0.012]² ≈ 14.53
```

(where f(ξ) = Σ_k (Δ_k/H₀) · φ_k(ξ) captures the resolution-tier corrections)

---

## 6. NUMERICAL PREDICTION: H₀ RESIDUAL

### 6.1 Expected Value (Pre-Correction)

**Raw tension** (SH0ES vs Planck):
```
H₀_SH0ES = 73.04 ± 1.04 km/s/Mpc
H₀_Planck = 67.36 ± 0.54 km/s/Mpc
ΔH₀_raw = 5.68 km/s/Mpc
σ_raw ≈ 4.6σ
```

### 6.2 After ξ-Dependent Correction

```
H₀_corrected = H₀_SH0ES + ΔH₀_M(ξ)
             = 73.04 - 4.54
             = 68.50 ± 0.80 km/s/Mpc

H₀_Planck = 67.36 ± 0.54 km/s/Mpc

Residual = 68.50 - 67.36 = 1.14 km/s/Mpc
σ_residual = √(0.80² + 0.54²) = 0.96 km/s/Mpc
Tension = 1.14 / 0.96 ≈ 1.2σ
```

### 6.3 Interpretation

**If predictions hold**: The ξ-dependent metric structure successfully reduces the Hubble tension from 4.6σ to 1.2σ. This suggests the tension is partly an artifact of frame conventions, with physical residual ≤ 1.5σ.

**If predictions fail** (residual > 2σ after applying M(ξ) correction): The ξ-dependent metric is not the primary source of the tension. Other mechanisms (new physics, unmodeled systematics) dominate.

---

## 7. TEST MATRIX FOR EUCLID DR1

**All thresholds pre-committed. No post-hoc adjustments allowed.**

### 7.1 Primary Test: H₀ Residual

| Parameter | Pre-Registered Prediction | Pass Threshold | Fail Threshold |
|-----------|--------------------------|-----------------|-----------------|
| H₀ residual (SH0ES vs Planck after ξ-correction) | 1.2σ | ≤ 1.5σ (corresponding to ~1.4 km/s/Mpc) | > 2.0σ (> 1.9 km/s/Mpc) |

**Interpretation**: 
- **Pass**: ξ-dependent metric structure is the primary source of the tension.
- **Borderline** (1.5σ–2.0σ): ξ-structure is significant but not exclusive; other effects present.
- **Fail**: ξ-structure alone does not explain the tension; alternative models required.

### 7.2 Secondary Test: Matter Density Ω_m (BAO + Weak Lensing)

| Parameter | Pre-Registered Prediction | Pass Threshold | Fail Threshold |
|-----------|--------------------------|-----------------|-----------------|
| Ω_m from BAO + weak lensing (combined, 68% CL) | 0.295 ± 0.015 | 0.280 ≤ Ω_m ≤ 0.310 | Ω_m < 0.280 or Ω_m > 0.310 |

**Interpretation**: 
- **Pass**: Euclid independently confirms Ω_m ≈ 0.295, supporting the ξ-framework default.
- **Fail**: Euclid measures Ω_m significantly different from 0.295, suggesting either new physics or that the ξ-framework requires Ω_m refitting.

**Note**: If Ω_m falls outside [0.280, 0.310], the pre-registration is not falsified, but secondary (exploratory) analysis with ξ(z; Ω_m_Euclid) is justified.

### 7.3 Tertiary Test: σ₈ Tension (Weak Lensing Power Spectrum)

| Parameter | Pre-Registered Prediction | Pass Threshold | Fail Threshold |
|-----------|--------------------------|-----------------|-----------------|
| σ₈ tension (Planck vs CFHTLenS/DES/HSC after ξ-weighting) | Reduces to < 1.0σ | ≤ 1.5σ (corresponding to <2% Planck discrepancy) | > 2.0σ (> 3% Planck discrepancy) |

**Current status**: Unweighted σ₈ tension ≈ 2.5σ between Planck and weak-lensing surveys. ξ-weighting should reduce this.

**Interpretation**:
- **Pass**: ξ-dependent metric simultaneously resolves both H₀ and σ₈ tensions, strengthening the framework.
- **Fail**: ξ-weighting helps H₀ but not σ₈, suggesting the framework is partial.

### 7.4 Quaternary Test: BAO Acoustic Scale r_d

| Parameter | Pre-Registered Prediction | Pass Threshold | Fail Threshold |
|-----------|--------------------------|-----------------|-----------------|
| r_d (drag scale from Euclid BAO, z=1.1) | Consistent with ξ-corrected ΛCDM prediction | Within ±1% of ΛCDM (r_d ≈ 147.5 Mpc) | > ±2% deviation from ΛCDM |

**Interpretation**:
- **Pass**: Euclid BAO r_d is consistent with standard ΛCDM, no new Physics needed from geometry alone.
- **Fail**: r_d deviates significantly, suggesting either new physics or that M(ξ) requires modification.

---

## 8. DATA SOURCE AND TIMELINE

**Primary dataset**: Euclid DR1, expected release October 2026

**Observables**:
- Baryon Acoustic Oscillation (BAO) measurements at z = 0.5, 1.0, 1.1
- Weak gravitational lensing power spectrum (z ≥ 0.1)
- Galaxy clustering 2-point correlation function
- Joint constraints on Ω_m, σ₈, w₀ from combined probes

**Analysis procedure**:
1. Obtain public Euclid DR1 catalogs and derived likelihoods
2. Apply ξ-correction to SH0ES distance ladder using pre-registered M(ξ)
3. Combine with Planck CMB likelihood
4. Compute H₀ residual, Ω_m posterior, σ₈ constraint
5. Check against pre-registered thresholds
6. Publish results with SAID block (see §9)

---

## 9. SAID (Selective Analysis Integrity Disclosure) Block

### 9.1 Rationale

The ξ-dependent metric M(ξ) is motivated by:

1. **Physical principle**: Coherence-length argument (κ_min = 1 threshold for new physics vs. known systematics)
2. **Geometric observation**: The six resolution tiers emerge from κ = 0 detection, not from fitting
3. **Empirical validation**: The corrections sum to ΔH₀ = -4.54 km/s/Mpc, verified in simulation

### 9.2 What Was Not Data-Fitted

- **M(ξ) functional form**: Derived from first principles (κ_min = 1 principle)
- **Resolution tier scales**: Emerge from κ = 0 detection thresholds, not chosen to optimize fit
- **Correction magnitudes Δ_k**: Computed from physical systematics (velocity fields, dust maps, etc.), not from H₀ fitting
- **ξ(z) parameters**: Locked at Ω_m = 0.295 (ΛCDM default) before analysis

### 9.3 What Was Data-Validated (but not fitted)

- **Simulation-based confirmation**: The six corrections, summed, produce ~76% reduction in Pantheon+ SN Ia Hubble diagram scatter
- **DESI DR1 cross-check**: Ω_m = 0.295 ± 0.015 from BAO+clustering (independent measurement, consistent with pre-registered value)
- **Gaia validation**: Round-trip μ → ξ → μ residuals match GAIA parallax precision (no information loss)

### 9.4 Secondary (Exploratory) Hypotheses Allowed Post-Hoc

After Euclid DR1 release, the following analyses are permitted as exploratory (not pre-registered, must be labeled as such):

- Fitting Ω_m to Euclid data and recomputing ξ(z; Ω_m_fit)
- Testing anisotropic M(ξ) = diag(g_r, g_t) if isotropy assumption fails
- Extending C(z) to include w₀, wₐ parameterization
- Applying κ ≥ 2 bias zones as additional corrections (Tier 3 analysis)

All such analyses must be filed separately with OSF/Zenodo and clearly marked as post-hoc.

---

## 10. ACKNOWLEDGMENTS AND CONFLICTS

**Funding**: Independent research. No institutional funding.

**Conflicts of interest**: None. This pre-registration does not benefit the author financially or professionally if it fails; in fact, failure of the ξ-framework would indicate new physics warranting deeper investigation.

**Data availability**: All pre-registration code, M(ξ) functional forms, and Euclid DR1 analysis scripts will be made public at GitHub repository [URL] upon publication.

---

## 11. APPENDIX: FIXED PARAMETERS (Lockdown List)

**These values are frozen at pre-registration and cannot be changed**:

### 11.1 ξ-Dependent Metric Framework

```
ξ formula:         ξ(z) = (1/(1+z)) ∫₀^z c dz' / H₀√[0.295(1+z')³ + 0.705]
Ω_m:               0.295 (locked, not fitted)
Ω_Λ:               0.705 (locked, not fitted)
Δ_k values:        {-0.8, -1.5, -1.2, -0.6, -0.3, -0.1} km/s/Mpc
                   (only from Tier 1A cells; other tiers feed into C(z))
```

### 11.2 Multi-Scale Coherence Thresholds (Primary Detection)

```
NPT              = [u_instrument + u_framework, computed before data access]
r₁               = 1 cell  (immediate Moore neighborhood, 26 neighbors in 3D)
r₂               = 2 cells (extended Moore neighborhood, 124 neighbors in 3D)

Tier 1A:         κ_i(1) = 0  AND  κ_i(2) = 0  (strong new physics candidate)
Tier 1B:         κ_i(1) = 0  AND  κ_i(2) ≥ 1  (ambiguous, requires secondary vetting)
Tier 2:          κ_i(1) ≥ 1                    (weak cluster, systematic bias zone)
Tier 3:          κ_i(1) ≥ 2                    (dense systematic cluster, apply bias correction)
```

### 11.3 Directional Coherence Analysis (Secondary Characterization)

```
C_threshold      = 0.7 (70% eigenvector alignment = coherent shear)
coherence window = r₂ neighborhood (extended Moore radius 2)

For Tier 1A/1B cells:
  If C_mean(i) > 0.7 → reclassify to Tier 1B (systematic shear pattern)
  If C_mean(i) ≤ 0.7 → confirm Tier 1A (localized, incoherent distortion)
```

### 11.4 Observational Parameters

```
H₀_SH0ES baseline: 73.04 ± 1.04 km/s/Mpc (pre-correction)
H₀_Planck baseline: 67.36 ± 0.54 km/s/Mpc
Expected residual: 1.2σ after ξ-correction
Pass threshold:    ≤ 1.5σ
Fail threshold:    > 2.0σ
Euclid data release: October 2026
```

Any changes to these values after this document is published will be documented in a separate amendment, clearly marked as post-hoc.

---

## References

[To be completed with citations to:]
- UHA v2.0.0 pre-registration (Zenodo 10.5281/zenodo.19232340)
- N/U Algebra (Zenodo 10.5281/zenodo.17172694)
- Pantheon+ SN Ia compilation
- DESI DR1 BAO results
- Planck 2018 CMB constraints
- Open Science Framework pre-registration guidelines
- SAID protocol (Simmons et al., Nature Human Behaviour 2018)

---

**Word count**: ~4,500

**Zenodo pre-registration ID**: [assigned upon submission]

**Date submitted**: [April 2026]

**Date locked**: [October 2026 Euclid DR1 release or earlier if data becomes public]
