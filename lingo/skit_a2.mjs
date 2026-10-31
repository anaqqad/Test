// "Living in the USA with A2 English": comedy skit, narrator voice-over + short dialogues.
// who: N = narrator, S = Sami (our A2 hero), A/B = the other person in the scene.
// fx: emoji that pops above Sami ("?", "!", "sweat"), bald: Sami's hair after the barber.

export const SKIT = {
  key: "a2usa",
  title: "Living in the USA with A2 English",
  voices: {
    N: { model: "en_GB-alan-medium", speed: 1.0 },
    S: { model: "en_US-joe-medium", speed: 1.12 },
    A: { model: "en_US-ryan-high", speed: 0.82 },   // fast American guy
    B: { model: "en_US-amy-medium", speed: 0.85 },  // fast American woman
    C: { model: "en_US-lessac-high", speed: 0.9 },
  },
  sami: { skin: "tan", hair: "short", hairColor: "black", outfit: { type: "tunic", color: "#2f6fb0", trim: "#f2c94c" }, expression: "smile" },
  scenes: [
    {
      setting: "airport", label: "Day 1: the airport",
      other: { who: "A", char: { skin: "light", hair: "short", hairColor: "brown", mustache: true, outfit: { type: "shirt", color: "#1f3a5f", tie: "#1d1d1d", vest: "#1f3a5f" }, hat: { type: "flatcap", color: "#1f3a5f" }, expression: "neutral" } },
      lines: [
        ["N", "This is Sami. Sami has just landed in the United States of America. His English level: A two. Let us observe him in his new habitat."],
        ["A", "Good afternoon sir. What's the purpose of your visit, and how long do you intend to stay?"],
        ["S", "Yes.", "?"],
        ["A", "The purpose. Of your visit."],
        ["S", "Yes. Thank you. Very good."],
        ["N", "Sami learned three phrases at school. He will now use them for every situation in his life."],
      ],
    },
    {
      setting: "coffee", label: "Ordering coffee",
      other: { who: "B", char: { fem: true, skin: "pale", hair: "ponytail", hairColor: "auburn", outfit: { type: "shirt", color: "#2e6b4f", vest: "#2e6b4f" }, hat: { type: "beanie", color: "#2e6b4f", color2: "#f4f1e8" }, expression: "grin" } },
      lines: [
        ["B", "Hi! What can I get started for you today?"],
        ["S", "One coffee, please."],
        ["B", "Sure! Hot or iced? Small, medium, large, or venti? Oat, almond or whole milk? Any syrups? Can I get a name for the order?"],
        ["S", "...Yes.", "sweat"],
        ["N", "Sami has just ordered a large iced oat milk vanilla caramel something. He does not know what it is. He will now order it every single day."],
        ["B", "Large iced oat vanilla for... Salami?"],
        ["N", "His name is now Salami."],
      ],
    },
    {
      setting: "barber", label: "The barber shop",
      other: { who: "A", char: { skin: "brown", hair: "bald", hairColor: "black", beard: true, outfit: { type: "shirt", color: "#f4f1e8", vest: "#1d1d1d" }, expression: "grin" } },
      lines: [
        ["A", "Alright my man, what are we doing today? Low fade, mid fade, taper? Keep a little length on top?"],
        ["S", "Short. Little. Not too much. Thank you."],
        ["N", "Sami asked for a little. The barber heard: take it all."],
        ["A", "Boom! Lookin' fresh, bro!", null, { bald: true }],
        ["S", "...Yes. Very good.", "sweat", { bald: true }],
      ],
    },
    {
      setting: "store", label: "Self-checkout",
      other: { who: "C", machine: true },
      lines: [
        ["C", "Unexpected item in the bagging area."],
        ["S", "Sorry."],
        ["C", "Unexpected item in the bagging area."],
        ["S", "Sorry! Sorry!", "sweat"],
        ["N", "Sami apologized to the machine eleven times. The machine did not accept his apology."],
      ],
    },
    {
      setting: "street", label: "Small talk",
      other: { who: "A", char: { skin: "pale", hair: "short", hairColor: "blonde", outfit: { type: "tunic", color: "#c0392b", trim: "#f4f1e8" }, hat: { type: "beanie", color: "#1d1d1d", color2: "#1d1d1d" }, expression: "grin" } },
      lines: [
        ["A", "Yo, what's up man?"],
        ["N", "Sami knows that this is a question. He does not know the answer."],
        ["S", "...The sky?", "?"],
        ["A", "Haha! Good one bro!"],
        ["N", "Sami now believes he is a comedian."],
      ],
    },
    {
      setting: "apartment", label: "Calling the bank",
      other: { who: "B", phone: true },
      lines: [
        ["B", "Thank you for calling. This call may be recorded for quality assurance. Please say or enter your sixteen digit account number, followed by the pound sign."],
        ["S", "Hello? Human? Human please!", "sweat"],
        ["B", "Sorry, I didn't get that."],
        ["N", "Sami has now been on hold for forty seven minutes. He knows the hold music better than his national anthem."],
      ],
    },
    {
      setting: "doctor", label: "At the doctor",
      other: { who: "C", char: { fem: true, skin: "olive", hair: "bun", hairColor: "brown", outfit: { type: "coat", color: "#f4f6f8", inner: "#7fb2e5" }, glasses: true, expression: "smile" } },
      lines: [
        ["C", "So, on a scale of one to ten, how would you describe your pain? Is it sharp, dull, throbbing or burning?"],
        ["S", "Pain is... medium. Here. Bad.", "sweat"],
        ["C", "Okay, any allergies to medication?"],
        ["S", "Yes. Thank you. Very good."],
        ["N", "Sami has been prescribed something. He will take it twice a day. With confidence."],
      ],
    },
    {
      setting: "party", label: "The house party",
      other: { who: "A", char: { skin: "dark", hair: "curly", hairColor: "black", outfit: { type: "tunic", color: "#8e44ad", trim: "#f2c94c" }, glasses: true, expression: "grin" } },
      lines: [
        ["A", "Dude, this party is lit! We gotta hang out more, no cap."],
        ["S", "Lit? ...Fire? Where is fire? And I don't have cap.", "!"],
        ["N", "Sami called the fire department. Everyone left the party. It was, in fact, no longer lit."],
      ],
    },
    {
      setting: "street", label: "One year later",
      other: null,
      lines: [
        ["N", "One year later. Sami's English level: still A two. But now he says gonna, y'all, and no cap. He is officially fluent in vibes."],
        ["S", "Y'all gonna like and subscribe? No cap. Thank you. Very good."],
      ],
    },
  ],
};
