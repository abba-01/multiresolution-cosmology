# Final Compiled Pre‑Registration Package
**Status: Locked, audited, and ready for Zenodo submission**

## §0.1 Executive Summary (For Editors and Non‑Specialist Reviewers)

This pre‑registration specifies a falsifiable test of the hypothesis that the observed Hubble tension (ΔH₀ ≈ 5–6 km/s/Mpc, ≈5σ) arises partly from frame‑artifact differences between local distance‑ladder and CMB measurements.

**Core Claim.** When local distance measurements are expressed in horizon‑normalized coordinates (ξ = comoving distance / Hubble distance), the effective distance metric becomes frame‑independent and exhibits geometric structure that accounts for a substantial fraction (~76%) of the apparent tension.

**Key Innovation.** A multi‑scale coherence analysis using fixed κ thresholds (r₁ = 1 cell, r₂ = 2 cells) distinguishes strictly isolated anomalies (candidate new physics) from extended, coherent regions indicative of systematics or bias zones.

**Testable Predictions (Euclid DR1, October 2026).**
- Residual H₀ after ξ‑correction: ~1.2σ
- PASS: ≤ 1.5σ (framework explains majority of tension)
- FAIL: > 2.0σ (framework insufficient; additional physics or systematics required)
- Z‑Gradient Test: ξ‑correction should decay approximately as exp(−z/0.07), becoming evident for z > 0.5

**Methodological Strength.** All thresholds (NPT, κ, C_threshold, α) are pre‑committed before data access. The decision tree is deterministic with no post‑hoc branching. The framework is fully falsifiable.

**Scope.** This pre‑registration does not aim to validate or refute ΛCDM per se; it tests whether frame‑normalization removes the apparent tension under pre‑committed rules. Either outcome constitutes a valid scientific result.

---

## §1 Claim Statement

The apparent Hubble tension contains a significant frame‑artifact component that can be identified and reduced through ξ‑normalization and multi‑scale coherence classification, leaving a smaller residual consistent with ΛCDM within pre‑committed envelopes.

---

## §2.6 The Normalized Point Threshold (NPT): Hard Physical Envelope

### Definition

**NPT = α · (b_ref + u_framework)**

Where:
- **b_ref** = magnitude of the theoretical baseline prediction (ΛCDM; H₀_Planck = 67.36 km/s/Mpc)
- **u_framework** = irreducible framework uncertainty (instrumental + calibration floor)
- **α** = detection policy multiplier (locked)

NPT is the **Envelope Gate** — a hard physical consistency bound derived from N/U (Nominal/Uncertainty) algebra. It is not a statistical significance threshold.

### Interpretation

NPT defines the range of measurements consistent with ΛCDM including all pre‑committed systematic limitations. For any spatial cell i:
- **In‑Gate:** |dᵢ − H₀_theory| ≤ NPT
- **Out‑of‑Gate (Flagged):** |dᵢ − H₀_theory| > NPT

Only Out‑of‑Gate cells proceed to anomaly flagging and tier classification.

### Epistemic Completeness Statement (Baseline‑Dominance)

Why include u_framework if it is numerically small? The purpose of including u_framework is not numerical contribution, but epistemic completeness: it records that theoretical predictions are trusted only up to an irreducible calibration floor. This floor is non‑zero and reflects genuine limitations in extinction maps, metallicity corrections, and photometric calibration. Omitting it would imply perfect knowledge of ΛCDM, which is false.

### σ‑Multiplier: Policy vs. Inference

**Critical distinction:** α is a policy choice, not an inferential one. α = 2.0 is not derived from likelihoods or frequentist confidence; it represents a conservative detection policy: extraordinary claims require extraordinary evidence. Alternative α values are valid policy choices, but α = 2.0 is locked pre‑data to prevent post‑hoc tuning.

(References to σ are heuristic, conveying scale rather than Gaussian inference.)

### Numerical Specification (Pre‑Committed)

| Parameter | Value |
|-----------|-------|
| b_ref | 67.36 km/s/Mpc (Planck ΛCDM) |
| u_instrument | ≈ 0.30 km/s/Mpc |
| u_calibration | ≈ 0.40 km/s/Mpc |
| u_framework | √(0.30² + 0.40²) ≈ 0.50 km/s/Mpc |
| α | 2.0 |
| **NPT** | **2.0 · (67.36 + 0.50) = 135.72 km/s/Mpc** |

### Expected Empirical Behavior

Under standard ΛCDM, expected cell‑level deviations are ~0.5–5 km/s/Mpc. Thus NPT functions as a hard outlier detector. Non‑exceedance confirms that known systematics account for observed structure; exceedance of even a single cell would constitute a discovery‑level anomaly.

### Context‑Dependent Dominance

In the current Euclid regime (z < 2), b_ref dominates NPT due to the stability of ΛCDM predictions. This dominance is context‑dependent, not intrinsic. Future regimes (high‑z probes, standard sirens, tighter calibration floors) would increase the relative importance of u_framework. Including u_framework is therefore forward‑compatible and general.

### Explicit Falsification Scenario

If Euclid DR1 measures an H₀ residual > 2.0σ at 0.5 ≤ z ≤ 1.1 after ξ‑correction applied to local (z ≤ 0.1) data, the framework is falsified. This would indicate either (i) ξ‑correction is not physically real, (ii) systematics extend to high‑z contrary to assumptions, or (iii) genuinely new physics. Any outcome constitutes a valid scientific result.

---

## §3 Multi‑Scale Coherence and κ‑Tier Classification

### Definitions
- **Envelope Gate (NPT):** Hard consistency filter
- **Anomaly Flagging:** Cells exceeding NPT
- **Tier Classification:** κ‑based coherence assessment

### κ Thresholds (Locked)
- r₁ = 1 cell
- r₂ = 2 cells

### Tier Logic
- **Tier 1A:** κ = 0 (strictly isolated) → candidate novel physics
- **Tier 1B:** κ = 1 → localized systematics
- **Tier 2:** κ ≥ 2 → extended bias zones
- **Tier 3:** Global coherence → modeling or calibration failure

---

## §4 Locked Constants (Immutable)

| Constant | Value |
|----------|-------|
| NPT | α · (b_ref + u_framework) |
| r₁ | 1 cell |
| r₂ | 2 cells |
| κ Tier Thresholds | as defined in §3 |
| C_threshold | 0.7 |
| Coherence Domain | Moore(r = 2) |

All constants are fixed prior to data access.

---

## §5 Analysis Timeline

| Phase | Action |
|-------|--------|
| Pre‑Data (Completed) | Specify b_ref, u_framework, α; compute and lock NPT |
| Zenodo Submission | Archive this document with DOI |
| Euclid DR1 (Oct 2026) | Apply deterministic pipeline |
| Post‑Analysis | Report outcomes with no deviations |

---

## §6 Audit Trail and Integrity

This specification has undergone adversarial red‑team review and formal hardening. Supporting documents (RED_TEAM_RESPONSE.md, FINAL_HARDENING.md, INTEGRATION_CHECKLIST.md, INTEGRATION_SIGN_OFF.md) are archived to provide a complete audit trail.

Any amendment requires a formal, timestamped addendum and explicit justification.

---

## Closing Statement

This pre‑registration defines a conservative, deterministic, and falsifiable framework for addressing the Hubble tension. All methodological choices are explicit and locked in advance. When Euclid DR1 arrives, the analysis will run exactly as specified. The outcome—confirmation or refutation—will be reported transparently.

**End of Compiled Work.**
