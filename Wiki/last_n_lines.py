# -*- coding: utf-8 -*-
## desplay last n lines of file
## used for creating menwiki-demo.xml
## the end of xml is </text>\n<sha1>31x3gg6qhy7oxv090i7ki97r6dzglpv</sha1>\n</revision>\n</page>\n</mediawiki>
## created on Feb 1, 2015 by Li
## last modified Feb 1, 2015 by Li

import os, codecs
os.chdir('D:/Program Files/Projects/Knowhedge/Wiki')	# Li PC
n_lines = 200
fname = "enwiki-20141208-pages-articles1.xml"

def tail( f, lines=20 ):
    total_lines_wanted = lines
    
    BLOCK_SIZE = 1024
    f.seek(0, 2)
    block_end_byte = f.tell()
    lines_to_go = total_lines_wanted
    block_number = -1
    blocks = [] # blocks of size BLOCK_SIZE, in reverse order starting
                # from the end of the file
    while lines_to_go > 0 and block_end_byte > 0:
        if (block_end_byte - BLOCK_SIZE > 0):
            # read the last block we haven't yet read
            f.seek(block_number*BLOCK_SIZE, 2)
            blocks.append(f.read(BLOCK_SIZE))
        else:
            # file too small, start from begining
            f.seek(0,0)
            # only read what was not read
            blocks.append(f.read(block_end_byte))
        lines_found = blocks[-1].count('\n')
        lines_to_go -= lines_found
        block_end_byte -= BLOCK_SIZE
        block_number -= 1
    all_read_text = ''.join(reversed(blocks))
    return '\n'.join(all_read_text.splitlines()[-total_lines_wanted:])

rf = codecs.open(fname, 'r', encoding='utf-8')
with open("a.txt","w+") as wf:
	print (tail(rf, lines=n_lines), file=wf)
