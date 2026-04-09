# Layer 0: Top-Level Classification

Determine the most applicable class of the fatality report. The categories 001HE, 002OC, 003II are mutually exclusive, only select one. Use the domain reference provided in this context to understand BASE jumping terminology, equipment, and accepted practice.

## 0.1 Human Error Present (001HE)

The narrative explicitly states or provides sufficient information to reasonably deduce that one or more human errors contributed to the fatal outcome. This includes cases where the domain reference makes a human error pathway deducible even when the narrative does not explicitly state it.

## 0.2 Other Cause (002OC)

The narrative contains positive evidence that the fatal outcome resulted from factors outside the jumper's reasonable control or anticipation. Absence of human error language does not qualify. There must be affirmative evidence pointing to a non-human-error cause. No HFACS coding is applied. The cause is reported descriptively.

002OC applies when the narrative supports one or more of the following:

1. **Unforeseeable environmental event:** Unsafe conditions that were not identifiable as unsafe before or at the time of the jump, given what a competent BASE jumper could reasonably have assessed from the exit point. If the conditions were observable or forecastable before the jump and the jumper decided to jump anyway, the decision is a human error (001HE), not an other cause. 002OC applies only when the environmental factor was genuinely unforeseeable, such as sudden unexpected wind shear, a localized gust undetectable from the exit point, or a thermal event with no surface indicators.
2. **Equipment failure independent of human error:** A material or mechanical failure of equipment that was not caused by the jumper's packing, rigging, assembly, maintenance, modification, or equipment selection. If the jumper packed incorrectly, misrigged, used inappropriate gear for the jump, or failed to maintain equipment, the equipment failure is a consequence of human error (001HE). 002OC applies only when the equipment was correctly packed, rigged, and maintained according to accepted practice, and the failure resulted from a manufacturing defect, material fatigue not detectable through normal inspection, or an inherent design limitation that the jumper could not reasonably have known about.
3. **Other non-human cause:** Any other cause supported by positive evidence in the narrative where the jumper acted within accepted practice and the fatal outcome resulted from a factor the jumper could not reasonably have anticipated or controlled.

## 0.3 Insufficient Information (003II)

Neither 001HE nor 002OC can be supported by the narrative. The narrative does not contain sufficient information to reasonably deduce a human error pathway (001HE) and does not contain positive evidence of a non-human cause (002OC). No HFACS coding is applied. The record is reported as unclassifiable. This is a valid and expected determination. Prefer coding 003II over forcing a classification you are not confident about.

## Output Format

Return valid JSON only:

```
{"record_id": "<BFL number>", "L0_classification": "<001HE|002OC|003II>", "L0_description": "<1-3 sentence basis for classification>"}
```