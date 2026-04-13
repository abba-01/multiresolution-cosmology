# Epistemic Convergence Requires Resolution Refinement

**Eric D. Martin**
ORCID: 0009-0006-5944-1742
Independent Researcher
April 2026

---

## Abstract

Disagreement among high-confidence scientific inferences is often interpreted as evidence of noise, bias, or physical inconsistency. We show that such disagreement can instead arise from epistemic collapse induced by representational resolution, and that genuine convergence imposes a necessary constraint on how disagreement behaves under resolution refinement. Using a minimal deterministic construction, we first demonstrate that inference performed at a single effective resolution may be asymptotically correct while remaining epistemically incomplete when the underlying system exhibits multiscale structure; disagreement between locally valid inferences then persists in the infinite-data limit and cannot be eliminated by increased precision or improved sampling. We formalize this as Proposition 1 (Representational Insufficiency Under Fixed Resolution). We then derive Theorem 1 (ΔT Monotonicity Criterion): if inference converges toward a complete representation of a multiscale system, the epistemic distance ΔT(ℓ) must decrease monotonically under increasing resolution. Non-monotonic, constant, or increasing ΔT under resolution refinement constitutes evidence of unresolved structure. Any claim of convergence based solely on fixed-resolution stabilization is therefore epistemically underdetermined. The contribution is diagnostic and domain-independent; an operational instantiation in a multiresolution cosmological framework is provided as illustration.

---

## 1. Introduction

Disagreement among high-precision scientific measurements is often interpreted as evidence of insufficient data, experimental bias, or failure of existing theoretical models. These interpretations implicitly assume that the inferential framework itself preserves all distinctions required to adjudicate competing descriptions of the data.

This paper examines a distinct possibility: that apparent disagreement may arise not from error or missing physics, but from epistemic collapse caused by representational choices. In particular, we analyze inference performed at a single effective resolution and show that such inference can be asymptotically correct while remaining epistemically incomplete when the underlying system exhibits structure across multiple characteristic scales.

Single-resolution inference is ubiquitous. Global regressions, pooled likelihoods, and aggregated estimators are central tools across scientific disciplines. Their use presupposes that projection onto a single representational scale yields a sufficient statistic for the system under investigation. The central question addressed here is whether that assumption holds in general.

We show that it does not. Using a deterministic, noise-free construction, we demonstrate that multiscale structure can produce structural disagreement that persists in the limit of infinite data, despite convergence of global estimators. This disagreement is not statistical in origin and cannot be eliminated by increased precision, additional data, or conventional model-selection criteria. Instead, it reflects irreversible information loss induced at the level of representation.

This result is formalized as Proposition 1 (Representational Insufficiency Under Fixed Resolution). The proposition does not prescribe alternative inference procedures, nor does it privilege any resolution as epistemically superior. Its role is diagnostic: it constrains what conclusions can and cannot be drawn from inference under representational collapse.

The proposition, however, leaves open a second question: what does genuine convergence require? If fixed-resolution stabilization is insufficient as a convergence criterion, a necessary condition must be identified. This paper derives that condition as Theorem 1 (ΔT Monotonicity Criterion): epistemic distance ΔT(ℓ) must decrease monotonically under increasing resolution if an inference converges toward a complete representation of the system. Persistence, increase, or non-monotonic behavior of ΔT under resolution refinement is diagnostic of unresolved structure.

The paper is organized as follows. Section 2 introduces resolution as an epistemic operator, defines epistemic collapse, and defines epistemic distance. Section 3 constructs a minimal multiscale system in which global inference converges while local inferences remain irreconcilable. Section 4 interprets this behavior as structural epistemic disagreement. Section 5 states Proposition 1 and closes with the exclusion it entails. Section 6 derives Theorem 1 (ΔT Monotonicity Criterion). Section 7 illustrates the criterion operationally. Section 8 situates the results relative to prior work. Section 9 discusses scope and limitations.

---

## 2. Definitions and Preliminaries

### 2.1 Resolution as an Epistemic Operator

Let
$$\mathcal{D} = \{(x_i, y_i)\}_{i=1}^{N}$$
denote a dataset generated by a system containing structure across multiple characteristic scales.

We define a **resolution operator** $R_\ell$ as an epistemic mapping
$$R_\ell : \mathcal{D} \to \tilde{\mathcal{D}}$$
that retains only distinctions expressible at an effective scale $\ell$, discarding structure below that scale.

