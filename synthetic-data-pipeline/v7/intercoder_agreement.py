#!/usr/bin/env python3
"""
Intercoder agreement — v7.

Three 'coders':
  GT   = hand-coded ground-truth.jsonl
  Opus = Claude Opus 4.6 output (./output/classification_results.jsonl)
  GPT  = GPT-5.4 output          (./output-gpt/classification_results.jsonl)

Agreement metrics:
  L0 — Cohen's κ (pairwise), simple accuracy, Fleiss' κ (all three)
  L1 — exact set-match agreement and per-category binary Cohen's κ
       * Equivalence rule: L1 = None/empty is treated equal to L1 = {103II}
         (both semantically mean "no specific unsafe act identified")
  L2 — exact subcategory-set agreement and per-subcategory binary Cohen's κ

n = 30 records.
"""

import json
from pathlib import Path
from sklearn.metrics import cohen_kappa_score
import numpy as np

ROOT = Path(__file__).resolve().parent

def load_jsonl(p):
    out = {}
    with open(p) as f:
        for line in f:
            line = line.strip()
            if line:
                r = json.loads(line)
                out[r["record_id"]] = r
    return out

gt   = load_jsonl(ROOT / "ground-truth.jsonl")
opus = load_jsonl(ROOT / "output/classification_results.jsonl")
gpt  = load_jsonl(ROOT / "output-gpt/classification_results.jsonl")

rids = sorted(gt.keys())

def l0(r): return r.get("L0_classification")

def l1_norm(r):
    """Normalize L1: None/empty/{103II-only} → None ('no specific act')."""
    acts = r.get("L1_unsafe_acts")
    if not acts:
        return None
    cats = frozenset(a.get("category") for a in acts if a.get("category"))
    if cats == frozenset({"103II"}):
        return None
    return cats

def l2_subs(r):
    preconds = r.get("L2_preconditions")
    if preconds is None:
        return None
    subs = set()
    for p in preconds:
        s = p.get("subcategory") or p.get("category")
        if s:
            subs.add(s)
    return frozenset(subs)


# ---------------------------------------------------------------------------
# L0
# ---------------------------------------------------------------------------
gt_l0   = [l0(gt[r])            for r in rids]
opus_l0 = [l0(opus.get(r, {}))  for r in rids]
gpt_l0  = [l0(gpt.get(r, {}))   for r in rids]

def pct_agree(a, b):
    return sum(1 for x, y in zip(a, b) if x == y) / len(a)

print("=" * 70)
print(f"  Intercoder Agreement — v7 (n={len(rids)})")
print("=" * 70)

print("\n--- L0 (Top-Level, 3 classes) ---\n")
print(f"{'Pair':<14s} {'Accuracy':>10s} {'Cohen κ':>10s}")
for a_name, a, b_name, b in [
    ("GT × Opus",  gt_l0,   "", opus_l0),
    ("GT × GPT",   gt_l0,   "", gpt_l0),
    ("Opus × GPT", opus_l0, "", gpt_l0),
]:
    name = a_name
    k = cohen_kappa_score(a, b)
    acc = pct_agree(a, b)
    print(f"{name:<14s} {acc:>10.3f} {k:>10.3f}")

# Fleiss' κ for three coders, 3 categories
def fleiss_kappa(ratings):
    """ratings: list of lists, each inner list has the categorical label per coder."""
    N = len(ratings)
    cats = sorted({c for row in ratings for c in row})
    n = len(ratings[0])
    M = np.zeros((N, len(cats)), dtype=int)
    for i, row in enumerate(ratings):
        for c in row:
            M[i, cats.index(c)] += 1
    P_i = (M.sum(axis=1)**0 * 0) + ((M**2).sum(axis=1) - n) / (n * (n - 1))
    P_bar = P_i.mean()
    p_j = M.sum(axis=0) / (N * n)
    P_e = (p_j**2).sum()
    return (P_bar - P_e) / (1 - P_e) if (1 - P_e) > 0 else float("nan")

