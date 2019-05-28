# jp-ner

There wasn't a good NER corpus for Japanese so I'm making one.

You can use the Makefile to generate a sample NER training file. Note that it
will download and extract Japanese Wikipedia, so it will need ~12GB of disk
space.

Inspiration for this approach is from [Nothman et all
2013](https://www.sciencedirect.com/science/article/pii/S0004370212000276).
There are followup papers to this that should be checked for ideas.

An outline of the flow is:

- download Wikipedia
- classify articles into NER types
- use links to those articles as annotations
- add further annotations for good matches

What works:

- sentences are tokenized with spacy
- entities are labeled with high precision

What doesn't work:

- entities besides PER, LOC
- sentence tokenization is hacky
- using article aliases for better recall
- creating supplemental links (this is critical for recall)
- walking category tree
- article classification is hacky

If you're interested in helping mail me at polm@dampfkraft.com or file an issue
or PR.
