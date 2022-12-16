import re
import os

def reorder(raw_file,tfile,ofile1,ofile2):
	f=open(raw_file,'r')
	d={}
	while True:
		line=f.readline().strip()
		if not line:break
		ele=line.split('\t')
		d[ele[0]]=line
	o1=open(ofile1,'w+')
	o2=open(ofile2,'w+')
	f2=open(tfile,'r')
	c=1
	while True:
		line=f2.readline().strip()
		if not line:break
		ele=line.split()
		o1.write('>'+str(c)+'\n'+ele[0]+'\n')
		o2.write(d[ele[0]]+'\n')
		c+=1


reorder('Pos-snp-kmer-all.txt','/mnt/d/My_Research/Bio_DB_Prj/NAR_web_server_try/KMC_db/KMC_build_db_bash/H1N1.txt','Pos-snp-kmer-all-new.fa','Pos-snp-kmer-all-new.txt')
os.system(' mv Pos-snp-kmer-all.txt Pos-snp-kmer-all-raw.txt')
os.system(' mv Pos-snp-kmer-all.fa Pos-snp-kmer-all-raw.fa')
os.system(' mv Pos-snp-kmer-all-new.txt Pos-snp-kmer-all.txt')
os.system(' mv Pos-snp-kmer-all-new.fa Pos-snp-kmer-all.fa')

reorder('SubCls_kmer.txt','/mnt/d/My_Research/Bio_DB_Prj/NAR_web_server_try/KMC_db/KMC_build_db_bash/H1N1_sub.txt','SubCls_kmer_new.fa','SubCls_kmer_new.txt')

os.system(' mv SubCls_kmer.txt SubCls_kmer-raw.txt')
os.system(' mv SubCls_kmer.fa SubCls_kmer-raw.fa')
os.system(' mv SubCls_kmer_new.txt SubCls_kmer.txt')
os.system(' mv SubCls_kmer_new.fa SubCls_kmer.fa')
