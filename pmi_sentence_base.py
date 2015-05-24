# -*- coding: utf-8 -*-
import pymongo
from pymongo import MongoClient
from collections import Counter
import pickle
import os
import logging


class WordUtils(object):
	"""
	Utilities for word operations such as co-occurrence and Mutural Information
	"""
	def __init__(self, **kwargs):

		loglevel = logging.DEBUG if 'verbose' in kwargs and kwargs['verbose'] == True else logging.INFO
		logging.basicConfig(format='[%(levelname)s] %(message)s', level=loglevel)  

		## base: could be post-based or sentence-based
		self.based = 'post' if 'based' not in kwargs else kwargs['based']

		self.AllPairs = {}
		self.PMI = {}

	def build_dist(self, path, **kwargs):
		"""
		build(+save)/load word distribution

		Parameters
		==========
		path: str
			path to the all-pairs, which contains the mapping of { post-id : pairs }
			where `pairs` are the list of ( word, Pos-tag ) tuples

		options:

			mongo_addr: str
			mongo_db:   str
			mongo_cos:  list
			override:   True/False
		"""

		## mongodb
		mongo_addr = 'doraemon.iis.sinica.edu.tw' if 'mongo_addr' not in kwargs else kwargs['mongo_addr']
		mongo_db = 'espanol' if 'mongo_db' not in kwargs else kwargs['mongo_db']

				## support multiple target collections
		mongo_cos = ['bk.posts', 'qy.posts']
		## mongo_cos = ['bk.posts'] if 'mongo_cos' not in kwargs else kwargs['mongo_cos']

		override = False if 'override' not in kwargs else kwargs['override']

		## check if self.AllPairs exists
		if self.AllPairs and not override:
			logging.info('AllPairs already exists')
			return False

		if os.path.exists(path) and not override:
			logging.info('Load AllPairs from %s' % (path))
			self.AllPairs = pickle.load(open(path))
			return True

		### fetch data from mongodb
		self.AllPairs = {}
		client = MongoClient(mongo_addr)
		self.db = client[mongo_db]
		
		for mongo_co in mongo_cos:

			self.co = self.db[mongo_co]
			logging.info('Collect posts from %s' % (self.co.full_name))

			total = self.co.count()
			for i, mdoc in enumerate(self.co.find()):
				if 'parsed' not in mdoc or len(mdoc['parsed']) == 0:
					logging.debug('> skip %d/%d mongo doc' % (i+1, total))
					continue
				
				logging.debug('> process %d/%d mongo doc' % (i+1, total))
				## "_id" : ObjectId("5406a2aa3480ad1b9b828c52"),
				## post_id will be "5406a2aa3480ad1b9b828c52"
				post_id = str(mdoc['_id'])

				for i, parsed_sent in enumerate(mdoc['parsed']):
					## parsed_sent
					# '\u7684(DE)\u3000\u591c\u666f(Na)\u3000\u4e0d\u932f(VH)'
 
					## init pairs
					pairs = Counter()
 
					spliited = parsed_sent.strip().split(u'　')
					## spliited:
					# [u'\u7684(DE)',
					#  u'\u591c\u666f(Na)'
					#  u'\u4e0d\u932f(VH)'] 
 
					for word_pos in spliited:
						token = '('.join(word_pos.split('(')[:-1])
						postag = word_pos.split('(')[-1].split(')')[0]
						## token: \u591c\u666f --> 夜景
						## token: Na
						pairs[ (token,postag) ] += 1
 
 
					 ## collect AllPairs in sentence level
					sent_id = post_id+"_"+str(i)
					self.AllPairs[sent_id] = pairs


			logging.info('dumping AllPairs into %s' % (path))
			pickle.dump(self.AllPairs, open(path, 'wb'), protocol=2)
			return True

	def build_cooccurrence(self, tag='N', targetList='resources/wordlist.owl.pkl', output=None, order=False, case=False, threshold=5):
		"""
		calculate post-based, order-nonsenitive co-occurrence

		Parameters
		==========
		AllPairs: Counter
			{ post-id : occurrence distribution }

		tag: str
			filter out the word with the specified part-of-speech tag
		
		targetList: str
			path to the list that contains anchor words
			in this project, the targetList is the list of words appearing in the OWL ontology

		order: True/False
			consider ordering or not
			e.g., if this is set `True`, ("travel", "spain") and ("spain", "travel") are the different word pairs
		"""

		## load target word list
		logging.debug('load targetList from %s' % (targetList))
		wlist = set(pickle.load(open(targetList)))

		## occurrence of words (post-based)
		self.Occur = Counter()
		## co-occurrence of words (post-based)
		self.Cooccur = Counter()

		logging.info('calculate occurrence and co-occurrence')
		## post-based
		for pid in self.AllPairs:

			dist = self.AllPairs[pid]

			## filter out words
			words = set([w for w,p in dist.keys() if p.startswith(tag)])

			## intersection with ontology words
			inter = [w for w in words if w in wlist]

			## pairwise <inter-words>
			pairs = [ (m,n) for m in inter for n in words if m != n]

			## update co-occurrence
			for pair in pairs:

				pair = map(lambda x:x.lower(), pair) if not case else pair

				key = tuple(sorted(pair)) if not order else pair
				
				self.Cooccur[ key ] += 1

			## update occurrence
			for word in words:
				word = word.lower() if not case else word
				self.Occur[ word ] += 1

		## pruning
		OccurPrune = Counter()
		for w in self.Occur:
			OccurPrune[w] = self.Occur[w]
		self.Occur = OccurPrune

		CooccurPrune = Counter()
		#######################################
		for key, val in self.Cooccur.items():
			if val > threshold:
				CooccurPrune[key] = val
		#######################################
		self.Cooccur = CooccurPrune

		if output:
			ocDict = {
				'occur': self.Occur,
				'cooccur': self.Cooccur
			}
			## output could be `bk.cooccur.pkl`
			## add threshold infomation: `bk.cooccur.5.pkl`
			# if threshold:
				# output = output.replace('.pkl', '.'+str(threshold)+'.pkl')

			logging.info('save co/occurrence to %s' % (output))
			pickle.dump(ocDict, open(output, 'w'))

	def build_PMI(self, path):
		"""
		pmi(x,y) = log( p(x,y)/p(x)p(y) ) 
			where p(x), p(y) are the probability of the word x and y respectively
			and p(x,y) is the probability of the pair (x,y)
		"""
		if os.path.exists(path):
			logging.info('loading PMI from %s' % (path))
			self.PMI = pickle.load(open(path))
			return True

		from math import log
		num_of_post = float(len(self.AllPairs))

		logging.info('calculate PMI of each pair')
		self.PMI = {}
		for pair, count in self.Cooccur.iteritems():
			
			x, y = pair

			f_x, f_y = self.Occur[x], self.Occur[y]
			p_x, p_y = f_x/num_of_post, f_y/num_of_post

			f_x_y = count
			p_x_y = count/num_of_post

			pmi_x_y = log( p_x_y/(p_x*p_y) )

			self.PMI[(x,y)] = pmi_x_y

		logging.info('dumping PMI into %s' % (path))
		pickle.dump(self.PMI, open(path, 'wb'), protocol=2)

	def get_PMI(self, w1, w2, path=None, case=False, order=False):

		## check self.PMI and path
		if not self.PMI and not path:
			logging.error("cannot find PMI data, run `build_PMI(path='...')` first")
			return False
		elif not self.PMI and path:
			if not os.path.exists(path):
				logging.error("the path (%s) to PMI pkl does not exist" % (path))
				return False
			else:
				self.PMI = pickle.load(open(path))
		else:
			pass

		## build pair from w1, w2
		pair = [w1, w2] if not case else [w1.lower(), w2.lower()]
		pair = tuple(sorted(pair)) if not order else tuple(pair)
		pair = tuple(pair)

		## fetch PMI of w1, w2
		if pair in self.PMI:
			return self.PMI[pair]
		else:
			print "can't find the pair", w1, w2, "in PMI data"
			return 0.0

