"""Swimming: the 67 objectives that had no drills, two question types each.

Sources, in the order a card leans on them: the objective's own essential knowledge (which names its research
where it has any), USA Swimming's Foundations of Coaching chapters 5 and 6 (read; see usas-foc-2007), and the
World Aquatics rules (read in full) for every legal-or-illegal call. Energy-zone heart rates and paces are not on
any card because the course's zone charts were not in the text read.

A card cannot watch a stroke. Technique objectives are drilled as what a card can hold: naming the phase, picking
the fault's cause and its correction, and the arithmetic that measures a stroke off a clock or a clip. The
swimming itself stays in the pool.
"""
from opl_dsl import Q

FILE, FRAMEWORK = "sw-core", "swimming"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
HY, TQ, WL, PH, VD, PR, CH, RU, PC, TR = ("swim.hydro", "swim.technique", "swim.walls", "swim.physiology",
                                          "swim.video", "swim.practice", "swim.coaching", "swim.rules",
                                          "swim.pacing", "swim.training")
ADD = []


def F(code, name, skill, rows, explain):
    ADD.append((code, Q(name, skill, "{{q}}", pace="recall",
                        cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
                        choice=MC, correct="0", verify="authored", explain=explain)))


def N(code, *a, **k):
    ADD.append((code, Q(*a, **k)))


# ── unit 1: hydrodynamics ─────────────────────────────────────────────────────────────────────────────────────
F("SW-1.1.A", "sw-resistance-type", HY, [
    ("A swimmer's hips sink and the legs trail low. The resistance this adds is mainly:", "Form resistance", "Friction resistance", "Wave resistance", "None"),
    ("A baggy, rough suit mainly adds:", "Friction resistance", "Form resistance", "Wave resistance", "Buoyancy"),
    ("The bow wave a swimmer pushes at the surface is:", "Wave resistance", "Form resistance", "Friction resistance", "Lift"),
    ("A kick that opens wider than the body's shadow mainly adds:", "Form resistance", "Friction resistance", "Wave resistance", "Propulsion"),
], "Shape and alignment set form resistance, the surface sets wave resistance, and skin and suit set friction")
F("SW-1.1.A", "sw-resistance-rank", HY, [
    ("Of the three resistances, the one a coach can change most through body position is:", "Form resistance", "Friction resistance", "Wave resistance", "They are equal"),
    ("The least significant of the three resistances is:", "Friction resistance", "Form resistance", "Wave resistance", "They are equal"),
    ("Shaving down before a championship reduces:", "Friction resistance", "Form resistance", "Wave resistance", "Stroke rate"),
    ("Before asking a swimmer to kick harder to fix low legs, first:", "Fix body position to cut resistance", "Add a pull buoy permanently", "Raise stroke rate", "Lift the head"),
], "Reduce resistance before adding propulsion: position is free speed, and kicking harder to hold up a poor line costs energy")
N("SW-1.1.B", "sw-drag-power-factor", HY, "Swimming speed rises by {{pc}}%. With drag proportional to v² and power to v³, by what percentage does the power needed rise?",
  given={"pc": {"pick": [2, 5, 10]}}, value="((1 + pc/100)^3 - 1)*100", tex="\\%", tol=0.005,
  verify="((1 + Rational(pc, 100))**3 - 1)*100",
  explain="Power is drag times speed, so it goes as the cube: 5% faster costs about 16% more power. This is why small drag savings beat small fitness gains")
N("SW-1.1.B", "sw-drag-factor", HY, "A swimmer's frontal drag coefficient-area product falls by {{pc}}% at the same power output. By what percentage does speed rise? (P ∝ C·v³)",
  given={"pc": {"pick": [5, 10, 20]}}, value="((1/(1 - pc/100))^(1/3) - 1)*100", tex="\\%", tol=0.005,
  verify="((1/(1 - Rational(pc, 100)))**Rational(1, 3) - 1)*100",
  explain="Speed goes as the cube root of the drag saving, so a 10% cut in drag is worth about 3.6% in speed, a huge margin in a race")
F("SW-1.1.C", "sw-underwater-why", HY, [
    ("Kicking underwater off a wall can beat surface swimming because:", "Wave resistance falls away with depth", "Water is thinner below the surface", "Friction disappears underwater", "The kick is stronger underwater"),
    ("A push-off at about 0.6 m depth compared with 0.2 m is roughly:", "20% more efficient", "The same", "20% less efficient", "Twice as efficient"),
    ("Pushing off on the surface is slow because:", "The swimmer makes waves from the first metre", "The wall is slippery there", "The legs cannot extend", "Friction is highest at the surface"),
], "Wave-making is a surface cost. Leaving the wall below it carries push-off speed further")
F("SW-1.1.C", "sw-underwater-limit", HY, [
    ("The rules cap the underwater phase at 15 m because:", "Underwater kicking was faster than swimming and races were moving under water", "Of pool depth", "Of camera coverage", "Of lane-rope length"),
    ("Staying under past the point where kicking speed drops below swimming speed:", "Costs time and oxygen", "Is always faster", "Reduces drag further", "Is required"),
    ("In the end lane next to a wall, wave resistance is:", "Higher, from reflected waves", "Lower", "Zero", "Unchanged"),
], "Underwater speed is an advantage only while it is above surface speed and affordable in oxygen")
F("SW-1.2.A", "sw-streamline-elements", HY, [
    ("In a tight streamline the head sits:", "Between the arms, ears just covered by them", "Lifted to look forward", "Tucked hard to the chest", "To one side"),
    ("Lifting the head slightly in streamline does what to resistance?", "Roughly doubles it", "Nothing", "Halves it", "Raises it by 5%"),
    ("Stacking one hand on the other in streamline:", "Narrows the leading edge", "Adds propulsion", "Raises the hips", "Is required by rule"),
    ("Pointed toes in streamline matter because:", "Flexed feet add form resistance at the back of the body", "They add thrust", "They raise the hips", "They are required by rule"),
], "Every element of the streamline is there to shrink frontal area or keep the flow attached")
F("SW-1.2.A", "sw-body-balance", HY, [
    ("To bring the legs up without kicking harder, a swimmer should:", "Press the chest down and keep the arms forward", "Lift the head", "Bend the knees", "Arch the back"),
    ("Low hips usually trace back to:", "A high head", "A weak kick", "Small hands", "A slow stroke rate"),
    ("Tucking the chin toward the chest compared with a neutral head changes resistance:", "Very little", "Doubles it", "Halves it", "Triples it"),
], "The body is a see-saw about the lungs: weight forward and down lifts the back end")
N("SW-1.2.B", "sw-glide-decay", HY, "A swimmer leaves the wall at {{v0}} m/s and glides with quadratic drag, dv/dt = −k·v² with k = {{kk}} per metre. After how many seconds has speed fallen to {{vk}} m/s?",
  given={"v0": {"pick": [2.8, 3.2]}, "kk": {"pick": [0.4, 0.5]}, "vk": {"pick": [1.6, 2.0]}}, value="(1/vk - 1/v0)/kk", tex="t", tol=0.005,
  verify="(1/nsimplify(vk) - 1/nsimplify(v0))/nsimplify(kk)",
  explain="With drag going as v², 1/v grows linearly in time: the glide loses its speed in well under a second. Start the kick as the glide reaches kicking speed, not after it")
F("SW-1.2.B", "sw-glide-when", HY, [
    ("The first kick off a wall should start when glide speed:", "Has dropped to about kicking speed", "Reaches zero", "Is still at its maximum", "Equals swimming speed exactly"),
    ("Kicking immediately at push-off speed:", "Adds drag without adding speed", "Is fastest", "Is illegal", "Saves oxygen"),
    ("Gliding until the body nearly stops:", "Throws away speed the swimmer must rebuild", "Saves the most energy", "Is the fastest option", "Is required in breaststroke only"),
], "The push-off is faster than any swimmer can kick; the skill is handing over at the right speed")
N("SW-1.3.A", "sw-thrust-momentum", HY, "A hand and forearm push {{mr}} kg of water per second backward, speeding it up by {{dv}} m/s. What thrust results, in newtons?",
  given={"mr": {"pick": [20, 35, 50]}, "dv": {"pick": [1.5, 2.0, 3.0]}}, value="mr*dv", tex="N", final=True,
  verify="mr*nsimplify(dv)",
  explain="Thrust is the rate at which backward momentum is given to water. A big surface moving a lot of water a little is more efficient than a small one moving a little water a lot")
F("SW-1.3.A", "sw-high-elbow", HY, [
    ("A high-elbow catch helps because:", "The forearm joins the hand as a backward-facing paddle early", "It shortens the stroke", "It lifts the body", "It rests the shoulder"),
    ("A dropped elbow in the catch means the forearm:", "Slips through the water instead of pressing it back", "Presses more water", "Lifts the hips", "Adds lift"),
    ("Coaches now say 'anchor' rather than 'pull' because:", "The hand holds water while the body moves past it", "The arm should not move", "Pulling is illegal", "It is slower"),
], "Propulsion comes from pressing water backward with as much area as possible for as long as possible")
F("SW-1.3.B", "sw-lift-vs-drag", HY, [
    ("Counsilman's lift model said propulsion came mainly from:", "Sculling hands acting like foils", "Pushing water straight back", "The kick", "Body roll"),
    ("Three-dimensional studies of elite swimmers found propulsion in most strokes is mainly:", "Drag-based, with straighter hand paths", "Lift-based", "From the kick", "From body roll"),
    ("The stroke in which lift from sculling matters most is:", "Breaststroke", "Freestyle", "Backstroke", "Butterfly"),
], "The S-pull came from the lift model; the evidence moved toward pressing water back along a straighter path")
F("SW-1.3.B", "sw-scull-purpose", HY, [
    ("Sculling drills are kept in practice mainly to build:", "Feel for the water", "Shoulder strength", "Kick power", "Lung capacity"),
    ("If propulsion is drag-dominant, the hand's palm and forearm should mostly face:", "Backward, toward the feet", "Downward", "Sideways", "Forward"),
    ("A wide S-shaped pull compared with a straighter one:", "Spends force sideways", "Adds thrust", "Is required for rotation", "Reduces drag"),
], "Feel for pressure on the hand is trainable by sculling even though the race stroke presses mostly straight back")
N("SW-1.3.C", "sw-propelling-efficiency", HY, "A swimmer produces {{pw}} W of mechanical power with a propelling efficiency of {{ef}}%. How many watts go into overcoming drag?",
  given={"pw": {"pick": [200, 320, 450]}, "ef": {"pick": [45, 60, 75]}}, value="pw*ef/100", tex="W", final=True,
  verify="Rational(pw*ef, 100)",
  explain="The rest moves water rather than the swimmer. Raising efficiency from 45% to 60% is a one-third gain in useful power with no fitness change")