To ground this formally: binning data into intervals of width $\ell$ instantiates $R_\ell$ as a step-function projection; band-limiting to frequencies below $1/\ell$ instantiates it as a low-pass filter; truncating a Z-order (Morton) encoding at depth $\ell$ instantiates it as a spatial coarsening to cells of linear size $2^{-\ell}$. In each case, $R_\ell$ is an information-reducing map whose image is a strict subset of the original representational space when the underlying system contains sub-$\ell$ structure.

Resolution is distinct from numerical precision, sampling density, or noise level. Increasing measurement precision while holding $\ell$ fixed does not restore information removed by $R_\ell$. Resolution therefore governs which distinctions are representable, independent of statistical uncertainty.

**Notation convention.** Throughout this paper, $N$ denotes the number of observations (sample size), while $\ell$ indexes representational resolution. These are independent parameters: increasing $N$ refines statistical estimates at fixed resolution; increasing $\ell$ admits previously suppressed structure regardless of $N$.

### 2.2 Single-Resolution Inference

Inference is said to be performed at a **single effective resolution** when all data are processed through a fixed resolution operator $R_\ell$, yielding a global estimator $\hat{f}_\ell$ defined over the full observation domain.

Single-resolution inference is standard practice, motivated by tractability and interpretability. Its implicit assumption is that $\hat{f}_\ell$ constitutes a sufficient statistic for the underlying system dynamics.

### 2.3 Epistemic Collapse

**Definition 2.1 (Epistemic Collapse).**
Epistemic collapse occurs when a resolution operator $R_\ell$ eliminates distinctions required to reconcile locally valid but globally incompatible descriptions of a system.

Under epistemic collapse:

- distinct inferential states are projected into a single representation,
- disagreement cannot be recovered from the aggregated representation,
- additional data do not restore the lost distinctions.

Epistemic collapse is therefore a structural loss of representational capacity, not a failure of estimation.

### 2.4 Epistemic Distance

**Definition 2.2 (Epistemic Distance).**
Let $\mathcal{I}^{(i)}(\ell)$ and $\mathcal{I}^{(j)}(\ell)$ denote inferential representations derived from the same dataset $\mathcal{D}$ under resolution $\ell$ but from distinct observational frames, scale regimes, or methodological choices. The **epistemic distance** at resolution $\ell$ is a non-negative functional
$$\Delta T(\ell) = \left\| \mathcal{I}^{(i)}(\ell) - \mathcal{I}^{(j)}(\ell) \right\|$$
measuring irreducible disagreement between the two representations after all frame artifacts, calibration offsets, and statistical uncertainties have been propagated.

Three properties are required of any admissible instantiation of $\Delta T$:

1. **Non-negativity:** $\Delta T(\ell) \geq 0$, with $\Delta T = 0$ only if the representations are epistemically indistinguishable at resolution $\ell$.
2. **Resolution-dependence:** $\Delta T(\ell)$ must be computable at each $\ell$ independently; it is not a global fit statistic.
3. **Propagated uncertainty:** the denominator must incorporate all known systematic and statistical uncertainty, so that $\Delta T$ measures signal relative to total epistemic spread, not raw disagreement.

**Operational form.**
In the multiresolution framework developed in the companion empirical work \citep{Martin2026_UHA, Martin2025_MultiProbe}, resolution is indexed by Morton encoding depth $k$ (bit-depth), and $\Delta T$ takes the form
$$\Delta T(k_i, k_j) = \frac{\left| C(k_i) - C(k_j) \right|}{\sigma_{\text{eff}}},$$
where $C(k)$ is the cumulative systematic correction at depth $k$ and $\sigma_{\text{eff}}$ is the total propagated uncertainty including epistemic penalty terms. We denote sample size by $N$ and Morton encoding depth (resolution) by $k$ throughout to avoid ambiguity.

**Convergence threshold.**
Empirical evaluation across multiple probe combinations \citep{Martin2025_MultiProbe} yields a calibrated threshold: $\Delta T < 0.15$ is consistent with convergent behavior across the tested systems. This value is an empirical calibration, not a derivation from the $\Delta T$ functional form; it should be treated as a benchmark for the class of systems studied and not extrapolated without independent validation.

---

