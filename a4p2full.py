from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk import Tree
from nltk.corpus import brown
import re
import nltk

#########################################################
#Used to initialize the chunker and chunk the sentences #
#########################################################
def initialize():
	adj_or_count='(<JJ.*|CD.*>(<,>)?)*'
	basic_np='(<DT|AT>?<RB>?)?'+adj_or_count+'(<N.*>)+'
	pp='(<IN.*>'+basic_np+')*'
	pp_pre='(<IN>(<[^NVW].*>)*)?'
	#rule = ChunkRule(r'(<DT|AT>?<RB>?)?<JJ.*|CD.*>*(<JJ.*|CD.*><,>)*(<N.*>)+',	'Chunk NPs')
	#rule = ChunkRule(pp_pre+basic_np+pp,'Chunk NPs') #doesnt work so well
	
	#Using the following rule to avoid having the chunker chunk the following
	#
	#  S=NP1 PP NP2 such as NP3 - > gets chunked originall as 
	#              - > (NP1) PP (NP2) such as (NP3)
	#	And so (NP2) and (NP3) are put into a relation, where in fact it could
	#  have been (NP1) and (NP3), this groups the sentence as following
	#
	#  S=(NP1 PP NP2) such as (NP3)
	#
	#  and is parsed more downstream
	#
	rule = ChunkRule(basic_np+pp,'Chunk NPs')
	parser = RegexpChunkParser([rule],
		chunk_node='NP',   # the name to assign to matched substrings (optional)
		top_node='S')      # the name to assign the top tree node (optional)
	
	#Allows to easily select only every n'th sentence
	n=1
	taggedText=[]
	bs=brown.tagged_sents()
	for i in range(len(bs)/n):
		taggedText=taggedText+[bs[i*n]]
	#Does the chunking and returns it
	chunked=[]
	chunked = [parser.parse(t) for t in taggedText]
	return chunked



#############################################
# Some precompiled RE's that are used later #
#############################################
# A RE to match regular NP
np_s='[(]NP [^)]*[)]' 
# A RE to match an NP that contains 'a/an'
np_s_article='[(]NP[^)]*\s+a[n]?/AT[^)]*[)]'
# A RE to match a regular NP and put it in a entry called 'hypernym'
np_r='(?P<hypernym>'+np_s+')'
# A RE to match a NP that contains 'a/an', and put it in an entry called 'hypernym'
np_r_article='(?P<hypernym>'+np_s_article+')' 
# A RE to match 'and' or 'or'
and_or='(?:(?:and/\S+)|(?:or/\S+))'
# A RE to match 'and\s+' or 'or\s+'
and_or_space='(?:'+and_or+'\s+)'
# A RE to match 'and\s+' or 'or\s+' or ''
and_or_maybe='(?:'+and_or+'\s+)?'
# A RE to match all alpha-numeric groups
alpha_numeric_re=re.compile('(\s*\w+\s*)')
# A RE to match a ',\s+' or 'and\s+' or 'or\s+'
comma_and_or_space='(?:(?:[,]/[,]\s+)|'+and_or_space+')'
# A RE to match any propositional phrase
pp_re=re.compile('/IN')
# A RE to return a groupped np_s
extract_nps_re=re.compile('('+np_s+')')
# A RE used to get ride of Articles
reduce_expression_re=re.compile('(\S+)/(?!AT)')
# Used to grab, 'NP V (PP?) NP' from chunked data
grab_re=re.compile('(?P<np1>'+np_s+')\s+(?P<v>\S+/V\S*)\s+(?:(?P<pp>(?:(?:to)|(?:with))/\S+)\s+)?(?P<np2>'+np_s+')')

#This function is used to turn a peice from a pprint'd
#sentence, into just regular lower case words
def reduce_expression(s):
	return alpha_numeric(" ".join(reduce_expression_re.findall(s))).lower()

def alpha_numeric(s):
	return "".join(alpha_numeric_re.findall(s))

#Function used to extract relations from a list of hypernym's
#and hyponym's
def extract_relations(d):
	if pp_re.search(d['np1'])==None:
		d['np1']=reduce_expression(d['np1'])
	else:
		d['np1']=None
	if pp_re.search(d['np2'])==None:
		d['np2']=reduce_expression(d['np2'])
	else:
		d['np2']=None
	d['v']=reduce_expression(d['v'])
	if d['pp']!=None:
		d['pp']=reduce_expression(d['pp'])
	if d['np1']!=None and d['np2']!=None:
		return d
	else:
		return None

#Used to find common_ancestor of two synset objects
common_ancestor=nltk.corpus.reader.wordnet._lcs_by_depth
#Wordnet corpus
wn=nltk.corpus.wordnet

