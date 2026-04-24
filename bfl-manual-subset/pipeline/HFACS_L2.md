# HFACS_L2

# Layer 2: Preconditions for Unsafe Acts

The Layer 1 unsafe acts for this record are provided in the user message.

## Precondition Test

A factor is coded at Layer 2 if it contributed to or enabled the Layer 1 unsafe act but did not itself produce the fatal outcome. Each L2 factor must directly relate to the specific L1 error identified above. A factor that was present but unrelated to the L1 act is not coded.

An empty L2 array is valid and expected. Most BFL narratives are short and do not contain enough detail to identify preconditions. Do not code a precondition to fill an empty array. Do not speculate about preconditions from routine BASE jumping circumstances.

---

## 201C - Conditions of the Jumper

Physical, mental, or cognitive conditions of the jumper that degraded performance or judgment and contributed to the unsafe act. These are states or conditions of the person, not actions or choices.

### 201C1 - Mental Awareness Conditions

Failures in how the jumper directed or managed attention during the task, that negatively affected perception, situational awareness, or task performance and contributed to the active failure. 

Common examples (not exhaustive):
- **Inattention/Complacency:** Failed to maintain sufficient situational awareness, including reduced alertness from high familiarity with a site, equipment, or procedure.
- **Channelized Attention/Fixation:** Focused attention on a limited number of cues to the exclusion of other critical information.
- **Task Saturation:** Demands exceeded mental capacity in the time available. Cognitively overloaded, not inattentive.
- **Distraction:** An external stimulus diverted attention at a critical moment.
- **Geographically Lost:** The jumper was at a different position relative to terrain than they believed. (e.g. wingsuit pilots flying another line than they think they fly or jumpers who jumped from the wrong exit point)

### 201C2 - State of Mind Conditions

Psychological or motivational states that affected judgment or willingness to act prudently contributing to the active failure. These are mental states or motivations that drove a poor decision or impaired judgement, not attention management failures (201C1) or physiological conditions (201C3).

Common examples (not exhaustive):
- **Psychological Disorder:** A diagnosable condition that impaired judgment or decision-making capacity.
- **Life Stressors/Emotional State:** External life circumstances impaired cognitive performance or judgment on the day.
- **Personality Style:** An enduring behavioral pattern that contributed to the unsafe act. Requires strong narrative evidence of a stable pattern, not a single-instance inference.
- **Overconfidence:** The jumper unreasonably overestimated their own capability relative to the specific task. Requires strong narrative evidence that the jumper acted in a manner inconsistent with what a reasonable jumper in a similar situation would have done (their overestimation is above and beyond). Do not infer from the outcome alone.
- **Pressure/Haste/Misplaced Motivation:** A clearly identifiable pressure or motivation, separate from the merits of the decision itself, drove the jumper to proceed. Requires strong narrative evidence that the jumper felt compelled to proceed.

### 201C3 - Adverse Physiological Conditions

Physical or physiological conditions that degraded performance capacity and contributed to the unsafe act. Things that that impaired the condition of the jumpers physical or cognitive capabilities.

Common examples (not exhaustive):
- **Substance Effects:** Performance impaired by alcohol, drugs, or medication.
- **Physical Illness/Injury:** A pre-existing illness or injury degraded performance.
- **Physical Overexertion:** Acute physical overexertion immediately before or during the jump degraded performance. Needs strong narrative evidence that it was causally contributing and not just the merits itself. Distinct from Fatigue, which is general and sleep-related.
- **Fatigue:** General fatigue from sleep deprivation that negatively affected performance.
- **Anthropometric/Biomechanical Limitations:** Physical characteristics insufficient for the specific demands of the task.
- **Dehydration/Poor Nutrition:** Nutritional state or hydration level negatively affected performance.
- **Startle Response/Freeze:** An automatic physiological response triggered by an unexpected event, resulting in temporary inability to act.
- **Spatial Disorientation:** Sensory systems failed to correctly perceive position, motion, or orientation relative to terrain. Includes *visual illusions* (e.g. flat light, snow cover, featureless terrain) that caused the jumper to misperceive altitude, distance, or terrain proximity,  and *vestibular disorientation* leading to loss of spatial orientation due to tumble, spin, or in visually impoverished conditions.