N("SW-1.3.C", "sw-efficiency-vs-power", HY, "Speed goes as the cube root of useful power. Propelling efficiency rises from {{e1}}% to {{e2}}% at the same total power. By what percentage does speed rise?",
  given={"e1": {"pick": [50, 60]}, "e2": {"pick": [66, 72]}}, value="((e2/e1)^(1/3) - 1)*100", tex="\\%", tol=0.005,
  verify="(Rational(e2, e1)**Rational(1, 3) - 1)*100",
  explain="Compare this with a 10% rise in aerobic power, worth about 3.2% in speed. Technique that wastes less is often the bigger lever")
F("SW-1.3.D", "sw-dolphin-wave", HY, [
    ("The dolphin kick's thrust comes from:", "A body wave whose amplitude grows toward the feet", "Bending the knees sharply", "The arms", "Lifting the head"),
    ("Most of the dolphin kick's thrust is produced on the:", "Downkick", "Upkick only", "Glide", "Knee bend"),
    ("A dolphin kick driven from the knees rather than the chest and hips:", "Adds drag and loses the wave", "Is faster", "Is illegal", "Saves oxygen"),
], "The kick is a whip: a small movement high in the body becomes a fast one at the feet")
F("SW-1.3.D", "sw-dolphin-upkick", HY, [
    ("The upkick becomes propulsive when the feet:", "Press water backward as they rise", "Leave the water", "Are flexed", "Stop moving"),
    ("A swimmer with stiff ankles loses dolphin-kick thrust because:", "The feet cannot face backward on the downkick", "The knees lock", "The hips sink", "The wave reverses"),
    ("Kicking with a larger amplitude than needed:", "Adds form resistance", "Always adds speed", "Reduces oxygen cost", "Is required underwater"),
], "Thrust needs a surface facing backward; ankle flexibility decides how much of the foot does")

# ── unit 2: freestyle and backstroke ──────────────────────────────────────────────────────────────────────────
F("SW-2.1.A", "sw-free-phases", TQ, [
    ("The freestyle phases in order are:", "Entry, catch, pull, push, recovery", "Catch, entry, push, pull, recovery", "Entry, pull, catch, recovery, push", "Recovery, push, catch, entry, pull"),
    ("Propulsive force in freestyle is concentrated:", "From the catch to the end of the push", "During the entry", "During the recovery", "Equally in all phases"),
    ("The purpose of the entry is to:", "Set up the catch with little splash", "Produce thrust", "Rest the arm", "Lift the head"),
], "Two phases set up, three produce: knowing which is which tells you where a fault costs speed")
F("SW-2.1.A", "sw-free-essentials", TQ, [
    ("To breathe in freestyle the head should:", "Roll with the body, staying low", "Lift forward", "Turn before the body rolls", "Stay fixed"),
    ("Body rotation to each side in freestyle is about:", "40 degrees", "10 degrees", "90 degrees", "No rotation"),
    ("In a relaxed freestyle recovery the elbow is:", "High, with the hand below it", "Locked straight", "Below the hand", "Dragged through the water"),
], "A steady head, a rolling body and a high-elbow recovery are the skills the full stroke is built from")
F("SW-2.1.B", "sw-free-timing", TQ, [
    ("In catch-up timing the recovering hand:", "Arrives in front before the other begins to pull", "Passes the pulling hand at the shoulder", "Is opposite the pulling hand", "Never extends"),
    ("More overlap between the arms gives:", "Longer distance per stroke at a lower rate", "Higher rate and shorter strokes", "No change", "More kick"),
    ("Sprint freestyle moves toward opposition timing because:", "Propulsion becomes continuous at a high rate", "It saves energy", "It lengthens the glide", "It is required"),
], "Timing trades glide for continuity: distance swimmers buy length, sprinters buy rate")
N("SW-2.1.B", "sw-rate-length-speed", TQ, "A swimmer holds {{sr}} cycles per minute at {{dp}} m per cycle. What is the swimming speed in m/s?",
  given={"sr": {"pick": [36, 45, 54]}, "dp": {"pick": [1.8, 2.2, 2.5]}}, value="sr/60*dp", tex="v", tol=0.005,
  verify="Rational(sr, 60)*nsimplify(dp)",
  explain="Speed is rate times length. A timing change moves one against the other, and only the product matters")
F("SW-2.1.C", "sw-free-fault", TQ, [
    ("A hand entering across the midline usually causes:", "Snaking hips", "A faster catch", "Higher hips", "A longer stroke"),
    ("A scissor kick on the breathing stroke usually comes from:", "Lifting or over-turning the head to breathe", "Weak legs", "A short stroke", "Tight ankles"),
    ("A dropped elbow in the pull is corrected by cueing:", "Fingertips down, forearm facing back", "A faster recovery", "A wider entry", "A harder kick"),
    ("Low legs in freestyle are most often fixed at the:", "Head and chest", "Feet", "Knees", "Hands"),
], "Faults show downstream of their cause: fix the head and entry before the kick they disturb")
F("SW-2.1.C", "sw-free-fault-cost", TQ, [
    ("A crossover entry costs speed mainly by:", "Adding form resistance as the body bends", "Reducing stroke rate", "Shortening the recovery", "Adding friction"),
    ("A dropped elbow costs speed mainly by:", "Wasting the pull's impulse", "Adding wave resistance", "Raising the hips", "Slowing the kick"),
    ("When several faults appear together, correct first the one that:", "Sits furthest upstream, usually head or body line", "Is easiest to see", "Is at the feet", "Appeared last"),
], "Each fault either adds drag or wastes impulse; say which before choosing the fix")
F("SW-2.2.A", "sw-back-catch", TQ, [
    ("The backstroke hand enters:", "Little finger first, arm straight", "Thumb first", "Palm flat", "Elbow first"),
    ("Arms enter at about which clock positions?", "11 and 1 o'clock", "12 and 12", "9 and 3", "10 and 4"),
    ("Rotation lets the backstroke pull:", "Go deep enough with a bent elbow beside the body", "Stay at the surface", "Cross under the spine", "Skip the catch"),
    ("The catch in backstroke is set about how deep?", "12 to 18 inches", "At the surface", "Three feet", "Six inches"),
], "Without rotation the arm sweeps wide at the surface; with it the bent arm presses water back beside the body")
F("SW-2.2.A", "sw-back-rotation", TQ, [
    ("Shoulders and hips in backstroke roll about:", "30 to 40 degrees", "5 degrees", "90 degrees", "Not at all"),
    ("The backstroke head should:", "Stay still while the body rolls", "Roll with the shoulders", "Lift to see the feet", "Tip back under water"),
    ("A very deep, straight-arm backstroke catch is:", "Weak, pushing down before pushing back", "The strongest position", "Required", "Fastest for sprinters"),
], "A still head with a rolling body is the same idea as freestyle, turned over")
F("SW-2.2.B", "sw-back-fault", TQ, [
    ("Sitting hips in backstroke are usually caused by:", "A lifted head", "A strong kick", "Too much rotation", "A deep catch"),
    ("Entering behind the head, past the shoulder line, causes:", "The hips to swing side to side", "A longer pull", "Higher hips", "A faster rate"),
    ("A flat body with no rotation leads to:", "A wide, shallow pull at the surface", "A deeper catch", "A stronger kick", "A higher rate with more thrust"),
], "Head level, hips at the surface, entry in line with the shoulder")
F("SW-2.2.B", "sw-back-correction", TQ, [
    ("To correct overreaching in backstroke, cue the entry:", "In line with the shoulder", "Behind the head", "Outside the lane rope", "Thumb first"),
    ("To correct sitting hips, cue:", "Head back and still, chest up", "Kick deeper", "Bend the knees", "Look at the feet"),
    ("To build rotation, the teaching progression uses:", "Streamline kick to a one-arm pull and side glide", "Double-arm backstroke only", "Vertical kicking only", "Pulling with a buoy only"),
], "The correction is chosen from the cause: head for hips, shoulder line for snaking, side glide for rotation")

# ── unit 3: butterfly ─────────────────────────────────────────────────────────────────────────────────────────
F("SW-3.1.A", "sw-fly-wave", TQ, [
    ("The butterfly body wave pivots near the:", "Hips", "Head", "Knees", "Feet"),
    ("Pressing the chest down in butterfly:", "Lifts the hips", "Sinks the hips", "Stops the kick", "Lifts the head"),
    ("What leads the butterfly wave?", "The head", "The feet", "The hands on recovery", "The knees"),
    ("Butterfly rhythm is:", "Chest down, hips up, then chest up, hips down", "Hips and chest down together", "Head up throughout", "Knees driving the hips"),
], "The wave runs head to feet about the hips; the hips stay near the surface while the ends move")
F("SW-3.1.A", "sw-fly-short-axis", TQ, [
    ("Butterfly and breaststroke are called short-axis strokes because the body:", "Rocks about an axis through the hips", "Rolls about the spine", "Does not move", "Rotates at the shoulders only"),
    ("In good butterfly the hips:", "Stay at or near the surface", "Drop a foot each cycle", "Rise out of the water", "Swing side to side"),
    ("What should travel forward rather than up and down?", "The swimmer's centre of mass", "The hands", "The feet", "The head only"),
], "Undulation is a means of going forward; anything that goes mostly up and down is cost")
F("SW-3.1.B", "sw-fly-over-undulation", TQ, [
    ("Too much undulation slows butterfly mainly by:", "Adding form and wave resistance", "Raising stroke rate", "Reducing kick depth", "Shortening recovery"),
    ("A swimmer who dives deep on every entry will find:", "The catch starts too deep and tempo drops", "A stronger pull", "Higher hips throughout", "A faster rate"),
    ("The cue that best limits over-undulation is:", "Land forward, not down", "Kick harder", "Lift the head higher", "Bend the knees more"),
], "Vertical travel is paid for twice: once in drag and again in tempo")
N("SW-3.1.B", "sw-fly-vertical-cost", TQ, "A butterflyer's frontal area rises by {{pc}}% because of over-undulation, at the same speed. By what percentage does the power needed rise? (P ∝ A·v³)",
  given={"pc": {"pick": [8, 15, 25]}}, value="pc", tex="\\%", final=True, verify="Integer(pc)",
  explain="At fixed speed, power scales directly with frontal area. Or, at fixed power, speed falls by the cube root: a 15% bigger shape costs nearly 5% in speed")
