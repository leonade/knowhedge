# -*- coding: utf-8 -*-
## transform wiki dump into plain text, using Wiki2Plain.py
## created on Feb 1, 2015 by Li
## last modified Feb 1, 2015 by Li
import os
import codecs
os.chdir('D:/Program Files/Projects/Knowhedge/Wiki')	# Li PC
from Wiki2Plain import Wiki2Plain
import xml.etree.ElementTree as ET
# from xml.dom.minidom import parseString
# from xml.parsers.expat import ExpatError


def read_xml(fname):
	fwiki = codecs.open(fname, 'r', encoding='utf-8')
	xml_file = fwiki.readlines()
	# xml_file[0] = u'<mediawiki>\n'
	xml_file = '\n'.join(xml_file)

	# parser = ET.XMLParser(encoding="utf-8")
	tree = ET.fromstring(xml_file.encode('UTF-8'))
	# tree = parseString(xml_file)

	text = tree.findall("page/revision/text")
	# .encode('utf-8', errors='ignore')
	text = [t.text for t in text]
	text = [t for t in text if not t.startswith("#REDIRECT")]
	text = [Wiki2Plain(t).text for t in text]
	return text


if __name__ == '__main__':
	# fname = 'enwiki-minidemo.xml'
	fnames = os.listdir('D:/Program Files/Projects/Knowhedge/Wiki/WikiFiles')
	# fname = "enwiki-20141208-pages-articles1.xml"
	
	for f in fnames:
		text = read_xml('WikiFiles/'+f)
		with codecs.open('WikiPages/' + f[:-4] + '.txt', 'w+', encoding='utf-8') as fw:
			fw.write('\n\n\n\n'.join(text))

# def get_char(line,col,l=5):
	# x = xml_file.split("\n")[line-1]
	# print(x[col-l:col+l+1])
	# return x[col-l:col+l+1]

# get_char(286,4086)
# get_char(286,4086,0)