---

## 202P - Planning/Coordination Conditions

Failures in preparatory actions, planning, or coordination that created conditions enabling the unsafe act. These are things the jumper did or failed to do before the jump, not states of the person (201C) or skill level (203T).

### 202P1 - Jump Preparation and Communication

Failures in the jumper's immediate pre-jump preparation or coordination that created conditions enabling the unsafe act. The absence of additional or extra preparation is not a preparation failure. Code only when the jumper failed to perform or performed inadequately a specific preparatory action that accepted practice requires and that would have prevented or detected the condition leading to the L1 error.

Common examples (not exhaustive):
- Failure to perform a pre-jump gear check that would have caught the L1 factor
- Inadequate equipment configuration for the planned jump
- Inadequate briefing or coordination in group jumps

### 202P2 - Failure to Correct Known Deficiency

The jumper was aware of a recurring problem through personal experience, near-misses, or feedback from others and failed to take corrective action. This is a sustained pattern of inaction over time, not a single-instance preparation failure (which is 202P1).

Common examples (not exhaustive):
- Failure to correct a recurring performance issue despite awareness
- Progressively riskier behavior clearly exceeding accepted norms (normalization of deviance)
- Failure to correct a known equipment problem over an extended period

---

## 203T - Training Conditions

The jumper’s training, experience, or currency was clearly insufficient for the specific task attempted, and this insufficiency contributed to the L1 error. Codes the state of the jumper’s capability at the time of the fatal jump. Distinct from 202P (specific preparatory actions) and 201C (temporary states). If the L1 error could plausibly also have occurred in a fully trained jumper, do not code 203T.

Common examples (not exhaustive):

- **Insufficient Skydiving Experience:** Attempted BASE jumping or advanced BASE disciplines with clearly insufficient skydiving experience.
- **Insufficient BASE Experience:** Attempted an advanced BASE discipline or task that requires a substantially higher BASE experience level than the jumper had, per widely accepted BASE progression norms. Do not code merely because the jump was challenging.
- **Lack of BASE Specific Training:** Attempted BASE jumping without accepted training (first jump course, competent mentor).
- **Lack of Currency:** Previously trained to proficiency but had not performed the relevant activity for an extended period explicitly stated in the narrative. Do not infer lack of currency from context.
- **Insufficient Knowledge:** The narrative positively establishes that the specific decision reflects a knowledge gap that accepted BASE education would have corrected. Do not infer from the decision being wrong that the jumper must have lacked knowledge.

---

## 204E - Environmental Conditions

An environmental factor present during the jump that actively degraded the jumper’s execution and directly contributed to the L1 unsafe act. The environment must have directly impaired performance (physiologically, mechanically, or perceptually), not merely been the setting in which the error occurred. The narrative must describe how the environmental factor degraded a specific aspect of execution, not merely state that it was present at the time of the error.

If the narrative frames the environmental condition as something the jumper should have assessed and declined to jump in, the condition is decision content at Layer 1 and is not coded here, regardless which L1 category is assigned.

Common examples (not exhaustive):
- Exit surface condition (ice, wet rock, loose debris…) that degraded exit performance
- In-flight atmospheric disturbance (turbulence, rotor, gust, thermal…) degraded the jumper's ability to maintain body position, heading, or canopy control.
- Degraded visual conditions (flat light, fog, sun glare).. that impaired ability to assess terrain proximity, or maintain orientation.
- Ambient temperature effect that physically degraded execution capacity

---

## Output

{"record_id": "", "L2_preconditions": [{"category": "<201C|202P|203T|204E>", "subcategory": "<201C1|201C2|201C3|202P1|202P2|null>", "label": "<reference label or custom 2-6 word label>", "linked_L1": "<101D|102S>", "description": "<1-3 sentences grounded in narrative evidence>"}]}

subcategory is null for 203T and 204E. Empty array is valid when no preconditions are supported.