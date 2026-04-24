**Layer 2: Preconditions for Unsafe Acts**

The following unsafe acts were identified at Layer 1: **{L1 result inserted here}**

**Precondition (Layer 2) Test**

A factor is coded at Layer 2 if it contributed to or enabled the Layer 1 unsafe act identified above, but its own direct effect was not the mechanism that produced the fatal outcome.

Preconditions include:

- Conditions that degraded the jumper's capacity to perform correctly (fatigue, overconfidence, inexperience)
- Preparatory failures that created the conditions under which the L1 error occurred (inadequate site assessment, wrong equipment configuration)
- Omissions that failed to detect or prevent the L1 failure but did not themselves produce the outcome (omitted gear check, failure to correct a known deficiency)
- Environmental factors that impaired performance during execution

A precondition is coded only if it contributed to the specific Layer 1 unsafe act above. If no preconditions are supported by the narrative with sufficient evidence, return an empty L2_preconditions array. An empty array is a valid and expected outcome. Not all unsafe acts have identifiable preconditions in the narrative. Do not infer preconditions solely to avoid returning an empty result.

**Label Coding**

Each Layer 2 subcategory lists common examples. If an example fits the narrative, use or adapt it. If no example fits but the narrative clearly describes a precondition belonging to the parent group, create a short descriptive label (3-8 words). Do not create a new label that overlaps with an existing example.

### 2.1 Conditions of the Jumper (201C)