def usage():

	module = __file__.replace('.py','')
	print """
	Usage Examples of %s
	==================%s

	>> from WordUtils import WordUtils

	>> wu = WordUtils(verbose=True)

	## To build PMI of certain data:

		>> wu.build_dist(path="resources/all-pairs.pkl")

		or specify the mongo address, collections and override it
		and finally save AllPairs in `resources/new.data.pairs.pkl`
		>> wu.build_dist(path="resources/new.data.pairs.pkl", mongo_addr="your.own.mongo", mongo_cos=["bk.posts", "qy.posts"], override=True)

		>> wu.build_cooccurrence()

		or dump the co-occurrence/occurrence data
		by specifying the destination path
		>> wu.build_cooccurrence(output="resources/bk.cooccur.pkl")                 ## will dump to resources/bk.cooccur.pkl 
		>> wu.build_cooccurrence(output="resources/bk.cooccur.5.pkl", threshold=5)    ## will dump to resources/bk.cooccur.5.pkl 

		>> wu.build_PMI(path="resources/bk-owl.pmi.pkl")

		or specify a new path for storing PMI data 
		>> wu.build_PMI(path="resources/bk-qy-owl.pmi.pkl")

	## To find the PMI of certain word pair

		>> wu.get_PMI(w1, w2)
	""" % (module, '='*len(module))

if __name__ == '__main__':
	
	usage()
