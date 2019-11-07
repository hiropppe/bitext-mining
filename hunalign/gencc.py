import click
import numpy as np

from pathlib import Path
from tqdm import tqdm


@click.command()
@click.argument("dataname")
@click.argument("l1")
@click.argument("l2")
def main(dataname, l1, l2):
    lang = l1 + "-" + l2
    opus_lang = "-".join(sorted([l1, l2]))

    opus_l1_path = "./{:s}/{:s}.{:s}.{:s}".format(dataname.lower(), dataname, opus_lang, l1)
    opus_l2_path = "./{:s}/{:s}.{:s}.{:s}".format(dataname.lower(), dataname, opus_lang, l2)

    opus_l2 = [l.strip() for l in open(opus_l2_path).readlines()]
    opus_l1 = [l.strip() for l in open(opus_l1_path).readlines()]

    opus_l2_dedup = []
    opus_l1_dedup = []
    prev_l2 = None
    prev_l1 = None

    opus_gen = zip(opus_l2, opus_l1)
    prev_l2, prev_l1 = next(opus_gen)
    for en, ja in opus_gen:
        if prev_l2 != en and prev_l1 != ja:
            opus_l2_dedup.append(en)
            opus_l1_dedup.append(ja)

        prev_l2 = en
        prev_l1 = ja

    opus_l2 = opus_l2_dedup
    opus_l1 = opus_l1_dedup

    opus_size = len(opus_l2)

    np.random.seed(123)
    opus_inds = np.random.permutation(np.arange(opus_size))

    gold_size = int(opus_size * 0.5)

    gold_inds = opus_inds[:gold_size]
    mono_inds = opus_inds[gold_size:]
    mono_size = len(mono_inds)//2
    mono_l2_inds = mono_inds[:mono_size]
    mono_l1_inds = mono_inds[mono_size:]

    mono_l2 = []
    mono_l1 = []
    gold_ladder = []

    i = 0
    for en, ja in tqdm([(enja[0], enja[1]) for enja in zip(opus_l2, opus_l1)]):
        l2_size = len(mono_l2)
        l1_size = len(mono_l1)
        if i in gold_inds:
            mono_l2.append(opus_l2[i])
            mono_l1.append(opus_l1[i])
            gold_ladder.append("{:d}\t{:d}".format(l2_size, l1_size))
        elif i in mono_l2_inds:
            mono_l2.append(opus_l2[i])
        elif i in mono_l1_inds:
            mono_l1.append(opus_l1[i])
        else:
            raise ValueError(i)
        i += 1

    lang_dir = Path(dataname.lower()) / lang
    if not lang_dir.exists():
        lang_dir.mkdir()

    with open("./{:s}/{:s}/{:s}.mono.{:s}".format(dataname.lower(), lang, lang, l1), "w") as f:
        for e in mono_l1:
            print(e, file=f)
    with open("./{:s}/{:s}/{:s}.mono.{:s}".format(dataname.lower(), lang, lang, l2), "w") as f:
        for e in mono_l2:
            print(e, file=f)
    with open("./{:s}/{:s}/{:s}.gold.ladder".format(dataname.lower(), lang, lang, l1), "w") as f:
        for e in gold_ladder:
            print(e, file=f)


if __name__ == "__main__":
    main()