## 3. Toy-Universe Construction: A Minimal Multiscale System

### 3.1 Generative Model

Let the observable $y(x)$ be defined on $x \in [0, L]$ by
$$y(x) = g(x) + S(x),$$
where
$$g(x) = a x, \quad S(x) = A \sin(\omega x),$$
with constant $a$, finite $A$, and $\omega \gg 1$.

The system contains:

- a smooth global component,
- structured local variation at scale $2\pi/\omega$.

The derivative is
$$\frac{dy}{dx} = a + A\omega \cos(\omega x),$$
spanning $[a - A\omega,\; a + A\omega]$.

### 3.2 Global Inference

Performing a global least-squares regression,
$$\hat{a} = \frac{\int_0^L x\, y(x)\, dx}{\int_0^L x^2\, dx},$$
yields
$$\lim_{L \to \infty} \hat{a} = a,$$
since the sinusoidal term integrates to zero. The global estimator is unbiased, consistent, and asymptotically exact, with shrinking confidence intervals as the sample size $N$ increases.

### 3.3 Local Inference

Partition the domain into local windows
$$\Omega_i = [x_i,\; x_i + \Delta], \quad \Delta \ll 2\pi/\omega.$$

Local slope estimates satisfy
$$\hat{a}_i \approx a + A\omega \cos(\omega x_i),$$
spanning the full interval $[a - A\omega,\; a + A\omega]$.

### 3.4 Persistence of Local Variability

The variance of local slope estimates is
$$\mathrm{Var}(\hat{a}_i) = \frac{(A\omega)^2}{2},$$
which remains finite as the sample size $N \to \infty$. Thus:

- global inference converges,
- local inferences diverge systematically,
- disagreement persists without noise.

---

## 4. Resolution-Induced Epistemic Disagreement

### 4.1 Structural Versus Statistical Disagreement

The toy-universe construction in Section 3 demonstrates a system in which global inference converges asymptotically while local inferences remain persistently dispersed. This dispersion does not diminish with increasing sample size; it is therefore not attributable to statistical noise, estimator variance, or finite-sampling effects.

We distinguish two qualitatively different sources of inferential disagreement:

- **Statistical disagreement**, arising from stochastic noise or insufficient data, which vanishes as data increase.
- **Structural disagreement**, arising from irrecoverable information loss induced by representational constraints.

The system constructed in Section 3 lies strictly in the second category. The disagreement among local slope estimates persists in the infinite-data limit even though the global estimator is exact. Epistemic disagreement can therefore arise from the structure of the inference pipeline itself, rather than from imperfections in the data or model.

### 4.2 Observer Dependence Under Fixed Resolution

Consider two observers analyzing the same underlying dataset $\mathcal{D}$, but operating under different effective resolutions. One observer performs inference globally, applying a single resolution operator $R_\ell$ over the full domain. Another restricts attention to a local subdomain $\Omega_i \subset \Omega$, effectively operating at a finer resolution.

Both observers use valid inference procedures. Both obtain results that are locally self-consistent and statistically well-defined. Yet the laws inferred are incompatible: one infers a unique global gradient, while the other infers a family of locally varying gradients. This incompatibility is not resolved by additional data. It reflects the fact that $R_\ell$ destroys the distinctions required to reconcile the two descriptions.

### 4.3 Generalization of Simpson's Paradox

This phenomenon is a continuous generalization of Simpson's paradox. In the classical discrete case, aggregation over a confounding variable can reverse or conceal relationships present within subsets of the data. Resolution-induced collapse plays an analogous role in continuous settings without categorical conditioning.

Instead of aggregation over categories, collapse arises from aggregation over scale. The effect is the same: inference performed after aggregation can yield conclusions incompatible with those obtained when structure is resolved. Simpson-type reversals are therefore not anomalies confined to categorical data analysis but manifestations of a broader epistemic principle: aggregation across hidden structure can invalidate otherwise sound inference.

### 4.4 Persistence in the Infinite-Data Limit

A key implication is that epistemic disagreement need not diminish with improved data quality. In the toy-universe example, both global and local estimators converge almost surely as observations increase, yet they converge to different objects. This persistent divergence falsifies the assumption that increasing data alone suffices to reconcile conflicting inferences.

Formally, the disagreement signal — measured by the variance of local parameter estimates — remains finite and resolution-dependent as $N \to \infty$. The limit of infinite data does not restore epistemic completeness.

