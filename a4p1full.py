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
reduce_np_re=re.compile('(\S+)/(?!AT)')
#The precompiled relation RE's in a dictionary form
relation_res={\
'such_np_as':re.compile('such/\S+\s+'+np_r+'\s+as/\S+\s+(?P<hyponyms>'+np_s+'\s+(?:(?:'+comma_and_or_space+np_s+'\s+)*(?:[,]/[,]\s+)?'+and_or+'\s+'+np_s+'\s+)?)'),\
'np_such_as':re.compile(np_r+'\s+such/\S+\s+as/\S+\s+(?P<hyponyms>'+np_s+'\s+(?:(?:'+comma_and_or_space+np_s+'\s+)*(?:[,]/[,]\s+)?'+and_or+'\s+'+np_s+'\s+)?)'),\
'nps_or_other_np':re.compile('(?P<hyponyms>'+np_s+'\s+(?:'+comma_and_or_space+np_s+'\s+)*)(?:[,]/[,]\s+)?or/\S+\s+other/\S+\s+'+np_r),\
'nps_and_other_np':re.compile('(?P<hyponyms>'+np_s+'\s+(?:'+comma_and_or_space+np_s+'\s+)*)(?:[,]/[,]\s+)?and/\S+\s+other/\S+\s+'+np_r),\
'np_including_nps':re.compile(np_r+'\s+(?:[,]/[,]\s+)?including/\S+\s+(?P<hyponyms>'+np_s+'\s+(?:(?:'+comma_and_or_space+np_s+'\s+)*(?:[,]/[,]\s+)?'+and_or+'\s+'+np_s+'\s+)?)'),\
'np_especially_nps':re.compile(np_r+'\s+(?:[,]/[,]\s+)?especially/\S+\s+(?P<hyponyms>'+np_s+'\s+(?:(?:'+comma_and_or_space+np_s+'\s+)*(?:[,]/[,]\s+)?'+and_or+'\s+'+np_s+'\s+)?)'),\
#'np_is_a':re.compile('(?P<hyponyms>'+np_s+')\s+is/\S+\s+'+np_r_article),\
#'np_like':re.compile(np_r+'\s+like/\S+\s+(?P<hyponyms>'+np_s+')'),\
#'np_called':re.compile(np_r+'\s+called/\S+\s+(?P<hyponyms>'+np_s+')'),\
#'np_a':re.compile('(?P<hyponyms>'+np_s+')\s+[,]/[,]\s+'+np_r_article),\
}

#This function is used to turn a peice from a pprint'd
#sentence, into just regular lower case words
def reduce_np(s):
	return alpha_numeric(" ".join(reduce_np_re.findall(s))).lower()

def alpha_numeric(s):
	return "".join(alpha_numeric_re.findall(s))

#Function used to extract relations from a list of hypernym's
#and hyponym's
def extract_relations(d):
	hypernyms=[]
	for hypernym in extract_nps_re.findall(d['hypernym']):
		if pp_re.search(hypernym)==None:
			hypernyms+=[reduce_np(hypernym)]
	results=[]
	for hyponym in extract_nps_re.findall(d['hyponyms']):
		if pp_re.search(hyponym)==None:
			for hypernym in hypernyms:
				results.append([hypernym,reduce_np(hyponym)])
	return results

#Check for all possible relations, and add the results to results variable
def check_for_all_relations(s,results):
	s=' '+s+' ' # pad the line, because some RE's dont account for this
	for relation_re_key in relation_res.keys(): #for every hard coded type of relation
		relation_re=relation_res[relation_re_key] #get the re for the relation
		matches=relation_re.finditer(s) 
		for match in matches: #for every non-overlapping match of the RE in the sentence
			match_relations=extract_relations(match.groupdict())
			#iterate over all relations found in the current sentence
			for match_relation in match_relations:
				key=str(match_relation)
				if not results.has_key(key):
					results[key]=[0,[]]
				results[key][0]+=1
				results[key][1].append(s)

#Find all the relations in the given chunked data
def find_all_relations(chunked):
	results={}
	for x in chunked:
		l=x.pprint().replace('\n','')
		check_for_all_relations(l,results)
	return results



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

#The four different cases defined as in assignment, for 
#the evaluation of part 1
def case_1(hypernym,hyponym):
	return is_hypernym_hyponym(hypernym,hyponym)

def case_2(hypernym,hyponym):
	return case_1(hyponym,hypernym)

def case_3(hypernym,hyponym):
	if len(wn.synsets(hypernym))>0 and len(wn.synsets(hyponym))>0 and not is_hypernym_hyponym(hypernym,hyponym):
		return 1
	return 0

def case_4(hypernym,hyponym):
	if len(wn.synsets(hypernym))==0 or len(wn.synsets(hyponym))==0:
		return 1
	return 0


def populate_cases(results):
	#prepare a list of dictionaries to store the output
	#each dictionary will store information on each confidence
	#level for that case
	cases=[{},{},{},{},{}] #one extra to make it 1 based
	for key in results.keys():
		#Get some local variables with needed values from results
		hypernym,hyponym=eval(key)
		count,sentences=results[key]
		#Add setence/relation to each case it applies to
		if case_1(hypernym,hyponym)==1:
			if not cases[1].has_key(count):
				cases[1][count]=[]
			cases[1][count].append({'count':count,'sentences':sentences,'hypernym':hypernym,'hyponym':hyponym})
		if case_2(hypernym,hyponym)==1:
			if not cases[2].has_key(count):
				cases[2][count]=[]
			cases[2][count].append({'count':count,'sentences':sentences,'hypernym':hypernym,'hyponym':hyponym})
		if case_3(hypernym,hyponym)==1:
			if not cases[3].has_key(count):
				cases[3][count]=[]
			cases[3][count].append({'count':count,'sentences':sentences,'hypernym':hypernym,'hyponym':hyponym})
		if case_4(hypernym,hyponym)==1:
			if not cases[4].has_key(count):
				cases[4][count]=[]
			cases[4][count].append({'count':count,'sentences':sentences,'hypernym':hypernym,'hyponym':hyponym})
	return cases

#write all infor in the cases to disk
def output_cases(cases):
	for x in range(1,5):
		h=open('part1.case%d' % x,'w')
		to_write='Output from part1\n'+'-'*80+'\n'+'Found %s confidence classes for case %d\n' % (str(cases[x].keys()),x) + '-'*80 +'\n'
		for level in cases[x].keys():
			to_write+='Found %d instances for confidence level %d\n' % (len(cases[x][level]),level) + '-'*80 +'\n'
		for key in cases[x].keys():
			to_write+='-'*80+'\n'+'Dump of elements in confidence level %d\n' % key + '-'*80+'\n'
			for d in cases[x][key]:
				to_write+='Count: %d, hypernym: %s, hyponym:%s\n' % (d['count'],d['hypernym'],d['hyponym'])
				to_write+='XYZ: %s & %s \\\\\n' % (d['hypernym'],d['hyponym'])
				count=1
				for sentence in d['sentences']:
					to_write+='%d:' % count + sentence+'\n'
					count+=1
				to_write+='\n'
		#print to_write
		h.write(to_write)
		h.close()


#Do all the work in the correct order
print "Initializing chunked sentences..."
chunked=initialize()
print "Looking for hypernym/hyponym relations..."
results=find_all_relations(chunked)
print "Populating the cases..."
cases=populate_cases(results)
print "Writing all cases info to disk..."
output_cases(cases)
print "Done!"






