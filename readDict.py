# -*- coding: utf-8 -*-

# import string
# import numpy as np
# import pandas as pd


def readDict(dir):
	import os
	# import unicodedata;
	import codecs
	
	def isLetters(check_str):
		isletters = []
		for ch in check_str:
			isletters.append(ch.isalpha())
				
		return isletters
		
	def isChinese(check_str):
		ischinese = []
		for ch in check_str:
			if u'\u4e00' <= ch <= u'\u9fa5':
				ischinese.append(True)
			else:
				ischinese.append(False)
				
		return ischinese
		
	def parseDict(str):
		import re
		
		def whichIsTrue(bool_list):
			return [idx for idx, value in enumerate(bool_list, 0) if value]
			
		def isType(str):
			return (str in ['n','v','vi','vt','a','ad','adj','adv','num','art','prep','pron','conj','interj',
						   'noun','verb','aux','auxv','u','c','pl','int','abbr'])
		def shortType(str):
			brief = {'n':'n','v':'v','vi':'v','vt':'v','a':'a','ad':'a','adj':'adj','adv':'adv','num':'num','art':'art','prep':'prep','pron':'pron','conj':'conj','interj':'interj','noun':'n','verb':'v','aux':'auxv','auxv':'auxv','u':'n','c':'n','pl':'n','int':'interj','abbr':'abbr'}
			return brief[str]
		def isTypeConnector(str):
			return((str == '/') or (str == '\\'))
		def isValidChnMeaning(str):
			return((len(str)>0) and	# meaning is not empty
				   (sum(isChinese(str))>0) and	# meaning is not synonym nor meaningless symbols
				   (not(isTypeConnector(str)))	  and	# not a double type
				   (not(str in ['亦作','也作','亦做','也做','过去式','过去分词']))	# meaning is not synonym
				  )
				  
		
		# clean str first
		temp = str.split(' ')
		spell = temp[0]
		
		if len(temp)>1 and temp[1][0] == '[' and temp[1][-1] == ']':	#if temp[1] is phonogram
			temp = temp[1:]
		
		temp = ';'.join(temp[1:])
		temp = re.sub('；|,|，|\.|。|\r|\n',';',temp)	# replace other sep's
		# split joining types
		tempIsLetters = isLetters(temp)
		for i in list(range(len(temp)))[:0:-1]:
			if tempIsLetters[i] ^ tempIsLetters[i-1]:
				temp = temp[:i-1] + ';' + temp[i-1:]
				
		temp,num = re.subn(';+',';',temp)
		temp = temp.split(';')
		
		mean = []
		t=[]
		this_t_mean = []
		hasTypeConnector = False
		for m in temp:
			if isType(m):
				m = shortType(m)
				if hasTypeConnector:	# multiple types (v.&n.)
					t.append(m)
					hasTypeConnector = False
				elif (len(this_t_mean)>0):	# new type (xxx;n.ooo)
				# if (t!='') or (len(this_t_mean)>0):
					mean.extend([ [_t,this_t_mean] for _t in t ])
					t=[m]
					this_t_mean = []
				else:	#first type (^n.xxx)
					t=[m]
			elif (isValidChnMeaning(m)):
				this_t_mean.append(m)
			elif (isTypeConnector(m)):
				hasTypeConnector = True
		if(len(this_t_mean)>0):		
			if(len(t)==0):
				mean.append(['',this_t_mean])
			else:
				mean.extend([ [_t,this_t_mean] for _t in t ])
		
		if len(mean) > 0:
			return({'spell':spell, 'mean':mean})
		else:
			return({'spell':' ', 'mean':' '})
	def stripDict(Dict):
		def eliminateDuplicatedMean(word):
			# merge empty-type meanings
			def eliminateEmptyTypes(empty_type,means_w):
				for mean_w in means_w:
					for et in empty_type[1]:
						if et in mean_w[1]:
							empty_type[1].remove(et)
			for mean_w in word['mean']:
				if mean_w[0] == '':
					empty_type = mean_w
					word['mean'].remove(empty_type)
					eliminateEmptyTypes(empty_type,word['mean'])
					# append unmatched meanings
					if(len(empty_type[1])>0):
						word['mean'].append(empty_type)
			return(word)
			
		def mergeWord(w1,w2):
			# merge meanings
			for mean_w1 in w1['mean']:
				for mean_w2 in w2['mean']:
					if mean_w1[0] == mean_w2[0]:
						mean_w1[1] = list(set(mean_w1[1] + mean_w2[1]))
						w2['mean'].remove(mean_w2)
			
			w1['mean'] +=   w2['mean']
			
			return eliminateDuplicatedMean(w1)
		
		print('stripping...')
		Dict = sorted(Dict, key=lambda word : word['spell'])
		newDict = [Dict[0]];
		for word in Dict[1:]:
			if word['spell']==newDict[-1]['spell']:
				newDict[-1] = mergeWord(word,newDict[-1])
			else:
				newDict.append(eliminateDuplicatedMean(word))
		return newDict
	
	
	print('read in dictionary...')
	dictFiles = os.listdir(dir)
	Dict = []
	for file in dictFiles:
		fh = codecs.open(dir + '/' + file, 'r', encoding='utf-8')
		print(file)
		for line in fh.readlines(): 
			Dict.append(parseDict(line))
		# print()
	Dict = filter(lambda word : sum(isLetters(word['spell'])) == len(word['spell']),Dict)
	return stripDict(Dict)

