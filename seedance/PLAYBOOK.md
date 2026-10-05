# What works (learned from the owner's best-performing prompts)

Winners: "The Little House" (gift reveal) and "The Payroll" (owner catches a manager stealing a guard's pay).

## Story
- 3 archetypes: the humble good person, the snob/villain who mocks or cheats them, and the reveal (the hidden
  mansion, the owner who steps out of the car). The villain is always caught or silenced on camera.
- Real everyday stakes stated in the first line: rent, a house, a salary. Concrete numbers beat vague ones
  ("fifteen hundred" vs "three thousand").
- One physical prop carries the story: a rusty key, a cracked phone, a payroll screen.
- Evidence insert: a close-up of a screen, deed or receipt with the exact text written in the prompt.
- End on the good person's face (tears, grateful smile) or a big joyful wide shot.

## Hook (0s-4s)
- First frame is a close-up of the good person already speaking; dialogue starts at 0.0s.
- The line itself is emotional and has stakes ("Mom, I got paid. Fifteen hundred again.").
- By 2s-4s the second force enters (car pulls up, villain mocks).

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
