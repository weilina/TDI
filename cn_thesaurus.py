# -*- coding: utf-8 -*-
import goslate
import json
import os
import pickle
import re
import csv
import re

'''
Read csv word by word, and convert each word with its translation to a dict
To translate words in Spanish to zh-tw
'''

## Create a Goslate instance first
gs = goslate.Goslate()
## You could get all supported language list through get_languages
languages = gs.get_languages()
print(languages['zh'])
## resultado->English
##print gs.translate('clima','zh-tw')

f = open('corpus_CN.csv','rw')
corpus = f.readlines()
## change all words in low case

es_cps = []
cn_cps = []
for x in corpus:
	low = x.lower()
	w = low.strip()
	es_cps.append(w)
	tk = gs.translate( w,'zh-tw')
	cn_cps.append(tk)

cn_cps_dict = dict(zip(corpus,cn_cps)) 
### after each key was added \n ????????????why?????????
'''
To save a dict to a txt file (use JSON modules)
''' 
## json.dump(obj, fp, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, encoding="utf-8", default=None, sort_keys=False, **kw)
json.dumps


def print_txt(total_owl, output="corpus.txt"):
	## branch form
	branch = '-'
	## to save as a txt
	import codecs
	with codecs.open(output, "w", "utf-8") as fw:
		## give it a description of the tree
		for levels, texts, zh_TW, zh_CN, ENG in total_owl:
			## the depth of the value
			depth = len(levels)-1
			## how values will be attached in a line
			line =  branch*depth + '-'.join(levels) +','+','.join(zh_TW) +','+','.join(texts).decode("utf-8") +'\n'

			print line
			## write the file
			fw.write(line)

''' To make all csvs into a list of labels from a owl file'''

## to indicate the path of the file
path = "/home/wei/Documentos/owl"
## to declare what we want is csv file if not e.g., temperal file, we omit it
csvs = [x for x in os.listdir(path) if not x.startswith('.')]

## to creat a function to seperate levels and texts into two lists
def collect_level_and_text(clear_items_lst):
	## extract level (e.g., "02") and text (e.g.,"VISADO EUROPEO") in clear_items_lst
	levels, texts = [], []

	for element in clear_items_lst:
		element = element.strip() # ' LEGISLACION TURISTICA' --> 'LEGISLACION TURISTICA'
		if len(element) == 0:
			## ignore empty strings
			continue
		else:
			## not empty
			## check if a level
			if re.match(r'^[0-9]+$', element):
				levels.append( element )
			else:
				## text
				texts.append( element )
	# return { 'levels': levels, 'texts': texts }
	return (levels, texts)

## to collect objets that we can put in "collect_level_and_text" function 
all_objs = []

## open each .csv file
for csv in csvs:

	## for each csv file, open and read into lines
	fn = os.path.join(path, csv)
	lines = open(fn).read().strip().split('\n') ## strip to avoid empty items

	## process each line in lines
	for line in lines:

		## filter out empty content and collect userful information into a list
		## i.e., get len()>0 and get clear items
		clear_items_lst = filter(lambda x: len(x.strip()), line.split(','))

		level_text_tpl = collect_level_and_text(clear_items_lst)
	  
		all_objs.append( level_text_tpl )

		# print levels, texts
		# print '-'.join(levels), '\t', ','.join(texts)
	
	
''' to convert Spanish text in Chinese and English. '''

gs = goslate.Goslate()
cht = gs.translate('turismo', 'zh')


owl = []

for levels, texts in all_objs:

	##print 'traslating', ','.join(texts)

	zh_TW = map(lambda x: gs.translate(x, 'zh-TW'),texts)
	zh_CN = map(lambda x: gs.translate(x, 'zh-CN'),texts)
	ENG = map(lambda x: gs.translate(x, 'en'),texts)


	new_obj = (levels, texts, zh_TW, zh_CN, ENG)
	
	owl.append( new_obj )

###### if timeout
## 
import pickle

## pickle.dump(owl, open("owl.part1.pkl", "w"))
## old_owl = pickle.load(open("owl.part1.pkl"))
## old_levels = [levels for (levels, texts, zh_TW, zh_CN, ENG) in old_owl]
## old_levels = ['-'.join(levels) for (levels, texts, zh_TW, zh_CN, ENG) in old_owl]

old_owl = pickle.load(open("owl.part1.pkl"))

old_levels = set(['-'.join(levels) for (levels, texts, zh_TW, zh_CN, ENG) in old_owl])

result = []

for levels, texts in all_objs:
	
	if '-'.join(levels) in old_levels:
		print 'skip', '-'.join(levels)
		continue
	else:
		print 'translating', ','.join(texts)

		zh_TW = map(lambda x: gs.translate(x, 'zh-TW'),texts)
		zh_CN = map(lambda x: gs.translate(x, 'zh-CN'),texts)
		ENG = map(lambda x: gs.translate(x, 'en'),texts)


		new_obj = (levels, texts, zh_TW, zh_CN, ENG)
	
		result.append( new_obj )



total_owl = old_owl + result
pickle.dump(total_owl, open("owl.pkl","w"))



'''print a tree to see the structure'''

