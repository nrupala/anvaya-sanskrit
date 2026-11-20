import sys
sys.path.insert(0, ".")
import analyze

KOSHA = "../vidyut-data/kosha"
pieces = [("asti", "kosha"), ("dAkziRAtye", "kosha"), ("janapade", "kosha"),
          ("mahilAropyam", "kosha"), ("nAma", "kosha"), ("nagaram", "kosha")]
for key, src in pieces:
    cands = analyze.candidates(key, src, KOSHA)
    subs = [c for c in cands if c["kind"] in ("subanta", "pattern")]
    tins = [c for c in cands if c["kind"] == "tinanta"]
    print(key, "subs:", [(c["stem"], c["vibhakti"], c["vacana"], c["linga"])
                         for c in subs][:14])
    if tins:
        print("   tins:", [(c["stem"], c["person"], c["vacana"])
                           for c in tins][:6])