F("SW-3.2.A", "sw-fly-two-kicks", TQ, [
    ("The first butterfly kick happens as the:", "Hands enter", "Hands exit", "Head lifts", "Arms recover overhead"),
    ("The second butterfly kick happens as the:", "Hands push and exit", "Hands enter", "Arms are extended in front", "Body glides"),
    ("The first kick's main job is to:", "Lift the hips and balance the body", "Lift the shoulders", "Start the breath", "End the stroke"),
    ("The second kick's main job is to:", "Add thrust and lift the shoulders for recovery", "Sink the hips", "Start the catch", "Slow the stroke"),
], "Kick the hands in, kick the hands out: one kick for each end of the pull")
F("SW-3.2.A", "sw-fly-kick-count", TQ, [
    ("How many dolphin kicks go with one butterfly arm cycle?", "Two", "One", "Three", "Four"),
    ("When the second kick disappears late in a race:", "The shoulders stay low and the recovery drags", "The hips rise", "Stroke rate climbs", "The breath gets easier"),
    ("The two kicks are usually:", "Unequal, each timed to one end of the pull", "Identical and evenly spaced", "Both before the catch", "Both during recovery"),
], "Count the kicks per cycle and place each against the hands; that is the timing check")
F("SW-3.2.B", "sw-fly-pull-path", TQ, [
    ("Butterfly hands enter:", "In front of the shoulders", "Crossed at the midline", "Far outside the shoulders", "Beside the hips"),
    ("The high-elbow catch in butterfly is set:", "Just outside the shoulders", "Under the hips", "At the surface behind the head", "After the push"),
    ("The butterfly pull finishes with a push:", "Past the hips", "At the chest", "At the shoulders", "In front of the head"),
], "Enter at shoulder width, anchor just outside, press under the body and out past the hips")
F("SW-3.2.B", "sw-fly-entry-quality", TQ, [
    ("A crashing butterfly entry is corrected by:", "Placing the hands and letting the chest submerge", "Entering wider", "Kicking later", "Lifting the head"),
    ("A low-splash entry matters because:", "Splash is energy that did not move the swimmer", "It is required by rule", "It lifts the hips", "It lengthens the recovery"),
    ("Dropped elbows in the butterfly catch are corrected by:", "Fingertips down, palms and forearms facing back", "A straight-arm pull", "A wider entry", "A later breath"),
], "The entry sets the catch: placed hands and a pressing chest put the forearms where they can hold water")
F("SW-3.2.C", "sw-fly-kick-kick-pull", TQ, [
    ("Both kicks landing before the catch is called:", "Kick-kick-pull timing", "Catch-up timing", "Opposition timing", "A glide stroke"),
    ("Kick-kick-pull timing forces the swimmer to:", "Arch the back and push down in the pull", "Rotate", "Breathe late", "Shorten the kick"),
    ("The correction for kick-kick-pull is to cue:", "One kick in, then a small second kick as the hands exit", "Two harder kicks", "A longer glide", "A wider pull"),
], "With no kick left for the exit, the shoulders have nothing to lift them")
F("SW-3.2.C", "sw-fly-timing-check", TQ, [
    ("From a side-on clip, kick timing is checked by noting where the hands are when:", "The feet finish each downkick", "The head lifts", "The hips drop", "The elbows bend"),
    ("In correct timing the second downkick finishes as the hands:", "Leave the water", "Enter", "Reach full extension", "Pass the shoulders"),
    ("Single-arm butterfly is used to fix timing because:", "It slows the stroke so each kick can be placed", "It is faster", "It removes the kick", "It is a legal race stroke"),
], "Timing faults are found by pairing each kick with a hand position, one frame at a time")
F("SW-3.3.A", "sw-fly-breath-timing", TQ, [
    ("The butterfly head lift begins:", "With the pull", "At the entry", "During the recovery", "After the hands exit"),
    ("The inhale happens as:", "The mouth clears during the push", "The hands enter", "The arms recover overhead", "The hips drop"),
    ("The face returns to the water:", "Before the hands enter", "After the hands enter", "During the catch", "At the second kick"),
    ("During the breath the chin stays:", "Near the waterline", "High above the water", "Tucked to the chest", "Turned to the side"),
], "Head up with the pull, air at the push, face back in ahead of the hands")
F("SW-3.3.A", "sw-fly-breath-low", TQ, [
    ("A low, forward breath protects speed because:", "The hips stay up", "It takes more air", "It lengthens the pull", "It rests the neck"),
    ("If the head is still up when the hands enter:", "The chest cannot press and the hips drop", "The kick is stronger", "The stroke is longer", "Nothing changes"),
    ("The butterfly breath is taken:", "Forward", "By rolling to the side", "Every third stroke by rule", "During the glide"),
], "The head is the front of the wave: where it is at entry decides whether the chest can press")
F("SW-3.3.B", "sw-fly-late-breath", TQ, [
    ("A breath that starts at the end of the pull:", "Locks the shoulders and drops the hips", "Raises the hips", "Speeds the recovery", "Lengthens the stroke"),
    ("A late butterfly breath is corrected by timing the head with the:", "Catch", "Recovery", "Entry of the next stroke", "Second kick only"),
    ("A high head lift is corrected by cueing:", "Chin on the water, eyes forward and down", "Look at the far wall", "Breathe to the side", "Hold the breath longer"),
], "Late and high are the two breath faults; both end with sunk hips")
F("SW-3.3.B", "sw-fly-breath-cost", TQ, [
    ("A high head lift costs speed mainly through:", "Form resistance from dropped hips", "Lost stroke rate only", "Friction", "A weaker kick"),
    ("The first visible sign of a late breath is usually:", "The arms dragging low in recovery", "A wide entry", "A double kick", "A long glide"),
    ("Checking breath timing on video means comparing the head's rise with:", "The hands' position in the pull", "The feet", "The wall", "The lane rope"),
], "Name the cost before the cue: the breath fault is expensive because of what it does to the hips")
F("SW-3.3.C", "sw-fly-breath-pattern", TQ, [
    ("For a 50 butterfly, the usual choice is:", "Few breaths, since each adds drag", "Every stroke", "Every stroke on the first half only", "No kick, more breaths"),
    ("For a 200 butterfly, regular breathing is chosen to:", "Keep the race aerobic", "Reduce drag", "Raise stroke rate", "Shorten the stroke"),
    ("A 1-up-1-down pattern is a compromise between:", "Oxygen supply and drag", "Kick and pull", "Rate and turns", "Start and finish"),
], "Each breath costs a little drag and buys oxygen; the race distance sets the exchange rate")
N("SW-3.3.C", "sw-fly-breath-count", TQ, "A swimmer takes {{ns}} strokes per length and breathes on a {{pt}}-stroke pattern (one breath every {{pt}} strokes). How many breaths in a {{nl}}-length race?",
  given={"ns": {"pick": [18, 20, 24]}, "pt": {"pick": [1, 2]}, "nl": {"pick": [2, 4, 8]}}, value="ns/pt*nl", tex="breaths", final=True,
  verify="Rational(ns*nl, pt)",
  explain="Halving the breaths on a 200 means dozens fewer, which is why the pattern is an oxygen decision there and a drag decision in a 50")
F("SW-3.4.A", "sw-fly-fault", TQ, [
    ("A bent-knee butterfly kick is corrected by cueing:", "Hips at the surface, kick from the chest", "Kick harder", "Bend more", "Point the toes up"),
    ("Arms dragging through the water on recovery usually mean:", "The second kick is missing or late", "The entry is too wide", "The catch is too deep", "The breath is too early"),
    ("A crashing entry is corrected by:", "Placing the hands and letting the chest submerge", "Entering faster", "A wider entry", "A longer glide"),
], "Each butterfly fault has one standard correction, and most trace back to timing or hip height")
F("SW-3.4.A", "sw-fly-fault-rank", TQ, [
    ("With dropped hips and a slightly wide entry, correct first:", "The hips", "The entry", "Both at once", "Neither"),
    ("A fault at the hands is usually worth less than a fault in:", "Body position or timing", "Finger spacing", "Suit choice", "Cap fit"),
    ("Why correct one thing at a time?", "The swimmer can attend to one cue, and you can see what changed", "It is faster", "Rules require it", "It avoids fatigue"),
], "Body position and timing before hand path: the bigger cost first, one cue at a time")
F("SW-3.4.B", "sw-fly-fatigue", TQ, [
    ("Late in a 200 butterfly the first thing usually lost is:", "The second kick", "The entry width", "The start", "The streamline"),
    ("As butterfly fatigues, stroke rate and hips usually:", "Both fall", "Both rise", "Rate rises, hips fall", "Stay the same"),
    ("The cue that best protects speed on the last 50 is:", "Hold hip height and keep the second kick", "Breathe less", "Kick wider", "Lift the head"),
], "Fatigue takes the second kick, then the recovery, then the hips; defend them in that order")
N("SW-3.4.B", "sw-fly-fade-speed", TQ, "On the last 50 a swimmer's stroke rate falls by {{a}}% and distance per stroke by {{b}}%. By what percentage does speed fall?",
  given={"a": {"pick": [4, 8, 11]}, "b": {"pick": [0, 3, 6]}}, value="(1 - (1 - a/100)*(1 - b/100))*100", tex="\\%", tol=0.005,
  verify="(1 - (1 - Rational(a, 100))*(1 - Rational(b, 100)))*100",
  explain="Speed is rate times length, so the losses multiply. Knowing which one fell tells you what to train")
