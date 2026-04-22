# v7 Pipeline — Per-Record Results

Pipeline output paired with ground truth for each of the 30 synthetic records.

---

## SYN-CS01

### L0 ✓

- **Pipeline:** `001HE` — The jumper chose to exit in clearly dangerous wind conditions—sustained strong gusts with flags horizontal—after companions declined to jump and explicitly warned him. The wind overpowered his canopy and drove him into the wall. The conditions were observable and assessed as unsafe by peers before the jump, making the decision to jump a human error.
- **Ground truth:** `001HE`

### L1 ✓

**Pipeline:**
- `101D` — **Jumped in clearly excessive winds**
  > The jumper launched in conditions that were explicitly identified as terrible by his companions, with sustained strong gusts and horizontal flags at the restaurant (indicating winds well above any safe threshold for BASE). Two companions declined to jump and directly warned him. The wind overpowered his canopy's forward penetration capability, pushing him back into the wall. The decision to jump in these conditions was the producing mechanism for the fatality — execution was adequate (good exit, on-heading opening, full flight attempting to penetrate), but no amount of skill could overcome wind that exceeded the canopy's airspeed.

**Ground truth:**
- `101D` — Decided to jump in known high winds

### L2 ✓

**Pipeline:**
- `201C2` → `101D` — **Pressure/Haste/Misplaced Motivation**
  > The narrative explicitly states Brett was on his last day in Lauterbrunnen and 'desperate to get one final jump in before his flight home the next morning.' This last-chance urgency was a clearly identifiable pressure, separate from the merits of the wind assessment, that drove him to proceed despite companions warning him and walking down.

**Ground truth:**
- `201C2` → `101D` — Pressure/Haste, flight home tomorrow, last chance, pressed forward after group stood down

---

## SYN-CS02

### L0 ✓

- **Pipeline:** `001HE` — The bridle was misrouted around the right leg strap during packing/rigging, preventing canopy extraction and causing a total malfunction (PC in tow). This is a rigging error — a clear human error. Additionally, neither the jumper nor his partner performed a gear check that would have caught the misrouting.
- **Ground truth:** `001HE`

### L1 ✓

**Pipeline:**
- `102S` — **Bridle misrouted during packing**
  > The jumper routed the bridle around the right leg strap during packing, preventing the pilot chute from extracting the canopy. This rigging error directly produced a total malfunction (PC in tow with container closed), which was the mechanism of death. The jumper intended correct rigging but failed in execution, likely due to rushing through the packing process.

**Ground truth:**
- `102S` — Misrouted bridle during gearing up

### L2 ✗

**Pipeline:**
- `202P1` → `102S` — **Failure to perform gear check**
  > Neither the jumper nor his companion performed a pre-jump gear check. The companion explicitly states that running a hand along the bridle routing would have immediately caught the misrouted bridle. This omission allowed the rigging error made during packing to persist undetected to the exit.

**Ground truth:**
- `202P1` → `102S` — Omitted gear check before exit
- `201C2` → `102S` — Haste, rushing to catch early morning conditions

---

## SYN-CS03

### L0 ✓

- **Pipeline:** `001HE` — The jumper chose to fly a wingsuit proximity line in flat-light conditions (snow, no shadows, no contrast, no texture) that eliminated depth perception cues, resulting in complete loss of altitude awareness and controlled flight into terrain. The decision to fly proximity in conditions that destroyed visual altitude references constitutes a human error — flat light over snow is a well-known hazard that was observable before exit and made proximity flying unmanageable.
- **Ground truth:** `001HE`

### L1 ✓

**Pipeline:**
- `101D` — **Flying proximity in flat light conditions**
  > The jumper chose to fly a wingsuit proximity line on a day with heavy fresh snow, no shadows, no contrast, and no texture on the snowfield — complete flat light conditions. These conditions are known to eliminate depth cues essential for terrain flying. The decision to fly proximity to terrain in conditions that made altitude assessment impossible was the producing mechanism: he could not perceive his altitude and flew into the ground at full speed with no deployment attempt. This was not an execution error — his flight technique was textbook — but the decision to fly near terrain when visual depth perception was fundamentally compromised was clearly and specifically inadequate.

**Ground truth:**
- `101D` — Decided to fly wingsuit line in flat light with no depth cues

### L2 ✗

**Pipeline:**
- `201C3` → `101D` — **Spatial Disorientation**
  > Complete flat light conditions — heavy fresh snow, no shadows, no contrast, no texture on the snowfield — created a visual illusion that eliminated all depth cues. The helmet cam confirms he perceived himself to be much higher than he was, maintaining a relaxed posture with zero corrective input until impact. This visual illusion directly caused the fatal altitude misperception that the decision to fly in flat light enabled.
