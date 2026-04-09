# Layer 1: Unsafe Acts

## Active Failure Test

A factor is coded at Layer 1 if its direct effect produced the fatal outcome. The question is: was this factor the mechanism through which the jumper died?

An action qualifies when the action itself generated the conditions that killed the jumper. A decision to jump in unsafe conditions qualifies because the decision placed the jumper in the lethal situation. A misrouted bridle qualifies because the misrouting produced the deployment failure.

An omission qualifies as an active failure only if the omitted action would itself have produced a safe outcome. Failing to deploy the parachute qualifies because deploying would have produced survival.

An omission that would merely have detected or prevented a separate producing failure is not an active failure. Omitting a gear check that would have caught a packing error did not produce the deployment failure; the packing error did. The omitted gear check is a precondition (Layer 2), not an unsafe act.

When multiple factors are present, identify which factor or factors actually produced the fatal outcome through their own direct effect. These are coded at Layer 1. All other contributing factors are candidates for Layer 2.

## Category Discrimination

Layer 1 has three categories of unsafe acts, distinguished by where the failure lies:

- **Decision Errors (101D):** The jumper's chosen course of action was wrong for the situation. The problem was the plan, the choice, or the decision, not the execution.
- **Skill-Based Errors (102S):** The jumper's chosen course of action was appropriate but execution failed. The problem was physical or cognitive performance, not what was decided.
- **Perceptual Errors (103O):** The jumper acted on a false sensory perception caused by a specific identifiable perceptual mechanism. The action was consistent with what the jumper perceived, but perception did not match reality.

Apply this axis first: Was the problem in what the jumper decided, in how the jumper executed, or in what the jumper perceived?

Identify all applicable unsafe acts from the following categories. For each, report the most suitable subcategory or multiple subcategories if distinct. When coding multiple unsafe acts, each entry must describe a distinct action or failure. Do not code the same act twice under different labels. If the narrative supports the category but not a specific subcategory, report only the category (101D, 102S, 103O, 104II).

## 1.1 Decision Errors (101D)

The jumper consciously selected a course of action that was inadequate or inappropriate for the situation. The decision proceeded as intended, but the decision itself was the problem. This includes both decisions made before the jump (planning-level decisions that were the direct producing mechanism, not merely preconditions) and decisions made during the jump under time pressure.

If the jumper decided to jump in adverse conditions that were observable before the jump (weather, wind, visibility, site hazards), the conditions are the content of this decision error and are not coded under Environmental Conditions 204E. If the jumper decided to proceed with the jump rather than abort and hike down despite conditions warranting an abort, this is a decision error.

The following labels are provided as reference. Report the most applicable label if one fits, or describe the decision error in your own terms.

- **Wrong procedure applied:** The jumper applied an incorrect defined procedure to a recognized situation, such as the wrong emergency response to a malfunction type, or an incorrect packing configuration for the jump type.
- **Poor judgment or risk acceptance:** The jumper selected an inappropriate course of action in a situation requiring judgment. This includes choosing to jump in conditions that exceed safe limits, selecting an object beyond the jumper's current ability, choosing a flight line with insufficient margin, attempting maneuvers without sufficient proficiency, or choosing to deploy at a dangerously low altitude.
- **Improvised response to novel situation:** The jumper faced a compound or cascading emergency for which no practiced procedure existed and devised a real-time solution that proved inadequate.

## 1.2 Skill-Based Errors (102S)

The jumper intended the correct outcome and selected an appropriate course of action, but failed in the physical or cognitive execution. The plan was adequate. The performance was not.

The following labels are provided as reference. Report the most applicable label if one fits cleanly, or describe the skill-based error in your own terms.

- **Attention failure:** The jumper failed to monitor or respond to critical information during execution. The information was available but the jumper did not attend to it. Includes losing altitude awareness during freefall and failing to assess terrain proximity during wingsuit flight.
- **Memory failure:** The jumper failed to perform an action they knew to be necessary and intended to perform. This is not about forgetting a step in a formal checklist but about failing to carry out something the jumper would have done if reminded. Includes forgetting to connect the pilot chute to the bridle after a repack, leaving a packing tool inside the container, or forgetting a planned deployment altitude. Coded here only if the omission produced the fatal outcome (see Active Failure Test).
- **Technique error:** The jumper attempted the correct action but executed it with inadequate technique. Includes poor body position at exit or deployment, incorrect packing technique, weak pilot chute throw, and poor tracking or flight technique resulting in insufficient separation.

## 1.3 Perceptual Errors (103O)

Do not code 103O unless the narrative identifies or clearly implies a specific perceptual mechanism that distorted the jumper's perception. General misjudgment of altitude, distance, or speed without a stated perceptual cause is a decision error (101D) or skill-based error (102S), not a perceptual error.

A perceptual error is coded when the jumper's action or inaction was based on a false perception of the environment produced by a specific sensory distortion. The jumper acted consistently with what they perceived, but their perception did not match reality. The error is the action taken on faulty sensory input, not the sensory degradation itself (which is coded as a precondition under Adverse Physiological Conditions 201C3 if applicable).

Qualifying perceptual mechanisms include:

- **Visual illusion:** Environmental conditions (flat light, snow cover, leafless vegetation, featureless terrain, fog blending sky and ground) caused the jumper to misperceive altitude, distance, or terrain proximity. The jumper flew or deployed at what they believed was a safe altitude or distance, but the visual environment made the terrain appear farther than it was.
- **Vestibular/spatial disorientation:** Loss of spatial orientation during tumble, spin, or in visually impoverished conditions caused the jumper to misperceive their body position, heading, or proximity to the object. The jumper attempted to act (deploy, track, correct) based on a false sense of orientation.

If neither of these mechanisms (or an equivalent specific sensory distortion) is present in the narrative, do not code 103O.

## 1.4 Insufficient Information (104II)

The narrative is too short, vague, or ambiguous to determine one or multiple active human errors present.

Provide a brief qualitative description of what the narrative states about the circumstances of the fatal outcome, without coding any specific unsafe act category.

## Output Format

Return valid JSON only:

```
{"record_id": "<BFL number>", "L1_unsafe_acts": [{"category": "<101D|102S|103O>", "label": "<reference label or custom 3-8 word label>", "description": "<what the jumper did/failed to do that produced the fatal outcome, 2-4 sentences>"}], "L1_insufficient": <true|false>}
```

If 104II: L1_unsafe_acts is an empty array and L1_insufficient is true.