
import nltk
common_ancestor=nltk.corpus.reader.wordnet._lcs_by_depth
wn=nltk.corpus.wordnet

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

def get_class(hyponym):
	synsets=wn.synsets(hyponym)
	min_dist=1000000000000000000
	cl=None
	for synset in synsets:
		if synset.pos=='n':
			paths=synset.hypernym_paths()
			for path in paths:
				path.reverse()
				for node_index in range(min(len(path),min_dist)):
					if classes.has_key(path[node_index]) and node_index<min_dist:
						min_dist=node_index
						cl=classes[path[node_index]]
	return cl
	

def case_1(hypernym,hyponym):
	return case_1(hypernym,hyponym)

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