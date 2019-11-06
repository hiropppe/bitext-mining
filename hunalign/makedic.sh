bitextor=/root/bitextor

cat Tatoeba.en-ja.en | sed "s/&apos;/'/g" | sed 's/&quot;/\"/g' | sed 's/&amp;/\&/g' | $bitextor/preprocess/moses/tokenizer/tokenizer.perl -q -b -a -l en > corpus.tok.en
cat Tatoeba.en-ja.ja | sed "s/&apos;/'/g" | sed 's/&quot;/\"/g' | sed 's/&amp;/\&/g' | mecab -Owakati > corpus.tok.ja

cat corpus.tok.en | $bitextor/preprocess/moses/tokenizer/lowercase.perl > corpus.tok.low.en
cat corpus.tok.ja | $bitextor/preprocess/moses/tokenizer/lowercase.perl > corpus.tok.low.ja

perl $bitextor/utils/clean-corpus-n.perl corpus.tok.low en ja corpus.clean 1 80 corpus.lines-retained

mkdir -p mgiza
$bitextor/mgiza/mgizapp/bin/plain2snt corpus.clean.en corpus.clean.ja 2> /dev/null > /dev/null
mv corpus.clean.en_corpus.clean.ja.snt mgiza/corpus.ja-en-int-train.snt
mv corpus.clean.ja_corpus.clean.en.snt mgiza/corpus.en-ja-int-train.snt
cp corpus.clean.en.vcb mgiza/corpus.en.vcb
cp corpus.clean.ja.vcb mgiza/corpus.ja.vcb

$bitextor/clustercat/bin/mkcls -c50 -n2 -p./corpus.clean.en -Vmgiza/corpus.en.vcb.classes opt 2> /dev/null > /dev/null
$bitextor/clustercat/bin/mkcls -c50 -n2 -p./corpus.clean.ja -Vmgiza/corpus.ja.vcb.classes opt 2> /dev/null > /dev/null

$bitextor/mgiza/mgizapp/bin/snt2cooc mgiza/corpus.ja-en.cooc mgiza/corpus.en.vcb mgiza/corpus.ja.vcb mgiza/corpus.ja-en-int-train.snt 2> /dev/null
$bitextor/mgiza/mgizapp/bin/snt2cooc mgiza/corpus.en-ja.cooc mgiza/corpus.ja.vcb mgiza/corpus.en.vcb mgiza/corpus.en-ja-int-train.snt 2> /dev/null

$bitextor/mgiza/mgizapp/bin/mgiza -ncpus 8 -CoocurrenceFile mgiza/corpus.ja-en.cooc -c mgiza/corpus.ja-en-int-train.snt -m1 5 -m2 0 -m3 3 -m4 3 -mh 5 -m5 0 -model1dumpfrequency 1 -o mgiza/corpus.ja-en -s mgiza/corpus.en.vcb -t mgiza/corpus.ja.vcb -emprobforempty 0.0 -probsmooth 1e-7 2> /dev/null > /dev/null
$bitextor/mgiza/mgizapp/bin/mgiza -ncpus 8 -CoocurrenceFile mgiza/corpus.en-ja.cooc -c mgiza/corpus.en-ja-int-train.snt -m1 5 -m2 0 -m3 3 -m4 3 -mh 5 -m5 0 -model1dumpfrequency 1 -o mgiza/corpus.en-ja -s mgiza/corpus.ja.vcb -t mgiza/corpus.en.vcb -emprobforempty 0.0 -probsmooth 1e-7 2> /dev/null > /dev/null

cat ./mgiza/corpus.en.vcb | egrep ' [^ ][^ ]+$' > mgiza/corpus.en.filtered.vcb
cat ./mgiza/corpus.ja.vcb | egrep ' [^ ][^ ]+$' > mgiza/corpus.ja.filtered.vcb

python symdic.py ./mgiza/corpus.en.filtered.vcb ./mgiza/corpus.ja.filtered.vcb ./mgiza/corpus.en-ja.t3.final ./mgiza/corpus.ja-en.t3.final en ja en-ja.dic

python hundic.py en-ja.dic en ja hunalign.dic
