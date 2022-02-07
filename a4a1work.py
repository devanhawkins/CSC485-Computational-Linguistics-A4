
import re
np_s='[(]NP [^)]*[)]'
np_r='(?P<hypernym>'+np_s+')'
np_o='[(]NP (?P<hyponym>[^)]*)[)]'
and_or='(?:(?:and/\S+)|(?:or/\S+))'
and_or_maybe='(?:'+and_or+'\s+)?'
example='(S  (NP Nikolai/NP Cherkasov/NP)  ,/,  (NP the/AT Russian/JJ actor/NN)  who/WPS  has/HVZ  played/VBN  such/ABL  (NP heroic/JJ roles/NNS)  as/CS  (NP Alexander/NP Nevsky/NP)  and/CC  (NP Ivan/NP)  the/AT-TL  Terrible/JJ-TL  ,/,  performs/VBZ  (NP the/AT lanky/JJ Don/NP Quixote/NP)  ,/,  and/CC  does/DOZ  so/RB  with/IN  (NP a/AT simple/JJ dignity/NN)  that/WPS  bridges/VBZ  (NP the/AT inner/JJ nobility/NN)  and/CC  (NP the/AT surface/NN absurdity/NN)  of/IN  (NP this/DT poignant/JJ man/NN)  ./.)'
example2='(S  (NP The/AT decreases/NNS)  ,/,  which/WDT  are/BER  largely/RB  in/IN  (NP construction/NN)  and/CC  in/IN  (NP aircraft/NN procurement/NN)  ,/,  are/BER  offset/VBN  in/IN  (NP part/NN)  by/IN  (NP increases/NNS)  for/IN  (NP research/NN)  and/CC  (NP development/NN)  and/CC  for/IN  (NP procurement/NN)  of/IN  other/AP  (NP military/JJ equipment/NN)  such/JJ  as/CS  (NP tanks/NNS)  ,/,  (NP vehicles/NNS)  ,/,  (NP guns/NNS)  ,/,  and/CC  (NP electronic/JJ devices/NNS)  ./.)'

extract_nps_re=re.compile('('+np_s+')')

reduce_np_re=re.compile('(\S+)/(?!AT)')
def reduce_np(s):
	return " ".join(reduce_np_re.findall(s))

def extract_relations(d):
	hypernyms=[]
	for hypernym in extract_nps_re.findall(d['hypernym']):
		hypernyms+=[reduce_np(hypernym)]
	results=[]
	for hyponym in extract_nps_re.findall(d['hyponyms']):
		for hypernym in hypernyms:
			results.append([hypernym,reduce_np(hyponym)])
	return results

such_np_as_relation_re=re.compile('such/\S+\s+'+np_r+'\s+as/\S+\s+(?P<hyponyms>'+np_s+'\s+(?:(?:[,]/[,]\s+'+np_s+'\s+)*(?:[,]/[,]\s+)?'+and_or+'\s+'+np_s+'\s+)?)')
def such_np_as_relation(s):
	results=[]
	m=such_np_as_relation_re.search(s)
	if m!=None:
		results+=extract_relations(m.groupdict())
	return results

np_such_as_relation_re=re.compile(np_r+'\s+such/\S+\s+as/\S+\s+(?P<hyponyms>'+np_s+'\s+(?:(?:[,]/[,]\s+'+np_s+'\s+)*(?:[,]/[,]\s+)?'+and_or+'\s+'+np_s+'\s+)?)')
def np_such_as_relation(s):
	results=[]
	m=np_such_as_relation_re.search(s)
	if m!=None:
		results+=extract_relations(m.groupdict())
	return results

nps_or_other_np_re=re.compile('(?P<hyponyms>'+np_s+'\s+(?:[,]/[,]\s+'+np_s+'\s+)*)(?:[,]/[,]\s+)?or/\S+\s+other/\S+\s+'+np_r)
def nps_or_other_np(s):
	results=[]
	m=nps_or_other_np_re.search(s)
	if m!=None:
		results+=extract_relations(m.groupdict())
	return results


nps_and_other_np_re=re.compile('(?P<hyponyms>'+np_s+'\s+(?:[,]/[,]\s+'+np_s+'\s+)*)(?:[,]/[,]\s+)?and/\S+\s+other/\S+\s+'+np_r)
def nps_and_other_np(s):
	results=[]
	m=nps_and_other_np_re.search(s)
	if m!=None:
		results+=extract_relations(m.groupdict())
	return results
		
def check_for_all_relations(s):
	s=' '+s+' '
	results=[]
	results+=such_np_as_relation(s)
	results+=np_such_as_relation(s)
	results+=nps_or_other_np(s)
	results+=nps_and_other_np(s)
	return results

results=[]
for x in chunked:
	l=x.pprint().replace('\n','')
	q=re.compile('Nike.*Z')
	if q.search(l):
		print l
	results+=check_for_all_relations(l)
