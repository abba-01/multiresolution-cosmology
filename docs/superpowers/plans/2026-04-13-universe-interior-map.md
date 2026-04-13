# Universe Interior Map Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the s* = r/R(T_meta) universe interior map as a testable Python module with a 16-vector basis sampler and Gram matrix cross-comparator.

**Architecture:** Three focused modules — `structures.py` (cosmic structure database as N/U bounded pairs), `sstar.py` (s* normalization, shell classification, horizon), `basis.py` (16-vector basis, Gram matrix). A `report.py` module formats the output table. All modules are pure functions with no global state. Tests use pytest with hardcoded expected values derived from known physics.

**Tech Stack:** Python 3.10+, numpy (Gram matrix), pytest. No external data files — all structures are hardcoded from published values.

---

## File Map

| File | Responsibility |
|------|---------------|
| `universe_map/structures.py` | Cosmic structure database — name, distance r (Gly), uncertainty u (Gly) as N/U pairs |
| `universe_map/sstar.py` | s* = r/R computation, shell classification, horizon constant |
| `universe_map/basis.py` | 16-vector basis (4D hypercube vertices), Gram matrix, cross-comparison |
| `universe_map/report.py` | Format and print the map table |
| `tests/test_structures.py` | Validate structure data integrity |
| `tests/test_sstar.py` | Validate s* computation and shell bins |
| `tests/test_basis.py` | Validate basis generation and Gram matrix properties |

---

## Task 1: Cosmic Structure Database

**Files:**
- Create: `universe_map/__init__.py`
- Create: `universe_map/structures.py`
- Create: `tests/__init__.py`
- Create: `tests/test_structures.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_structures.py
from universe_map.structures import STRUCTURES, Structure

def test_structure_fields():
    s = STRUCTURES[0]
    assert hasattr(s, 'name')
    assert hasattr(s, 'r_gly')   # nominal distance in Gly
    assert hasattr(s, 'u_gly')   # uncertainty bound in Gly
    assert s.u_gly >= 0

def test_all_distances_positive():
    for s in STRUCTURES:
        assert s.r_gly >= 0, f"{s.name} has negative distance"

def test_horizon_is_last():
    assert STRUCTURES[-1].name == "Observable Horizon"

def test_count():
    assert len(STRUCTURES) == 16  # 16 structures for 16-vector symmetry
```

- [ ] **Step 2: Run — expect FAIL**

```bash
cd /scratch/repos/multiresolution-cosmology
python -m pytest tests/test_structures.py -v
```
Expected: `ModuleNotFoundError: No module named 'universe_map'`

- [ ] **Step 3: Create module and structure database**

```python
# universe_map/__init__.py
# empty

# universe_map/structures.py
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Structure:
    name: str
    r_gly: float   # nominal distance, billion light-years
    u_gly: float   # uncertainty bound, billion light-years

    @property
    def M(self) -> float:
        """Epistemic budget: M = |r| + u"""
        return abs(self.r_gly) + self.u_gly

# All distances are comoving, in billion light-years (Gly)
# Sources: PDG 2022, Planck 2018, NED distance database
STRUCTURES: List[Structure] = [
    Structure("Earth / apparatus",          0.0,           0.0),
    Structure("Solar System",               0.000000015,   0.000000001),
    Structure("Proxima Centauri",           0.00000407,    0.00000001),
    Structure("Milky Way center",           0.000026,      0.000002),
    Structure("Milky Way edge",             0.0001,        0.00001),
    Structure("Andromeda (M31)",            0.00252,       0.00005),
    Structure("Local Group boundary",       0.010,         0.002),
    Structure("Virgo Cluster",              0.0535,        0.005),
    Structure("Laniakea center",            0.250,         0.030),
    Structure("Laniakea boundary",          0.520,         0.050),
    Structure("Sloan Great Wall",           1.40,          0.10),
    Structure("Peak star formation epoch",  4.60,          0.20),
    Structure("Hercules-Corona Borealis",   10.0,          1.0),
    Structure("Quasar epoch midpoint",      23.0,          2.0),
    Structure("CMB last scattering",        45.7,          0.1),
    Structure("Observable Horizon",         46.5,          0.0),
]
```

- [ ] **Step 4: Run — expect PASS**