def printDict(Dict,num=47,type='',file = ''):
	import sys
	
	if(not file):
		file = sys.stdout
	
	def printWord(word):
		print(word['spell'], end='', file=file)
		for m in word['mean']:
			print('\t%s.%s' %(m[0],','.join(m[1])), end='\n', file=file)
		# print(file=file)

		if type!='nosynonym':
			printSynonym(word)
		
	def printSynonym(word):	
		print('\t%s'
				%(',\n\t'.join(['%s:%.3f'%(s,word['synonym'][s]) 
								for s in word['synonym'] ])
				 ),
			 file=file
			 )
	
	count=0
	if type=='all':
		count = len(list(Dict.keys()))
	if(isinstance(Dict,list)):
		for word in Dict:
			printWord(word)
			count += 1
			if count == num:
				break
	if(isinstance(Dict,list)):
		for word in Dict:
			printWord(word)
			count += 1
			if count == num:
				break
	elif(isinstance(Dict,dict)):
		if 'mean' in Dict.keys():	# if Dict is one word
			printWord(Dict)
		else:
			for word in Dict:
				printWord(Dict[word])
				count += 1
				if count == num:
					break

def printDictToJSON(Dict,radius=5):
	# http://www.cnblogs.com/coser/archive/2011/12/14/2287739.html
	# http://liuzhijun.iteye.com/blog/1859857
	def getSubDict(Dict,radius):
		subDict = {}
		wordList = list(Dict.keys())[0]
		count = 0
		for word in Dict:
			addNode(word)
			count += 1
			if count == radius:
				break
		return(subDict)
	
	def transformToJSON(word):
		# "nodes":[
		# {"name":"Mme.Hucheloup","group":8}
		# ],
		# "links":[
		# {"source":1,"target":0,"value":1}
		# ]
		JSONDict = {'nodes':[],'links':[]}
		JSONDict['nodes'].append({'name':word,'group':count+1})
		JSONDict['nodes'].extend({'name':word,'group':count+1})
		JSONDict['links'].extend({"source":1,"target":0,"value":1},)
	
	import json
	
	subDict = getSubDict(Dict,radius)
	printDict(subDict)
	encodedjson = json.dumps(subDict)
	print(repr(subDict))
	print(encodedjson)

