import sys

with open(sys.argv[4], "wt") as outw:
    with open(sys.argv[1], "rt") as inr:
        header = inr.readline().strip()
        langs = header.split("\t")
        if langs[0] == sys.argv[2] and langs[1] == sys.argv[3]:
            inverse = True
        else:
            inverse = False
        for inline in inr:
            columns = inline.strip().split("\t")
            if inverse:
                outw.write(columns[1]+" @ "+columns[0]+"\n")
            else:
                outw.write(columns[0]+" @ "+columns[1]+"\n")