- `204E` → `101D` — **Flat Light Eliminating Depth Cues**
  > Heavy fresh snow with no shadows, contrast, or texture on the snowfield created complete flat light that physically eliminated the visual depth cues required for terrain proximity assessment. This environmental condition directly degraded the jumper's ability to perceive altitude and terrain proximity during flight, making the consequences of the decision to fly proximity in these conditions unsurvivable.

**Ground truth:**
- _(empty)_

---

## SYN-CS04

### L0 ✓

- **Pipeline:** `002OC` — The fatality resulted from a latent manufacturing defect in the harness webbing (incorrect heat treatment during production) that caused the main lift web to fail during canopy flight. The defect was undetectable without destructive testing, the manufacturer confirmed the defective batch and issued a recall, and the jumper's packing, rigging, maintenance, inspection, and execution were all correct. This is an equipment failure independent of human error.
- **Ground truth:** `002OC`

---

## SYN-CS05

### L0 ✓

- **Pipeline:** `002OC` — The jumper executed all phases correctly—stable exit, good track, on-heading opening with separation from the wall. A sudden localized rotor caused by a temperature inversion and differential heating violently collapsed his canopy approximately three seconds after inflation, turning him into the wall with no time to react. Meteorologists confirmed the event could not have been predicted or detected from the exit point, and no wind indicators showed movement before or after the jump. This constitutes an unforeseeable environmental event outside the jumper's reasonable control.
- **Ground truth:** `002OC`

---

## SYN-CS06

### L0 ✓

- **Pipeline:** `002OC` — The jumper suffered a massive brainstem stroke caused by a congenital arterial malformation that had never produced symptoms, resulting in instant incapacitation and inability to deploy his parachute. He had no prior medical history and a clean physical two months prior. This was an unforeseeable sudden medical event outside the jumper's reasonable control or anticipation, with no human error contributing to the outcome.
- **Ground truth:** `002OC`

---

## SYN-CS07

### L0 ✓

- **Pipeline:** `001HE` — Two clear human errors are identified: the jumper decided to jump in wind conditions (20 knots sustained, gusts over 30) that four experienced companions deemed unsafe and stood down from, and he then had an unstable exit in the crosswind gust and failed to prioritize deployment over stability recovery, resulting in subterminal impact with terrain.
- **Ground truth:** `001HE`

### L1 ✗

**Pipeline:**
- `101D` — **Jumped in clearly unsafe wind conditions**
  > The jumper chose to exit in 20-knot sustained winds with gusts well over 30 knots from the side, conditions that four experienced companions unanimously deemed unsafe and stood down from. The domain reference states few objects are good in winds over 10 mph and no objects are good over 20 mph; these conditions (35+ mph gusts) were far beyond any acceptable threshold. The crosswind gust caught him immediately on exit, pushing him sideways and back into the wall, directly producing the fatal impact.

**Ground truth:**
- `101D` — Decided to jump in known unsafe winds
- `102S` — Unstable exit with failure to deploy

### L2 ✗

**Pipeline:**
- _(empty — no preconditions identified)_

**Ground truth:**
- `201C2` → `101D` — Pressure/Haste, stayed behind after entire group stood down

---

## SYN-CS08

### L0 ✓

- **Pipeline:** `001HE` — Multiple human errors are clearly identifiable. The jumper jumped while severely impaired from heavy alcohol consumption (threw up twice, visibly unsteady, splitting headache), which degraded his physical coordination contributing to the unstable exit. He then failed to deploy his pilot chute during approximately 6 seconds of freefall, fixating on stability recovery instead of prioritizing deployment — a clear violation of the fundamental principle that deploying in any position is better than impact with nothing out.
- **Ground truth:** `001HE`

### L1 ✓

**Pipeline:**
- `102S` — **Failure to deploy parachute**
  > The jumper spent the entire freefall attempting to recover stability rather than deploying the pilot chute. Despite approximately 6 seconds of freefall from a slider-up cliff, he fixated on regaining a belly-to-earth position and never extracted the PC from the BOC, impacting the talus with the system still closed. The domain reference is explicit: whatever happens, pull — deploying low on your back with an off-heading is bad, but beats impact with nothing out. Priority order is (1) deploy, (2) deploy at the right altitude, (3) deploy in stable body position.
