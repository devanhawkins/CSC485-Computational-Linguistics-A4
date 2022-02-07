
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

reduce_expression_re=re.compile('(\S+)/(?!AT)')
def reduce_expression(s):
	return alpha_numeric(" ".join(reduce_expression_re.findall(s))).lower()

def alpha_numeric(s):
	return " ".join(alpha_numeric_re.findall(s))

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


grab_re=re.compile('(?P<np1>'+np_s+')\s+(?P<v>\S+/V\S*)\s+(?:(?P<pp>(?:(?:to)|(?:with))/\S+)\s+)?(?P<np2>'+np_s+')')


def check_causal_match(d):
	class_np1=get_class(d['np1'])
	class_np2=get_class(d['np2'])
	if class_np1==None or class_np2==None:
		if d['v']=='lead':
			print d
		return False
	if d['v']=='cause' or d['v']=='causes':
		return True
	if class_np2=='phenomenon':
		return True
	if class_np1!='entity' and d['v']=='associated' and d['pp']=='with':
		if class_np2!='abstraction' and class_np2!='group' and class_np2!='possession':
			return True
	if class_np1!='entity' and d['v']=='related' and d['pp']=='to':
		if class_np2!='abstraction' and class_np2!='group' and class_np2!='possession':
			return True
	if class_np1!='entity' and class_np2=='event':
		return True
	if class_np1!='abstraction' and (class_np2=='event' or class_np2=='act'):
		return True
	if (d['v']=='lead' or d['v']=='leads') and d['pp']=='to':
		if class_np2!='entity' and class_np2!='group':
			return True
	return False

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


def check_for_all_relations(s,r):
	results=[]
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

results={}
for x in chunked:
	l=x.pprint().replace('\n','')
	check_for_all_relations(l,results)


# write out some results #
h=open('part2.causal_relations','w')
to_write='Output from part 2, in total there were %d causal relations found\n' % len(results) + '-'*80 + '\n'
for key in results.keys():
	count,sentences=results[key]
	to_write+='Count: %d, %s\n' % (count,key)
	k=1
	for sentence in sentences:
		to_write+='%d: %s\n' % (k,sentence)
		k+=1

h.write(to_write)
h.close()


