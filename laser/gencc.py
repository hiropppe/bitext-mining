import click
import numpy as np

from pathlib import Path
from tqdm import tqdm


@click.command()
@click.argument("dataname")
@click.argument("lang")
def main(dataname, lang):
    l1 = lang
    l2 = "en"
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

    len(opus_l2), len(opus_l2_dedup)
    len(opus_l1), len(opus_l1_dedup)

    opus_l2 = opus_l2_dedup
    opus_l1 = opus_l1_dedup

    opus_size = len(opus_l2)
    train_size = opus_size//2
    test_size = opus_size - train_size

    np.random.seed(123)
    opus_inds = np.random.permutation(np.arange(opus_size))

    train_gold_size = int(train_size * 0.5)
    test_gold_size = int(test_size * 0.5)

    train_inds = opus_inds[:train_size]
    test_inds = opus_inds[train_size:]

    train_gold_inds = train_inds[:train_gold_size]
    train_mono_inds = train_inds[train_gold_size:]
    train_mono_size = len(train_mono_inds)//2
    train_mono_l2_inds = train_mono_inds[:train_mono_size]
    train_mono_l1_inds = train_mono_inds[train_mono_size:]

    test_gold_inds = test_inds[:test_gold_size]
    test_mono_inds = test_inds[test_gold_size:]
    test_mono_size = len(test_mono_inds)//2
    test_mono_l2_inds = test_mono_inds[:test_mono_size]
    test_mono_l1_inds = test_mono_inds[test_mono_size:]

    train_mono_l2 = []
    train_mono_l1 = []
    train_gold = []
    train_gold_ladder = []
    test_mono_l2 = []
    test_mono_l1 = []
    test_gold = []
    test_gold_ladder = []
    i = 0
    for en, ja in tqdm([(enja[0], enja[1]) for enja in zip(opus_l2, opus_l1)]):
        train_l2_size = len(train_mono_l2) + 1
        train_l1_size = len(train_mono_l1) + 1
        test_l2_size = len(test_mono_l2) + 1
        test_l1_size = len(test_mono_l1) + 1
        if i in train_gold_inds:
            train_mono_l2.append("{:s}-{:08d}\t{:s}".format(l2, train_l2_size, opus_l2[i]))
            train_mono_l1.append("{:s}-{:08d}\t{:s}".format(l1, train_l1_size, opus_l1[i]))
            train_gold.append("{:s}-{:08d}\t{:s}-{:08d}".format(l1,
                                                                train_l1_size, l2, train_l2_size))
            train_gold_ladder.append("{:d}\t{:d}".format(train_l2_size-1, train_l1_size-1))
        elif i in train_mono_l2_inds:
            train_mono_l2.append("{:s}-{:08d}\t{:s}".format(l2, train_l2_size, opus_l2[i]))
        elif i in train_mono_l1_inds:
            train_mono_l1.append("{:s}-{:08d}\t{:s}".format(l1, train_l1_size, opus_l1[i]))
        elif i in test_gold_inds:
            test_mono_l2.append("{:s}-{:08d}\t{:s}".format(l2, test_l2_size, opus_l2[i]))
            test_mono_l1.append("{:s}-{:08d}\t{:s}".format(l1, test_l1_size, opus_l1[i]))
            test_gold.append("{:s}-{:08d}\t{:s}-{:08d}".format(l1, test_l1_size, l2, test_l2_size))
            test_gold_ladder.append("{:d}\t{:d}".format(test_l2_size-1, test_l1_size-1))
        elif i in test_mono_l2_inds:
            test_mono_l2.append("{:s}-{:08d}\t{:s}".format(l2, test_l2_size, opus_l2[i]))
        elif i in test_mono_l1_inds:
            test_mono_l1.append("{:s}-{:08d}\t{:s}".format(l1, test_l1_size, opus_l1[i]))
        else:
            raise ValueError(i)
        i += 1

    lang_dir = Path(dataname.lower()) / lang
    if not lang_dir.exists():
        lang_dir.mkdir()

    with open("./{:s}/{:s}/{:s}.training.{:s}".format(dataname.lower(), lang, lang, l1), "w") as f:
        for e in train_mono_l1:
            print(e, file=f)
    with open("./{:s}/{:s}/{:s}.training.{:s}".format(dataname.lower(), lang, lang, l2), "w") as f:
        for e in train_mono_l2:
            print(e, file=f)
    with open("./{:s}/{:s}/{:s}.training.gold".format(dataname.lower(), lang, lang), "w") as f:
        for e in train_gold:
            print(e, file=f)
    with open("./{:s}/{:s}/{:s}.test.{:s}".format(dataname.lower(), lang, lang, l1), "w") as f:
        for e in test_mono_l1:
            print(e, file=f)
    with open("./{:s}/{:s}/{:s}.test.{:s}".format(dataname.lower(), lang, lang, l2), "w") as f:
        for e in test_mono_l2:
            print(e, file=f)
    with open("./{:s}/{:s}/{:s}.test.gold".format(dataname.lower(), lang, lang), "w") as f:
        for e in test_gold:
            print(e, file=f)

    # for comparison to hunalign (l2-l1)
    with open("./{:s}/{:s}/{:s}-{:s}.training.hunalign.ladder".format(dataname.lower(), lang, l2, l1), "w") as f:
        for e in train_gold_ladder:
            print(e, file=f)
    with open("./{:s}/{:s}/{:s}-{:s}.test.hunalign.ladder".format(dataname.lower(), lang, l2, l1), "w") as f:
        for e in test_gold_ladder:
            print(e, file=f)


if __name__ == "__main__":
    main()
