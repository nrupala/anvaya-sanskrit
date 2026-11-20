import sys
sys.path.insert(0, ".")
import analyze

K = "../vidyut-data/kosha"
for key in ["parityajya", "pfzWatas", "miTyA", "rakzApuruzA",
            "rakzApuruzAs", "saMjIvakam", "bahvapAyam"]:
    cs = analyze.candidates(key, "kosha", K)
    print(f"== {key}: {len(cs)} cands")
    for c in cs[:14]:
        print("   ", c.get("kind"), c.get("stem"), c.get("vibhakti"),
              c.get("vacana"), c.get("linga"), "krt=", c.get("krt"),
              "avy=", c.get("avyaya"))