- `102S` — **Unstable exit with poor push-off**
  > The jumper's legs buckled on the push-off, producing an immediately unstable exit that rolled him onto his back into a slow tumble. This poor exit technique eliminated the separation and stable body position needed for a controlled deployment sequence, and consumed the limited freefall time with recovery attempts rather than deployment.

**Ground truth:**
- `102S` — Failed to deploy during unstable freefall

### L2 ✗

**Pipeline:**
- `201C3` → `102S` — **Substance Effects**
  > The jumper was heavily intoxicated the night before and still visibly impaired at the time of the jump — splitting headache, vomiting twice on the hike, visibly unsteady. This acute hangover state directly degraded his physical coordination, contributing to his legs buckling on the push-off and the resulting unstable exit.
- `201C1` → `102S` — **Channelized Attention/Fixation**
  > The jumper fixated entirely on recovering stability during freefall to the exclusion of the higher-priority task of deploying the parachute. This channelized attention on regaining a belly-to-earth position prevented him from executing the fundamental priority of pulling, despite approximately 6 seconds of available freefall time.
- `202P2` → `102S` — **Failure to Correct Known Deficiency**
  > The narrative states the jumper had jumped hung over before without issues and that the decision to jump impaired was not unusual for him. This indicates a sustained pattern of jumping while substance-impaired — a normalization of deviance that enabled the conditions present on this fatal jump.

**Ground truth:**
- `201C3` → `102S` — Adverse physiological state from heavy drinking
- `201C1` → `102S` — Fixation on stability recovery excluding deployment task
- `201C2` → `102S` — Pressing, told to stop, went anyway

---

## SYN-CS09

### L0 ✓

- **Pipeline:** `001HE` — Multiple human errors contributed to the fatal outcome. The jumper used a tracking suit on a cliff without adequate training (only 2 skydives in the suit, zero cliff jumps with it), chose an intermediate-to-advanced exit requiring effective tracking despite lacking the skill to fly the suit, ignored a more experienced jumper's suggestion to start with a more forgiving exit, and was visibly exhausted from driving 14 hours through the night. His inability to achieve forward separation in the tracking suit led directly to impact with terrain.
- **Ground truth:** `001HE`

### L1 ✗

**Pipeline:**
- `101D` — **Jumped unfamiliar suit at demanding site**
  > The jumper chose to jump a tracking suit from an intermediate-to-advanced cliff requiring mandatory tracking past a technical section where the wall comes back in, despite having only two skydives in the suit and zero cliff jumps with it. The domain reference establishes that a tracking suit requires 40-50 tracking suit skydives before BASE use, and the jumper must have found the ideal body position for maximum forward speed and glide before jumping it from a cliff. With only 2 skydives in the suit, the jumper lacked the foundational ability to fly it effectively, making the decision to use it at this site the producing mechanism for the fatal outcome — he could not generate the forward separation required to clear the technical section regardless of execution quality on the day.

**Ground truth:**
- `102S` — Failed to achieve forward drive in tracking suit

### L2 ✓

**Pipeline:**
- `203T` → `101D` — **Insufficient Tracking Suit Training**
  > The jumper had only 2 skydives in the tracking suit and zero cliff jumps with it. Accepted practice requires 40-50 tracking suit skydives before BASE use, with mastery of ideal body position for maximum forward speed and glide. This profound training deficit meant the jumper lacked the physical skill to fly the suit effectively, directly enabling the fatal outcome when he chose to jump it at this site.
- `201C3` → `101D` — **Physical Overexertion / Fatigue**
  > The jumper drove 14 hours straight through the night and was visibly exhausted at the exit point. This acute fatigue from sleep deprivation likely degraded his judgment capacity, contributing to his decision to proceed with the unfamiliar suit at a demanding site despite a more experienced jumper's suggestion to start with something more forgiving.
- `201C2` → `101D` — **Overconfidence from Video Observation**
  > The jumper dismissed a suggestion to start with a more forgiving exit, stating the site 'looked easy from the footage.' This indicates the jumper unreasonably overestimated his capability based on watching videos rather than actual experience, substituting vicarious observation for the progression experience he lacked with the tracking suit.

**Ground truth:**
- `203T` → `102S` — Untrained on tracking suit
- `201C3` → `102S` — Exhausted from 14-hour drive
- `201C2` → `102S` — Overconfidence and pressing

---

## SYN-CS10

### L0 ✓

- **Pipeline:** `001HE` — The jumper experienced a 180° off-heading opening facing the building and attempted a brake turn correction by pulling only the right toggle hard, which drove her into a diving turn into the building. Grabbing only one toggle and pulling it hard without first arresting forward speed (e.g., via rear risers or both toggles) constitutes a human error in off-heading correction technique that directly produced the fatal object strike.
- **Ground truth:** `001HE`