### 4.5 From Demonstration to General Result

The results of Sections 3 and 4 motivate a general inference principle: when a system exhibits structure across multiple characteristic scales, projection onto a single effective resolution does not guarantee preservation of the information required to characterize its dynamics fully. We now show that the phenomena illustrated above are not artifacts of the toy construction, but consequences of a general limitation on single-resolution inference.

---

## 5. Proposition: Representational Insufficiency Under Fixed Resolution

**Proposition 1 (Representational Insufficiency Under Fixed Resolution).**
Let $y(x)$ be generated by a system with multiscale structure. Let inference be performed via projection through a single resolution operator $R_\ell$, yielding a global estimator $\hat{f}_\ell$. Then $\hat{f}_\ell$ is not, in general, a sufficient statistic for the system dynamics.

There exist systems for which:

1. $\hat{f}_\ell$ converges as $N \to \infty$;
2. local inferences remain mutually incompatible for all $N$;
3. the incompatibility arises from epistemic collapse induced by $R_\ell$.

**Proof (Sketch).**
Consider inference performed via minimization of a global loss functional
$$\hat{g} = \arg\min_{g_\theta} \int_\Omega \left[y(x) - g_\theta(x)\right]^2 dx,$$
where $g_\theta$ is restricted to a low-complexity function class and $\Omega$ is the full observation domain. Because $\int_\Omega S(x)\,dx = 0$ by construction, the aggregate estimator converges to the true global component $g(x)$ as data increase. However, projection onto the aggregate loss removes all information carried by the structured variation $S(x)$. When inference is performed on local subdomains $\Omega_i \subset \Omega$, the contribution of $S(x)$ no longer averages to zero, and local estimators recover systematically different effective dynamics. The variance among $\{\hat{a}_i\}$ does not decrease with additional global data, since the lost information is structural rather than stochastic. Hence $\hat{f}_\ell$ is asymptotically correct yet epistemically incomplete. ∎

**Corollary 1 (Persistence of Disagreement).**
Epistemic disagreement may persist in the infinite-data limit and does not imply failure of estimation or data quality.

The Corollary establishes that disagreement persisting in the infinite-data limit is not, by itself, evidence of estimation failure. The converse interpretive error is equally consequential: **any claim of convergence based solely on fixed-resolution stabilization is epistemically underdetermined.** Stabilization of $\hat{f}_\ell$ as $N \to \infty$ establishes only that the projection of the system onto scale $\ell$ has been recovered; it does not establish that the projection is complete. A necessary condition for completeness is the subject of the following section.

---

## 6. Theorem: The ΔT Monotonicity Criterion

### 6.1 Proposition: Resolution-Dependent Convergence

**Proposition 2 (Resolution-Dependent Convergence).**
Let $\mathcal{D}$ be a dataset generated by a system containing structure across multiple characteristic scales. Let inference be performed under a fixed representational resolution $\ell$, producing an inferred model $\mathcal{I}(\ell)$. Let $\Delta T(\ell)$ be the epistemic distance at resolution $\ell$ (Definition 2.2).

Then convergence of $\mathcal{I}(\ell)$ under iterative refinement at fixed resolution $\ell$ does not imply epistemic completeness. In particular, there exist multiscale systems for which:

(a) $\mathcal{I}(\ell)$ stabilizes under iterative refinement at fixed $\ell$;

(b) $\Delta T(\ell) > 0$ remains invariant under additional refinement;

(c) the apparent convergence arises from representational saturation, not resolution of suppressed structure.

### 6.2 Theorem 1: Tolerance-Aware ΔT Monotonicity Criterion

**Theorem 1 (Tolerance-Aware ΔT Monotonicity Criterion).**
Let $\ell$ index representational resolution, ordered so that increasing $\ell$ corresponds to explicit admission of previously suppressed structure. Let $\Delta T(\ell)$ be an epistemic distance measured at resolution $\ell$, and let $U(\ell)$ denote the associated uncertainty or tolerance bound arising from finite sampling, numerical effects, or stochastic estimation.

**Definition ($\Delta T$ Uncertainty Band).** $U(\ell)$ denotes the smallest bound such that repeated estimation of $\Delta T(\ell)$ under fixed resolution yields values in $[\Delta T(\ell) - U(\ell),\, \Delta T(\ell) + U(\ell)]$. No probability distribution is assumed; $U(\ell)$ measures admissible epistemic variation at resolution $\ell$.

