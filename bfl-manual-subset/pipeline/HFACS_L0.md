# HFACS_L0

# Layer 0: Top-Level Classification

Determine the most applicable class. The categories 001HE, 002OC, 003II are mutually exclusive.

## 001HE - Human Error Present

The narrative explicitly states or provides clear information to identify that one or more human errors contributed to the fatal outcome. This includes cases where the domain reference makes a human error pathway clearly identifiable even when the narrative does not explicitly state it.

## 002OC - Other Cause

The narrative contains positive evidence that the fatal outcome resulted from factors outside the jumper’s reasonable control or anticipation. Absence of human error language does not qualify. There must be affirmative evidence pointing to a non-human-error cause.

002OC applies when the narrative supports one or more of the following:

- **Unforeseeable environmental event:** Conditions not identifiable as unsafe before the jump given what a competent BASE jumper could reasonably have assessed. If the conditions were clearly observable or forecastable and the jumper decided to jump anyway, the decision is human error (001HE).
- **Equipment failure independent of human error:** A material or mechanical failure not caused by the jumper’s packing, rigging, assembly, maintenance, modification, or equipment selection. If the jumper packed incorrectly, misrigged, used inappropriate gear, or failed to maintain equipment, the failure is a consequence of human error (001HE).
- **Other non-human cause:** Any other cause where the jumper acted within accepted practice and the fatal outcome resulted from a factor the jumper could not reasonably have anticipated or controlled. Includes sudden medical events with no prior indication. If the jumper had a known medical condition making such an event foreseeable and chose to jump, the decision is human error (001HE).

## 003II - Insufficient Information

Neither 001HE nor 002OC can be supported. The narrative does not contain clear information to deduce a human error pathway and does not contain positive evidence of a non-human cause. This is a valid and expected determination. Prefer 003II over forcing a classification.

## Output

{"record_id": "", "L0_classification": "<001HE|002OC|003II>", "L0_label": "<2-6 word label>", "L0_description": "<1-3 sentence basis>"}