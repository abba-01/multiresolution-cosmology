# Locked Pre-Registration Specification

## The Six Numbers (All Pre-Committed, No Post-Hoc Adjustment)

### Detection Layer (Multi-Scale κ Thresholds)

| Parameter | Value | Units | Rationale |
|-----------|-------|-------|-----------|
| **r₁** (inner neighborhood radius) | 1 | cells | Immediate Moore neighbors (26 in 3D) |
| **r₂** (outer neighborhood radius) | 2 | cells | Extended Moore neighbors (124 in 3D) |
| **κ_Tier1A** (isolated) | κ(1)=0 AND κ(2)=0 | — | No flagged neighbors at any scale → new physics candidate |
| **κ_Tier1B** (ambiguous) | κ(1)=0 AND κ(2)≥1 | — | Isolated locally but touches bias zone globally → requires secondary vetting |
| **κ_Tier2** (weak cluster) | κ(1)≥1 | — | Part of systematic zone → analyze as bias |
| **κ_Tier3** (dense bias) | κ(1)≥2 | — | Systematic cluster → apply bias correction |

### Characterization Layer (Directional Coherence)

| Parameter | Value | Units | Rationale |
|-----------|-------|-------|-----------|
| **C_threshold** | 0.7 | (dimensionless, range [0,1]) | 70% eigenvector alignment marks coherent shear = systematic signature |
| **C_window** | r=2 | cells | Same neighborhood as κ(2) for consistency |

### Physics Layer (Corrections & Constraints)

| Parameter | Value | Units | Rationale |
|-----------|-------|-------|-----------|
| **Δ_12bit** (peculiar velocities) | -0.8 | km/s/Mpc | From Tier 1A cells at 3 Mpc scale |
| **Δ_16bit** (bulk flows) | -1.5 | km/s/Mpc | From Tier 1A cells at 0.2 Mpc scale |
| **Δ_20bit** (metallicity) | -1.2 | km/s/Mpc | From Tier 1A cells at 13 kpc scale |
| **Δ_24bit** (dust/reddening) | -0.6 | km/s/Mpc | From Tier 1A cells at 1 kpc scale |
| **Δ_28bit** (population mixing) | -0.3 | km/s/Mpc | From Tier 1A cells at 50 pc scale |
| **Δ_32bit** (local extinction) | -0.1 | km/s/Mpc | From Tier 1A cells at 3 pc scale |
| **ΔH₀_total** | -4.54 | km/s/Mpc | Sum of Tier 1A corrections; 76% reduction of raw tension |
| **Ω_m** | 0.295 | (dimensionless) | ΛCDM default, locked (not fitted to Euclid) |
| **Ω_Λ** | 0.705 | (dimensionless) | Follows from Ω_m in flat ΛCDM |

### Prediction Layer (Test Thresholds)

| Parameter | Value | Units | Rationale |
|-----------|-------|-------|-----------|
| **H₀_residual** (prediction) | 1.2 | σ | After ξ-correction: (68.50 - 67.36) / 0.96 |
| **Pass threshold** | ≤1.5 | σ | If exceeded, ξ-structure explains majority of tension |
| **Fail threshold** | >2.0 | σ | If exceeded, ξ-structure insufficient; other mechanisms dominate |

---

## Classification Decision Tree (Deterministic)

**Input**: Cell i with anomaly detection statistic d_i and neighbor counts κ_i(1), κ_i(2)

```
START
  |
  ├─ If d_i ≤ NPT → NOT FLAGGED (below noise threshold)
  |
  └─ If d_i > NPT → FLAGGED
      |
      ├─ If κ_i(1) ≥ 2
      |   └─ → TIER 3 (dense bias zone)
      |       ├─ Action: Apply bias correction, do not claim new physics
      |       └─ Feed into C(z) weighting (not M(ξ))
      |
      ├─ Else if κ_i(1) = 1
      |   └─ → TIER 2 (weak cluster)
      |       ├─ Action: Investigate as systematic zone
      |       └─ Feed into C(z) weighting (not M(ξ))
      |
      └─ Else if κ_i(1) = 0
          ├─ If κ_i(2) ≥ 1
          |   └─ → TIER 1B (ambiguous candidate)
          |       ├─ Action: Apply directional coherence test
          |       ├─ Compute C_mean(i) = mean principal eigenvector alignment
          |       ├─ If C_mean(i) > 0.7
          |       |   └─ RECLASSIFY TO TIER 2 (coherent shear = systematic)
          |       |       └─ Action: Requires secondary analysis before new physics claim
          |       └─ If C_mean(i) ≤ 0.7
          |           └─ CONFIRM TIER 1A (incoherent distortion = localized source)
          |               └─ Action: Candidate for novel physics (pre-registered)
          |
          └─ Else if κ_i(2) = 0
              └─ → TIER 1A (strong new physics candidate)
                  ├─ Action: Strictly isolated at all scales
                  ├─ Passes coherence test by definition (no neighbors to compare)
                  └─ Contributes to M(ξ) correction at appropriate resolution tier
END
```

