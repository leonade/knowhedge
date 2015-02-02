# -*- coding: utf-8 -*-
## split xml file into small files by <page></page>
## note: <siteinfo> and its children tabs are deleted
## created on Feb 1, 2015 by Li
## last modified Feb 1, 2015 by Li
import codecs
# import sys
# from __future__ import print_function

def wiki_split(xml_file_name,size = 200000):
	with open(fname) as f:
		nfiles = sum(1 for _ in f)
	nfiles = nfiles/size + 1
	
	fwiki = codecs.open(fname, 'r', encoding='utf-8')	
	line = ''
	while ('<page>' not in line):
		line = fwiki.readline()
		# print(line)
	nfile = 1
	while(line != ''):
		temp = line
		for nline in range(size):
			temp += fwiki.readline()
		while ('</page>' not in line):
			line = fwiki.readline()
			temp += line
			
			# if reach eof
			if(line == ''):
				lines = temp.split('\n')
				n=-1
				while ('</page>' not in lines[n]):
					n-=1
				temp = '\n'.join(lines[:(n+1)])
				break
		
		print(str(nfile) + '/' + str(nfiles))
		
		# save file
		# temp = temp.decode('utf-8', errors='ignore').encode('utf-8')
		temp = '<mediawiki>' + temp + '</mediawiki>'
		temp = temp.encode('utf-8', errors='ignore')
		temp = temp.replace("–", "-")
		temp = temp.replace('&',"&amp;")
		with codecs.open('WikiFiles/' + fname[:-4] + '_' + str(nfile) + '.xml', 'w+', encoding='utf-8') as fw:
			# UTF8Writer = codecs.getwriter('utf8')
			# fw = UTF8Writer(fw)
			fw.write(temp.decode('utf-8'))
			# print >>fw, temp
			nfile += 1
			line = fwiki.readline()

if __name__ == '__main__':
	# fname = 'enwiki-minidemo.xml'
	# fname = "enwiki-demo.xml"
	fname = "enwiki-20141208-pages-articles1.xml"

	wiki_split(fname)
	
