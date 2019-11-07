cat ./tatoeba/en-ja/en-ja.mono.en | cut -f2 | /root/bitextor/preprocess/moses/tokenizer/tokenizer.perl -q -b -a -l en | /root/bitextor/preprocess/moses/tokenizer/lowercase.perl > ./tatoeba/en-ja/en-ja.mono.tok.en
cat ./tatoeba/en-ja/en-ja.mono.ja | cut -f2 | mecab -Owakati | /root/bitextor/preprocess/moses/tokenizer/lowercase.perl > ./tatoeba/en-ja/en-ja.mono.tok.ja

/root/hunalign/src/hunalign/hunalign hunalign.dic ./tatoeba/en-ja/en-ja.mono.tok.en ./tatoeba/en-ja/en-ja.mono.tok.ja -hand=./tatoeba/en-ja/en-ja.gold.ladder 
