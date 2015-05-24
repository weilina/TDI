def collect_highPmiPairs (pmi_value = "resources/TDI_pmi_15.pkl", terms= "terms.pkl", output= None, threshold = 5):
	'''
	findout top(i) tokens related with terms in the special words list and return a dict

	Parameters
	===========
		sp_word: str
			path to the dictionary that contains anchor words eg.,-> 'FRONTERA': ['\xe5\x9c\x8b\xe5\xa2\x83', '\xe9\x82\x8a\xe7\x95\x8c']
			here it is a dict of list of tokens (['\xe5\x9c\x8b\xe5\xa2\x83', '\xe9\x82\x8a\xe7\x95\x8c']) relative with tourism destination image attribute('FRONTERA')
		pmi: str
			path to the dictionary that contains eg.,-> (Pairs): pmi value
		threshold: int
			number that indicates the top "number" pmi words we look for
			here is sorted_spanish [:number]
	Returns
	=======
		objective_pairs: dict
			Key will be spanish and value will be a list containing tuples(pairs) 
	NOTE
	=====
		¿¿¿¿need to convert chinese from utf-8 to unicode????
		¿¿¿¿how to write a threshold???? 
	'''

	pmi_value = pickle.load(open("resources/TDI_pmi_15.pkl", 'r'))
	terms = pickle.load(open("terms.pkl", 'r'))

	objective_pairs = defaultdict(list)

	for spanish, chinese in terms.values():
		## chinese is a list of tokens-> ValueError: need more than 1 value to unpack
		for cn_tk in chinese:
			spanish = filter(lambda x:x[0][0] == cn_tk or x[0][1] == cn_tk, pmi_value.items())
			sorted_spanish = sorted(spanish, key=lambda x:x[1], reverse=True)
			for ((w1, w2), pmi) in sorted_spanish[:5]:
				objective_pairs[spanish].append((w1,w2))
				print (w1,w2) + "are collecting into" + spanish

	pickle.dump(objective_pairs,open(output,'wb'))		
	return objective_pairs