#function returns 1 if the given,
#hypernym actually corresponds to a hypernym
#of the given hyponym, otherwise returns 0
def is_hypernym_hyponym(hypernym,hyponym):
	hypernym_synsets=wn.synsets(hypernym)
	hyponym_synsets=wn.synsets(hyponym)
	if (len(hypernym_synsets)==0 or len(hyponym_synsets)==0):
		return 0
	for hypernym_synset in hypernym_synsets:
		for hyponym_synset in hyponym_synsets:
			try:
				hypernym_synset.common_hypernyms(hyponym_synset).index(hypernym_synset)
				return 1
			except ValueError:
				pass
	return 0

#The classes as defined in the assignment
classes={\
wn.synset('entity.n.01'):'entity',\
wn.synset('psychological_feature.n.01'):'psychological_feature',\
wn.synset('abstraction.n.06 '):'abstraction',\
wn.synset('state.n.02'):'state',\
wn.synset('event.n.01'):'event',\
wn.synset('act.n.02'):'act',\
wn.synset('group.n.01'):'group',\
wn.synset('possession.n.02'):'possession',\
wn.synset('phenomenon.n.01'):'phenomenon',\
}

#Get the class of a given string,
#relative to the dictionary classes
def get_class(hyponym):
	synsets=wn.synsets(hyponym)
	min_dist=1000000000000000000 # max wornet depth < 100, this is fine
	cl=None
	for synset in synsets:
		if synset.pos=='n': #We are only ever using this for nouns in this case
			paths=synset.hypernym_paths()
			for path in paths:
				path.reverse()
				for node_index in range(min(len(path),min_dist)):
					if classes.has_key(path[node_index]) and node_index<min_dist:
						min_dist=node_index
						cl=classes[path[node_index]]
	return cl


#These are the rules indicating casual relations in the assignment
#The match must pass at least one of these
#If a NP does not match something it wordnet the matching stops here
#and no result is reported
def check_causal_match(d):
	class_np1=get_class(d['np1'])
	class_np2=get_class(d['np2'])
	if class_np1==None or class_np2==None:
		return False
	if d['v']=='cause' or d['v']=='causes':
		return True
	if class_np2=='phenomenon':
		return True
	if class_np1!='entity' and (d['v']=='associated' or d['v']=='associates') and d['pp']=='with':
		if class_np2!='abstraction' and class_np2!='group' and class_np2!='possession':
			return True
	if class_np1!='entity' and (d['v']=='related' or d['v']=='relates' or d['v']=='relate') and d['pp']=='to':
		if class_np2!='abstraction' and class_np2!='group' and class_np2!='possession':
			return True
	if class_np1!='entity' and class_np2=='event':
		return True
	if class_np1!='abstraction' and (class_np2=='event' or class_np2=='act'):
		return True
	if (d['v']=='lead' or d['v']=='leads' or d['v']=='led') and d['pp']=='to':
		if class_np2!='entity' and class_np2!='group':
			return True
	return False

#These are the non-causal relations in the assignment,
#to be reported a match must not pass any of these
def check_non_causal_match(d):
	class_np1=get_class(d['np1'])
	class_np2=get_class(d['np2'])
	if (d['v']=='induce' or d['v']=='induces') and (class_np2=='entity' or class_np2=='abstraction'):
		return False
	if class_np2!='group' and class_np2!='state' and class_np2!='event' and class_np2!='act':
		return False
	if class_np1=='entity' and class_np2!='state' and class_np2!='event' and class_np2!='phenomenon':
		return False
	return True

#Check for all possible relations, and add the results to results variable
def check_for_all_relations(s,r):
	s=' '+s+' ' # pad the line, because some RE's dont account for this
	grabbed=grab_re.finditer(s)
	for grab in grabbed:
		d=extract_relations(grab.groupdict())
		if d and check_causal_match(d) and check_non_causal_match(d):
			key=str(d)
			if not r.has_key(key):
				r[key]=[0,[]]
			r[key][0]+=1
			r[key][1].append(s)


#Find all the relations in the given chunked data
def find_all_relations(chunked):
	results={}
	for x in chunked:
		l=x.pprint().replace('\n','')
		check_for_all_relations(l,results)
	return results

#This writes all the results to disk
def output_results(results):
	# write out all results
	h=open('part2.causal_relations','w')
	to_write='Output from part 2, in total there were %d causal relations found\n' % len(results) + '-'*80 + '\n'
	for key in results.keys():
		count,sentences=results[key]
		d=eval(key)
		to_write+='XYZ: %s & %s & %s & %s \\\\\n' % (d['np1'],d['v'],d['pp'],d['np2'])
		to_write+='Count: %d, NP1: %s, V: %s, PP: %s, NP2: %s\n' % (count,d['np1'],d['v'],d['pp'],d['np2'])
		k=1
		for sentence in sentences:
			to_write+='%d: %s\n\n' % (k,sentence)
			k+=1
	h.write(to_write)
	h.close()


#Do all the work in the correct order
print "Initializing chunked sentences..."
chunked=initialize()
print "Looking for causal relations..."
results=find_all_relations(chunked)
print "Writing all results to disk..."
output_results(results)
print "Done!"






