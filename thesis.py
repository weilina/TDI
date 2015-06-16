#coding: utf-8
import pymongo
from pymongo import MongoClient
from collections import Counter
import pickle
import os
import logging
import operator

'''
With existing keywords to create word-pairs from its cooccurence

	Parameter
	=========
	oc_path: dict
		path to ocDict = {occur': self.Occur,'cooccur': self.Cooccur}
	TDI_path: list
		path to list = ['','']


'''
def find_cooccure(oc_path= "Documentos/resources/TDI_postBcooccur_1.pkl", TDI_path= "Documentos/resources_1/TDIwordlist.owl.pkl" ):
	ocDict = pickle.load(open(oc_path,'r'))
	tdi_ls = pickle.load(open('TDI_path', 'r'))
	co_dict = ocDict['cooccur']
	## a new count_dict with all terms in tdi_ls and the cooccurence in forums
	new_dict = dict((k,v) for k, v in co_dict.iteritems() if k[0] or k[1] in tdi_ls)
==========================================================================
	tdi_cooccurence = {}

	for t in tdi_ls:
		for x in new_dict.keys():
			for g in x:
				if g == t:
					vl = new_dict[x]
					print owl_pairs



		## compare all value in the dict and get key with top 5 value
		owl_pairs_dict= sorted(new_dict, key= new_dict.get, reverse = True)[:5]
	 

	for k, v in new_dict:
		s_v = sorted(v)[:5]


	owl_pairs_dict = dict()
		
	for k, v in co_dict.iteritems():
		if k[0] or k[1] in tdi_ls:
			sort_v= sorted(v, reverse=True)
			for ((w1, w2), val) in sorted_v[:5]:
				owl_pairs_dict[k]
				print (w1,w2), val


		if w in new_dict.keys()
			

	for x in new_dict.keys():
		for g in x:
			if g == u'\u967d\u53f0':
				print x 

		co_term_pair_ls = ocDict['cooccur'].keys() ## collections.Counter
		co_term_orden_ls = sorted(ocDict['cooccur'].values(),reverse= True)

	for t_pair, t_orden in ocDict['cooccur']:
		print t_pair
		if u'\u7b2c\u4e09' == x in t_pair :
			print t_pair
		#elif u'\u7b2c\u4e09' == y :
		#	print x,y
		else:
			continue


	for x, y in co_term_pair_ls:

		for term in tdi_ls:
			if term in co



			u'\u7b2c\u4e09'

	## mongodb
	mongo_addr = 'localhost'
	mongo_db = 'espanol' if 'mongo_db' not in kwargs else kwargs['mongo_db']

	## support multiple target collections
	mongo_cos = ['bk.posts', 'qy.posts']
	# mongo_cos = ['bk.posts'] if 'mongo_cos' not in kwargs else kwargs['mongo_cos']

	override = False if 'override' not in kwargs else kwargs['override']

	## check if self.AllPairs exists
	if AllPairs and not override:
		logging.info('AllPairs already exists')
	    return False

	if os.path.exists(path) and not override:
	    logging.info('Load AllPairs from %s' % (path))
	    AllPairs = pickle.load(open(path))
	    return True

	### fetch data from mongodb
	client = MongoClient(mongo_addr)
	db = client[mongo_db]

服务 u'\u670d\u52a1'
服務 u'\u670d\u52d9'
======================================================================================
'''
 convierte la palabra a uncode 
	 input -> '住宿' 
	 output-> u'\u4f4f\u5bbf'
'''

def turn_tk_unicode(term):
	tk = term
	uni_tk= tk.decode('utf-8')
	print uni_tk
	return uni_tk

'''
Tengo "alojamiento" (u'\u4f4f\u5bbf')y busco palabras que están enparejadas con "alojamiento" para construir owl en bk.posts
Paso 1. número de posts mencionan a "alojamiento"
Paso 2.

'''
def count_occurrence(wd= u'\u4f4f\u5bbf',inputfile= 'Documentos/bk_resources/all-pairs.pkl'):
	## pairs that we have made before
	all_pairs = pickle.load(open(inputfile,'rb'))
	
	wd_ct_by_st = 0
	wd_ct_by_post = 0
	## ky = '5406a3343480ad1b9b829007', vl= Counter({(u'?', u'QUESTIONCATEGORY'): 14,..
	for ky, vl in all_pairs.iteritems():
		## k= (u'?', u'QUESTIONCATEGORY'): v= 14
		for k, v in vl.iteritems():
			if wd in k:
				print '%s found' %(wd), " in %s's post" %(ky)
				wd_ct_by_post +=1
				wd_ct_by_st += v
			# else: print 'no found'
	print '%s appears in'%(wd), wd_ct_by_post,'posts'
	print '%s appears'%(wd), wd_ct_by_st,'times'


def wd_percentageOFappearence(post_num=995, appear_times= 1368, inputfile= "Documentos/bk_resources/all-pairs.pkl", inputdb=db.bk.posts):
	all_pairs = pickle.load(open(inputfile,'rb'))
	
	tot_tokens = 0
	for ky, vl in all_pairs.iteritems():
		tot_tokens += sum(vl.values())
		app_per = 100* float(appear_times)/float(tot_tokens)
	print "This word occupys %f percentage of all the content" %(app_per)

	
	client = MongoClient('localhost')
	db = client['espanol']
	co = inputdb 
   	tot_post = co.count()
	pt_per = 100* float(post_num)/float(tot_post)
	
	print  "This word appears in %f percentage of posts" % (pt_per)