def print_tree(total_owl, output="mytree.txt"):
	## branch form
	branch = '---'
	## trunk form
	trunk = '|'
	## to save as a txt
	import codecs
	with codecs.open(output, "w", "utf-8") as fw:
		## give it a description of the tree
		for levels, texts, zh_TW, zh_CN, ENG in total_owl:
			## the depth of the value
			depth = len(levels)-1
			## how values will be attached in a line
			line =  trunk + branch*depth + '-'.join(levels) + ','.join(zh_TW) + ','.join(texts).decode("utf-8") +'\n'

			print line
			## write the file
			fw.write(line)
'''clear empty element'''



'''sort element by levels'''

# test = [ ['20', '09', '05', '20'], ['20', '09'], ['20'] ]
def str_to_point(string):

	shift = len(string)-1
	return int(string)/(10.0**shift )

	['20', '04', '03', '23']
	['20', '04']

strig = ''.join(x[0])

sorted_total_owl = sorted( total_owl, key=lambda x: str_to_point( ''.join(x[0]) )  )

for x in total_owl:
	string = ''.join(x[0])
	if not string.startswith('2'): continue
	print string, '-->', str_to_point(string)

print_tree(total_owl)

'''
from .csv file to create a dict -> cn_ts 

02,INFRAESTRUCTURA GENERAL,基礎設施,一般設施,,,,,
-02-01,TRANSPORTE,交通運輸,交通,運輸,,,,
--02-01-01,ARTICULO DE VIAJE,旅遊文章,,,,,,
---02-01-01-01,EQUIPAJE,行李,,,,,,
----02-01-01-01-01,EQUIPAJE DE MANO,手提行李,隨身行李,,,,,
----02-01-01-01-02,EQUIPAJE FACTURADO,托運行李,,,,,,
--02-01-02,CAPACIDAD DE TRANSPORTE,承載力,承載量,,,,,
---02-01-02-01,PASAJERO,乘客,,,,,,
---02-01-02-02,VIAJERO,旅客,遊客,游客,,,,

terms = {"INFRAESTRUCTURA GENERAL":["基礎設施","一般設施"],
"TRANSPORTE":["交通運輸","交通","運輸"],
"ARTICULO DE VIAJE":["旅遊文章"]"
}

level = {"INFRAESTRUCTURA GENERAL": 02, 
"TRANSPORTE": 02-01,
"ARTICULO DE VIAJE": 02-01-01	
}

cn_ts = { 'terms': terms, 'level': level
	
}

print cn_ts['terms'] #  {"INFRAESTRUCTURA GENERAL":["基礎設施","一般設施"],
"TRANSPORTE":["交通運輸","交通","運輸"],
"ARTICULO DE VIAJE":["旅遊文章"]"
}

print cn_ts['terms']['INFRAESTRUCTURA GENERAL'] # ["基礎設施","一般設施"]
'''
import csv
import re 
with open('Documentos/Corpus_CN.csv', mode= 'r') as csvfile:
	data = csv.reader(csvfile)


	level = {}
	terms = {}
	for row in data:
		r = filter(lambda x: x != "",row)
		nb = r[0]
		lv = nb.strip('-')
		tm = r[2:]
		level[lv] = r[1]
		terms[r[1]]= tm

	print terms
cn_thesaurus = {'level': level, 'terms':terms}

## pickle.dump(cn_thesaurus, open("cn_thesaurus.pkl", "w"))

'''
Convert terms dict (utf-8) to a owl_words list (unicode form) :

{'FRONTERA': ['\xe5\x9c\x8b\xe5\xa2\x83', '\xe9\x82\x8a\xe7\x95\x8c'],
 'VIDEOJUEGO': ['\xe9\x9b\xbb\xe7\x8e\xa9\xe9\x81\x8a\xe6\x88\xb2'],
 'DOCUMENTAL': ['\xe7\xb4\x80\xe9\x8c\x84\xe7\x89\x87'],
 'DEPORTES SOBRE RUEDAS': ['\xe8\xbc\xaa\xe4\xb8\x8a\xe9\x81\x8b\xe5\x8b\x95'],
 'UNION ECONOMICA Y MONETARIA': ['\xe7\xb6\x93\xe6\xbf\x9f\xe5\x92\x8c\xe8\xb2\xa8\xe5\xb9\xa3\xe8\x81\xaf\xe7\x9b\x9f'],
 'VACACIONES DE VERANO': ['\xe6\x9a\x91\xe5\x81\x87'],
 'CAFE': ['\xe5\x92\x96\xe5\x95\xa1'],
 'ESCALADA': ['\xe6\x94\x80\xe5\xb2\xa9'],
 'VOLCAN': ['\xe7\x81\xab\xe5\xb1\xb1'],
}

[u'\u7bc9\u57ce',
 u'\u570b\u6703\u57ce\u5e02',
 u'\u65c5\u904a\u540d\u93ae',
 u'\u65c5\u904a\u5340',
 u'\u81ea\u7136\u8cc7\u6e90',
 u'\u6c23\u5019',
 u'\u53f0\u7ad9',
 u'\u51ac\u5b63',
 u'\u79cb\u5b63',
 u'\u6625',
 u'\u590f\u5b63',
 u'\u6c23\u5019\u56e0\u7d20',
 u'\u96e8',
 u'\u96ea',
]

'''
o_v = terms.values()
merged = list(itertools.chain(*o_v))
owl_words_ls = [x.decode('utf-8') for x in merged]
pickle.dump(owl_words_ls,open('Documentos/TDIwordlist.owl.pkl','w'))

