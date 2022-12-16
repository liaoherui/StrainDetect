import re
import os

f=open('head_file.txt','r')
o=open('head_file_new.txt','w+')
#line=f.readline().strip()
#o.write(line+'\n')
while True:
	line=f.readline().strip()
	if not line:break
	ele=line.split('\t')
	ele[-1]='GISAID:'+ele[-1]
	o.write('\t'.join(ele)+'\n')