```bash
python -m pytest tests/test_structures.py -v
```
Expected: 4 tests PASS

- [ ] **Step 5: Commit**

```bash
git add universe_map/ tests/
git commit -m "feat: cosmic structure database — 16 N/U bounded pairs from Earth to horizon"
```

---

## Task 2: s* Normalization and Shell Classification

**Files:**
- Create: `universe_map/sstar.py`
- Create: `tests/test_sstar.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_sstar.py
from universe_map.sstar import s_star, classify_shell, R_HORIZON_GLY, SHELLS

def test_s_star_zero_at_origin():
    assert s_star(0.0, R_HORIZON_GLY) == 0.0

def test_s_star_one_at_horizon():
    assert s_star(R_HORIZON_GLY, R_HORIZON_GLY) == 1.0

def test_s_star_cmb():
    result = s_star(45.7, R_HORIZON_GLY)
    assert abs(result - 0.983) < 0.001

def test_s_star_virgo():
    result = s_star(0.0535, R_HORIZON_GLY)
    assert abs(result - 0.00115) < 0.00005

def test_shell_local():
    assert classify_shell(0.0012) == "Local"

def test_shell_supercluster():
    assert classify_shell(0.005) == "Supercluster"

def test_shell_large_scale():
    assert classify_shell(0.05) == "Large-scale structure"

def test_shell_deep():
    assert classify_shell(0.5) == "Deep universe"

def test_shell_horizon():
    assert classify_shell(0.95) == "Horizon shell"

def test_all_shells_defined():
    assert len(SHELLS) == 5
```

- [ ] **Step 2: Run — expect FAIL**

```bash
python -m pytest tests/test_sstar.py -v
```
Expected: `ImportError: cannot import name 's_star'`

- [ ] **Step 3: Implement s* and shell classifier**

```python
# universe_map/sstar.py

# Comoving particle horizon radius, Planck 2018 ΛCDM
R_HORIZON_GLY: float = 46.5  # billion light-years

# Shell boundaries in s* units
SHELLS = [
    (0.0,    0.001,  "Local"),
    (0.001,  0.01,   "Supercluster"),
    (0.01,   0.10,   "Large-scale structure"),
    (0.10,   0.90,   "Deep universe"),
    (0.90,   1.001,  "Horizon shell"),
]

def s_star(r: float, R_T_meta: float) -> float:
    """
    Normalized UHA coordinate: s* = r / R(T_meta).
    
    Args:
        r:        raw observable distance (same units as R_T_meta)
        R_T_meta: horizon radius at the meta-temporal constraint parameter

    Returns:
        s* in [0, 1]; values > 1 are outside the admissible domain.
    """
    if R_T_meta <= 0:
        raise ValueError(f"R(T_meta) must be positive, got {R_T_meta}")
    return r / R_T_meta

def classify_shell(s: float) -> str:
    """Return the shell name for a given s* value."""
    for lo, hi, name in SHELLS:
        if lo <= s < hi:
            return name
    return "Inadmissible"  # s* >= 1
```

- [ ] **Step 4: Run — expect PASS**

```bash
python -m pytest tests/test_sstar.py -v
```
Expected: 10 tests PASS

- [ ] **Step 5: Commit**

```bash
git add universe_map/sstar.py tests/test_sstar.py
git commit -m "feat: s* normalization and shell classifier — 5 shells from Local to Horizon"
```

---

## Task 3: 16-Vector Basis and Gram Matrix