### L1 ✓

**Pipeline:**
- `102S` — **Incorrect off-heading correction technique**
  > After a 180° off-heading opening facing the building, the jumper grabbed only the right toggle and pulled it hard. This single-brake input created a diving turn into the building rather than arresting forward speed. Accepted practice for a 180° off-heading is to first apply both rear risers (or both brakes) to halt forward movement toward the object, then release one side to turn away. The asymmetric single-toggle input was a technique execution error that directly produced the fatal object strike.

**Ground truth:**
- `102S` — Inappropriate toggle input after off-heading opening

### L2 ✓

**Pipeline:**
- _(empty — no preconditions identified)_

**Ground truth:**
- _(empty)_

---

## SYN-CS11

### L0 ✓

- **Pipeline:** `001HE` — The jumper chose to exit in near-zero visibility conditions (fog obscuring the wall, fjord, and landing area) when all other jumpers declined to jump. This decision to jump in conditions that prevented visual navigation and altitude/terrain awareness constitutes a clear human error. He tracked into an unseen protruding ledge and impacted in terminal freefall with his pilot chute still stowed, indicating he never saw the terrain obstacle and lost altitude awareness.
- **Ground truth:** `001HE`

### L1 ✓

**Pipeline:**
- `101D` — **Jumped in zero visibility**
  > The jumper chose to exit in conditions where visibility was essentially zero — the fjord, landing area, and wall were not visible. This decision was clearly and specifically wrong: jumping a terminal cliff with no ability to see terrain features, including a known protruding ledge 120 meters below, made it impossible to navigate freefall safely. He tracked into an unseen ledge and impacted in terminal freefall with his pilot chute still stowed, meaning the zero-visibility decision directly produced the fatal outcome regardless of execution quality.

**Ground truth:**
- `101D` — Decided to jump in zero visibility conditions

### L2 ✗

**Pipeline:**
- `201C2` → `101D` — **Overconfidence**
  > The jumper stated he had done this exit dozens of times and 'knew the heading by feel,' asserting he could navigate by feel alone despite zero visibility. This unreasonable overestimation of his ability to safely track past terrain features he could not see — when every other jumper present recognized the conditions as unjumpable and packed up to hike down — directly drove the decision to exit.
- `204E` → `101D` — **Zero visibility from fog**
  > Low-level clouds reduced visibility to essentially zero, obscuring the fjord, landing area, and wall below the exit. This environmental condition directly prevented the jumper from seeing the protruding ledge he tracked into, making terrain avoidance during freefall physically impossible regardless of skill or familiarity with the site.

**Ground truth:**
- `201C1` → `101D` — Complacency from site familiarity

---

## SYN-CS12

### L0 ✓

- **Pipeline:** `001HE` — The jumper interrupted his track to adjust a helmet-mounted camera mid-flight, losing his tracking body position and separation from the wall. He drifted into the cliff without deploying his parachute or making any corrective input. This represents clear human error: distraction from a critical task (tracking/deployment) to attend to filming equipment.
- **Ground truth:** `001HE`

### L1 ✓

**Pipeline:**
- `102S` — **Attention failure during tracking**
  > Marcus reached up to adjust his helmet-mounted GoPro during the tracking phase, which caused him to abandon his tracking body position and go flat. This loss of active tracking resulted in leftward drift toward the wall. He failed to monitor his proximity to terrain and made no corrective input despite the ledge being in clear view for several seconds, ultimately impacting in terminal freefall without deploying.

**Ground truth:**
- `102S` — Attention failure, lost terrain awareness while adjusting camera during flight

### L2 ✓

**Pipeline:**
- `201C1` → `102S` — **Channelized Attention/Fixation**
  > Marcus became fixated on adjusting his helmet-mounted GoPro during flight, channeling his attention onto the camera to the exclusion of maintaining tracking body position, monitoring terrain proximity, and initiating deployment. This attentional fixation on a secondary task directly enabled the sustained loss of situational awareness described in the L1 error.

**Ground truth:**
- `201C1` → `102S` — Distraction, camera equipment diverted attention from primary task

---

## SYN-CS13

### L0 ✓

- **Pipeline:** `001HE` — The jumper had a recognized, recurring problem with angle of attack control that led to repeated near-miss stalls. He acknowledged the need for remedial skydiving training but continued jumping cliffs without addressing the deficiency. The fatal stall and terrain impact resulted directly from this known skill deficit and the decision to continue proximity flying without corrective action.
- **Ground truth:** `001HE`

