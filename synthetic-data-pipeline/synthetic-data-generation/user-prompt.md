# Task

You are designing and generating a synthetic validation dataset for a BASE jumping fatality classification pipeline. The pipeline classifies real accident narratives from the BASE Fatality List (BFL) using the HFACS-BASE framework.

Your job is to create 30 synthetic fatality records that will be used as pre-labeled test cases to evaluate the pipeline before it processes real data. You must design the cases yourself based on your understanding of the uploaded materials.

# Uploaded Files

- `bfl_fatalities.jsonl`: 537 real fatality records. Study these thoroughly for writing style, narrative voice, JSON schema, vocabulary, structural variation, information density, and the range of accident types. Your synthetic records must be stylistically indistinguishable from real ones. Do not copy or closely paraphrase any real record.
- `BASE_DOMAIN_CONTEXT.md`: Domain knowledge about BASE jumping. Use this to ensure technical plausibility.
- `HFACS-Pipeline-Instructions.md`: The exact classification framework the pipeline applies. Study this carefully. It contains specific boundary rules, gating criteria, and tests (e.g., Active Failure Test, 103O perceptual error gate, 204E three-condition test, 002OC criteria) that define where the pipeline is most likely to succeed or fail. Your cases should probe these boundaries.

# What to Generate

**20 clear-signal cases:** Each must have an unambiguous correct classification. Design these to cover the full taxonomy (all L0 categories, all L1 categories, all L2 groups) and to specifically test classification boundaries and discrimination challenges you identify from reading the HFACS definitions. Include rare categories (e.g., 002OC, 103O) that appear infrequently in the real BFL but must work correctly. Include cases that test multi-label scenarios and the L1-L2 relationship logic.

**10 noisy cases:** Each must be genuinely difficult or impossible to classify correctly. Design these to test whether the pipeline avoids false positives, handles ambiguity, and resists over-classification. These should include various forms of insufficient, contradictory, misleading, or information-sparse narratives.

Assign each case an ID (CS-01 through CS-20 for clear-signal, N-01 through N-10 for noisy).

# Output Format

One JSON object per line (valid JSONL). Use the exact same field schema as `bfl_fatalities.jsonl` with the addition of a `ground_truth` field:

```
{...<all BFL fields>..., "ground_truth": {"L0": "<001HE|002OC|003II>", "L1": [{"category": "<code>", "label": "<short description>"}] or null, "L2": [{"category": "<code>", "subcategory": "<code or null>", "linked_L1": "<code>", "label": "<short description>"}] or null, "test_id": "<CS-XX or N-XX>", "test_purpose": "<1 sentence: what this case tests>", "expected_difficulty": "<easy|moderate|hard>"}}
```

For 002OC and 003II records, L1 and L2 are null.

# Requirements

- Write all narratives in naturalistic BFL witness-perspective language. Never use HFACS terminology, category codes, or analytical framing in the narrative text. The classifier must infer the categories.
- Vary narrative length substantially (some under 30 words, some over 200 words).
- Vary object types (B, A, S, E), suit types (slick, tracking, wingsuit at different levels), metadata completeness (some records with full structured fields, some with mostly nulls), and time period (some 1980s-era with old equipment, some modern).
- Ground truth labels must be correct according to the definitions in `HFACS-Pipeline-Instructions.md`. Pay particular attention to the boundary rules and gating criteria.
- Each case must have a clear test purpose. Do not generate generic cases.
- Output all 30 records as valid JSONL, one record per line, no markdown formatting.

**Known classification challenge:** LLM classifiers tend to struggle with the distinction between active failures (Layer 1) and enabling preconditions (Layer 2) when both involve the same causal chain. For example, a packing error that produced a malfunction is an active failure at L1, while an omitted gear check that would have caught it is a precondition at L2. Similarly, environmental factors can appear at three different levels depending on context: as the content of a decision error at L1 (jumper chose to jump in observable bad conditions), as a precondition at L2 (conditions indirectly degraded execution), or as an other cause at L0 (genuinely unforeseeable event with no human error). Ensure your cases include scenarios that probe these specific discrimination challenges.