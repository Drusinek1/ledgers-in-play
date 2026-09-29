# Ledger Kit

Seal hidden facts before a game, then prove afterwards that nobody changed them.

This small tool comes from *Ledgers in Play*, an informal pilot of knights-and-knaves role-play games with a language model (Daniel Rusinek, 2026). It works for any game, experiment, or prediction where you want to commit to something secret now and reveal it later.

## How it works

1. **Seal.** Write down the hidden facts. The tool adds a random salt and publishes a SHA-256 hash, a fingerprint of the facts. Share the hash before play and keep the facts secret.
2. **Play.** Nobody can work out the facts from the hash, and the salt stops anyone from simply guessing and hashing each possibility.
3. **Reveal and verify.** At the end, reveal the facts exactly as saved. Anyone can recompute the hash. If it matches, the facts were not changed.

## Requirements

Python 3.8 or later. No installation or extra packages needed.

## Usage

**Seal a ledger.** Describe the hidden facts in a JSON file. A list means "pick one at random"; anything else is kept as written.

```json
{
  "guard": ["knight", "knave"],
  "chest": ["gold", "empty"],
  "safe_bridge": ["left", "right"]
}
```

```
python3 ledger.py seal examples/castle_spec.json
```

This prints the **public hash** to share, and saves the **secret opening** to `castle_spec.opening.txt`. Keep that file hidden until the game ends.

**Verify one ledger.**

```
python3 ledger.py verify castle_spec.opening.txt <published-hash>
```

**Verify many at once** from a JSON list of `{"name", "opening", "hash"}` records:

```
python3 ledger.py check examples/ledgers_in_play_2026-09-28.json
```

The example file contains the six ledgers from the *Ledgers in Play* pilot, so you can check those results yourself.

## Running a game with an AI

A protocol that worked in the pilot:

1. Seal the hidden facts before play and post the hash in the chat.
2. Allow players to invent new facts, as long as they don't contradict the sealed ones.
3. Tag anything meant for real, outside the story, as **OOF** (out of frame).
4. If the AI reports times, have it read a real clock every turn. Never let it estimate.
5. For a surprise coin flip, write down what it will decide *before* flipping.
6. Mark the end of each game clearly, reveal the opening, and verify the hash.
7. Log slips, leaks, and corrections as they happen.

## What a matching hash proves, and what it doesn't

- **It proves** the revealed facts are the ones sealed at the start.
- **It does not prove** the facts were drawn fairly, or that no player saw them early. Whoever holds the opening can peek. For a stronger setup, let someone who is *not* playing or narrating run `seal` and keep the opening.
- **Copy openings exactly.** Changing even one space or quote changes the hash.

## Timestamps

Git commit dates can be edited, so they are weak evidence of *when* something was sealed. For a trustworthy public date, archive releases through [Zenodo](https://zenodo.org), which issues a permanent DOI.

## Ethics

If you use this for experiments with people, keep the game frame obvious, get informed consent, provide an always-working way to step out of the game, and debrief afterwards. Never deceive participants about real-world facts, only about the fiction.

## License

MIT. Free to use, change, and share, with attribution.