### L1 ✗

**Pipeline:**
- `101D` — **Continued proximity flying despite known skill deficiency**
  > The jumper explicitly recognized that his angle of attack control was inadequate, had experienced at least four near-miss stalls in the preceding three months, and identified the specific corrective action needed (returning to skydiving for stall recovery training). Despite this clear self-assessment, he consciously chose to continue flying wingsuit BASE at cliffs every weekend without addressing the deficiency. This was not an execution error on the fatal jump—the decision to keep exposing himself to proximity terrain flying with a known, repeated, and acknowledged inability to maintain adequate airspeed was the producing mechanism. The stall that killed him was the same failure mode he had identified and failed to correct.

**Ground truth:**
- `102S` — Stalled wingsuit during flight (technique error)

### L2 ✗

**Pipeline:**
- `202P2` → `101D` — **Failure to Correct Known Deficiency**
  > The jumper experienced at least four near-miss stalls over three months due to poor angle of attack control, explicitly acknowledged the problem to peers, identified the specific corrective action (50 skydiving stall recovery training jumps), yet never followed through. This sustained pattern of inaction over multiple weekends directly enabled the continued decision to fly proximity terrain with the uncorrected deficiency.

**Ground truth:**
- `202P2` → `102S` — Failed to correct known stall problem despite multiple near-misses and own stated intent to retrain
- `203T` → `102S` — Insufficient stall recovery proficiency

---

## SYN-CS14

### L0 ✓

- **Pipeline:** `001HE` — The jumper experienced a 90-degree off-heading opening toward guy wires and made no corrective input whatsoever—no riser or toggle action—despite approximately two seconds of available reaction time. This failure to attempt any heading correction constitutes a clear human error that directly contributed to the fatal object strike. Additionally, jumping a 900-foot antenna at night with only two prior antenna jumps (both from taller, more forgiving structures) and limited overall BASE experience (60 jumps) represents a decision error in object selection relative to experience level.
- **Ground truth:** `001HE`

### L1 ✓

**Pipeline:**
- `102S` — **Failure to perform heading correction**
  > The canopy opened with a 90-degree off-heading pointing directly at guy wires approximately 40 feet away. Despite having approximately two seconds and both riser and toggle inputs available, the jumper made no corrective input whatsoever — his arms remained at his sides. Multiple witnesses confirmed he took no action. This failure to execute any heading correction, a fundamental and practiced skill for antenna jumps, was the direct mechanism of the fatal object strike.

**Ground truth:**
- `102S` — Failed to perform corrective steering after off-heading opening

### L2 ✗

**Pipeline:**
- `201C3` → `102S` — **Startle Response/Freeze**
  > Multiple witnesses stated he 'completely froze the moment he saw the wires directly in front of him' — his arms stayed at his sides with no toggle or riser input despite approximately two seconds available. This is consistent with an automatic startle/freeze response triggered by the unexpected sight of guy wires directly ahead, rendering him temporarily unable to initiate any corrective action.
- `203T` → `102S` — **Insufficient Antenna Experience**
  > The jumper had only two previous antenna jumps, both from taller structures where guy wires were further from the exit point. This antenna presented guy wires approximately 40 feet from the flight path — a significantly more constrained environment than his prior antenna experience. His insufficient antenna-specific experience likely contributed to his inability to execute an immediate heading correction under the time pressure and proximity demands of this object.

**Ground truth:**
- `201C3` → `102S` — Startle/Freeze, involuntary physiological freeze response upon seeing guy wires directly ahead

---

## SYN-CS15

### L0 ✓

- **Pipeline:** `001HE` — The jumper knowingly used a pilot chute with a large tear in the mesh after being advised by multiple people to replace it. The damaged PC could not inflate properly, resulting in a total malfunction (PC in tow / collapse in burble) and closed-container impact. The decision to jump with known-damaged critical equipment is a clear human error.
- **Ground truth:** `001HE`

### L1 ✓

**Pipeline:**
- `101D` — **Jumped with known-damaged PC**
  > The jumper was aware of a significant tear (~4 inches) in his pilot chute mesh, was advised by companions to replace it, was offered spare PCs, yet consciously decided the damaged PC would still function adequately. This decision was clearly and specifically wrong: a PC with a large tear in the mesh cannot reliably generate sufficient drag to extract the packjob, and the jumper had both the knowledge and the means to use a functional PC. The damaged PC failed to inflate, resulting in a total malfunction (PC in tow) and closed-container impact.

**Ground truth:**
- `101D` — Decided to jump with known damaged pilot chute

