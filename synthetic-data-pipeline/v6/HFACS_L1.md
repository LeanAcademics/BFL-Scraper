# L1 Active Failures

**Active Failure Test**

A factor is coded at Layer 1 if its direct effect produced the fatal outcome. The question is: was this factor the mechanism through which the jumper died?

An action qualifies when the action itself generated the conditions that killed the jumper. A pre-jump decision qualifies as a Layer 1 active failure only if the decision alone was sufficient to produce the fatal outcome regardless of subsequent execution quality. If the jumper could have survived by executing correctly after making the decision, the decision is a precondition (Layer 2) and the execution failure is the Layer 1 active failure. The counterfactual asks whether correct execution would have produced survival, not whether correct execution was realistic given the jumper's actual skill level. A training deficit or pattern of inaction that made correct execution unlikely is coded at Layer 2, not promoted to Layer 1

An omission qualifies as an active failure only if the omission itself is the mechanism that produced the fatal outcome. An omission that would merely have detected or prevented a separate producing failure is not an active failure.

When multiple factors are present, identify which factor or factors actually produced the fatal outcome through their own direct effect. These are coded at Layer 1. All other contributing factors are candidates for Layer 2.

Identify the unsafe act or acts that produced the fatal outcome. When coding multiple unsafe acts, each entry must describe a distinct action or failure. Do not code the same act twice under different labels. If the narrative supports the category but not a specific characterization, report only the category (101D, 102S, 103II).

## 1.1 Decision Errors (101D)

The jumper consciously selected a course of action that was inadequate or inappropriate for the situation. The decision proceeded as intended, but the decision itself was the problem. This includes both decisions made before the jump (planning-level decisions that were the direct producing mechanism, not merely preconditions) and decisions made during the jump under time pressure.

Note that a decision to jump only qualifies if this would have lead to the fatal outcome regardless of subsequent execution quality. If the jump was merely to challenging for the jumper it is a skill-based-error (102S) not a decision error.

Common Examples:

- **Wrong procedure applied:** The jumper applied an incorrect procedure to a recognized situation.
- **Poor judgment or risk acceptance:** The jumper selected an inappropriate course of action in a situation requiring judgment.
- **Improvised response to novel situation:** The jumper faced a compound or cascading emergency for which no practiced procedure existed and devised a real-time solution that proved inadequate.

## 1.2 Performance/Skill-Based Errors (102S)

The jumper intended the correct outcome and selected an appropriate course of action, but failed in the physical or cognitive execution. The failed execution itself produced the fatal outcome.

Common Examples:

- **Attention failure:** The jumper failed to monitor or respond to critical information during execution. The information was available but the jumper did not attend to it
- **Memory failure:** The jumper failed to perform an action they knew to be necessary and intended to perform. Coded only if the omission was the direct active cause for the fatal outcome.
- **Technique error:** The jumper attempted the correct action but executed it with inadequate technique.

## 1.4 Insufficient Information (103II)

The narrative is too short, vague, or ambiguous to determine one or multiple active human errors present.

Provide a brief qualitative description of what the narrative states about the circumstances of the fatal outcome, without coding any specific unsafe act category.

At L1, 103II means human error is established but the narrative does not provide enough detail to distinguish whether the error was a decision error or a skill-based error. If the narrative makes clear that a human error occurred, code 103II rather than forcing a specific category.

## Output Instructions

Return JSON only. No markdown, no code fences, no text outside the JSON.

{
"record_id": "<BFL record id>",
"L1_unsafe_acts": [
{
"category": "<101D|102S|103II>",
"label": "<reference label or custom 3-5 word label>",
"description": "<1-3 sentences, grounded in narrative evidence>"
}
]
}