Physical, mental, or cognitive conditions of the individual jumper that degraded performance or judgment and contributed to the unsafe act. These are states or conditions of the person, not actions or choices. Distinct from Planning/Coordination (which codes preparatory actions the jumper failed to take) and from Training (which codes the jumper's skill/experience level). Here, the jumper's body or mind was in a degraded state that impaired their ability to perform or decide.

**201C1 vs 201C2 discrimination:** 201C1 codes failures in how the jumper directed or managed cognitive attention during the task. 201C2 codes the jumper's psychological or motivational disposition that affected judgment or willingness to act prudently. If the narrative describes attention going to the wrong place or failing to be maintained, code 201C1. If the narrative describes a mental state or motivation that drove a poor decision or impaired judgment, code 201C2.

#### 2.1.1 Mental Awareness Conditions (201C1)

Failures in the jumper's attention management that negatively affected perception, situational awareness, or task performance and contributed to the unsafe act. Common examples:

- **Inattention/Complacency:** Failed to maintain sufficient readiness or situational awareness, including reduced alertness from high familiarity.
- **Channelized Attention/Fixation:** Focused all attention on a limited number of cues to the exclusion of other critical information.
- **Task Saturation:** Demands exceeded mental capacity in the time available.
- **Distraction:** An external stimulus diverted attention from the primary task at a critical moment.
- **Geographically Lost:** The jumper was at a different position relative to terrain than they believed.

#### 2.1.2 State of Mind Conditions (201C2)

Psychological or motivational states that affected the jumper's judgment or willingness to act prudently, contributing to the unsafe act. Common examples:

- **Psychological Disorder:** A diagnosable condition that impaired judgment or decision-making capacity.
- **Life Stressors/Emotional State:** External life circumstances impaired cognitive performance or judgment on the day.
- **Personality Style:** An enduring behavioral pattern that contributed to the unsafe act. Requires strong narrative evidence of a stable pattern, not a single-instance inference.
- **Overconfidence:** The jumper unreasonably overestimated their own capability relative to the specific task. Requires narrative evidence such as dismissing warnings, rejecting advice, or making statements contradicted by their experience level. Do not infer overconfidence from the fact that the jumper attempted the task and failed.
- **Pressure/Haste/Misplaced Motivation:** The motivation to proceed was driven by factors other than a sound assessment of readiness and conditions. Requires narrative evidence that the jumper felt compelled to proceed despite recognizing conditions or readiness were inadequate.

#### 2.1.3 Adverse Physiological Conditions (201C3)

Physical or physiological conditions of the jumper that degraded performance capacity and contributed to the unsafe act. Common examples:

- **Substance Effects:** Performance impaired by alcohol, drugs, or medication.
- **Physical Illness/Injury:** A pre-existing illness or injury degraded performance.
- **Physical Overexertion:** Acute physical overexertion immediately before or during the jump degraded performance. Distinct from Fatigue, which is general and sleep-related.
- **Fatigue:** General fatigue from sleep deprivation that negatively affected performance.
- **Anthropometric/Biomechanical Limitations:** Physical characteristics insufficient for the specific demands of the task.
- **Dehydration/Poor Nutrition:** Nutritional state or hydration level negatively affected performance.
- **Startle Response/Freeze:** An automatic physiological response triggered by an unexpected event, resulting in temporary inability to act.
- **Spatial Disorientation:** Sensory systems failed to correctly perceive position, motion, or orientation relative to terrain. Code Spatial Disorientation only if Perceptual Error (103O) was identified in the Layer 1 results above. If 103O was not identified at Layer 1, do not code Spatial Disorientation here.

### 2.2 Planning/Coordination Conditions (202P)

Failures in the jumper's preparatory actions, planning, or coordination with other jumpers that created the conditions enabling the unsafe act. These are things the jumper did or failed to do before the jump, not states of the jumper's body or mind (which fall under Conditions of the Jumper) and not the jumper's skill level (which falls under Training). A planning failure is coded when the jumper should have taken a specific preparatory action and did not. If a preparatory failure was the direct causal link to the fatal outcome with no other actively causal intervening action, it is coded at Layer 1, not here.

#### 2.2.1 Jump Preparation and Communication (202P1)

Failures in the jumper's immediate pre-jump preparation or coordination that created conditions enabling the unsafe act. Code only when the jumper omitted a specific preparatory action that accepted practice requires and that would have prevented or detected the condition enabling the L1 error. Routine BASE activities (jumping from a new exit, flying an unfamiliar line, hiking a long approach) are not preparation failures. Common examples:

- Failure to perform a pre-jump gear check.
- Inadequate site assessment for hazards.
- Inadequate equipment configuration for the planned jump.
- Inadequate briefing or coordination in group jumps.

#### 2.2.2 Failure to Correct Known Deficiency (202P2)

The jumper was aware of a recurring problem through personal experience, near-misses, or feedback from others, and failed to take corrective action such as additional training, returning to skydiving to practice, or adjusting behavior. This is a sustained pattern of inaction, not a single-instance preparation failure (which falls under Jump Preparation 202P1). This category codes the sustained preparatory failure itself: the pattern of knowing about a problem and not addressing it.

Includes normalization of deviance: the gradual acceptance of progressively riskier behavior as the jumper's personal standard.

### 2.3 Training Conditions (203T)

The jumper's training, experience, or currency was insufficient for the demands of the specific task, contributing to the unsafe act. This codes the state of the jumper's capability at the time of the fatal jump, not the process of how they arrived at that state (which is coded under Planning/Coordination if a failure to correct is identified). Distinct from Conditions of the Jumper (which codes temporary physical or mental states) and from Planning/Coordination (which codes specific preparatory actions not taken). Here, the jumper's baseline skill or experience level was inadequate regardless of their state on the day. This can be derived from explicit statements in the narrative or from clear implicit information suggesting the task exceeded what is considered appropriate for the jumper's level according to accepted BASE progression norms.

### 2.4 Environmental Conditions (204E)

Environmental factors that directly degraded the jumper's performance during execution and contributed to the identified Layer 1 unsafe act. Code 204E only if all three of the following conditions are met:

1. The environmental factor is not already captured as the content of a Layer 1 decision error. If the environmental conditions are coded as the basis of a 101D act, the same factor is not additionally coded as 204E. If the environmental factor contributed to a Layer 1 act of a different category (102S or 103O), it may be coded as 204E because L1 and L2 are describing different things: the error and the condition that degraded performance.
2. The environmental factor degraded the jumper's performance during execution of the L1 factor. The environment must have actively impaired the jumper's ability to perform, not merely been the setting in which an error occurred.
3. The environmental factor contributed to the specific Layer 1 unsafe act identified above.

If any of these three conditions is not met, do not code 204E.

Examples: unexpected wind shear or turbulence during flight that was not forecastable from the exit point, sudden fog or cloud engulfment during descent, thermal activity that could not have been anticipated.

## Output Format

Return valid JSON only:

```
{"record_id": "<BFL number>", "L2_preconditions": [{"category": "<201C|202P|203T|204E>", "subcategory": "<201C1|201C2|201C3|202P1|202P2|203T|204E|null>", "label": "<reference label or custom 3-8 word label>", "linked_L1": "<101D|102S|103O>", "description": "<how this precondition contributed to the L1 unsafe act, 1-3 sentences>"}]}
```

L2_preconditions can be an empty array if no preconditions are supported by the narrative.