### L2 ✗

**Pipeline:**
- `202P1` → `101D` — **Failed to replace damaged PC**
  > The jumper's pilot chute had a ~4-inch tear in the mesh from the previous jump. Despite being advised by companions to replace it and being offered spare PCs, the jumper failed to swap the damaged component before jumping. Replacing a known-damaged PC is a basic equipment preparation action that would have directly prevented the total malfunction.

**Ground truth:**
- `201C2` → `101D` — Overconfidence, unreasonable assessment that damaged PC would function

---

## SYN-CS16

### L0 ✓

- **Pipeline:** `001HE` — The narrative explicitly describes multiple human errors contributing to the fatality: the group failed to establish an exit order separation plan with specific delays, flight paths, or opening altitudes; the deceased tracked over another jumper and deployed directly into that jumper's inflating canopy without checking airspace. These failures in planning and situational awareness led to the fatal canopy entanglement.
- **Ground truth:** `001HE`

### L1 ✓

**Pipeline:**
- `102S` — **Failed to check airspace before deployment**
  > David deployed his pilot chute directly into the second jumper's inflating canopy after tracking over that jumper. The narrative explicitly states he did not check his airspace before deploying. This is an attention/awareness failure during execution — he failed to monitor his position relative to other jumpers before initiating deployment, which is a fundamental execution requirement in multi-way jumps. The deployment into another jumper's canopy caused the fatal entanglement.

**Ground truth:**
- `102S` — Deployed into occupied airspace without checking

### L2 ✓

**Pipeline:**
- `202P1` → `102S` — **Inadequate multi-way planning**
  > The narrative explicitly states that nobody properly went through the exit order or separation plan, no specific delays were set, and no one discussed flight paths or opening altitudes. This failure to coordinate staged openings and horizontal/vertical separation directly created the conditions in which David tracked over another jumper and deployed into that jumper's airspace without awareness of the conflict. Accepted practice for multi-way jumps requires pre-planned separation, staged openings, and briefed flight paths.

**Ground truth:**
- `202P1` → `102S` — Inadequate group jump planning, no delays, no flight paths, no briefing

---

## SYN-CS17

### L0 ✓

- **Pipeline:** `001HE` — The jumper deliberately delayed pilot chute extraction too long, resulting in insufficient altitude for canopy deployment. He had a pattern of progressively extending delays beyond safe limits despite warnings from other jumpers. The narrative explicitly states there were no equipment, weather, or exit issues — he simply pulled too low.
- **Ground truth:** `001HE`

### L1 ✓

**Pipeline:**
- `101D` — **Deliberately excessive delay**
  > The jumper had a clean exit, good track, and no equipment or weather issues. He consciously chose to extend his delay beyond what the altitude could support, a pattern of progressively longer delays (4 to 6 to 8+ seconds) that other jumpers had warned him about repeatedly. On this jump he deliberately pulled too low for the canopy to complete extraction before impact. The decision to pull at that altitude was the producing mechanism for the fatality.

**Ground truth:**
- `101D` — Deliberately pulled at dangerously low altitude

### L2 ✓

**Pipeline:**
- `202P2` → `101D` — **Failure to correct known deficiency**
  > The jumper was aware of his progressively longer delays through repeated warnings from other jumpers over the past season. Despite this feedback, he failed to correct the pattern, continuing to extend delays from 4 to 6 to 8+ seconds. This sustained normalization of deviance directly enabled the fatally excessive delay on this jump.

**Ground truth:**
- `202P2` → `101D` — Normalization of deviance, progressive acceptance of riskier delays over the season despite warnings

---

## SYN-CS18

### L0 ✓

- **Pipeline:** `001HE` — The jumper flew an expert-level wingsuit (Aura 1) with only approximately 10 skydives in the suit before using it in BASE, far below the accepted minimum of 40-60 skydives with the specific suit. During flight, he stalled the suit and was unable to recover, resulting in terminal impact. This represents clear human errors in both equipment selection/progression and in-flight technique (flying too slowly/high AoA leading to stall).
- **Ground truth:** `001HE`

### L1 ✓

**Pipeline:**
- `102S` — **Loss of airspeed control leading to stall**
  > Midway through the flight, the jumper's angle of attack shifted and he stalled the wingsuit. His glide transitioned from shallow to nearly vertical over approximately two seconds, and he sank out rapidly without recovering. This is a performance/execution failure — he was flying an appropriate line but failed to maintain adequate airspeed and angle of attack, entering an unrecoverable stall.

**Ground truth:**
- `102S` — Stalled wingsuit during flight (technique error)

