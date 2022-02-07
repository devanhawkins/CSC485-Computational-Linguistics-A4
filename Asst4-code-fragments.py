from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk import Tree
from nltk.corpus import brown

rule = ChunkRule(r'(<DT|AT>?<RB>?)?<JJ.*|CD.*>*(<JJ.*|CD.*><,>)*(<N.*>)+',
	'Chunk NPs')
parser = RegexpChunkParser([rule],
	chunk_node='NP',   # the name to assign to matched substrings (optional)
	top_node='S')      # the name to assign the top tree node (optional)

taggedText = brown.tagged_sents()

chunked = [parser.parse(t) for t in taggedText]

#######

chunked = []
for id in brown.fileids():
	if id not in ['cf07', 'cf08', 'cg54', 'ck05', 'ck07']:
		taggedText = brown.tagged\_sents(id)
		chunked.extend([parser.parse(t) for t in taggedText])