F("SW-3.5.A", "sw-fly-legal-stroke", RU, [
    ("Butterfly with an alternating flutter kick is:", "Illegal", "Legal", "Legal for one kick per length", "Legal after the turn"),
    ("A breaststroke kick during butterfly under World Aquatics rules is:", "Illegal", "Legal", "Legal once per length", "Legal on the finish"),
    ("Butterfly arms must be brought forward:", "Together, over the water", "One at a time", "Under the water", "In any manner"),
    ("Butterfly leg movements must be:", "Simultaneous, though the legs need not be level", "Alternating", "Level at all times", "Still"),
], "Arms forward together over the water, back together under it; legs up and down together")
F("SW-3.5.A", "sw-fly-legal-why", RU, [
    ("An underwater arm recovery in butterfly is a disqualification because the rule requires recovery:", "Over the water", "Under the water", "At the surface", "Beside the body"),
    ("A swimmer whose feet are not at the same level during a simultaneous dolphin kick is:", "Legal", "Illegal", "Warned", "Disqualified at the turn only"),
    ("Who may disqualify a swimmer for a stroke infraction?", "An official with jurisdiction who observed it", "Any coach", "The timer alone", "Another swimmer"),
], "The call rests on what the rule requires, not on how the stroke looked")
F("SW-3.5.B", "sw-fly-masters-kick", RU, [
    ("In U.S. Masters competition, a breaststroke kick in butterfly is:", "Legal", "Illegal", "Legal in relays only", "Legal over 60 only"),
    ("Under World Aquatics rules the same kick is:", "Illegal", "Legal", "Legal for Masters", "Legal on turns"),
    ("USMS allows, per arm pull:", "One breaststroke kick, except before the turn and finish", "Any number", "Two", "None"),
], "The Masters allowance is a national rule difference; the international rule has no breaststroke kick in butterfly")
F("SW-3.5.B", "sw-fly-masters-which-rule", RU, [
    ("A Masters swimmer entering a World Aquatics Masters meet should kick butterfly:", "With dolphin kick only", "With breaststroke kick", "With either", "With flutter kick"),
    ("May a USMS swimmer mix dolphin and breaststroke kicks in one race?", "Yes, interchangeably", "No", "Only in the 200", "Only on the last length"),
    ("The reason to learn which body's rules a meet uses is that:", "The same stroke can be legal in one and a disqualification in the other", "Times are scored differently", "Lanes differ", "Starts differ"),
], "Know the sanctioning body before the race, since the kick rule is the one that differs")
F("SW-3.5.C", "sw-fly-legal-touch", RU, [
    ("A one-hand touch at a butterfly turn is:", "Illegal", "Legal", "Legal if the other hand is close", "Legal at the finish only"),
    ("Both hands touching together but under the water surface is:", "Legal", "Illegal", "Legal at turns only", "Legal at the finish only"),
    ("Hands touching one on top of the other (stacked) are:", "Illegal, since they are not separated", "Legal", "Legal at the finish", "Legal if simultaneous"),
    ("A staggered touch, one hand clearly before the other, is:", "Illegal", "Legal", "Legal at turns", "Legal with a fast finish"),
], "Two hands, separated, at the same time; at, above or below the surface")
F("SW-3.5.C", "sw-fly-touch-meaning", RU, [
    ("'Separated' in the touch rule means the hands:", "Are not stacked; no visible gap is needed", "Are shoulder-width apart", "Are at different heights", "Touch different walls"),
    ("May the two hands touch at different heights on the wall?", "Yes, if simultaneous and separated", "No", "Only at the finish", "Only in Masters"),
    ("The same two-hand touch rule applies to butterfly and:", "Breaststroke", "Freestyle", "Backstroke", "No other stroke"),
], "Simultaneous and separated are the two tests; level is not one of them")
F("SW-3.5.D", "sw-fly-legal-body", RU, [
    ("Kicking on the side underwater after a butterfly start is:", "Legal", "Illegal", "Legal for 5 m only", "Legal in Masters only"),
    ("Being on the back at the first arm stroke in butterfly is:", "Illegal", "Legal", "Legal off turns", "Legal off the start"),
    ("From the first arm stroke the body must be:", "On the breast", "On the side", "On the back", "In any position"),
], "Any position underwater, but on the breast from the first arm stroke")
F("SW-3.5.D", "sw-fly-body-when", RU, [
    ("The on-the-breast requirement in butterfly starts:", "At the first arm stroke after the start and each turn", "At the start signal", "At 15 m", "At the touch"),
    ("A swimmer pushes off a butterfly turn on the side and rotates to the breast before pulling. This is:", "Legal", "Illegal", "Illegal past 5 m", "Legal at the start only"),
    ("How many arm pulls may be taken under water in butterfly after a start or turn?", "One, which must bring the swimmer to the surface", "None", "Two", "Any number within 15 m"),
], "The rule fixes position at the pull, which is why side-kicking underwaters are allowed")

# ── unit 4: breaststroke and IM ───────────────────────────────────────────────────────────────────────────────
F("SW-4.1.A", "sw-breast-timing", TQ, [
    ("Breaststroke timing is:", "Pull, breathe, kick, glide", "Kick, pull, breathe, glide", "Pull and kick together", "Glide, kick, pull, breathe"),
    ("Breaststroke is the most drag-sensitive stroke because:", "Arms and legs recover under water against the flow", "It is the slowest", "It has no glide", "The head stays under"),
    ("The breaststroke breath comes:", "Late in the pull", "Before the pull", "During the kick", "During the glide"),
], "The speed swings most within a breaststroke cycle, so the streamlined glide carries it")
F("SW-4.1.A", "sw-breast-glide", TQ, [
    ("The breaststroke kick should land as the hands:", "Shoot forward into streamline", "Begin the outsweep", "Are under the chest", "Finish the insweep"),
    ("A breaststroker with no glide loses:", "The part of the cycle with the least drag", "Stroke rate", "The breath", "The kick"),
    ("'Swim downhill' in breaststroke means:", "Lean forward so the hips ride high", "Dive deep each stroke", "Kick downward", "Look at the bottom of the far wall"),
], "Kick into a long body line: the glide is where the kick's speed is kept")
F("SW-4.1.B", "sw-breast-fault", TQ, [
    ("Knees drawn up under the hips in breaststroke:", "Add frontal area like a brake", "Add thrust", "Raise the hips", "Shorten the glide usefully"),
    ("The correction for knees under the hips is:", "Heels to the seat with knees narrow", "Wider knees", "A slower kick", "A deeper pull"),
    ("A pull that sweeps back past the shoulders:", "Delays the recovery and adds drag", "Adds thrust", "Is required", "Lifts the hips"),
    ("A late kick, after the arms are already extended, causes:", "A dead spot where the body slows", "A faster glide", "A higher breath", "A shorter stroke"),
], "Narrow knees, heels up, a compact pull, and a kick timed to the hands shooting forward")
F("SW-4.1.B", "sw-breast-kick-direction", TQ, [
    ("A good breaststroke kick pushes water:", "Backward with the insides of the feet", "Downward", "Sideways", "Upward"),
    ("At the catch of the breaststroke kick the feet are:", "Turned out and flexed", "Pointed", "Together", "Crossed"),
    ("The teaching progression for breaststroke kick starts:", "On the wall, then on the back, then on the belly", "With full stroke", "With a pull buoy", "With fins"),
], "The feet must face backward to push backward, which is why they turn out and flex")
F("SW-4.2.A", "sw-breast-pullout", RU, [
    ("How many butterfly kicks are allowed in a breaststroke pull-out?", "One", "None", "Two", "Any number before 15 m"),
    ("The head must break the surface before the hands:", "Turn inward at the widest part of the second stroke", "Start the first pull-down", "Leave the wall", "Finish the second stroke"),
    ("Two dolphin kicks during the pull-out is:", "Illegal", "Legal", "Legal off the start only", "Legal in the 50 only"),
], "One pull-down, one dolphin kick, then the head up before the second stroke turns in")
F("SW-4.2.A", "sw-breast-pullout-sequence", RU, [
    ("A legal pull-out contains:", "One arm stroke back to the legs, one butterfly kick, then a breaststroke kick", "Two arm strokes", "Flutter kicks", "No kick at all by rule"),
    ("A common teaching count for the pull-out is:", "Streamline 3, pull down 2, recover 1", "1, 2, 3", "5, 5, 5", "No pause"),
    ("The single butterfly kick may be taken:", "Before the first breaststroke kick", "After every stroke", "On the surface each cycle", "At the finish"),
], "The pull-out is one underwater cycle with one extra kick; the count paces the glides")
F("SW-4.2.B", "sw-breast-legal-cycle", RU, [
    ("Two arm strokes followed by one kick in breaststroke is:", "Illegal", "Legal", "Legal at the turn", "Legal in Masters"),
    ("A downward butterfly kick mid-length in breaststroke is:", "Illegal", "Legal", "Legal once per length", "Legal at the finish"),
    ("A breaststroke touch must be made with:", "Both hands, separated and simultaneous", "One hand", "Either hand", "The head"),
    ("Breaststroke leg movements must be:", "Simultaneous and in the same horizontal plane", "Alternating", "Any style", "Scissor"),
], "One arm stroke then one kick, legs together, two hands on the wall")
F("SW-4.2.B", "sw-breast-legal-detail", RU, [
    ("During each breaststroke cycle some part of the head must:", "Break the surface", "Stay under", "Touch the hands", "Face sideways"),
    ("A scissor kick in breaststroke is:", "Illegal", "Legal", "Legal for one kick", "Legal in the IM"),
    ("The cycle order the rule requires is:", "One arm stroke and one leg kick, in that order", "Kick then pull", "Any order", "Two kicks then a pull"),
], "The head surfaces every cycle, which is what stops breaststroke being swum under water")
F("SW-4.2.C", "sw-im-order", RU, [
    ("The individual medley order is:", "Butterfly, backstroke, breaststroke, freestyle", "Backstroke, breaststroke, butterfly, freestyle", "Freestyle, backstroke, breaststroke, butterfly", "Butterfly, breaststroke, backstroke, freestyle"),
    ("The medley relay order is:", "Backstroke, breaststroke, butterfly, freestyle", "Butterfly, backstroke, breaststroke, freestyle", "Freestyle, butterfly, backstroke, breaststroke", "Backstroke, butterfly, breaststroke, freestyle"),
    ("The freestyle leg of an IM may not be swum as:", "Backstroke, breaststroke or butterfly", "Front crawl", "Any stroke", "Sidestroke"),
], "The relay starts with backstroke because that start is in the water")
F("SW-4.2.C", "sw-im-transition", RU, [
    ("Each section of the IM must finish according to:", "The rule for the stroke being finished", "The next stroke's rule", "Freestyle rules", "The swimmer's choice"),
    ("At the back-to-breast IM transition the swimmer must touch the wall:", "While still on the back", "On the breast", "With two hands", "With the feet"),
    ("At the fly-to-back transition the touch must be:", "Two hands, simultaneous", "One hand", "On the back", "With the feet"),
], "Finish each stroke by its own rule, then leave the wall by the next one")
N("SW-4.3.A", "sw-im-split-share", PC, "A 200 IM is swum with splits of {{f}} s fly, {{b}} s back, {{r}} s breast and {{c}} s free. What percentage of the race is the breaststroke leg?",
  given={"f": {"pick": [28, 30]}, "b": {"pick": [33, 35]}, "r": {"pick": [38, 41]}, "c": {"pick": [31, 33]}},
  value="r/(f + b + r + c)*100", tex="\\%", tol=0.005, verify="Rational(r*100, f + b + r + c)",
  explain="Breaststroke is the slowest leg for everyone, so its share is always the largest; the question is how it compares with a reference swimmer's share")