### L2 ✓

**Pipeline:**
- `203T` → `102S` — **Insufficient Experience with Expert Wingsuit**
  > The jumper had recently upgraded to an expert-level wingsuit (Aura 1) with only approximately 10 skydives in it before using it for BASE. Accepted progression norms require 40-60 wingsuit skydives with the specific suit before BASE use. The narrative explicitly states that expert-level wingsuits have stall boundaries requiring many flights to understand, and he had not put in that time. This insufficient familiarity with the suit's flight envelope directly contributed to his failure to recognize and recover from the developing stall.

**Ground truth:**
- `203T` → `102S` — Insufficient training on new wingsuit model (10 skydives before cliff)

---

## SYN-CS19

### L0 ✓

- **Pipeline:** `001HE` — The jumper had only 5 skydives and 0 BASE jumps, making this a 'death camper' scenario with grossly insufficient experience for any BASE jump, let alone a slider-up cliff requiring tracking. The jumper attempted a terminal cliff object with a tracking suit despite having zero BASE experience and far below the minimum 200+ skydives required before beginning BASE. The fatal outcome resulted from human errors in progression decisions and likely execution (unstable exit, insufficient separation, possible excessive delay).
- **Ground truth:** `001HE`

### L1 ✗

**Pipeline:**
- `101D` — **Attempted jump far beyond experience level**
  > The jumper had only 5 skydives, zero BASE jumps, and zero wingsuit skydives, yet attempted a slider-up terminal cliff jump wearing a tracking suit. Accepted progression norms require a minimum of 200+ skydives before beginning BASE, and tracking suit BASE jumping requires prior mastery of both regular BASE jumping and tracking suit skydiving. This decision represents a massive departure from what any competent jumper would consider appropriate, and the complete absence of foundational skills directly produced the fatal outcome.
- `102S` — **Unstable exit and inadequate separation**
  > The jumper executed an unstable exit resulting in insufficient forward separation from the cliff. With zero BASE experience and minimal skydiving experience, the jumper lacked the fundamental body position skills, sub-terminal tracking ability, and deployment skills needed to maintain object separation. The jumper impacted the terrain near the exit point, with the canopy partially deployed, indicating failure to achieve adequate separation through tracking and/or failure to deploy at a survivable altitude in a stable position.

**Ground truth:**
- `102S` — Insufficient separation from cliff (technique error during exit/flight)

### L2 ✗

**Pipeline:**
- `203T` → `101D` — **Insufficient Skydiving Experience**
  > The jumper had only 5 skydives total, far below the accepted minimum of 200+ skydives before beginning BASE. This complete lack of foundational skydiving training meant the jumper had no basis for evaluating the decision to attempt a slider-up terminal cliff jump.
- `203T` → `102S` — **Lack of BASE Specific Training**
  > With zero BASE jumps and only 5 skydives, the jumper had no BASE training, no sub-terminal tracking ability, no experience with BASE exits, and no object avoidance skills. This absence of any relevant training directly produced the unstable exit and failure to achieve adequate separation from the cliff.
- `201C2` → `101D` — **Overconfidence**
  > The jumper attempted a terminal slider-up cliff jump in a tracking suit with only 5 skydives and zero BASE jumps, a decision so far beyond any reasonable self-assessment that it demonstrates an extreme overestimation of personal capability. No reasonably calibrated individual would attempt this jump at this experience level.

**Ground truth:**
- `203T` → `102S` — Insufficient experience deduced from metadata (5 skydives, 0 BASE jumps)

---

## SYN-CS20

### L0 ✓

- **Pipeline:** `001HE` — The jumper made a packing error by placing the pilot chute inside the main container beneath the closing flaps instead of routing it to the BOC pouch. When he deployed, the BOC handle extracted cleanly but the PC remained trapped inside the closed container, resulting in a total malfunction (PC in tow) and fatal impact. This is a clear human error in equipment rigging/packing.
- **Ground truth:** `001HE`

### L1 ✓

**Pipeline:**
- `102S` — **Packing execution error**
  > During packing, the jumper placed the pilot chute inside the main container underneath the closing flaps instead of routing it out to the BOC pouch. When he reached for the BOC handle on deployment, the handle extracted cleanly but the PC remained trapped inside the closed container, resulting in a total malfunction. This was a fundamental execution error in a known procedural step of the pack job.

**Ground truth:**
- `102S` — Packed pilot chute inside container instead of BOC (technique error in packing)

### L2 ✓

**Pipeline:**
- _(empty — no preconditions identified)_

**Ground truth:**
- _(empty)_