**Files:**
- Create: `universe_map/basis.py`
- Create: `tests/test_basis.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_basis.py
import numpy as np
from universe_map.basis import basis_16, gram_matrix, compare_pair

def test_basis_count():
    vecs = basis_16()
    assert len(vecs) == 16

def test_basis_entries_pm1():
    for v in basis_16():
        for x in v:
            assert x in (-1, 1)

def test_basis_4d():
    for v in basis_16():
        assert len(v) == 4

def test_gram_matrix_shape():
    G = gram_matrix()
    assert G.shape == (16, 16)

def test_gram_diagonal_is_4():
    G = gram_matrix()
    # v · v = 1+1+1+1 = 4 for all unit hypercube vertices
    for i in range(16):
        assert G[i, i] == 4

def test_gram_symmetric():
    G = gram_matrix()
    assert np.allclose(G, G.T)

def test_gram_off_diagonal_range():
    G = gram_matrix()
    off = G[~np.eye(16, dtype=bool)]
    assert off.min() >= -4
    assert off.max() <= 4

def test_compare_pair_identical():
    v = (1, 1, 1, 1)
    result = compare_pair(v, v)
    assert result["inner_product"] == 4
    assert result["relation"] == "identical"

def test_compare_pair_orthogonal():
    v1 = (1, 1, 1, 1)
    v2 = (1, 1, -1, -1)
    result = compare_pair(v1, v2)
    assert result["inner_product"] == 0
    assert result["relation"] == "orthogonal"

def test_compare_pair_correlated():
    v1 = (1, 1, 1, 1)
    v2 = (1, 1, 1, -1)
    result = compare_pair(v1, v2)
    assert result["inner_product"] == 2
    assert result["relation"] == "correlated"
```

- [ ] **Step 2: Run — expect FAIL**

```bash
python -m pytest tests/test_basis.py -v
```
Expected: `ImportError: cannot import name 'basis_16'`

- [ ] **Step 3: Implement basis and Gram matrix**

```python
# universe_map/basis.py
import numpy as np
from itertools import product
from typing import List, Tuple, Dict

Vector4D = Tuple[int, int, int, int]

def basis_16() -> List[Vector4D]:
    """
    Generate all 16 vertices of the unit 4-hypercube.
    Each vertex is a 4-tuple of ±1 — the 16-vector basis.

    The four dimensions are:
        d0: s*     (normalized radial distance)
        d1: u*     (normalized uncertainty = u / R_H)
        d2: Δs*    (normalized structure extent)
        d3: shell  (shell index encoded as ±1: inner=-1, outer=+1)
    """
    return list(product((-1, 1), repeat=4))

def gram_matrix() -> np.ndarray:
    """
    Compute the 16×16 Gram matrix G where G[i,j] = v_i · v_j.
    Reveals directional correlations across the 4D state space.
    """
    vecs = np.array(basis_16(), dtype=float)  # shape (16, 4)
    return vecs @ vecs.T

def compare_pair(v1: Vector4D, v2: Vector4D) -> Dict:
    """
    Cross-compare two basis vectors.
    
    Returns:
        inner_product: v1 · v2 (integer in [-4, 4])
        relation:
            "identical"    — same direction (inner = 4)
            "opposite"     — antiparallel  (inner = -4)
            "orthogonal"   — independent   (inner = 0)
            "correlated"   — partial share (inner in {2, -2})
            "weakly_linked"— 1 shared dim  (inner in {1, -1, 3, -3}) [not reachable for ±1 vecs]
    """
    ip = sum(a * b for a, b in zip(v1, v2))
    if ip == 4:
        relation = "identical"
    elif ip == -4:
        relation = "opposite"
    elif ip == 0:
        relation = "orthogonal"
    else:
        relation = "correlated"
    return {"inner_product": ip, "relation": relation}
```

- [ ] **Step 4: Run — expect PASS**

```bash
python -m pytest tests/test_basis.py -v
```
Expected: 11 tests PASS

- [ ] **Step 5: Commit**

```bash
git add universe_map/basis.py tests/test_basis.py
git commit -m "feat: 16-vector basis (4D hypercube), Gram matrix, cross-comparison"
```

---

## Task 4: Report — Full Universe Interior Map

**Files:**
- Create: `universe_map/report.py`
- Create: `universe_map/map_universe.py` (entry point)

- [ ] **Step 1: Write the report module**

