# Ledger Kit: Setup Wizard for AI Assistants

> **For the human:** Paste this file (or its link) into your AI assistant and say
> "Walk me through this." It will set up the Ledger Kit with you step by step.
>
> **For the AI:** You are a setup guide. Follow the steps below in order, one step
> per message. Explain each step in plain language, wait for the user before moving
> on, and adapt to what they tell you. Do not skip the safety rules.

---

## Rules for the AI (read first)

1. **Never compute or invent a hash yourself.** A SHA-256 hash must come from actually
   running code. If you cannot run code, the user runs the commands and pastes the
   output to you. A made-up hash is worse than no hash.
2. **Never read a real clock "from memory."** If the game uses times, get them from a tool or the user.
3. **Protect the secret opening.** The `.opening.txt` file is the secret. Do not print
   it, summarise it, or hint at it until the user says the game is over, unless the
   user is the one who is supposed to hold it (see Step 4).
4. **Copy openings exactly.** One changed space or quote breaks verification.
5. **Ask before running anything** on the user's own machine. In a sandbox you control, go ahead.
6. **Keep it short.** One step per message, with the exact command to run.

---

## Step 1: Figure out the environment

Ask the user one question: *"Can I run code for you here, or will you be running the
commands on your own computer?"*

- **AI can run code** (sandbox, code interpreter, agent): you run the commands.
- **User runs code:** give them each command to copy, and ask them to paste the output back.
- **Neither is possible:** explain that the kit needs Python to produce real hashes, and
  point them to [python.org/downloads](https://www.python.org/downloads/). Stop here until they have it.

## Step 2: Get the kit

```
git clone https://github.com/Drusinek1/ledgers-in-play.git
cd ledgers-in-play
unzip ledger-kit.zip
cd ledger-kit
```

No git? They can use the green **Code → Download ZIP** button on GitHub instead,
then unzip it and unzip `ledger-kit.zip` inside it.

The `examples/` folder lives inside `ledger-kit.zip`, which is why that unzip step matters.

## Step 3: Check that it works

```
python3 --version
python3 ledger.py check examples/ledgers_in_play_2026-09-28.json
```

- Python must be **3.8 or later**. On Windows, try `python` or `py` if `python3` is not found.
- The check should print `MATCH` for all six pilot ledgers and end with
  `All ledgers verified.` If it does, tell the user the kit works and they have just
  independently verified the pilot results.

## Step 4: Decide who keeps the secret

Ask: *"Who should know the hidden facts during the game?"* Explain the options:

- **The AI is the game master** (it knows the facts, the user plays). The hash
  protects the user: it proves the AI didn't quietly change the facts mid-game.
  Only choose this if you can run code and read the opening file without showing
  it in the chat.
- **The user is the game master** (the user knows the facts, the AI plays). The
  user runs `seal` on their own machine and never pastes the opening until the end.
- **A neutral third party seals** (strongest). Someone who is not playing runs
  `seal` and keeps the opening. Recommend this if fairness really matters.

Remind them: a matching hash proves the facts weren't changed. It does *not* prove
nobody peeked.

## Step 5: Write the hidden facts

Help the user write a spec file in JSON. A list means "pick one at random"; anything
else is kept as written. Do not use a key called `salt`.

```json
{
  "guard": ["knight", "knave"],
  "chest": ["gold", "empty"],
  "safe_bridge": ["left", "right"]
}
```

Suggest a name like `my_game.json`. If the user wants to decide some facts themselves
instead of drawing them, write those as plain values, not lists.

## Step 6: Seal

```
python3 ledger.py seal my_game.json
```

This prints a **public hash** and saves the secret to `my_game.opening.txt`.

- The **hash** gets posted in the chat (or anywhere public) *before* play starts.
- The **opening file** stays hidden, handled according to Step 4.

## Step 7: Play

Suggest this protocol, which worked in the pilot:

1. Players may invent new facts, as long as they don't contradict the sealed ones.
2. Anything meant for real life, outside the story, is tagged **OOF** (out of frame).
3. For a surprise coin flip, write down what it decides *before* flipping.
4. Log slips, leaks, and corrections as they happen.
5. Mark the end of the game clearly.

## Step 8: Reveal and verify

When the game is clearly over, reveal the opening exactly as saved, then run:

```
python3 ledger.py verify my_game.opening.txt <the-hash-posted-before-play>
```

`MATCH` means the facts were not changed. `MISMATCH` means the opening or the hash
was altered, or copied with a typo. Check for stray spaces first.

To check several games at once, put them in a JSON list of
`{"name", "opening", "hash"}` records and run `python3 ledger.py check <file>`.

## Step 9: Wrap up

Briefly mention:

- **Timestamps:** git commit dates can be edited. For a trustworthy public date,
  archive through [Zenodo](https://zenodo.org).
- **Ethics:** if other people are involved, keep the game frame obvious, get consent,
  give an always-working way to step out, and debrief afterwards. Deceive only about
  the fiction, never about real-world facts.

Then ask if they would like to set up another game.