N("SW-4.3.A", "sw-im-weak-leg", PC, "A swimmer's breaststroke leg is {{r}} s where a reference swimmer of the same total time swims {{rr}} s. How many seconds is the swimmer giving away on that leg?",
  given={"r": {"pick": [39.5, 41.0, 42.5]}, "rr": {"pick": [37.0, 38.5]}}, value="r - rr", tex="s", verify="nsimplify(r) - nsimplify(rr)",
  explain="Compare leg by leg against someone of the same overall time: the leg with the largest positive difference is the weak one, and the others are paying for it")

# ── unit 5: starts, turns, underwaters ────────────────────────────────────────────────────────────────────────
F("SW-5.1.A", "sw-start-phases", WL, [
    ("The phases of a start in order are:", "Reaction, block, flight, entry", "Flight, block, reaction, entry", "Block, reaction, entry, flight", "Entry, flight, block, reaction"),
    ("The phase that contributes most to speed at entry is:", "The push from the block", "The reaction", "The flight", "The signal"),
    ("In a track start the feet are:", "One forward over the edge, one back", "Both over the edge", "Both back", "Crossed"),
], "A fast reaction saves hundredths; the push and a clean entry decide the speed carried into the water")
N("SW-5.1.A", "sw-start-reaction-share", WL, "A swimmer reaches 15 m in {{t15}} s with a reaction time of {{rt}} s. What percentage of the 15 m time is reaction?",
  given={"t15": {"pick": [5.8, 6.5, 7.4]}, "rt": {"pick": [0.62, 0.70, 0.78]}}, value="rt/t15*100", tex="\\%", tol=0.005,
  verify="nsimplify(rt)/nsimplify(t15)*100",
  explain="Reaction is about a tenth of the start. The other nine tenths are impulse, entry and underwater speed, which is where start practice pays")
F("SW-5.1.B", "sw-start-entry", WL, [
    ("An entry that is too flat costs time through:", "Splash and wave resistance", "A long path back up", "A slow reaction", "A weak push"),
    ("An entry that is too deep costs time through:", "A longer path back to the surface", "Wave resistance", "Splash", "A slow reaction"),
    ("A clean entry puts the whole body through:", "One hole in the water", "A wide splash", "The surface feet first", "Two holes"),
], "Deep enough to be under the waves, shallow enough to come up without a detour")
F("SW-5.1.B", "sw-start-safety", WL, [
    ("Before racing starts are taught, a swimmer must show:", "A shallow head-first entry into deep water", "A flip turn", "A legal breaststroke kick", "A 200 swim"),
    ("Start practice should be:", "Supervised, never left to swimmers alone", "Done in the shallow end", "Done without a coach", "Done with other swimmers in the lane ahead"),
    ("Young swimmers may be told not to dolphin kick off a start in shallow water because:", "They may drive themselves to the bottom", "It is illegal", "It is slower", "It tires them"),
], "The start is the one skill with a real injury risk, so depth and supervision come before speed")
F("SW-5.1.C", "sw-start-legal", RU, [
    ("A swimmer who starts before the signal is:", "Disqualified", "Warned once", "Recalled without penalty", "Given a time penalty"),
    ("In U.S. Masters competition, an in-water start is:", "Allowed", "Not allowed", "Allowed in relays only", "Allowed in backstroke only"),
    ("Movement on the block after 'take your marks' but before the signal that leads to an early start is judged:", "After the signal has sounded", "Before the signal only", "By the timers", "By the swimmers"),
], "One start: leaving before the signal is a disqualification, called once the signal has been given")
F("SW-5.1.C", "sw-start-legal-detail", RU, [
    ("After the command 'take your marks' swimmers must:", "Take a starting position and become stationary", "Dive immediately", "Step back", "Wave to the referee"),
    ("How many false starts does a swimmer get under the current rule?", "None; the first is a disqualification", "One", "Two", "One per session"),
    ("Backstroke and medley-relay starts are made:", "In the water", "From the blocks", "From the deck", "From either"),
], "The stationary requirement is what lets officials judge the start fairly")
F("SW-5.2.A", "sw-open-turn", WL, [
    ("In a butterfly or breaststroke turn the swimmer touches with:", "Both hands, then drops one elbow back", "One hand", "The feet first", "The head"),
    ("An open turn is shortened by:", "Tucking the knees tight for a small rotation radius", "Staying long", "Lifting the head high", "Pausing on the wall"),
    ("After the touch the sequence is:", "Two hands, one hand, no hands, push", "Push, then touch", "One hand, two hands, push", "Hands stay until the feet leave"),
    ("The push-off from an open turn is made:", "On the side, rotating to the breast", "Flat on the back", "Feet first", "At the surface"),
], "Touch, drop an elbow, tuck small, throw the head and arm over, leave on the side")
N("SW-5.2.A", "sw-turn-tuck-speed", WL, "Angular momentum is conserved in a turn. If a tighter tuck cuts the swimmer's moment of inertia by {{pc}}%, by what percentage does the rotation speed rise?",
  given={"pc": {"pick": [20, 33, 50]}}, value="(1/(1 - pc/100) - 1)*100", tex="\\%", tol=0.005,
  verify="(1/(1 - Rational(pc, 100)) - 1)*100",
  explain="Halving the moment of inertia doubles the spin. That is the whole argument for knees tight and heels to the seat")
N("SW-5.2.B", "sw-wall-time", WL, "A swimmer takes {{ti}} s from 5 m out to the wall and {{to}} s from the wall back to 5 m. What is the turn time in seconds?",
  given={"ti": {"pick": [2.9, 3.2, 3.6]}, "to": {"pick": [2.1, 2.4, 2.8]}}, value="ti + to", tex="s", verify="nsimplify(ti) + nsimplify(to)",
  explain="Turn time is always measured over fixed distances either side of the wall, so two swimmers or two attempts can be compared")
N("SW-5.2.B", "sw-wall-time-race", WL, "One turn is {{d}} s faster than before. Over a short-course {{dist}} race, how many seconds does that save across all the turns?",
  given={"d": {"pick": [0.1, 0.2, 0.3]}, "dist": {"pick": [100, 200, 500]}}, value="d*(dist/25 - 1)", tex="s",
  verify="nsimplify(d)*(Rational(dist, 25) - 1)",
  explain="A race of n lengths has n − 1 turns. A tenth per turn is nearly two seconds in a 500, more than most training blocks deliver")
F("SW-5.2.C", "sw-back-turn-legal", RU, [
    ("At a backstroke flip turn, after rolling onto the breast the swimmer may take:", "One continuous single or double arm pull to start the turn", "Several freestyle strokes", "A glide of any length with kicks", "No arm pull"),
    ("Kicking into the wall on the breast after the pull has finished, without starting the turn, is:", "Illegal", "Legal", "Legal for 2 kicks", "Legal in Masters"),
    ("When the feet leave the wall after a backstroke turn the swimmer must be:", "On the back", "On the breast", "On the side toward the breast", "In any position"),
], "Roll, one continuous pull into the turn, touch, and leave on the back")
F("SW-5.2.C", "sw-back-turn-count", RU, [
    ("To time a backstroke turn, a swimmer counts strokes from:", "The flags to the wall", "The start", "The 15 m mark", "The middle of the pool"),
    ("If it is four strokes from the flags to the wall, the roll comes on stroke:", "Four, taken across the body, after three on the back", "One", "Two", "Five"),
    ("At a backstroke turn, some part of the swimmer must:", "Touch the wall", "Stay above water", "Touch the lane rope", "Touch the bottom"),
], "The count from the flags is what makes the roll land at the right distance from the wall")
F("SW-5.3.A", "sw-15m-legal", RU, [
    ("The head must break the surface by how far after a start or turn in fly, back and free?", "15 m", "10 m", "20 m", "25 m"),
    ("A backstroker who surfaces at 16 m after the start is:", "Disqualified", "Legal", "Warned", "Legal in the 200"),
    ("The 15 m limit applies:", "After the start and after each turn", "After the start only", "On the last length only", "Never in freestyle"),
], "Fully submerged for at most 15 m off every wall")
F("SW-5.3.A", "sw-15m-which-strokes", RU, [
    ("The stroke with no 15 m underwater limit, because its pull-out is defined instead, is:", "Breaststroke", "Butterfly", "Backstroke", "Freestyle"),
    ("In freestyle, apart from the 15 m after start and turns, the swimmer must:", "Break the surface throughout the race", "Stay on the breast", "Use a flutter kick", "Touch with two hands"),
    ("What must break the surface by 15 m?", "The head", "A hand", "A foot", "The hips"),
], "Three strokes share the 15 m rule; breaststroke has its one-cycle pull-out")
N("SW-5.3.B", "sw-underwater-vs-surface", WL, "A swimmer kicks underwater at {{vu}} m/s and swims at {{vs}} m/s. Over {{d}} m, how many seconds does staying under save? (Negative means it costs time.)",
  given={"vu": {"pick": [1.6, 1.9, 2.2]}, "vs": {"pick": [1.7, 1.85]}, "d": {"pick": [5, 10]}}, value="d/vs - d/vu", tex="\\Delta t", tol=0.01,
  verify="d/nsimplify(vs) - d/nsimplify(vu)",
  explain="Stay under only while underwater speed is above surface speed. For many swimmers that is true for the first few metres and false by ten")
