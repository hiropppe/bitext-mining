# LASER: application to bitext mining
Test [bitext-mining with LASER](https://github.com/facebookresearch/LASER/tree/master/tasks/bucc)

## Set up a test environment
```
git clone https://github.com/hiropppe/bitext-mining.git
cd bitext-mining/laser
docker build -t laser .
docker run --runtime nvidia -td --name laser --hostname laser --net host laser /bin/bash
```

Enter the container and install the LASER model and external tools.  
```
docker exec -it laser /bin/bash
```
```
./install_models.sh
./install_external_tools.sh
```

## BUCC 2018
Download the BUCC shared task data [here](https://comparable.limsi.fr/bucc2017/cgi-bin/download-data-2018.cgi) and install it the directory "downloaded".   
```
git clone https://github.com/hiropppe/bitext-mining.git
cd bitext-mining
mkdir downloaded
cd downloaded
# wget https://...training-gold.tar.bz2
```

Running bitext-mining.
```
cd bitext-mining/laser
./minecc.sh bucc2018 fr
```

No test data is given, so only train data can be checked.
```
cat bucc2018.fr-en.train.log
#LASER: tools for BUCC bitext mining
# - reading sentences and IDs
# - reading candidates ./embed/bucc2018.fr-en.train.candidates.tsv
# - optimizing threshold on gold alignments ./bucc2018/fr-en/fr-en.training.gold
# - best threshold=1.088131: precision=91.52, recall=93.32, F1=92.41
```

## OPUS
Alignment testing with parallel corpora.  

ex: Tatoeba Corpus
```
mkdir tatoeba
cd tatoeba
wget https://object.pouta.csc.fi/OPUS-Tatoeba/v20190709/moses/en-ja.txt.zip
unzip en-ja.txt.zip
cd ..
# Generating comparable corpora
python gencc.py Tatoeba ja
./minecc.sh Tatoeba ja
```

Check the results.
```
# cat tatoeba.ja-en.train.log
LASER: tools for BUCC bitext mining
 - reading sentences and IDs
 - reading candidates ./embed/tatoeba.ja-en.train.candidates.tsv
 - optimizing threshold on gold alignments ./tatoeba/ja-en/ja-en.training.gold
 - best threshold=1.021966: precision=85.16, recall=74.17, F1=79.29
# cat tatoeba.ja-en.test.log
LASER: tools for BUCC bitext mining
 - reading sentences and IDs
 - reading candidates ./embed/tatoeba.ja-en.test.candidates.tsv
 - extracting bitexts for threshold 1.021966 into ./embed/tatoeba.ja-en.test.extracted.tsv
 - test threshold=1.021966: precision=85.07, recall=74.53, F1=79.45
