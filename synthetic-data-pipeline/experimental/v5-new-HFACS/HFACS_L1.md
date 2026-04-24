# L1 Active Failures

At L1 active failures / unsafe acts are factors where the jumper made an error that directly produced the fatal outcome. The Test: Would this factor alone have produced the fatal outcome, even if no other error or failure were present?

Identify the unsafe act or acts that produced the fatal outcome. When coding multiple unsafe acts, each entry must describe a distinct action or failure. Do not code the same act twice under different labels.

## (101D) – Decision Errors

The jumper consciously selected a course of action that was inadequate or inappropriate for the situation. The decision proceeded as intended, but the decision itself was the problem.

## (102S) – Performance/Skill-Based Errors

The jumper intended the correct outcome and selected an appropriate course of action, but failed in the physical or cognitive execution. The plan was adequate. The performance was not.

## (104II) – Insufficient Information

The narrative is too short, vague, or ambiguous to determine one or multiple active human errors present.

Provide a brief qualitative description of what the narrative states about the circumstances of the fatal outcome, without coding any specific unsafe act category.

At L1, 104II means human error is established but the narrative does not provide enough detail to distinguish whether the error was a decision error or a performance/skill-based error. If the narrative makes clear that a human error occurred, code 104II rather than forcing a specific category.

## Output Instructions

Return JSON only. No markdown, no code fences, no text outside the JSON.

{
"record_id": "<BFL record id>",
"L1_unsafe_acts": [
{
"category": "<101D|102S|104II>",
"label": "<reference label or custom 3-5 word label>",
"description": "<1-3 sentences, grounded in narrative evidence>"
}
]
}