If epistemic convergence toward a more complete representation occurs, then for any $\ell_2 > \ell_1$:
$$\Delta T(\ell_2) \;\leq\; \Delta T(\ell_1) + U(\ell_1).$$

Conversely, if for some $\ell_2 > \ell_1$:
$$\Delta T(\ell_2) \;>\; \Delta T(\ell_1) + U(\ell_1),$$
then unresolved structure remains present at scales not yet represented, and convergence claims at resolution $\ell_1$ are epistemically incomplete.

Monotonic decrease of $\Delta T$ within tolerance is therefore a **necessary**, but not sufficient, condition for epistemic convergence.

The monotonicity condition is not stated pointwise. Finite data, numerical noise, and estimator variability permit fluctuations in $\Delta T(\ell)$ at the level of $U(\ell)$. The criterion concerns systematic violations — increases in epistemic distance exceeding the uncertainty bound — rather than small-scale stochastic variation.

### 6.3 Proof

Let the system decompose into scale-indexed components:
$$S = \sum_{k} S_k,$$
where each $S_k$ contains structure localized at scale $k$. A representation at resolution $\ell$ suppresses all $k < \ell$:
$$\tilde{S}(\ell) = \sum_{k \geq \ell} S_k.$$

Epistemic distance measures unresolved disagreement attributable to omitted components:
$$\Delta T(\ell) \sim \sum_{k < \ell} \|S_k\|.$$