'''
busca las parejas de la palabra "alojamiento"
	Parameter
	=================
	input 
		uni_term -> u'\u4f4f\u5bbf'
		path_to_pmi -> pmi_value_dict {(u'\u5730\u9435', u'\u80cc\u5305'): 1.077244837797389,...}
	output
		dict(): {(u'\u4f4f\u5bbf', u'\u5de5\u4f5c'): 0.7953790232827842,..}
		keys son parejas de palabras que una de ellas es "alojamiento", 
	values son valores de pmi  
'''

def find_pmi_pairs(uni_term= u'\u4f4f\u5bbf', path_to_pmi = 'Documentos/bk_resources/TDI_pmi_5.pkl'):
	pmi_v_dict = pickle.load(open(path_to_pmi,'rb'))
	uni_term_dict = {}	
	for k, v in pmi_v_dict.iteritems():
		if uni_term in k:
			uni_term_dict[k] = v
			print "add key", k
		else:continue
	return uni_term_dict

'''
exportar un txt con el resultado ordenado por el valor 
	Parameter
	==================
	input
		dic = result of def find_pmi_pairs -> { (u'\u4f4f\u5bbf', u'\u9ad8\u5c71'): 2.373909398253808,
			(u'\u4f4f\u5bbf', u'\u9b6f'): 1.3299012436205504...}
	output 
		filename = 当名.txt
'''
def sorted_tp50_out_txt (dic, filename= "bk_pmi5"):
	fo = open(filename,"w")
	s_term_ls = sorted(dic.iteritems(), key=operator.itemgetter(1,0), reverse=True)
	top50 = s_term_ls[:50]
	for pr, val in top50:
		fo.write( "%s,%s \t---> %f \n" %(pr[0].encode('utf-8'), pr[1].encode('utf-8'), val))
		print "%s and %s are saved in %s" % (pr, val, filename)
	fo.close()
'''
exportar un txt donde aparece la lista de palabras con pmi positivo
	Parameter
	=========
	input:
		dic = "Documentos/bk_resources/TDI_pmi_5.pkl" ->((u'\u5730\u9435', u'\u80cc\u5305'), 1.077244837797389)
		term = unicode, eg.,u'\u4f4f\u5bbf'
	output:
		filename = nombre queremos que nombra el archivo de txt
'''
def sorted_positive_pmi (term=u'\u4f4f\u5bbf',dic= "bk_resources/TDI_pmi_10.pkl", filename= "bk_positive_pmi10"):
	fo = open(filename,"w")
	pmi_dic = pickle.load(open(dic,"rb"))
	lst = sorted(pmi_dic.items(), key=lambda x: x[1], reverse= True)
	
	pos_dict = {}
	for x in lst:
		if term in x[0] and x[1] > 0:
			print "Add", x[0], x[1], "in positive_dict"
			pos_dict[x[0]] = x[1]
		else:
			continue
	lst_pmi10 = sorted(pos_dict.iteritems(), key = operator.itemgetter(1,0),reverse=True)
	for pairs, vl in lst_pmi10:
		fo.write( "%s,%s \t -----> %f \n" %(pairs[0].encode('utf-8'), pairs[1].encode('utf-8'), vl))
	fo.close


	
	print len(pos_lst)



	
	

	
	for pr, val in top50:
		fo.write( "%s,%s \t---> %f \n" %(pr[0].encode('utf-8'), pr[1].encode('utf-8'), val))
		print "%s and %s are saved in %s" % (pr, val, filename)
	fo.close()

'''
ordena uni_term_dict según su valor y revisa con "enter" uno por uno
	input -> { (u'\u4f4f\u5bbf', u'\u9ad8\u5c71'): 2.373909398253808,
		(u'\u4f4f\u5bbf', u'\u9b6f'): 1.3299012436205504...}
	output -> 住宿 清潔 3.6122836293
			住宿 度假村 3.6122836293
			.
			.
			.
''' 
def raw_h_pmi(dic):
	s_term_ls = sorted(dic.iteritems(), key=operator.itemgetter(1,0), reverse=True)
	for pair, val in s_term_ls:
		s = raw_input()
		print pair[0], pair[1], val, s 

'''
calculate the average of a term (alojamiento" (u'\u4f4f\u5bbf'))shows in posts
	Parameter
	===============
	Input:

	Output:
'''
def count_average (term=u'\u4f4f\u5bbf'):
	occo = pickle.load(open("bk_resources/TDI_cooccur_1.pkl","r"))
	
	sum_of_occurence = 0
	num_of_pairs = 0
	for k, v in occo['cooccur'].iteritems():
		if term in k:
			sum_of_occurence += v
			num_of_pairs += 1
	avr = 100* float(num_of_pairs)/float(sum_of_occurence)
	print "There are totally %s type of combination. The sum of these combinations are %s times." % (num_of_pairs, sum_of_occurence), "\n\n", "The average is %s percent" %(avr)
