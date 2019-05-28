#!/usr/bin/env python3
from bs4 import BeautifulSoup

import json
import sys
import urllib.parse
import re
import fileinput
import spacy

ja = spacy.blank('ja')

# read in names

GAZ = {}
GAZ['PER'] = frozenset(open('names/per').read().split('\n'))
GAZ['LOC'] = frozenset(open('names/loc').read().split('\n'))

def get_entity_type(pagename):
    # there can't be collisions here because page names are unique
    # this does nothing for disambig pages
    for key, vals in GAZ.items():
        if pagename in vals:
            return key

def get_url_tail(link):
    return urllib.parse.unquote(link['href']).split('/')[-1]

def clean(name):
    return re.sub(" *\(.*\)", "", name)

def is_span_start(ii, spans):
    for span in spans:
        if span[0] == ii:
            return True
    return False

def is_in_span(ii, spans):
    for span in spans:
        if span[0] < ii < span[1]:
            return True
    return False

def print_iob(ents, sent):
    #import ipdb; ipdb.set_trace()
    tagseq = {}
    hay = ja(sent)
    for key, pagename, etype in ents:
        needle = ja(key)

        kl = len(needle)
        #TODO: more principled equality?
        segs = [(ii, ii+kl) for ii in range(len(hay)) if str(hay[ii:ii+kl]) == str(needle)]
        if not segs: continue # this is an error basically
        start, finish = segs[0] # shouldn't be more than one match usually
        tagseq[start] = 'B-{}'.format(etype)
        for ii in range(start+1, finish):
            tagseq[ii] = 'I-{}'.format(etype)

    print('# ' + sent) # for debugging
    #print(ents)
    for ii, word in enumerate(hay):
        tag = tagseq.get(ii, 'O')
        print(ii+1, word.orth_, word.lemma_, word.pos_, word.tag_, tag, sep='\t')
    print('') # conll seems to just use blank line separators

# read in articles
for line in fileinput.input():
    page = json.loads(line)
    for sent in page['text'].split('。'):
        sent = sent.replace('\n', '')
        if not '<a' in sent: continue
        doc = BeautifulSoup(sent, 'html.parser')
        links = doc.find_all('a')
        ents = []
        for link in links:
            #TODO: collect all entities in the sentence to mark them all up
            dest = get_url_tail(link)
            etype = get_entity_type(dest)
            if not etype: continue

            text = link.text
            if clean(dest) in text:
                ents.append( (clean(dest), dest, etype) )

        if ents:
            print_iob(ents, doc.text + '。')
