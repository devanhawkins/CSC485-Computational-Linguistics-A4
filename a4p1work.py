
import re
np_s='[(]NP [^)]*[)]'
np_s_article='[(]NP[^)]*\s+a[n]?/AT[^)]*[)]'
np_r='(?P<hypernym>'+np_s+')'
np_r_article='(?P<hypernym>'+np_s_article+')'
np_o='[(]NP (?P<hyponym>[^)]*)[)]'
and_or='(?:(?:and/\S+)|(?:or/\S+))'
and_or_space='(?:'+and_or+'\s+)'
and_or_maybe='(?:'+and_or+'\s+)?'
alpha_numeric_re=re.compile('(\w+)')
comma_and_or_space='(?:(?:[,]/[,]\s+)|'+and_or_space+')'

pp_re=re.compile('/IN')
extract_nps_re=re.compile('('+np_s+')')

reduce_np_re=re.compile('(\S+)/(?!AT)')
def reduce_np(s):
	return alpha_numeric(" ".join(reduce_np_re.findall(s)))

def alpha_numeric(s):
	return " ".join(alpha_numeric_re.findall(s))

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

def check_for_all_relations(s,results):
	s=' '+s+' ' # pad the line, because some RE's dont account for this
	for relation_re_key in relation_res.keys():
		relation_re=relation_res[relation_re_key]
		matches=relation_re.finditer(s)
		for match in matches:
			match_relations=extract_relations(match.groupdict())
			for match_relation in match_relations:
				key=str(match_relation).lower()
				if not results.has_key(key):
					results[key]=0
				results[key]+=1
				#h.write(s+'\n'+str(match_relation)+'\n')
				#print s
				#print match_relation

results={}
for x in chunked:
	l=x.pprint().replace('\n','')
	check_for_all_relations(l,results)

