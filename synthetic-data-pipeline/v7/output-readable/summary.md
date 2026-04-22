# v7 Pipeline Run — Summary

**Total records:** 30

## Headline Metrics

| Layer | Exact match | Rate |
|---|---|---|
| L0 | 28/30 | 93.3% |
| L1 | 13/19 | 68.4% |
| L2 | 10/19 | 52.6% |

## L0 Confusion Matrix

| GT ↓ / Pred → | 001HE | 002OC | 003II |
|---|---|---|---|
| **001HE** | 17 | 0 | 2 |
| **002OC** | 0 | 3 | 0 |
| **003II** | 0 | 0 | 8 |

## L0 Per-Class

| Class | P | R | F1 | TP | FP | FN |
|---|---|---|---|---|---|---|
| 001HE | 1.000 | 0.895 | 0.944 | 17 | 0 | 2 |
| 002OC | 1.000 | 1.000 | 1.000 | 3 | 0 | 0 |
| 003II | 0.800 | 1.000 | 0.889 | 8 | 2 | 0 |

## L1 Set-Based Metrics (macro avg across 001HE records)

- Precision: 0.763
- Recall: 0.763
- F1: 0.754

## L1 Per-Class

| Class | P | R | F1 | TP | FP | FN |
|---|---|---|---|---|---|---|
| 101D | 0.667 | 1.000 | 0.800 | 6 | 3 | 0 |
| 102S | 1.000 | 0.750 | 0.857 | 9 | 0 | 3 |
| 103II | 0.000 | 0.000 | 0.000 | 0 | 0 | 2 |

## L2 Set-Based Metrics (macro avg, subcategory level)

- Precision: 0.719
- Recall: 0.719
- F1: 0.702

## L1 Mismatches

| Record | GT | Pipeline |
|---|---|---|
| SYN-CS07 | ['101D', '102S'] | ['101D'] |
| SYN-CS09 | ['102S'] | ['101D'] |
| SYN-CS13 | ['102S'] | ['101D'] |
| SYN-CS19 | ['102S'] | ['101D', '102S'] |
| SYN-N09 | ['103II'] | None |
| SYN-N10 | ['103II'] | None |

## L2 Subcategory Mismatches

| Record | GT | Pipeline |
|---|---|---|
| SYN-CS02 | ['201C2', '202P1'] | ['202P1'] |
| SYN-CS03 | [] | ['201C3', '204E'] |
| SYN-CS07 | ['201C2'] | [] |
| SYN-CS08 | ['201C1', '201C2', '201C3'] | ['201C1', '201C3', '202P2'] |
| SYN-CS11 | ['201C1'] | ['201C2', '204E'] |
| SYN-CS13 | ['202P2', '203T'] | ['202P2'] |
| SYN-CS14 | ['201C3'] | ['201C3', '203T'] |
| SYN-CS15 | ['201C2'] | ['202P1'] |
| SYN-CS19 | ['203T'] | ['201C2', '203T'] |