```python
# universe_map/report.py
from universe_map.structures import STRUCTURES, Structure
from universe_map.sstar import s_star, classify_shell, R_HORIZON_GLY

def build_map(R_T_meta: float = R_HORIZON_GLY) -> list:
    """
    Compute s* and shell classification for all structures.
    Returns list of dicts with name, r, u, s*, shell.
    """
    rows = []
    for st in STRUCTURES:
        ss = s_star(st.r_gly, R_T_meta)
        shell = classify_shell(ss)
        rows.append({
            "name":  st.name,
            "r_gly": st.r_gly,
            "u_gly": st.u_gly,
            "s_star": ss,
            "M":     st.M,
            "shell": shell,
        })
    return rows

def print_map(R_T_meta: float = R_HORIZON_GLY) -> None:
    rows = build_map(R_T_meta)
    print(f"\ns* = r / R(T_meta)    R(T_meta) = {R_T_meta} Gly\n")
    print(f"{'s*':>12}  {'r (Gly)':>14}  {'u (Gly)':>10}  {'Shell':<22}  {'Structure'}")
    print("─" * 90)
    for r in rows:
        print(
            f"{r['s_star']:>12.6f}  "
            f"{r['r_gly']:>14.6g}  "
            f"{r['u_gly']:>10.4g}  "
            f"{r['shell']:<22}  "
            f"{r['name']}"
        )
    print("─" * 90)
    print(f"  Admissible domain: 0 ≤ s* < 1    Horizon: s* = 1.000000\n")
```

- [ ] **Step 2: Create entry point**

```python
# universe_map/map_universe.py
from universe_map.report import print_map
from universe_map.basis import gram_matrix, basis_16
import numpy as np

if __name__ == "__main__":
    print_map()

    print("\n16-Vector Basis (4D hypercube vertices):")
    for i, v in enumerate(basis_16()):
        print(f"  v{i+1:02d} = {v}")

    G = gram_matrix()
    print(f"\nGram Matrix summary:")
    print(f"  Diagonal (self-similarity):  all = {int(G[0,0])}")
    unique_off = sorted(set(int(G[i,j]) for i in range(16) for j in range(16) if i != j))
    print(f"  Off-diagonal values:         {unique_off}")
    print(f"  Orthogonal pairs (G=0):      {int((G == 0).sum() - 0) // 2}")
    print(f"  Correlated pairs (|G|=2):    {int((np.abs(G) == 2).sum()) // 2}")
    print(f"  Opposite pairs (G=-4):       {int((G == -4).sum()) // 2}")
```

- [ ] **Step 3: Run and verify output**

```bash
cd /scratch/repos/multiresolution-cosmology
python -m universe_map.map_universe
```

Expected output (partial):
```
s* = r / R(T_meta)    R(T_meta) = 46.5 Gly

        s*        r (Gly)     u (Gly)  Shell                   Structure
──────────────────────────────────────────────────────────────────────────
  0.000000               0           0  Local                   Earth / apparatus
  0.000000       1.5e-08    1e-09     Local                   Solar System
  ...
  0.983011            45.7         0.1  Horizon shell           CMB last scattering
  1.000000            46.5           0  Horizon shell           Observable Horizon
```

- [ ] **Step 4: Run full test suite**

```bash
python -m pytest tests/ -v
```
Expected: all 25 tests PASS

- [ ] **Step 5: Commit**

```bash
git add universe_map/report.py universe_map/map_universe.py
git commit -m "feat: universe interior map — s* table, 16-vector basis, Gram matrix report"
```

---

## Task 5: Neutron Lifetime — Apply Framework to Discrepancy

**Files:**
- Create: `universe_map/neutron.py`
- Create: `tests/test_neutron.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_neutron.py
from universe_map.neutron import (
    neutron_map, timelessness_check, dark_channel_bound
)

def test_midpoint():
    result = neutron_map()
    assert abs(result["n_tau"] - 882.725) < 0.001

def test_u_tau():
    result = neutron_map()
    assert abs(result["u_tau"] - 4.975) < 0.001

def test_s_star_bottle():
    result = neutron_map()
    assert abs(result["s_star_bottle"] - 0.99436) < 0.00001

def test_s_star_beam():
    result = neutron_map()
    assert abs(result["s_star_beam"] - 1.00564) < 0.00001

def test_timelessness_violated():
    result = timelessness_check(888.0, 2.0, 877.8, 0.3)
    assert result["violated"] is True
    assert abs(result["discrepancy"] - 10.2) < 0.1
    assert abs(result["combined_u"] - 2.3) < 0.1
    assert abs(result["hidden_systematic"] - 7.9) < 0.1

def test_dark_channel_bound():
    result = dark_channel_bound(877.75, 887.7)
    # τ_dark ≥ 1 / (1/τ_bottle - 1/τ_beam)
    assert result["tau_dark_lower_s"] > 70000
    assert result["lambda_dark"] > 0
```