N("SW-5.3.B", "sw-underwater-breakeven", WL, "Off a wall a swimmer's underwater speed starts at {{v0}} m/s and falls by {{dk}} m/s for every metre travelled. Surface speed is {{vs}} m/s. After how many metres should the swimmer surface?",
  given={"v0": {"pick": [2.6, 3.0]}, "dk": {"pick": [0.1, 0.15]}, "vs": {"pick": [1.6, 1.8]}}, value="(v0 - vs)/dk", tex="m", tol=0.005,
  verify="(nsimplify(v0) - nsimplify(vs))/nsimplify(dk)",
  explain="Surface where the two speeds cross. Past that point every metre under water is slower than swimming it, quite apart from the oxygen")
F("SW-5.3.C", "sw-underwater-kick-count", WL, [
    ("The number of underwater kicks per wall in a 200 fly should be one the swimmer can:", "Repeat on every wall when tired", "Hit only on the first wall", "Double on the last wall", "Skip in the middle"),
    ("Underwater kicking in a 200 costs mainly:", "Oxygen", "Stroke rate", "Friction", "Reaction time"),
    ("Compared with a 100, a 200 fly usually uses:", "Fewer kicks per wall", "More kicks per wall", "The same on every wall as a 50", "No underwater kicking"),
], "The count is a budget: choose what the last wall can still afford")
N("SW-5.3.C", "sw-underwater-total", WL, "A swimmer takes {{nk}} dolphin kicks off each wall in a short-course {{dist}} butterfly, including the start. How many underwater kicks is that in total?",
  given={"nk": {"pick": [4, 6, 8]}, "dist": {"pick": [100, 200]}}, value="nk*dist/25", tex="kicks", final=True, verify="Rational(nk*dist, 25)",
  explain="Start plus n − 1 turns is n walls. The total shows why two extra kicks per wall is a very different ask in a 200")
F("SW-5.3.D", "sw-breakout", WL, [
    ("The first stroke of a breakout should begin:", "Just before the head breaks the surface", "After a pause at the surface", "At the wall", "After the first breath"),
    ("Surfacing and then pausing before stroking:", "Loses the underwater speed", "Saves energy for later", "Is faster", "Is required"),
    ("On the first stroke of a freestyle breakout the swimmer should usually:", "Not breathe", "Breathe immediately", "Lift the head", "Stop kicking"),
], "Rise at kicking speed and stroke through the surface so the speed is handed on, not dropped")
F("SW-5.3.D", "sw-breakout-angle", WL, [
    ("A breakout that rises too steeply:", "Trades forward speed for height", "Is fastest", "Reduces drag", "Is required at 15 m"),
    ("A breakout that is too flat and long risks:", "Passing the 15 m mark or slowing below swim speed", "A false start", "A two-hand touch", "A scissor kick"),
    ("The sequence off every wall is:", "Streamline, kick, swim", "Swim, kick, streamline", "Kick, streamline, breathe", "Breathe, swim, kick"),
], "A shallow, steady rise keeps the speed pointed down the pool")

# ── units 7-9: race analysis, physiology, training ────────────────────────────────────────────────────────────
N("SW-7.2.B", "sw-slowdown-source", PC, "Between the first and last lengths a swimmer's stroke rate goes from {{s1}} to {{s2}} cycles/min and distance per cycle from {{d1}} to {{d2}} m. By what percentage did speed fall?",
  given={"s1": {"pick": [52, 56]}, "s2": {"pick": [46, 50]}, "d1": {"pick": [2.0, 2.1]}, "d2": {"pick": [1.9, 2.0]}},
  value="(1 - s2*d2/(s1*d1))*100", tex="\\%", tol=0.01, verify="(1 - s2*nsimplify(d2)/(s1*nsimplify(d1)))*100",
  explain="Split the loss into its two factors. In a 100 m sprint the fall is mostly stroke rate; in longer races distance per stroke often goes first")
F("SW-7.2.B", "sw-slowdown-read", PC, [
    ("Velocity fell 12% while stroke rate fell 11% and stroke length barely changed. The swimmer slowed by losing:", "Stroke rate", "Distance per stroke", "Both equally", "Neither"),
    ("Stroke rate held but distance per stroke fell 8%. The likely cause is:", "A slipping catch or dropped hips", "A slow turnover", "A late start", "A long glide"),
    ("Why separate the two causes?", "They are trained differently", "The rules require it", "They are the same thing", "Only one can be measured"),
], "Rate loss is a power and tempo problem; length loss is a technique-under-fatigue problem")
F("SW-7.3.A", "sw-pacing-profile", PC, [
    ("Going out too fast in a 200 fly mainly spends early:", "Glycolytic capacity", "Fat stores", "Reaction time", "Stroke count"),
    ("For the same average speed, an uneven pace costs:", "More energy than an even one", "Less energy", "The same", "No energy"),
    ("The usual advice for a 200 is to swim it:", "Close to even, with a controlled first 50", "All-out from the start", "Slow then sprint the last 25", "With a slow middle only"),
], "Because power goes as speed cubed, fast-then-slow is the most expensive way to reach an average")
N("SW-7.3.A", "sw-uneven-pace-cost", PC, "A swimmer covers half a race at {{dp}}% above average speed and half at {{dp}}% below. With power proportional to v³, by what percentage is the average power above that of even pace?",
  given={"dp": {"pick": [3, 5, 8]}}, value="(((1 + dp/100)^3 + (1 - dp/100)^3)/2 - 1)*100", tex="\\%", tol=0.01,
  verify="3*Rational(dp, 100)**2*100",
  explain="The extra is 3δ²: small for small swings and growing fast. Even pacing is the cheapest way to hold an average speed")
F("SW-8.1.A", "sw-energy-systems", PH, [
    ("The energy pathway that dominates the first 10 seconds of all-out work is:", "ATP-CP", "Anaerobic glycolysis", "Aerobic", "Fat oxidation"),
    ("Anaerobic glycolysis supplies high energy for up to about:", "2 minutes", "10 seconds", "20 minutes", "An hour"),
    ("The aerobic pathway dominates efforts longer than about:", "1.5 to 2 minutes", "10 seconds", "30 seconds", "10 minutes"),
    ("The pathway that can use fat as fuel is:", "Aerobic", "ATP-CP", "Anaerobic glycolysis", "None"),
], "Fastest and smallest first: phosphagen, then glycolysis, then the aerobic system with the largest capacity")
F("SW-8.1.A", "sw-energy-overlap", PH, [
    ("The three pathways during a race:", "Overlap, with the mix shifting over time", "Switch on one after another", "Never work together", "Work only in training"),
    ("Intensity and the duration it can be held are:", "Inversely related", "Unrelated", "Directly related", "Equal"),
    ("A byproduct of anaerobic glycolysis that accumulates in hard efforts is:", "Lactate", "Creatine", "Glycogen", "Oxygen"),
], "No pathway works alone; the question is always which one is carrying most of the load")
F("SW-8.1.B", "sw-aerobic-mix", PH, [
    ("An all-out 50 is supplied:", "Mostly anaerobically", "Mostly aerobically", "Evenly", "By fat"),
    ("An all-out 200 is supplied:", "Mostly aerobically", "Mostly by ATP-CP", "Entirely anaerobically", "By fat alone"),
    ("Aerobic and anaerobic contributions are about equal in an all-out effort of roughly:", "75 seconds", "10 seconds", "5 minutes", "20 minutes"),
], "The crossover near 75 seconds is why a 100 fly sits on the fence and a 200 is an aerobic event")
F("SW-8.1.B", "sw-aerobic-mix-train", PH, [
    ("A swimmer racing mainly 200s and up needs a training base that is mostly:", "Aerobic", "Phosphagen", "Start practice", "Maximal sprinting"),
    ("A 50 specialist still does aerobic work mainly to:", "Recover between efforts and support training volume", "Supply the race", "Raise stroke count", "Replace sprint work"),
    ("A race's energy mix is estimated first from its:", "Duration", "Stroke", "Pool length", "Lane"),
], "Duration tells you the mix, and the mix tells you what the training has to build")
F("SW-8.2.A", "sw-threshold", PH, [
    ("Maximal lactate steady state is the highest pace at which:", "Lactate production and removal balance", "Lactate is zero", "Heart rate is maximal", "Stroke rate peaks"),
    ("Above the threshold pace:", "Lactate climbs and time to exhaustion shortens sharply", "Lactate falls", "Nothing changes", "The effort becomes aerobic only"),
    ("Thresholds anchor training paces because:", "They mark where the body's response changes character", "They are easy to guess", "They never change", "Rules define them"),
], "The threshold is a boundary between sustainable and unsustainable, so paces are set relative to it")
F("SW-8.2.A", "sw-threshold-test", PH, [
    ("A long timed swim such as a T30 estimates:", "A sustainable aerobic pace", "Sprint power", "Reaction time", "Start speed"),
    ("As a swimmer gets fitter, the threshold pace:", "Gets faster", "Gets slower", "Stays fixed", "Disappears"),
    ("Training paces set from an old test become:", "Too easy as fitness improves", "Too hard", "More accurate", "Irrelevant to fitness"),
], "A threshold is measured, not assumed, and it moves, so the test is repeated through the season")
F("SW-8.2.B", "sw-adaptation-match", PH, [
    ("Basic and threshold aerobic work mainly builds:", "Capillaries and mitochondria", "Buffering", "Peak power", "Reaction time"),
    ("Lactate-tolerance sets mainly build:", "Buffering capacity", "Capillaries", "Flexibility", "Stroke length"),
    ("Short maximal sprints with long rest mainly build:", "Power and the rate of glycolysis", "Aerobic capacity", "Buffering", "Fat use"),
], "Specificity: the adaptation follows the stimulus, so the set is chosen from the adaptation wanted")
F("SW-8.2.B", "sw-training-principles", PH, [
    ("'Training must exceed what the body is used to' is the principle of:", "Overload", "Reversibility", "Specificity", "Recovery"),
    ("'Adaptation occurs in the systems and movements trained' is the principle of:", "Specificity", "Overload", "Progression", "Individual difference"),
    ("'Neglected qualities are lost' is the principle of:", "Reversibility", "Overload", "Specificity", "Progression"),
    ("Adaptation actually takes place during:", "Recovery", "The main set", "The warm-up", "The race"),
], "Six principles: overload, progression, individual difference, specificity, reversibility, recovery")
F("SW-9.3.A", "sw-season-cycles", TR, [
    ("A macrocycle is:", "The whole season, planned back from the key meet", "One week", "One practice", "A six-week block"),
    ("A mesocycle averages about:", "6 weeks", "1 week", "1 day", "6 months"),
    ("A microcycle is usually:", "One week", "Six weeks", "One season", "One set"),
    ("Across a season, volume peaks:", "Before intensity peaks", "After intensity peaks", "During the taper", "In the first week"),
], "Season, block, week: plan backward from the meet, and build volume before intensity")
N("SW-9.3.A", "sw-season-blocks", TR, "A season is {{wk}} weeks long and ends with a {{tp}}-week taper. How many full six-week training blocks fit before the taper?",
  given={"wk": {"pick": [10, 16, 20, 26]}, "tp": {"pick": [1, 2, 3]}}, value="floor((wk - tp)/6)", tex="blocks", final=True,
  verify="floor(Rational(wk - tp, 6))",
  explain="Taper time comes out of training time. A ten-week season cannot hold a three-week taper and still have two blocks, which is why short seasons use short tapers")