def splitWord(strList, maxLen = 10, minCohension = 10, minEntropy = 1):
	'''find co-occurrent chars in string'''
	def isWord(comb):
		key = comb
		comb = combStatistics[key]
		
		if (comb['left']  < minEntropy	or
			comb['right'] < minEntropy):	# independence
				return False
		for sp in range(1,len(key)):
			if (combStatistics[key[:sp]]['freq'] * 
				combStatistics[key[sp:]]['freq'] * 
				minCohension  > comb['freq']	# cohesiveness
				):
				return False
		return True
		
	# def eliminatePrefix(rootList):
		# rootList = sorted(rootList)
		# return([rootList[i-1] 
					# for i in list(range(1,len(rootList))) 
						# if rootList[i-1] not in rootList[i]
				# ])
	# def eliminateSurfix(rootList):
		# rootList = [word[::-1] for word in rootList]
		# rootList = sorted(rootList)
		# rootList = eliminatePrefix(rootList)	# eliminate surfix
		# rootList = [word[::-1] for word in rootList]
		# return(rootList)
	# def eliminateFixes(rootList):
		# rootList = eliminatePrefix(rootList)
		# rootList = eliminateSurfix(rootList)
		# return(sorted(rootList))
	
	def caculateEntropy(combStatistics,side):	#~,~,which side of entropy to calculate: left,right
		rootList = [comb for comb in combStatistics]
		if side == 'left':
			rootList = [word[::-1] for word in rootList]
		
		rootList = sorted(rootList, key = lambda x : (len(x),x))
		i=0
		j=0
		# count side diversity
		while(j<len(rootList)):
			# (*j)[:-1] = (*i) , (*i) is the prefix of (*j)
			if len(rootList[i]) + 1 < len(rootList[j]):
				i+=1
			elif (len(rootList[i]) + 1) > len(rootList[j]):
				j+=1
			else:
				if rootList[i] == rootList[j][:-1]:
					if side == 'right':
						combStatistics[rootList[i]]['right'].append(
						combStatistics[rootList[j]]['freq'])
					else:
						combStatistics[rootList[i][::-1]]['left'].append(
						combStatistics[rootList[j][::-1]]['freq'])
					
				elif rootList[i] < rootList[j][:-1]:
					i+=1				
				j+=1
		
		# calculate entropy
		import math
		for comb in combStatistics:
			combStatistics[comb][side].extend([1]*
					(combStatistics[comb]['freq'] - sum(combStatistics[comb][side]))
					)	# ending edge is regarded as independent neighbor for it is a strong sign for boundary
			combStatistics[comb][side] = list(map(lambda x,y : x/y, combStatistics[comb][side], [sum(combStatistics[comb][side])]*len(combStatistics[comb][side])))
			combStatistics[comb][side] = - sum(list(map(lambda x : math.log(x)*x, combStatistics[comb][side])))
			
		
		return(combStatistics)
		
	statistic = lambda wordSet:{ch: {'len': len(ch), 'freq': temp.count(ch), 'left': [], 'right': []}  for ch in wordSet}
	
	print('split word...')
	# statistic frequency
	print('\tstatistic frequency:',end='')
	temp = '\n'.join(strList)
	combStatistics = {}
	for wordLen in range(1,maxLen):
		print('%d'%wordLen,end='...')
		combStatistics.update(
					   statistic(
							set([temp[i:i+wordLen] 
								for i in list(range(len(temp)-wordLen))
								])
							)
					   )
		
	# combStatistics = list(filter(lambda comb: '\n' not in comb , combStatistics))
	combStatistics = {comb:combStatistics[comb] for comb in combStatistics if '\n' not in comb}
	print('\n\t%d protiencial words found'%(len(combStatistics)))	
	
	# transform frequency to rate
	print('\tstatistic entropy...')
	combStatistics = caculateEntropy(combStatistics,'right')
	combStatistics = caculateEntropy(combStatistics,'left')
	
	# transform frequency to rate
	lenStat = [0]
	lenStat.extend(
				[sum(combStatistics[comb]['freq'] for comb in combStatistics  if combStatistics[comb]['len'] == l)
					for l in range(1,maxLen)]
				)	
	for comb in combStatistics:
		combStatistics[comb]['freq']/=lenStat[combStatistics[comb]['len']]
	
	# combStatistics = {comb['comb'] : comb['freq'] for comb in combStatistics}
	
	
	rootList = []
	for comb in combStatistics:
		if(len(comb) > 1 and isWord(comb)):
			# rootList.update({comb:combStatistics[comb]})
			rootList.append(comb)
			
	fp = open('wordStat.txt','w')
	for comb in combStatistics:
		print('%s\t%f\t%d\t%f\t%f'%(comb,combStatistics[comb]['freq'],
						  combStatistics[comb]['len'],
						  combStatistics[comb]['left'],
						  combStatistics[comb]['right'],),file=fp)
	fp.close()
	
	return(rootList)
	