ratings_l0 = [[a, b, c] for a, b, c in zip(gt_l0, opus_l0, gpt_l0)]
print(f"\nFleiss κ (3 coders):  {fleiss_kappa(ratings_l0):.3f}")


# ---------------------------------------------------------------------------
# L1
# ---------------------------------------------------------------------------
gt_l1   = [l1_norm(gt[r])           for r in rids]
opus_l1 = [l1_norm(opus.get(r, {})) for r in rids]
gpt_l1  = [l1_norm(gpt.get(r, {}))  for r in rids]

print("\n--- L1 (Unsafe Acts, set match — None ≡ {103II}) ---\n")
print(f"{'Pair':<14s} {'Exact match':>12s}")
for name, a, b in [("GT × Opus", gt_l1, opus_l1),
                   ("GT × GPT",  gt_l1, gpt_l1),
                   ("Opus × GPT", opus_l1, gpt_l1)]:
    print(f"{name:<14s} {pct_agree(a, b):>12.3f}")

# Per-category binary κ (101D / 102S; 103II folded into None)
def bin_vec(norm_list, cls):
    return [int(cls in (x or frozenset())) for x in norm_list]

print("\n--- L1 per-category Cohen's κ ---\n")
print(f"{'Class':<8s} {'GT×Opus':>10s} {'GT×GPT':>10s} {'Opus×GPT':>10s}")
for cls in ["101D", "102S"]:
    a = bin_vec(gt_l1, cls); b = bin_vec(opus_l1, cls); c = bin_vec(gpt_l1, cls)
    k1 = cohen_kappa_score(a, b); k2 = cohen_kappa_score(a, c); k3 = cohen_kappa_score(b, c)
    print(f"{cls:<8s} {k1:>10.3f} {k2:>10.3f} {k3:>10.3f}")


# ---------------------------------------------------------------------------
# L2
# ---------------------------------------------------------------------------
gt_l2   = [l2_subs(gt[r])           for r in rids]
opus_l2 = [l2_subs(opus.get(r, {})) for r in rids]
gpt_l2  = [l2_subs(gpt.get(r, {}))  for r in rids]

print("\n--- L2 (Preconditions, exact subcategory-set match) ---\n")
print(f"{'Pair':<14s} {'Exact match':>12s}")
for name, a, b in [("GT × Opus", gt_l2, opus_l2),
                   ("GT × GPT",  gt_l2, gpt_l2),
                   ("Opus × GPT", opus_l2, gpt_l2)]:
    # Treat None (L2 skipped) and frozenset() (empty L2) as equivalent
    a2 = [x or frozenset() for x in a]
    b2 = [x or frozenset() for x in b]
    print(f"{name:<14s} {pct_agree(a2, b2):>12.3f}")

# Per-subcategory binary κ
all_subs = sorted({s for x in gt_l2 + opus_l2 + gpt_l2 if x for s in x})
print("\n--- L2 per-subcategory Cohen's κ ---\n")
print(f"{'Sub':<8s} {'GT×Opus':>10s} {'GT×GPT':>10s} {'Opus×GPT':>10s}")
for cls in all_subs:
    a = bin_vec(gt_l2, cls); b = bin_vec(opus_l2, cls); c = bin_vec(gpt_l2, cls)
    # Guard: if one vector is all-zeros, κ is 0 (degenerate)
    def safe_k(x, y):
        if len(set(x)) == 1 and len(set(y)) == 1 and x[0] == y[0]:
            return float("nan")  # both all-same; κ undefined
        return cohen_kappa_score(x, y)
    k1 = safe_k(a, b); k2 = safe_k(a, c); k3 = safe_k(b, c)
    f = lambda k: f"{k:>10.3f}" if not np.isnan(k) else f"{'n/a':>10s}"
    print(f"{cls:<8s} {f(k1)} {f(k2)} {f(k3)}")

print()