# ── unit 10: video ────────────────────────────────────────────────────────────────────────────────────────────
N("SW-10.1.A", "sw-video-cycle-time", VD, "On a {{fps}} fps clip one full stroke cycle takes {{fr}} frames. What is the stroke rate in cycles per minute?",
  given={"fps": {"pick": [30, 60, 120]}, "fr": {"pick": [36, 45, 80]}}, value="60*fps/fr", tex="cyc/min", tol=0.005,
  verify="Rational(60*fps, fr)",
  explain="Cycle time is frames over frame rate; rate is its inverse. Count from one hand entry to the same hand's next entry")
N("SW-10.1.A", "sw-stopwatch-rate", VD, "By stopwatch, five full stroke cycles take {{t5}} s. What is the time per cycle in seconds?",
  given={"t5": {"pick": [5.6, 7.4, 11.0]}}, value="t5/5", tex="s", verify="nsimplify(t5)/5",
  explain="Start the watch on a hand entry, count that as zero, stop on the fifth entry after it. The deck shortcut is double the time and move the decimal point")
N("SW-10.1.B", "sw-video-resolution", VD, "A swimmer moves at {{v}} m/s on a {{fps}} fps clip. How many centimetres does the swimmer travel between frames?",
  given={"v": {"pick": [1.5, 2.0, 2.4]}, "fps": {"pick": [30, 60, 120]}}, value="v/fps*100", tex="cm", tol=0.005,
  verify="nsimplify(v)*100/fps",
  explain="At 2 m/s, 30 fps gives nearly 7 cm per frame and 120 fps under 2 cm. The camera decides how fine an event you can place")
N("SW-10.1.B", "sw-video-timing-error", VD, "An event can be placed only to the nearest frame on a {{fps}} fps clip. What is the largest timing error, in milliseconds, from reading one frame boundary?",
  given={"fps": {"pick": [30, 60, 120, 240]}}, value="1000/fps", tex="ms", tol=0.005, verify="Rational(1000, fps)",
  explain="A 30 fps clip cannot resolve anything shorter than 33 ms, so it is fine for stroke rate and useless for comparing two touches")
F("SW-10.1.C", "sw-camera-angle", VD, [
    ("To see catch depth and kick timing, film from:", "The side, under water", "Directly in front", "Overhead", "Behind above water"),
    ("To see symmetry and hand path width, film from:", "The front", "The side", "The deck at an angle", "Behind above water"),
    ("To see body line and lateral snaking, film from:", "Overhead", "The side", "The front at water level", "Under the swimmer"),
], "Each fault lives in one plane, so the camera goes perpendicular to that plane")
F("SW-10.1.C", "sw-camera-parallax", VD, [
    ("An off-axis camera makes joint angles look:", "Different from their true size", "Exact", "Always larger", "Always smaller"),
    ("To measure an elbow angle from video the camera must be:", "Perpendicular to the plane of the arm", "As close as possible", "Moving with the swimmer", "Above the water"),
    ("Filming through the surface from the deck distorts the image because of:", "Refraction and surface ripple", "Frame rate", "Lens brand", "Pool temperature"),
], "Parallax and refraction are why an angle read off a casual clip should be treated as a rough guide")
N("SW-10.2.A", "sw-event-percent", VD, "A butterfly cycle is {{cy}} frames long. The second kick's downbeat finishes {{ev}} frames after hand entry. At what percentage of the cycle does it occur?",
  given={"cy": {"pick": [60, 72, 80]}, "ev": {"pick": [36, 42, 48]}}, value="ev/cy*100", tex="\\%", tol=0.005, verify="Rational(ev*100, cy)",
  explain="Events as a percentage of the cycle can be compared between clips at different speeds and frame rates; raw frame counts cannot")
F("SW-10.2.A", "sw-event-marking", VD, [
    ("The convenient zero for marking a butterfly cycle is:", "Hand entry", "The breath", "The hips' highest point", "The wall"),
    ("Events are expressed as a percentage of cycle time so that:", "Clips at different tempos compare", "The numbers are bigger", "Frame rate is ignored entirely", "They match the rules"),
    ("The key butterfly events to mark are:", "Entry, catch, push, exit, kick 1, kick 2 and breath", "Start and finish only", "Turns only", "Splits only"),
], "One zero, one cycle, every event as a fraction of it")
F("SW-10.2.B", "sw-video-diagnose", VD, [
    ("A clip shows low hips, a slightly wide entry and a late breath. Work first on:", "The late breath and hips, which cost the most", "The entry width", "All three at once", "None until next season"),
    ("Faults are ranked by:", "How much net force they cost", "How easy they are to see", "Their order in the stroke", "The swimmer's preference"),
    ("The usual order of priority is:", "Body position and timing before hand path", "Hand path first", "Kick last always", "Head last"),
], "Rank by cost, then pick one correction")
F("SW-10.2.B", "sw-video-one-cue", VD, [
    ("After diagnosis the swimmer should be given:", "One correction to work on", "A list of every fault", "No feedback", "Three cues per length"),
    ("A fault that disappears when the upstream cause is fixed was:", "A symptom", "The root cause", "Unrelated", "A rule violation"),
    ("Before choosing a correction from one clip, confirm the fault:", "Appears on more than one cycle", "Appears once", "Is on the worst length only", "Is visible to the swimmer"),
], "One cue at a time, aimed at a cause that shows up cycle after cycle")
F("SW-10.2.C", "sw-before-after", VD, [
    ("To test a correction, hold constant:", "Effort or stroke rate, and measure the other", "Nothing", "The suit only", "The time of day only"),
    ("Why change one thing at a time?", "Otherwise you cannot tell what caused the difference", "It is quicker", "Rules require it", "It avoids fatigue"),
    ("Why repeat each trial?", "A single swim cannot be told apart from normal variation", "To tire the swimmer", "To fill the session", "The watch needs calibrating"),
], "Fix one of rate or effort, change one thing, and repeat enough to beat the noise")
N("SW-10.2.C", "sw-trial-noise", VD, "Repeat 25 m times at fixed effort vary with a standard deviation of {{sd}} s. With {{n}} trials before and {{n}} after, what is the standard error of each mean, in seconds?",
  given={"sd": {"pick": [0.20, 0.30]}, "n": {"pick": [4, 9, 16]}}, value="sd/sqrt(n)", tex="s", tol=0.005, verify="nsimplify(sd)/sqrt(n)",
  explain="A change smaller than a couple of standard errors is not evidence. Four trials each halve the noise; one trial each tells you nothing")

# ── unit 11: practice design ──────────────────────────────────────────────────────────────────────────────────
F("SW-11.1.A", "sw-session-parts", PR, [
    ("The part of a session that carries the day's training purpose is the:", "Main set", "Warm-up", "Cool-down", "Kick set"),
    ("A warm-up exists to:", "Raise muscle temperature and rehearse technique", "Build aerobic capacity", "Test fitness", "Replace the main set"),
    ("A senior main set should last at least about:", "20 to 30 minutes", "5 minutes", "2 hours", "One repeat"),
], "Warm-up, pre-set, main set, cool-down: each part has one job")
F("SW-11.1.A", "sw-session-dirt", PR, [
    ("In DIRT, the letters stand for:", "Distance, interval, rest, time", "Drill, intensity, rate, tempo", "Distance, intensity, repeats, taper", "Dryland, interval, rest, turns"),
    ("In '10 x 100 on 1:30', the 1:30 is the:", "Interval (send-off)", "Rest", "Swim time", "Total time"),
    ("Changing which DIRT variable sets the intensity of a repeat?", "Time", "Distance", "Rest only", "None"),
], "Any interval set is fully described by four numbers, and changing one changes the stimulus")
N("SW-11.1.B", "sw-workout-yardage", PR, "A session is {{a}} warm-up, {{n1}} x {{d1}} and {{n2}} x {{d2}}, then {{c}} cool-down. What is the total distance?",
  given={"a": {"pick": [400, 600]}, "n1": {"pick": [8, 10]}, "d1": {"pick": [100, 200]}, "n2": {"pick": [12, 16]}, "d2": {"pick": [25, 50]}, "c": {"pick": [200, 300]}},
  value="a + n1*d1 + n2*d2 + c", tex="total", final=True, verify="a + n1*d1 + n2*d2 + c",
  explain="Repeats times distance, summed. Totalling a written workout before swimming it is how a coach checks it fits the hour")
