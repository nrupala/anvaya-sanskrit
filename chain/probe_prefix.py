import sys
sys.path.insert(0, ".")
import segment

K = "../vidyut-data/kosha"
keys = ["sakalakalApAraNgatas", "vahuSaktis", "paramadurmeDasas",
        "pravaramukuwamaRimarIcimaYjarIcarcitacaraRayugalas",
        "mahilAropyam", "anantaSaktis", "gatvAnyedyustam",
        "miTyAhus", "BItaparivAras", "asmatsvAmI",
        "DarmopArjitaBUriviBavas", "sarvamfgaparivftas"]
for key in keys:
    src = segment.validate(key, K)
    hits = []
    for i in range(3, len(key) - 1):
        pre = key[:i]
        if segment.validate(pre, K) == "kosha" and \
                segment._function_bearing(pre, K):
            hits.append(pre)
    print(key, "->", src, "fn-prefixes:", hits)