---

## SYN-N01

### L0 ✓

- **Pipeline:** `003II` — The report contains no accident narrative, no possible factors, no cause of death details, and no information about the jumper's experience, equipment, or conditions. There is insufficient information to determine whether human error or another cause contributed to the fatality.
- **Ground truth:** `003II`

---

## SYN-N02

### L0 ✓

- **Pipeline:** `003II` — The narrative provides almost no information: the jumper impacted talus with canopy out, there were no witnesses, and no details on experience, equipment, packing, weather, or possible factors are reported. There is insufficient information to identify a human error pathway or to positively establish a non-human cause.
- **Ground truth:** `003II`

---

## SYN-N03

### L0 ✓

- **Pipeline:** `003II` — Two experienced witnesses provide contradictory accounts — one reports a late pull, the other reports a pilot chute in tow / bridle issue with an earlier deployment. The gear was not available for inspection, making it impossible to determine whether the cause was a human error (late deployment) or an equipment malfunction. Neither 001HE nor 002OC can be adequately supported.
- **Ground truth:** `003II`

---

## SYN-N04

### L0 ✓

- **Pipeline:** `003II` — The jumper maintained an active body position throughout the flight but made no deployment attempt, impacting in terminal freefall. Equipment was recovered in perfect working order, autopsy and toxicology revealed no medical cause, and no human error pathway can be identified from the available evidence. The reason for the failure to deploy remains unknown, making this insufficient information.
- **Ground truth:** `003II`

---

## SYN-N05

### L0 ✓

- **Pipeline:** `003II` — The cause of death is impact in terminal freefall during a proximity wingsuit flight, but the narrative provides no factual details about what occurred during the flight — no description of the flight path, conditions encountered, equipment state, or specific errors. The entry explicitly states they are 'looking for more information.' Without evidence to identify a specific human error pathway or to positively establish a non-human cause, the information is insufficient to classify.
- **Ground truth:** `003II`

---

## SYN-N06

### L0 ✓

- **Pipeline:** `003II` — The jumper was found dead with canopy deployed, but nobody witnessed the jump, no gear inspection was performed before authorities removed the equipment, and all proposed explanations (off-heading, packing issue, thermals) are explicitly described as speculation. There is insufficient evidence to identify a specific human error pathway or to positively establish a non-human cause.
- **Ground truth:** `003II`

---

## SYN-N07

### L0 ✓

- **Pipeline:** `003II` — The jumper went missing and was found months later at the base of a cliff. No witnesses, no known jump date, no weather data, and no information about what occurred during the jump. While the site is known for strong crosswinds and prior fatalities, there is insufficient information to determine whether human error or an unforeseeable environmental event caused the fatality.
- **Ground truth:** `003II`

---

## SYN-N08

### L0 ✓

- **Pipeline:** `003II` — The narrative provides virtually no information about the jump, the jumper, the equipment, or the circumstances. The body was recovered but no details on gear, experience, or what happened are available. There is insufficient information to determine whether human error or another cause was involved.
- **Ground truth:** `003II`

---

## SYN-N09

### L0 ✗

- **Pipeline:** `003II` — The jumper clearly pulled too late, resulting in impact at line stretch. However, the narrative presents three competing hypotheses for why the late pull occurred — sun glare causing altitude misjudgment, unexpected suit performance causing faster descent than realized, or attentional fixation on the landing area — with no video evidence or other means to distinguish among them. Without sufficient information to identify the specific error mechanism, neither a specific human error pathway nor a non-human cause can be reliably established.
- **Ground truth:** `001HE`

### L1 ✗

**Pipeline:**
- _(not run — L0 ≠ 001HE)_

**Ground truth:**
- `103II` — Insufficient information to distinguish decision vs skill-based error

---

## SYN-N10

### L0 ✗

- **Pipeline:** `003II` — The jumper experienced a malfunction and failed to resolve it, but the GoPro footage does not show the canopy, so the type of malfunction and whether the jumper's response was appropriate cannot be determined. The cause is listed as 'Malfunction, Misrigging' and the narrative states it was not a manufacturer error, suggesting human error in rigging, but the narrative also says they cannot determine what type of malfunction occurred or whether the response was appropriate. The specific human error pathway—whether the fatal outcome resulted from the misrigging itself, from an inadequate malfunction response, or from both—cannot be clearly established from the available information.
- **Ground truth:** `001HE`

### L1 ✗

**Pipeline:**
- _(not run — L0 ≠ 001HE)_

**Ground truth:**
- `103II` — Insufficient information to distinguish decision vs skill-based error

---
