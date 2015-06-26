#coding: utf-8

import pymongo
from pymongo import MongoClient
from collections import Counter
import pickle
import os
import logging
import operator

'''
creat new dict from original dict
  Input: 
    gi = {'commercial_facility': u'\u5546\u5e97',
   'health_service': u'\u91ab\u9662',
   'telecommunication': (u'\u96fb\u4fe1', u'\u96fb\u8a71', u'\u7db2\u8def'),
   'transport': (u'\u4ea4\u901a', u'\u904b\u8f38')}
 output expect:
    out_dic={
    commercial_facilit : {u'\u5546\u5e97':[(),(),()...]},
    health_service : {u'\u91ab\u9662':[(),(),(),(),()...]}
    telecommunication : {u'\u96fb\u4fe1':[(),(),()...], u'\u96fb\u8a71':[(),(),(),...], u'\u7db2\u8def':[(),(),()...]},
    transport : {u'\u4ea4\u901a':[(),(),()...], u'\u904b\u8f38':[(),(),()...]}
    }
'''


out_dic = {}
for k, v in gi.iteritems():
	
	tk_dic = {}
	if type(v) == tuple:	
			
		for tk in v:
			cn = tesis.count_occurrence(tk)
			nb = tesis.wd_percentageOFappearence(cn[0],cn[1])
			#print cn, nb
			pmi_path = 'bk_resources/TDI_pmi_%d.pkl' %(nb+1)
			term_dic = tesis.find_pmi_pairs(tk,pmi_path)
			fn = '%s_pairs.txt' %(tk)
			tk_tp50_pairs = tesis.sorted_tp50_out_txt(term_dic,fn)
			tk_dic[tk]=tk_tp50_pairs

	else:
		cn = tesis.count_occurrence(v)
		nb = tesis.wd_percentageOFappearence(cn[0],cn[1])
		#print cn, nb
		pmi_path = 'bk_resources/TDI_pmi_%d.pkl' %(nb+1)
		term_dic = tesis.find_pmi_pairs(v,pmi_path)
		fn = '%s_pairs.txt' %(v)
		tk_tp50_pairs = tesis.sorted_tp50_out_txt(term_dic,fn)
		tk_dic.update({v:tk_tp50_pairs})


	out_dic[k] = tk_dic
	
'''
Tengo "alojamiento" (u'\u4f4f\u5bbf')y busco palabras que están enparejadas con "alojamiento" para construir owl en bk.posts
	Paso 1. número de posts mencionan a "alojamiento"
	Paso 2.
'''

def count_occurrence(wd= u'\u4f4f\u5bbf',inputfile= 'bk_resources/all-pairs.pkl'):
	## pairs that we have made before
	all_pairs = pickle.load(open(inputfile,'rb'))
	
	wd_ct_by_st = 0
	wd_ct_by_post = 0
	## ky = '5406a3343480ad1b9b829007', vl= Counter({(u'?', u'QUESTIONCATEGORY'): 14,..
	for ky, vl in all_pairs.iteritems():
		## k= (u'?', u'QUESTIONCATEGORY'): v= 14
		for k, v in vl.iteritems():
			if wd in k:
				#print '%s found' %(wd), " in %s's post" %(ky)
				wd_ct_by_post +=1
				wd_ct_by_st += v
			# else: print 'no found'
	print '%s appears in'%(wd), wd_ct_by_post,'posts'
	print '%s appears'%(wd), wd_ct_by_st,'times'
	return (wd_ct_by_post, wd_ct_by_st)		
	

def wd_percentageOFappearence(post_num=995, appear_times= 1368, inputfile= "bk_resources/all-pairs.pkl", inputdb=db.bk.posts):
	all_pairs = pickle.load(open(inputfile,'rb'))
	
	tot_tokens = 0
	for ky, vl in all_pairs.iteritems():
		tot_tokens += sum(vl.values())
		app_per = 100* float(appear_times)/float(tot_tokens)
	#print "This word occupys %f percentage of all the content" %(app_per)

	
	client = MongoClient('localhost')
	db = client['espanol']
	co = inputdb 
   	tot_post = co.count()
	pt_per = 100* float(post_num)/float(tot_post)
	
	print  "This word appears in %f percentage of posts" % (pt_per)
	return int(pt_per)

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

def find_pmi_pairs(uni_term= u'\u4f4f\u5bbf', path_to_pmi = 'bk_resources/TDI_pmi_5.pkl'):
	pmi_v_dict = pickle.load(open(path_to_pmi,'rb'))
	uni_term_dict = {}	
	for k, v in pmi_v_dict.iteritems():
		if uni_term in k:
			uni_term_dict[k] = v
			#print "add key", k
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

	top50_dic = {}
	for i,(pr, val) in enumerate(top50):
		fo.write( "%s,%s \t---> %f \n" %(pr[0].encode('utf-8'), pr[1].encode('utf-8'), val))
		print "Adding" , i+1, "(pairs:value)"
		#print "%s and %s are saved in %s" % (pr, val, filename)
		top50_dic[pr]=val
	fo.close()
	return top50_dic
