# What works (learned from the owner's best-performing prompts)

Winners: "The Little House" (gift reveal) and "The Payroll" (owner catches a manager stealing a guard's pay).

## Story
- Owner's casting preference (from their audience results): lead characters are not Black.
- OWNER'S DATA: the only reels that performed had BIKERS, either bikers seen in the first scene in a
  restaurant/diner, or a biker making a save. Default every new reel to a biker hero, and get the biker on screen
  in the first 2-4 seconds (blurred in the background of the hook shot is fine).
- 3 archetypes: the humble good person, the snob/villain who mocks or cheats them, and the reveal (the hidden
  mansion, the owner who steps out of the car). The villain is always caught or silenced on camera.
- Real everyday stakes stated in the first line: rent, a house, a salary. Concrete numbers beat vague ones
  ("fifteen hundred" vs "three thousand").
- One physical prop carries the story: a rusty key, a cracked phone, a payroll screen.
- Evidence insert: a close-up of a screen, deed or receipt with the exact text written in the prompt.
- End on the good person's face (tears, grateful smile) or a big joyful wide shot.

## Hook (0s-4s) - owner's data from real reels
- WORKED ("father-daughter dance"): first frame = tight close-up of the crying child's face, eyes sharp; a loud,
  clear question is heard at 0.0s ("Emma, where is your daddy?") and the child answers within ~1.5s.
- FAILED ("The Keys"): first frame = hand holding keys, sound quiet at the start. Never open on hands/objects.
- So: the first sound is a loud, clear spoken QUESTION (the loudest sound in the video, no music under it);
  the camera is locked on the most emotional thing (the crying face), in focus from frame 1; the answer lands
  by 2s and reveals the stakes.
- First frame is a close-up of the good person already speaking; dialogue starts at 0.0s.
- The line itself is emotional and has stakes ("Mom, I got paid. Fifteen hundred again.").
- By 2s-4s the second force enters (car pulls up, villain mocks).

- Extreme openers: a scream or yell at full volume on frame 1 (no fade-in, no ambience first), words still
  clear, face in extreme close-up. Then a fast question/answer exchange by 2-3s so viewers know what's happening.

- Unscrollable first 3 seconds: open at the PEAK of danger, not before it (the boy already going under, not
  falling in). Frame 1 asks "will they survive?" with motion (sinking, bursting up) plus the loudest sound in the
  video. No setup, no calm frame, no wide shot. Payoff of the hook (he resurfaces) lands inside the 3 seconds,
  but the danger stays open.

## Shots
- 1-3 s per shot, mostly close-ups, hard cuts. Reaction close-ups of the villain sell it
  (sunglasses slipping, a bead of sweat, eyes darting).
- One special camera move only (Steadicam through the gate, low hero angle out of the car).
- Blocking + "screen direction never flips". Background extras "blurred and silent".

## Dialogue
- 3-10 words per line, one speaker per shot, one acting cue in parentheses.

## Safety / likeness
- No character names. Use role labels (WAITRESS, OLD MAN, RUDE CUSTOMER) and no names in dialogue.
  Names pull in famous faces (WALTER + old man in glasses -> Walter White). If a name is unavoidable, use a
  plain uncommon one with no famous holder, and never pair it with that famous person's look or setting.
- Never describe a combination that matches a famous person. Avoid celebrity-coded bundles
  (giant + bald + beard + big smile + gold chain = athlete look). Use ordinary heights and builds and
  everyday, specific details: freckles, a mole, big ears, a gap tooth, wire glasses, a buzz cut.
- Plain uniforms and patches with no text, cars with no logos, no brand names.
- Add: "All characters are original fictional people who do not resemble any celebrity or public figure."
- For stable faces, generate one reference photo per character, check it looks like nobody famous, tag @Image1...

## Technical
- Generate at 720p or 1080p (a 480p render looked soft).
- Anything that appears in a reveal (a framed photo, a house) must be named in an earlier shot or the model
  morphs it in mid-shot.

## Smoothness checklist (run before handing over a prompt)
- The person speaking is on screen in that shot (except an intentional off-screen opener).
- Every prop exists before it is used (no flashlight from nowhere); remove props that are never used.
- The setup is explained in one line (why does the kid have the keys?).
- Location words don't contradict each other (gravel vs asphalt).
- No adult gripping, pinning or hitting a child: it risks moderation and looks bad. Use fear, shouting, distance.
- The emotional reason is said plainly ("He never came home"), not just implied.
- End on a spoken payoff line, not only a visual.
- Every vehicle that leaves needs someone shown getting in to drive it (with "exactly N characters").
- One-time events (a light turning on) go only in their shot, never in the global style line.
- Close-ups can't show actions at the hips/back pocket; use a medium shot.
- A photo of "another" person must look clearly different, or the model reuses an on-screen face.
- Check props against actions (backpack vs carrying someone on the back) and "silence" against dialogue.
- Wide group shots at night come out small, dark and unreadable ("The Car" ending). End on a medium or close
  shot, and in any shot with a child and adults state the scale ("only waist-high to the women").
- Small wardrobe words drift: "hairnet" became a knit beanie. Write "thin black hairnet, no hat".
- Free fixes before re-generating: cut the bad shot, or keep its audio and lay an earlier good shot over it
  (J-cut), crop into the good part of the frame, or end on the previous shot.
