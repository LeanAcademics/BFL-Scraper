# L0 Human Error Classification

Determine the most applicable class of the fatality report. The categories 001HE, 002OC, 003II are mutually exclusive, only select one.

## (001HE) – Human Error Present

The narrative explicitly states or provides sufficient information to reasonably deduce that one or more human errors contributed to the fatal outcome. This includes cases where the domain reference makes a human error pathway deducible even when the narrative does not explicitly state it.

## (002OC) – Other Cause

The narrative contains positive evidence that the fatal outcome resulted from factors outside the jumper's reasonable control or anticipation. There must be affirmative evidence pointing to a non-human-error cause, absence of human error language is not sufficient.

## (003II) – Insufficient Information

Neither 001HE nor 002OC can be supported by the narrative. The narrative does not contain sufficient information to reasonably deduce a human error pathway (001HE) and does not contain positive evidence of a non-human cause (002OC). Prefer coding 003II over forcing a classification you are not confident about. 

## Output Instructions

Return JSON only. No markdown, no code fences, no text outside the JSON.

{
"record_id": "<BFL record id>",
"L0_classification": "<001HE|002OC|003II>",
"L0_description": "<1-3 sentences stating the basis>"
}