def splitSyllable(wordList):
	# '''split syllable with word-splitting tricks failed'''
	'''split syllable with roots and fixes'''
	import re
	vowel = '[aeiou]'
	semivowel = '[y]'
	consonant = '[bcdefghjklmnpqrstvwxyz]'
	
	wordList = sorted(wordList, key = lambda x : (len(x),x))
	
	wordList = '$;^'.join(wordList)
	wordList = '^' + wordList + '$'
	wordList = wordList.split(';')
	
	re.match('^' + consonant + vowel + '{1,2}' + consonant + '{1,2}','hammy').group()
	
	
	prefix = [comb for comb in comblist if ('^' in comb) and ('$' not in comb)]
	prefix = [pre[ 1:] for pre in prefix]
	suffix = [comb for comb in comblist if ('$' in comb) and ('^' not in comb)]
	suffix = [suf[:-1] for suf in suffix]
	root = [comb for comb in comblist if ('^' not in comb) and ('$' not in comb)]
	

def isVowel(ch):
	return ch in ['a','e','i','o','u']
	
def isSemiVowel(ch):
	return ch in ['v','y']

def generateSynonym(Dict):
	'''generate synonym by Chinese meaning'''
	 
	def numberOfMeans(mean):
		meanList = []
		for m in mean:
			meanList.extend(m[1])
		meanList = list(set(meanList))
		return(len(meanList))
	print('generating synonyms...')
	
	# preprocessing Dict to extracting core meanings
	import re
	print('\textracting core meanings...')
	fix = re.compile(r'^似|似得$|似的|的$|地$|得$|\(...\)|\（...\）|\[...\]|\【...\】')
	DictCopy = Dict.copy()
	for word in DictCopy:
		for mean in word['mean']:
			for i in range(len(mean[1])):
				# eliminate fixes to get core meanings
				num = 1
				while(num>0):
					mean[1][i],num = fix.subn('',mean[1][i])
				
	# indexing via Chinese meanings
	print('\tindexing via Chinese meanings...')
	ChEnDict = {}
	for word in DictCopy:
		for mean in word['mean']:
			for m in mean[1]:
				if m in ChEnDict:
					ChEnDict[m].append(word['spell'])
				else:
					ChEnDict[m] = [word['spell']]
	
	# restructuralize Dict
	print('\trestructuralizing Dict...')
	newDict = {}
	for word in Dict:
		newDict[word['spell']] = word.copy()
		newDict[word['spell']]['synonym']=[]
	
	
	# write synonyms into Dict
	print('\twriting synonyms into Dict...')
	for mean in ChEnDict:
		for word in ChEnDict[mean]:
			newDict[word]['synonym'].extend(ChEnDict[mean])

	# calculate closeness for synonyms
	print('\tcalculatingcloseness for synonyms...')
	for word in newDict:
		synonyms = newDict[word]['synonym']
		try:
			newDict[word]['synonym'] = {sy:synonyms.count(sy)/
										# (len(newDict[word]['synonym']) - synonyms.count(newDict[word]['spell']))	# count / sum(count), sum(count) = sum(syn) - mean
										(numberOfMeans(newDict[word]['mean']))	# count / mean
											for sy in list(set(synonyms))}
			del newDict[word]['synonym'][newDict[word]['spell']]
		except ZeroDivisionError:
			newDict[word]['synonym'] = {}
		
	# restructure dict to list	
	return list(map(lambda word : newDict[word], newDict)),ChEnDict
	