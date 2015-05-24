
def collect_highPmiPairs (pmi_value = "resources/TDI_pmi_15.pkl", terms= "terms.pkl", out_path= "resources/obj_pairs", threshold = 5):
	'''
	findout top i tokens related with tokens in the special words list

	Parameters
	===========
		sp_word: str
			path to the dictionary that contains anchor words -> 'FRONTERA': ['\xe5\x9c\x8b\xe5\xa2\x83', '\xe9\x82\x8a\xe7\x95\x8c']
			here it is a dict of list of tokens (['\xe5\x9c\x8b\xe5\xa2\x83', '\xe9\x82\x8a\xe7\x95\x8c']) relative with tourism destination image attribute('FRONTERA')
		pmi: str
			path to the dictionary that contains -> (Pairs): pmi value
		threshold: int
			number that indicates the top "number" pmi words we look for
			here is sorted_spanish [:number]
	Returns
	=======
		objective_pairs: dict
			Key will be spanish and value will be a list containing tuples(pairs) 
	NOTE
	=====
		¿¿¿how to write a threshold???? 
	'''

	pmi_value = pickle.load(open("Documentos/resources_1/TDI_pmi_15.pkl", 'r'))
	terms = pickle.load(open("Documentos/terms.pkl", 'r'))
	## terms = {'español': ['chino','chino','chino'], 'español': ['chino'],... }
	## pmi_values = {(word_pairs): cifra,(word_pair):cifra,...} 

	## I want-> objective_pairs = {'español', [(pairs),(pairs),...], 'español': [(pairs),...], ...}	
	objective_pairs = defaultdict(list)

	for esp, cn in terms.iteritems():
		## Some spanish word doesn't have chinese translation 
		if len(cn) != 0:
			## if key(es) exist -> add only value(w1,w2)
			if es in objective_pairs.keys():
				for cn_tk in cn:
					#print es
					tk = cn_tk.decode('utf-8')
					es = esp.decode('utf-8')
					tk_es = filter(lambda x:x[0][0] == tk or x[0][1] == tk, pmi_value.items())
					sorted_tk_es = sorted(tk_es, key=lambda x:x[1], reverse=True)
					
					for ((w1, w2), pmi) in sorted_tk_es[:5]:
						objective_pairs[es].append((w1,w2))
						print es + " exists in dict. Appending " + w1,w2
			## else: add  key(es) + value(w1,w2)			
			else:
				for cn_tk in cn:
					#print es
					tk = cn_tk.decode('utf-8')
					es = esp.decode('utf-8')
					tk_es = filter(lambda x:x[0][0] == tk or x[0][1] == tk, pmi_value.items())
					sorted_tk_es = sorted(tk_es, key=lambda x:x[1], reverse=True)
					
					for ((w1, w2), pmi) in sorted_tk_es[:5]:
						objective_pairs[es] = [(w1,w2)]
						print w1,w2 + "are collecting into " + es
		else:
			print "-------------------------> empty value. Jump over"
			continue

	pickle.dump(objective_pairs,open("Documentos/resources/obj_pairs",'w'))		
	return objective_pairs
