# L2 Preconditions for Unsafe Acts

A factor is coded at Layer 2 if it contributed to or enabled the Layer 1 unsafe act identified above, but its own direct effect was not the mechanism that produced the fatal outcome.

An empty L2_preconditions array is a valid and expected outcome. Many narratives do not provide sufficient detail to identify preconditions for the identified unsafe act. Do not code a precondition to avoid an empty array. If the narrative does not support any precondition for the L1 act, return an empty array

## (201C) – Conditions of the Jumper

Physical, mental, or cognitive conditions of the individual jumper that degraded performance or judgment and contributed to the unsafe act. These are states or conditions of the person, not actions or choices.

### (201C1) – Mental Awareness Conditions

Failures in the jumper’s attention management that negatively affected perception, situational awareness, or task performance and contributed to the unsafe act. Failures in how the jumper directed or managed attention during the task.

### (201C2) – State of Mind Conditions

Psychological or motivational states that affected the jumper’s judgment or willingness to act prudently, contributing to the unsafe act. They are mental states or motivations that drove a poor decision or impaired judgement.

### (201C3) – Adverse Physiological Conditions

Physical or physiological conditions of the jumper that degraded performance capacity and contributed to the unsafe act. Things that that impaired the condition of the jumpers physical or cognitive capabilities.

## (202P) – Planning/Coordination Conditions

Failures in the jumper’s specific preparatory actions, planning, coordination with other jumpers, or self-correction of known issues., that created the conditions enabling the unsafe act.

### (202P1) – Jump Preparation and Communication

Failures in the jumper's immediate pre-jump preparation or coordination required by accepted practice that created conditions enabling the unsafe act. The absence of additional or extra preparation is not a preparation failure

### (202P2) – Failure to Correct Known Deficiency

The jumper was aware of a sustained recurring problem and failed to correct it. Applies to patterns of deficiencies present and uncorrected over a sustained period of time, not merely single events.

## (203T) – Training Conditions

The jumper's training, experience, or knowledge was clearly insufficient for the specific task attempted on the fatal jump, and this insufficiency enabled the L1 error. Code 203T only when the L1 error is attributable to a capability gap the jumper's training history would have closed. If the L1 error would plausibly have occurred in a fully trained jumper, do not code 203T. 203T codes a long-term capability state, not preparation for the specific jump, which is 202P1.

203T Relates to long-term training, not preperation for single specific jumps which is coded in 202P.

## (204E) – Environmental Conditions

An environmental factor present during the jump that actively degraded the jumper's execution of the Layer 1 unsafe act. The environment must have directly impaired performance (physiologically, mechanically, or perceptually), not merely been the setting in which the error occurred. The narrative must describe how the environmental factor degraded a specific aspect of execution, not merely state that it was present at the time of the error.

If the narrative frames the environmental condition as something the jumper should have assessed and declined to jump in, the condition is the content of a decision error at Layer 1 and is not coded here, regardless which L1 category is assigned. If the narrative frames the condition as an execution hazard that affected how the jumper performed, code 204E.

## Output Instructions

Return JSON only. No markdown, no code fences, no text outside the JSON.

{
"record_id": "<BFL record id>",
"L2_preconditions": [
{
"category": "<201C|202P|203T|204E>",
"subcategory": "<201C1|201C2|201C3|202P1|202P2|null>",
"label": "<reference label or custom 3-8 word label>",
"linked_L1": "<101D|102S>",
"description": "<1-3 sentences, grounded in narrative evidence>"
}
]
}

subcategory is null for 203T and 204E. Empty array is valid when no preconditions are supported.