### Here are some test cases that were used to test the general functionality of all the
### lexicosyntactic pattern RE's under the original chunker
### some commented out test cases correspond to the 4 additional patterns added from
### Snow et. al (2005)

ho1='(NP hyponym1/C)'
ho2='(NP hyponym2/C)'
ho3='(NP hyponym3/C)'
ho4='(NP hyponym4/C)'
ho5='(NP hyponym5/C)'
hy1='(NP hypernym/C)'
nd='and/C'
o='or/C'
such='such/C'
az='as/C'
c=',/,'
other='other/C'
including='including/C'
especially='especially/C'
i='is/C'
a='a/C'
an='an/C'
r1={"['hypernym', 'hyponym1']": 1}
r2={"['hypernym', 'hyponym1']": 1,"['hypernym', 'hyponym2']": 1}
r3={"['hypernym', 'hyponym1']": 1,"['hypernym', 'hyponym2']": 1,"['hypernym', 'hyponym3']": 1}

#Tests that should pass
should_pass=[\
{'s':such+' '+hy1+' '+az+' '+ho1,'r':r1},\
{'s':such+' '+hy1+' '+az+' '+ho1+' '+nd+' '+ho2,'r':r2},\
{'s':such+' '+hy1+' '+az+' '+ho1+' '+o+' '+ho2,'r':r2},\
{'s':such+' '+hy1+' '+az+' '+ho1+' '+c+' '+nd+' '+ho2,'r':r2},\
{'s':such+' '+hy1+' '+az+' '+ho1+' '+c+' '+ho2+' '+c+' '+nd+' '+ho3,'r':r3},\
{'s':such+' '+hy1+' '+az+' '+ho1+' '+c+' '+ho2+' '+nd+' '+ho3,'r':r3},\
{'s':ho1+' '+c+' '+ho2+' '+c+' '+o+' '+other+' '+hy1,'r':r2},\
{'s':ho1+' '+c+' '+ho2+' '+c+' '+ho3+' '+o+' '+other+' '+hy1,'r':r3},\
{'s':ho1+' '+c+' '+ho2+' '+c+' '+nd+' '+other+' '+hy1,'r':r2},\
{'s':ho1+' '+c+' '+ho2+' '+c+' '+ho3+' '+nd+' '+other+' '+hy1,'r':r3},\
{'s':hy1+' '+c+' '+including+' '+ho1,'r':r1},\
{'s':hy1+' '+including+' '+ho1,'r':r1},\
{'s':hy1+' '+c+' '+including+' '+ho1+' '+nd+' '+ho2,'r':r2},\
{'s':hy1+' '+c+' '+including+' '+ho1+' '+c+' '+ho2+' '+nd+' '+ho3,'r':r3},\
{'s':hy1+' '+c+' '+including+' '+ho1+' '+c+' '+ho2+' '+o+' '+ho3,'r':r3},\
{'s':hy1+' '+c+' '+especially+' '+ho1,'r':r1},\
{'s':hy1+' '+especially+' '+ho1,'r':r1},\
{'s':hy1+' '+c+' '+especially+' '+ho1+' '+nd+' '+ho2,'r':r2},\
{'s':hy1+' '+c+' '+especially+' '+ho1+' '+c+' '+ho2+' '+nd+' '+ho3,'r':r3},\
{'s':hy1+' '+c+' '+especially+' '+ho1+' '+c+' '+ho2+' '+o+' '+ho3,'r':r3},\
#{'s':ho1+' '+i+' '+a+' '+hy1,'r':r1},\
#{'s':ho1+' '+i+' '+an+' '+hy1,'r':r1}\
]

#Tests that should fail
should_fail=[\
{'s':such+' '+hy1+' '+az+' '+ho1+' '+nd+' '+c+' '+ho2,'r':r2},\
{'s':such+' '+hy1+' '+az+' '+ho1+' '+c+' '+ho2,'r':r2},\
{'s':such+' '+hy1+' '+az+' '+ho1+' '+c+' '+ho2+' '+c+' '+ho3,'r':r3},\
#{'s':such+' '+hy1+' '+az+' '+ho1+' '+nd+' '+ho2+' '+nd+' '+ho3,'r':r3},\
{'s':ho1+' '+ho2+' '+c+' '+o+' '+other+' '+hy1,'r':r2},\
{'s':ho1+' '+c+' '+ho2+' '+ho3+' '+nd+' '+other+' '+hy1,'r':r3},\
{'s':ho1+' '+ho2+' '+c+' '+nd+' '+other+' '+hy1,'r':r2},\
{'s':ho1+' '+c+' '+ho2+' '+ho3+' '+nd+' '+other+' '+hy1,'r':r3},\
{'s':hy1+' '+c+' '+nd+' '+ho1,'r':r1},\
{'s':ho1+' '+including+' '+hy1,'r':r1},\
{'s':hy1+' '+c+' '+including+' '+ho1+' '+az+' '+ho2,'r':r2},\
{'s':hy1+' '+c+' '+including+' '+ho1+' '+c+' '+ho2+' '+c+' '+ho3,'r':r3},\
{'s':hy1+' '+c+' '+including+' '+ho1+' '+c+' '+ho2+' '+ho3,'r':r3},\
{'s':ho1+' '+especially+' '+hy1,'r':r1},\
{'s':hy1+' '+c+' '+especially+' '+ho1+' '+az+' '+ho2,'r':r2},\
{'s':hy1+' '+c+' '+especially+' '+ho1+' '+c+' '+ho2+' '+c+' '+ho3,'r':r3},\
{'s':hy1+' '+c+' '+especially+' '+ho1+' '+c+' '+ho2+' '+ho3,'r':r3}\
]


def run_test(t,should):
	expected=t['r']
	r={}
	check_for_all_relations(t['s'],r)
	try:
		assert((r==expected)==should)
	except AssertionError:
		print "Expecting:" , expected
		print "Got:" , r

for x in range(len(should_pass)):
	run_test(should_pass[x],True)
	print "PASSED " + str(x)

for x in range(len(should_fail)):
	run_test(should_fail[x],False)
	print "PASSED " + str(x)