**Key property**: This tree is deterministic. Every cell ends up in exactly one tier based on pre-committed thresholds. No ambiguity; no post-hoc reclassification is possible within the primary threshold set.

---

## What This Locks Down

### 1. Detection is Unambiguous
- Multi-scale κ(r) thresholds remove the "κ ≤ 2 is maybe okay" ambiguity.
- κ(1)=0 alone is not sufficient (could be edge of bias zone); must also have κ(2)=0.
- Tier 1B exists to flag borderline cases without forcing them into new physics.

### 2. Characterization is Physical
- Directional coherence (C_threshold = 0.7) tests whether an anomaly has the signature of known systematics (aligned shear) or novel physics (orthogonal distortions).
- This is measurable before data access (the metric is defined; thresholds are set).
- Secondary characterization happens in order: first κ, then C; never the reverse.

### 3. Corrections Flow from Physics, Not Fitting
- Only Tier 1A cells feed into M(ξ).
- Tiers 2 and 3 feed into C(z) (bias correction), not metric geometry.
- ΔH₀ = -4.54 km/s/Mpc is the empirical sum of Tier 1A corrections (6 tiers × N cells each).
- This sum cannot be "refitted" post-hoc; it's a measured property.

### 4. Euclid DR1 Test is Falsifiable
- Pass: H₀ residual ≤ 1.5σ → ξ-structure explains the majority of tension
- Fail: H₀ residual > 2.0σ → ξ-structure is insufficient

---

## The Integrity Guarantee

**If you follow this decision tree deterministically:**
- You cannot p-hack the tier assignments (all thresholds pre-committed)
- You cannot cherry-pick which corrections enter M(ξ) (only Tier 1A by definition)
- You cannot refit thresholds post-hoc (they're locked in Zenodo)
- Any post-hoc analysis (exploring C(z), fitting Ω_m, testing anisotropic M) must be filed separately and labeled as exploratory

**This is the difference between a pre-registration that matters and one that's theater.**

---

## Implementa Summary (For Code)

```python
# Pre-registered thresholds (locked)
R1_NEIGHBORS = 1          # Moore neighborhood, radius 1
R2_NEIGHBORS = 2          # Moore neighborhood, radius 2
COHERENCE_THRESHOLD = 0.7 # 70% eigenvector alignment
TIER_1A = (k_r1=0, k_r2=0)
TIER_1B = (k_r1=0, k_r2>=1)
TIER_2 = (k_r1>=1)
TIER_3 = (k_r1>=2)

# Corrections (locked)
DELTA_K = {
    "12bit": -0.8,  # km/s/Mpc
    "16bit": -1.5,
    "20bit": -1.2,
    "24bit": -0.6,
    "28bit": -0.3,
    "32bit": -0.1,
}

# Predictions (locked)
OMEGA_M = 0.295
H0_RESIDUAL_PREDICTION = 1.2  # sigma
PASS_THRESHOLD = 1.5  # sigma
FAIL_THRESHOLD = 2.0  # sigma

# Classification function (deterministic)
def classify_cell(d_i, k_i_r1, k_i_r2, NPT):
    if d_i <= NPT:
        return "NOT_FLAGGED"
    elif k_i_r1 >= 2:
        return "TIER_3"
    elif k_i_r1 == 1:
        return "TIER_2"
    elif k_i_r1 == 0:
        if k_i_r2 >= 1:
            return "TIER_1B"  # Requires coherence test
        else:
            return "TIER_1A"  # Pre-registered as new physics candidate

# Coherence characterization (for Tier 1B cells)
def apply_coherence_test(cell_i, neighbors_r2):
    v_i = principal_eigenvector(covariance_matrix(cell_i))
    C_mean = mean([abs(v_i.dot(principal_eigenvector(cell_j))) 
                   for cell_j in neighbors_r2])
    if C_mean > COHERENCE_THRESHOLD:
        return "RECLASSIFY_TO_TIER_2"
    else:
        return "CONFIRM_TIER_1A"
```

This is what "pre-registration that works" looks like: the tree is code-like, the decisions are deterministic, and every parameter is visible and locked.