- [ ] **Step 2: Run — expect FAIL**

```bash
python -m pytest tests/test_neutron.py -v
```
Expected: `ImportError`

- [ ] **Step 3: Implement neutron module**

```python
# universe_map/neutron.py

TAU_BOTTLE = 877.75   # seconds
TAU_BEAM   = 887.70   # seconds
U_BEAM     = 2.0      # stated 1σ uncertainty, beam
U_BOTTLE   = 0.3      # stated 1σ uncertainty, bottle

def neutron_map() -> dict:
    """
    Apply s* = r / R(T_meta) to neutron lifetime measurements.
    R(T_meta) = unweighted midpoint (equal admissibility assumption).
    """
    n_tau = (TAU_BOTTLE + TAU_BEAM) / 2          # 882.725
    u_tau = abs(TAU_BEAM - TAU_BOTTLE) / 2       # 4.975
    R_T_meta = n_tau

    s_star_bottle = TAU_BOTTLE / R_T_meta
    s_star_beam   = TAU_BEAM   / R_T_meta
    delta_s_star  = s_star_beam - s_star_bottle

    return {
        "n_tau":          n_tau,
        "u_tau":          u_tau,
        "R_T_meta":       R_T_meta,
        "s_star_bottle":  s_star_bottle,
        "s_star_beam":    s_star_beam,
        "delta_s_star":   delta_s_star,
    }

def timelessness_check(
    n1: float, u1: float,
    n2: float, u2: float
) -> dict:
    """
    SSOT_Inv timelessness test: |n1 - n2| ≤ u1 + u2.
    If violated, compute minimum hidden systematic required to restore.
    """
    discrepancy  = abs(n1 - n2)
    combined_u   = u1 + u2
    violated     = discrepancy > combined_u
    hidden       = max(0.0, discrepancy - combined_u)
    return {
        "discrepancy":       discrepancy,
        "combined_u":        combined_u,
        "violated":          violated,
        "hidden_systematic": hidden,
    }

def dark_channel_bound(tau_bottle: float, tau_beam: float) -> dict:
    """
    If discrepancy is due to a dark neutron channel:
        λ_total = λ_proton + λ_dark
    Beam measures λ_proton (1/tau_beam).
    Bottle measures λ_total (1/tau_bottle).
    """
    lambda_total  = 1.0 / tau_bottle
    lambda_proton = 1.0 / tau_beam
    lambda_dark   = lambda_total - lambda_proton   # must be > 0

    if lambda_dark <= 0:
        tau_dark_lower = float('inf')
    else:
        tau_dark_lower = 1.0 / lambda_dark

    return {
        "lambda_total":    lambda_total,
        "lambda_proton":   lambda_proton,
        "lambda_dark":     lambda_dark,
        "tau_dark_lower_s": tau_dark_lower,
    }
```

- [ ] **Step 4: Run — expect PASS**

```bash
python -m pytest tests/test_neutron.py -v
```
Expected: 6 tests PASS

- [ ] **Step 5: Run full suite**

```bash
python -m pytest tests/ -v --tb=short
```
Expected: all 31 tests PASS

- [ ] **Step 6: Commit**

```bash
git add universe_map/neutron.py tests/test_neutron.py
git commit -m "feat: neutron lifetime — s* mapping, timelessness check, dark channel bound"
```

---

## Self-Review

**Spec coverage:**
- [x] s* = r / R(T_meta) normalization — Task 2
- [x] 16-vector basis (4D hypercube) — Task 3
- [x] Gram matrix cross-comparison — Task 3
- [x] Universe interior map with all 16 structures — Tasks 1 + 4
- [x] Shell classification (5 shells) — Task 2
- [x] Neutron lifetime application — Task 5
- [x] Timelessness check (SSOT_Inv) — Task 5
- [x] Dark channel bound — Task 5

**Placeholder scan:** None found. All code blocks are complete and runnable.

**Type consistency:** `s_star()` returns `float` in Task 2, used as `float` in Tasks 4 and 5. `basis_16()` returns `List[Vector4D]` in Task 3, iterated in Task 4. `neutron_map()` returns `dict` in Task 5 with keys matched to test assertions.