N("SW-11.1.B", "sw-set-duration", PR, "How many minutes does {{n}} x {{d}} on {{so}} seconds take?",
  given={"n": {"pick": [8, 10, 20]}, "d": {"pick": [50, 100]}, "so": {"pick": [60, 80, 90]}}, value="n*so/60", tex="min", tol=0.005,
  verify="Rational(n*so, 60)",
  explain="A set's length is repeats times send-off, whatever the swimmer's speed. That is what makes interval sets plannable to the minute")
N("SW-11.1.C", "sw-sendoff-choose", PR, "A swimmer's target pace is {{p}} s per 100. For repeats of {{d}} with about {{r}} s rest, what send-off, rounded up to the next 5 seconds, should be set?",
  given={"p": {"pick": [72, 78, 84]}, "d": {"pick": [100, 200]}, "r": {"pick": [10, 20]}}, value="ceil((p*d/100 + r)/5)*5", tex="s", final=True,
  verify="ceiling(Rational(p*d + 100*r, 500))*5",
  explain="Send-off is swim time plus rest, rounded to something readable on a pace clock")
N("SW-11.1.C", "sw-sendoff-rest", PR, "On 100s leaving every {{so}} s, a swimmer holding {{t}} s gets how many seconds of rest?",
  given={"so": {"pick": [80, 90, 105]}, "t": {"pick": [68, 72, 77]}}, value="so - t", tex="s", final=True, verify="so - t",
  explain="Interval equals swim time plus rest. The faster you swim, the more rest you earn, which is why the same set suits a range of swimmers")
F("SW-11.2.A", "sw-drill-choice", PR, [
    ("To isolate butterfly timing, a good drill is:", "One-arm butterfly", "Kick with a board", "Vertical kicking", "Pulling with paddles"),
    ("To build the body wave before adding arms, use:", "Head-lead body dolphin", "Catch-up freestyle", "Sculling", "Backstroke kick"),
    ("To build rotation and balance in freestyle, use:", "Kick on the side", "Double-arm backstroke", "Breaststroke pull", "Vertical kicking"),
], "A drill isolates one element; choose it from the fault")
F("SW-11.2.A", "sw-drill-transfer", PR, [
    ("A drill transfers to the race stroke only if it is followed by:", "Full stroke at race tempo", "More of the same drill", "A cool-down", "Kick sets"),
    ("A drill done well but never bridged back to full stroke:", "Improves the drill", "Improves the race stroke automatically", "Is the fastest route", "Is required"),
    ("A 3-3-3 pattern (three right, three left, three full) is a:", "Bridge from a single-arm drill to full stroke", "Rule", "Race strategy", "Turn"),
], "The bridge is part of the drill: isolate, then put it back together at speed")
N("SW-11.2.B", "sw-count-descend", PR, "A swimmer holds {{sc}} cycles per 25 m and descends 25 m time from {{t1}} s to {{t2}} s. What stroke rate, in cycles per minute, does the faster swim need?",
  given={"sc": {"pick": [8, 9, 10]}, "t1": {"pick": [18, 20]}, "t2": {"pick": [15, 16]}}, value="sc/t2*60", tex="cyc/min", tol=0.005,
  verify="Rational(sc*60, t2)",
  explain="With the count fixed, all the extra speed has to come from rate. A count-holding descend is a rate set in disguise")
F("SW-11.2.B", "sw-count-set-design", PR, [
    ("A set that holds stroke count while descending time trains:", "Raising rate without losing length", "Lowering rate", "Turns", "Breathing"),
    ("A set that holds time while cutting stroke count trains:", "Distance per stroke", "Stroke rate", "Starts", "Kick only"),
    ("Evidence of improvement is:", "Same count at a faster time, or same time on fewer strokes", "More strokes at the same time", "Slower with fewer strokes", "A higher heart rate"),
], "Fix one of rate or length and progress the other, since their product is the speed")
N("SW-11.3.A", "sw-polarised-split", PR, "A week holds {{vol}} m of swimming on a polarised plan with {{pc}}% of the volume easy. How many metres are hard?",
  given={"vol": {"pick": [20000, 30000, 36000]}, "pc": {"pick": [75, 80, 85]}}, value="vol*(100 - pc)/100", tex="m", final=True,
  verify="Rational(vol*(100 - pc), 100)",
  explain="The hard share is small on purpose, so those sessions can be truly hard. A week of all-moderate swimming is the thing to avoid")
F("SW-11.3.A", "sw-week-adapt", PR, [
    ("In a week with heavy exams, the right adjustment is to:", "Keep the few hard sessions hard and trim the easy volume", "Make every session moderate", "Add volume", "Drop all easy swimming and go hard daily"),
    ("Stress from school and work:", "Adds to training stress", "Is separate from training", "Reduces training stress", "Only matters for seniors"),
    ("A hard session placed the day after another hard session usually:", "Cannot be done hard enough to count", "Works best", "Is required", "Doubles the adaptation"),
], "Total stress is one budget; protect the quality sessions and let the easy ones flex")

# ── unit 12: coaching others ──────────────────────────────────────────────────────────────────────────────────
F("SW-12.1.A", "sw-fly-progression", CH, [
    ("A butterfly teaching progression starts with:", "The body wave and dolphin kick", "Full stroke 100s", "The breath", "Turns"),
    ("After the body dolphin, the next step is:", "Kick with the arms forward, then single-arm with timing", "Full stroke for distance", "Racing starts", "Breathing every stroke"),
    ("Full-stroke butterfly is first introduced over:", "Short distances", "200s", "Timed 100s", "A full practice"),
], "Wave, kick, one arm with timing, then full stroke in short doses")
F("SW-12.1.A", "sw-progression-criterion", CH, [
    ("A swimmer should advance to the next step when:", "A visible criterion is met", "A set number of days has passed", "Teammates advance", "The season ends"),
    ("If the skill breaks down at the new step, the coach should:", "Go back one step", "Push on", "Add distance", "Skip ahead"),
    ("A teaching progression is ordered so that each step:", "Adds one new demand to what is already secure", "Is harder in every way", "Is unrelated to the last", "Takes the same time"),
], "Advance on what you can see, not on the calendar")
F("SW-12.1.B", "sw-cue-external", CH, [
    ("An external-focus cue is:", "Push the water to your feet", "Bend your elbow to 90 degrees", "Tighten your core", "Rotate your shoulder joint"),
    ("External cues usually transfer better because they:", "Point attention at the effect, not the body part", "Are longer", "Are more technical", "Name the muscle"),
    ("How many cues should a swimmer be given for one length?", "One", "Three", "Five", "As many as there are faults"),
], "One cue, about the water or the outcome rather than the joint")
F("SW-12.1.B", "sw-cue-rewrite", CH, [
    ("The external version of 'keep your head still' is:", "Leave a quiet line on the water with your head", "Lock your neck", "Relax your shoulders", "Stop moving your skull"),
    ("The external version of 'kick from the hips' is:", "Make the water boil just behind your feet", "Contract your glutes", "Straighten your knees", "Use your hip flexors"),
    ("Feedback is most useful when it comes:", "Soon after the attempt, about one thing", "At the end of the week", "As a full list", "Only when asked"),
], "Rewrite the instruction as something the swimmer does to the water")
N("SW-12.2.A", "sw-lanes-equal-time", CH, "Lanes swim for the same {{tm}} minutes. A lane with a threshold pace of {{p}} s per 100 swims continuous 100s. How many whole 100s does it complete?",
  given={"tm": {"pick": [10, 15, 20]}, "p": {"pick": [75, 90, 105]}}, value="floor(tm*60/p)", tex="100s", final=True,
  verify="floor(Rational(tm*60, p))",
  explain="Equal time, different distance keeps the group on one clock. Each lane's distance comes from its own pace")
F("SW-12.2.A", "sw-lanes-common-clock", CH, [
    ("'Same but less' for a slower lane means:", "The same interval with shorter repeats", "A longer interval", "A different set", "No rest"),
    ("Running every lane on the same send-off keeps:", "The group starting together", "Everyone at the same speed", "All lanes at the same distance", "The clock unused"),
    ("Each lane's pace should come from:", "That lane's own tested pace", "The fastest lane", "The slowest lane", "The coach's guess for the group"),
], "One clock for the pool, each lane's distance or pace set from its own swimmers")
F("SW-12.2.B", "sw-season-mixed-group", CH, [
    ("A group with sprinters, distance and IM swimmers shares:", "An aerobic base early in the season", "Identical sets all season", "No sets at all", "Only the taper"),
    ("After the base, sets are split by:", "Event group", "Age only", "Lane number", "Height"),
    ("The taper calendar is set by:", "The key meets", "The first day of the season", "The pool schedule only", "The fastest swimmer"),
], "Common base, then specific work by event group, all planned back from the key meets")
F("SW-12.2.B", "sw-taper-by-swimmer", CH, [
    ("Which swimmers generally need the longest taper?", "Older, larger senior swimmers", "Young novices", "Everyone equally", "Nobody"),
    ("Young or lightly trained swimmers may need:", "Little or no taper", "Three weeks", "The longest taper", "A second taper"),
    ("In one group aiming at one meet, tapers are usually:", "Different lengths by swimmer and event", "Identical", "Skipped", "Set by lane"),
], "Taper length follows training load and body size, so one group can hold several tapers")
