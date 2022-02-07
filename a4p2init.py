from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk import Tree
from nltk.corpus import brown


adj_or_count='(<JJ.*|CD.*>(<,>)?)*'
basic_np='(<DT|AT>?<RB>?)?'+adj_or_count+'(<N.*>)+'
pp='(<IN.*>'+basic_np+')*'
pp_pre='(<IN>(<[^NVW].*>)*)?'
#rule = ChunkRule(r'(<DT|AT>?<RB>?)?<JJ.*|CD.*>*(<JJ.*|CD.*><,>)*(<N.*>)+',	'Chunk NPs')
#rule = ChunkRule(pp_pre+basic_np+pp,'Chunk NPs') #doesnt work so well
rule = ChunkRule(basic_np+pp,'Chunk NPs')
parser = RegexpChunkParser([rule],
	chunk_node='NP',   # the name to assign to matched substrings (optional)
	top_node='S')      # the name to assign the top tree node (optional)


#n=1
#taggedText=[]
#bs=brown.tagged_sents()
#for i in range(len(bs)/n):
#	taggedText=taggedText+[bs[i*n]]

chunked=[]
chunked = [parser.parse(t) for t in taggedText]




