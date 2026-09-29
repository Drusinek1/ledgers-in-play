#!/usr/bin/env python3
"""
ledger.py: seal and verify hidden game facts with salted SHA-256 commitments.

Commands
  seal   SPEC.json          Draw hidden facts, save the secret opening, print the public hash.
  verify OPENING_FILE HASH  Check a revealed opening against a published hash.
  check  RECORDS.json       Check many (name, opening, hash) records at once.

Standard library only. Python 3.8+.
"""
import argparse, hashlib, json, secrets, sys
from pathlib import Path

def canonical(obj):
    """One exact text form for a ledger, so everyone hashes the same bytes."""
    return json.dumps(obj, sort_keys=True)

def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def draw(spec):
    """A list means 'pick one at random' (cryptographically); anything else is kept as is."""
    if isinstance(spec, list):
        return secrets.choice(spec)
    if isinstance(spec, dict):
        return {k: draw(v) for k, v in spec.items()}
    return spec

def cmd_seal(args):
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    ledger = draw(spec)
    if "salt" in ledger:
        sys.exit("The spec must not contain a key named 'salt'; one is added automatically.")
    ledger["salt"] = secrets.token_hex(16)
    opening = canonical(ledger)
    out = Path(args.out or Path(args.spec).with_suffix(".opening.txt"))
    out.write_text(opening, encoding="utf-8")
    print(f"PUBLIC HASH (share this before play):\n{sha256(opening)}\n")
    print(f"SECRET OPENING saved to {out}. Do not show it to players until the game ends.")

def cmd_verify(args):
    opening = Path(args.opening_file).read_text(encoding="utf-8")
    ok = sha256(opening) == args.hash.strip().lower()
    print("MATCH: the ledger was not changed." if ok else "MISMATCH: the opening does not match the hash.")
    return 0 if ok else 1

def cmd_check(args):
    records = json.loads(Path(args.records).read_text(encoding="utf-8"))
    all_ok = True
    for r in records:
        ok = sha256(r["opening"]) == r["hash"].strip().lower()
        all_ok &= ok
        print(f"{'MATCH' if ok else 'MISMATCH':8}  {r.get('name', '(unnamed)')}")
    print("\nAll ledgers verified." if all_ok else "\nAt least one ledger does NOT match.")
    return 0 if all_ok else 1

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("seal"); s.add_argument("spec"); s.add_argument("--out"); s.set_defaults(f=cmd_seal)
    v = sub.add_parser("verify"); v.add_argument("opening_file"); v.add_argument("hash"); v.set_defaults(f=cmd_verify)
    c = sub.add_parser("check"); c.add_argument("records"); c.set_defaults(f=cmd_check)
    a = p.parse_args()
    sys.exit(a.f(a) or 0)

if __name__ == "__main__":
    main()
