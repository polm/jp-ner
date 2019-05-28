all: data.ner

jawiki.xml: 
	wget -O jawiki.xml.bz2 https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2
	bzip2 -d jawiki.xml.bz2
	mv jawiki*xml jawiki.xml

cats/%.cat: cats/%.pat jawiki.xml
	./get_cats.sh $@ $<

WikiExtractor.py: 
	wget https://raw.githubusercontent.com/attardi/wikiextractor/master/WikiExtractor.py
	chmod +x WikiExtractor.py

corpus/%: cats/%.cat WikiExtractor.py
	./WikiExtractor.py -q -o corpus/$* --json --filter_category cats/$*.cat jawiki.xml

names/%: corpus/%
	cat corpus/$*/*/* | jq -r .title > $@

linked-corpus: jawiki.xml WikiExtractor.py
	./WikiExtractor.py -q -l --json -o $@ jawiki.xml

data.ner: linked-corpus names/*
	./linkreader.py linked-corpus/*/* > $@