Under refinement $\ell \to \ell' > \ell$, newly admitted components $S_k$ become explicitly modeled, reducing previously latent discrepancies. Therefore:
$$\Delta T(\ell') \leq \Delta T(\ell).$$

If monotonicity fails, one of the following holds:

| ΔT Behavior | Interpretation |
|---|---|
| Decreases monotonically → 0 | Systematic origin (frame artifact or scale suppression) |
| Plateaus | Incomplete modeling; hidden structure at unresolved scale |
| Increases or non-monotonic | Physical residual; candidate new physics |

In neither non-monotonic case can fixed-resolution convergence be interpreted as epistemic completeness. ∎

**Interpretive note.**
$\Delta T$ is not a goodness-of-fit statistic. It quantifies the persistence of unresolved epistemic separation under representational refinement. A system whose $\Delta T$ decreases monotonically to zero has been epistemically exhausted by the resolution ladder; one whose $\Delta T$ plateaus or grows has not.

### 6.4 Counterexample: Truncated Multiscale System

Theorem 1 establishes monotonic decrease as a *necessary* condition for epistemic convergence. The following counterexample demonstrates that it is not *sufficient*.

Let the true structure be
$$S(x) = S_1(x) + S_2(x),$$
where $S_1$ contains structure at scale $k = 1$ and $S_2$ contains structure at scale $k = 10$.

As resolution increases from $\ell = 1$ to $\ell = 2$ to $\ell = 3$, component $S_1$ is admitted and $\Delta T(\ell)$ decreases within tolerance — the criterion is satisfied. Yet for all $\ell < 10$, component $S_2$ remains suppressed and $\Delta T(\ell)$ plateaus at a non-zero value:
$$\Delta T(1) > \Delta T(2) \geq \Delta T(3) \geq \cdots \geq \Delta T(9) > 0,$$
with each step satisfying $\Delta T(\ell+1) \leq \Delta T(\ell) + U(\ell)$.

Tolerance-aware monotonicity holds across $\ell \in [1, 9]$. The inference appears to be converging. But $S_2$ is entirely unresolved throughout this range. Only at $\ell \geq 10$ does $\Delta T(\ell)$ resume decreasing toward zero.

**Conclusion.** Monotonic decrease within tolerance alone does not imply epistemic completeness; it indicates only that the resolution ladder has resolved *some* structure. Completeness requires $\Delta T(\ell) \to 0$ as $\ell \to \infty$, not merely a decreasing trend over a finite resolution range.

---

## 7. Operational Consequences

The ΔT criterion is computable. We illustrate its behavior on two cases drawn from multiresolution cosmological inference \citep{Martin2026_UHA, Martin2025_MultiProbe}, where resolution is indexed by Morton encoding depth $k$ and epistemic distance is defined as in §2.4.

**Case 1: $H_0$ tension.**
Treating the tension between Cepheid-calibrated distance ladder measurements \citep{Riess2022} and CMB-inferred values \citep{Planck2020} as a candidate multiscale disagreement, resolution refinement via increasing $k$ produces
$$\Delta T \to 0.007 \ll 0.15.$$
The monotonicity criterion is satisfied. The inference is consistent with a systematic origin — specifically, scale-dependent calibration artifacts suppressed at coarse resolution — rather than a genuine physical residual. This does not resolve the tension; it classifies it as epistemically tractable under resolution refinement.

**Case 2: Early dark energy (EDE) candidate.**
Applying the same framework to the EDE parameter region yields
$$\Delta T \approx 2.4 \gg 0.15.$$
Monotonicity fails. Disagreement increases under resolution refinement, indicating that the residual does not originate from suppressed systematic structure. The inference is epistemically non-convergent; the candidate signal survives the criterion as a physical residual requiring independent resolution.

These cases illustrate the discriminating behavior of the criterion: it produces distinct outcomes for a systematic and a candidate physical effect without requiring a prior commitment to either interpretation. The criterion is not a test of whether new physics exists; it is a test of whether the inference framework has been exhausted at the tested resolution.

---

## 8. Related Work

The phenomenon of scale-dependent inference has been identified in several distinct literatures. The present work differs from each in scope and in the specific contribution it makes.

**Modifiable Areal Unit Problem.**
Openshaw (1984) demonstrated that spatial statistics computed over administrative regions depend on the choice of aggregation unit. This is the foundational empirical observation nearest to the present work, but MAUP is framed as a practical limitation of spatial data analysis rather than a general epistemic constraint. MAUP does not establish persistence of disagreement in the infinite-data limit, does not define epistemic completeness, and does not yield a convergence criterion.

**Ecological fallacy and Simpson's paradox.**
The ecological fallacy (Robinson 1950) and its categorical formalization as Simpson's paradox identify conditions under which aggregate and disaggregate statistics point in opposite directions. These results apply to discrete groupings. Proposition 1 extends the phenomenon to continuous resolution and proves that structural disagreement can persist under infinite data — a result the discrete formulations neither require nor imply.

**Wavelet and multiresolution analysis.**
Mallat (1989) and subsequent work develop algorithmic decompositions of signals across scale. This literature provides powerful tools for extracting scale-specific information but does not address inferential sufficiency: wavelets decompose a signal without asking whether any single-scale projection is sufficient to characterize system dynamics. No convergence criterion for inference is derived.

**Scale-dependent effective field theory.**
EFT explicitly integrates out sub-resolution degrees of freedom to construct tractable coarse-grained descriptions. This is a deliberate and controlled suppression of structure, not a failure mode. The EFT framework does not diagnose whether an inferred description is epistemically complete relative to the full system; epistemic completeness is not its concern.

**Summary.**
Each prior treatment identifies scale-dependence within its domain. None establishes a domain-general criterion for epistemic convergence under resolution refinement. The present work unifies these observations under a single epistemic framing and derives a falsifiable necessary condition — $\Delta T$ monotonicity — absent from prior treatments.

---

## 9. Discussion

The two results established here operate at different levels. Proposition 1 is a structural observation: single-resolution inference is not a sufficient statistic for multiscale systems, and disagreement can be persistent, structural, and irreducible at fixed resolution regardless of sample size. Theorem 1 is a necessary condition: genuine convergence toward a complete representation of a multiscale system requires that ΔT(ℓ) decrease monotonically under resolution refinement.

Neither result prescribes a specific multiresolution method. The theorem does not say that decreasing ΔT is achievable in any given setting, nor that a particular resolution ladder is appropriate. It establishes what must hold if convergence is genuine — and what its absence implies.

The normative consequence is direct: claims of convergence or agreement based on fixed-resolution stabilization are epistemically underdetermined. This constraint applies regardless of how well-specified the fixed-resolution model is, how large the dataset is, or how narrow the confidence intervals are.

**Connection to sufficiency in classical statistics.** The Lehmann-Scheffé theorem establishes that a complete sufficient statistic captures all information about a parameter that the data can provide. Proposition 1 can be read as identifying a systematic condition under which no single-resolution estimator achieves this: for multiscale systems, $\hat{f}_\ell$ is sufficient for the projected system $\tilde{S}(\ell)$ but not for the full system $S$. This is not a failure of the estimator — it is a structural consequence of the resolution operator. The ΔT criterion extends this naturally: rather than asking whether a sufficient statistic exists at a given resolution, it asks whether the residual insufficiency decreases as resolution increases. Tolerance of uncertainty is therefore a practiced principle here, not a concession — the framework does not demand completeness at any fixed $\ell$, only that incompleteness diminish under refinement.

**Limitations.** The ΔT criterion requires that epistemic distance be computable, which in turn requires that the resolution ladder be well-defined and that the inferred representations at each level be comparable. Not all systems admit a clean scale decomposition of the form $S = \sum_k S_k$; in systems with fractal or non-separable structure, the proof of §6.3 does not directly apply and additional conditions would be required. The empirical threshold $\Delta T < 0.15$ is calibrated on a specific class of cosmological probes and should not be applied to other domains without independent validation.

---

## 10. Conclusion

Single-resolution inference imposes an epistemic ceiling on multiscale systems. Proposition 1 shows that a global estimator can be asymptotically exact while remaining structurally incomplete, and that disagreement between locally valid inferences may persist without bound as data accumulate. Theorem 1 derives the necessary consequence: if inference genuinely converges toward a complete representation of a multiscale system, the epistemic distance $\Delta T(\ell)$ must decrease monotonically under increasing resolution. Failure of monotonicity — persistence, increase, or non-monotonic behavior — is diagnostic of unresolved structure, regardless of apparent fixed-resolution convergence.

The practical constraint is unambiguous: **any claim of convergence based solely on fixed-resolution stabilization is epistemically underdetermined.** This constraint does not depend on the domain, the estimation method, or the size of the dataset. It follows from the structure of representational projection.

Recognizing this limitation reframes how inferential disagreement should be interpreted and constrains what convergence claims are admissible. The extension to observer-frame separation and tensor-encoded epistemic distance — where $\Delta T$ is defined over observer-domain tensors rather than scalar corrections — represents a natural generalization and is the subject of ongoing work.

---

## References

```bibtex
@article{Martin2026_UHA,
  title   = {Resolution of the Hubble Tension through Multi-Resolution Spatial Encoding},
  author  = {Martin, Eric D.},
  year    = {2026},
  note    = {Preprint; submission in preparation}
}

@article{Martin2025_MultiProbe,
  title   = {Comprehensive Multi-Probe Cosmological Simulation Results},
  author  = {Martin, Eric D.},
  year    = {2025},
  note    = {Preprint; submission in preparation}
}

@article{Martin2026_PAMCMC,
  title   = {Payload-Augmented MCMC and the $\lambda$–$k$ Order Selection Theorem},
  author  = {Martin, Eric D.},
  year    = {2026},
  note    = {Submitted to Statistics \& Computing}
}

@article{Planck2020,
  author  = {{Planck Collaboration}},
  title   = {Planck 2018 results. VI. Cosmological parameters},
  journal = {Astronomy \& Astrophysics},
  volume  = {641},
  pages   = {A6},
  year    = {2020},
  doi     = {10.1051/0004-6361/201833910}
}

@article{Riess2022,
  author  = {Riess, Adam G. and others},
  title   = {A Comprehensive Measurement of the Local Value of the Hubble Constant},
  journal = {The Astrophysical Journal Letters},
  volume  = {934},
  pages   = {L7},
  year    = {2022},
  doi     = {10.3847/2041-8213/ac5c5b}
}

@article{Openshaw1984,
  author  = {Openshaw, Stan},
  title   = {The modifiable areal unit problem},
  journal = {Concepts and Techniques in Modern Geography},
  volume  = {38},
  year    = {1984}
}

@article{Robinson1950,
  author  = {Robinson, W. S.},
  title   = {Ecological correlations and the behavior of individuals},
  journal = {American Sociological Review},
  volume  = {15},
  number  = {3},
  pages   = {351--357},
  year    = {1950}
}

@article{Mallat1989,
  author  = {Mallat, St{\'e}phane G.},
  title   = {A theory for multiresolution signal decomposition},
  journal = {IEEE Transactions on Pattern Analysis and Machine Intelligence},
  volume  = {11},
  number  = {7},
  pages   = {674--693},
  year    = {1989}
}

```
