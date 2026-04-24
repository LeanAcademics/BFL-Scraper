# HFACS_L1

# Layer 1: Unsafe Acts

Identify the unsafe act(s) that produced the fatal outcome.

## Active Failure Test

A factor is coded at Layer 1 if it was the mechanism through which the jumper died.

An action qualifies when the error itself generated the conditions that killed the jumper. An omission qualifies as an active failure only if the omitted action would itself have directly produced survival (e.g. failing to deploy the parachute). 

An omission that would have detected or prevented a separate error is not an active failure but a precondition (Layer 2).

When multiple factors are present, identify which factor(s) actually produced the fatal outcome through their own direct effect. All other contributing factors are candidates for Layer 2.

## Category Discrimination

Apply this axis first: Was the problem in what the jumper decided, or in how the jumper executed?

If the fatal outcome resulted from how the jumper performed during the task rather than from the choice of task itself, the error is 102S. The difficulty or risk level of the chosen task does not make the decision a decision error. If the jumper could have survived this jump with correct execution, code 102S — even if the jumper should not have attempted the jump at all.

## 101D - Decision Errors

The jumper consciously selected a course of action that was inadequate or inappropriate for the situation in a way that is independent of execution quality. The execution proceeded as intended, but the decision itself was the problem.

**Critical: 101D requires that the decision was clearly and specifically wrong, not merely that it involved risk.** BASE jumping is inherently dangerous. Every jumper decides to accept risk. Code 101D only when the narrative establishes that the specific decision was identifiably, substantially wrong given the information available to the jumper at the time, and that decision was the producing mechanism. The decision must stand out as a clear departure from what a competent jumper with the same information would have done.

Do not code 101D merely because the jumper decided to perform the jump and died. Do not code 101D because a different decision would have prevented the death. The specific decision, its parameters, or its context must be demonstrably inadequate.

Common examples (not exhaustive, classify based on the definition):
- Wrong procedure applied to a recognized situation
- Judgment or risk acceptance that was clearly and specifically inappropriate
- Improvised response to a novel or cascading emergency that proved inadequate

## 102S - Performance/Skill-Based Errors

The jumper intended the correct outcome and selected an appropriate course of action, but failed in the physical or cognitive execution. The performance was insufficient.

Common examples (not exhaustive, classify based on the definition):
- Attention failure: failed to monitor or respond to critical information available during execution
- Memory failure: failed to perform an action they knew to be necessary and intended to perform (coded only if the omission produced the fatal outcome)
- Technique error: Executed the attempted action with inadequate technique
- Execution error: Failed to execute the action as intended (includes unstable exit, missed pulls)

## 103II - Insufficient Information

Human error is established (L0 = 001HE) but the narrative does not provide enough detail to determine whether the error was a decision error or a performance error. Provide a brief description of what the narrative states about the circumstances.

## Output

{"record_id": "", "L1_unsafe_acts": [{"category": "<101D|102S|103II>", "label": "<reference label or custom 3-5 word label>", "description": "<1-3 sentences grounded in narrative evidence>"}]}