import re
import os
import sys
import numpy as np
import scipy.sparse as sp
from sklearn.model_selection import ShuffleSplit
from sklearn.linear_model import Lasso, LassoCV
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold

def lasso_mpm(alphas,mse_path):
	mse_mean = np.mean(mse_path, axis=1)
	mse_std = np.std(mse_path, axis=1)
	mse_min_idx = np.argmin(mse_mean)
	mse_min = mse_mean[mse_min_idx]
	mse_min_std = mse_std[mse_min_idx]
	mse_min_std_min = mse_min - mse_min_std
	mse_min_std_max = mse_min + mse_min_std
	mse_mpm_idx = mse_min_idx
	for i in range(mse_min_idx-1, -1, -1):
		if (mse_mean[i]>=mse_min_std_min) and (mse_mean[i]<=mse_min_std_max):
			mse_mpm_idx = i
	alpha_mpm = alphas[mse_mpm_idx]
	mse_mean_mpm = mse_mean[mse_mpm_idx]
	mse_std_mpm = mse_std[mse_mpm_idx]
	return alpha_mpm, mse_mean_mpm, mse_std_mpm

def detect(npz_1,npz_2,db_name):
	ref_dict={'SCOV2':'>CHN/Wuhan_IME-WH04/2019','HIV':'>B.FR.83.HXB2_LAI_IIIB_BRU.K03455','H1N1':'>A/California/7/2009','Ebola':'>18FHV089','Dengue':'>New_Guinea_C_derivative','Zika':'>THA/PLCal_ZV/2013','Entero':'>CAN97-947','HBV':'>KM524350.1'}
	abs_file=__file__
	abs_dir=abs_file[:abs_file.rfind("/")]
	db_dir=abs_dir+'/DB/'+db_name

	k=25		# Default k size=25
	min_depth_percentile=10
	max_depth_percentile=90
	min_depth_absolute=2
	min_depth_rate=0.05
	snp_kmr_file=db_dir+'/Pos-snp-kmer-all.txt'
	matrix_file=db_dir+'/Strain_pos_snp_matrix_not_redundant_MM_Call.txt'
	snp_kmr_fa=db_dir+'/Pos-snp-kmer-all.fa'
	cls_file=db_dir+'/Strain_cls_info.txt'
	sub_kmr_file=db_dir+'/SubCls_kmer.txt'

	## Static variables
	BASE_ORDER=['A','T','G','C']
	BASE_P = {'A': [1, 0, 0, 0],'C':[0,1,0,0],'G':[0,0,1,0],'T':[0,0,0,1],}
	file_dir=sys.path[0]

	cls_arr=sp.load_npz(npz_1)
	cls_arr=cls_arr.A[0]


	######### Step-1 Load Pre-build File to memory ####
	## Kmer -> POS-SNP
	f1=open(snp_kmr_file,'r')
	dkps={}  # kmr -> {pos-snp:1,......}
	id2kmr={} # ID -> kmr
	pos=[]
	dpsc={} # pos-snp:  num
	c=0
	while True:
		line=f1.readline().strip()
		if not line:break
		ele=line.split('\t')
		dkps[ele[0]]=''
		id2kmr[c]=ele[0]
		c+=1
		ps=re.split(',',ele[1])
		for e in ps:
			dkps[ele[0]]=e # Set to 1 for Counter -> Dict Merge
			dpsc[e]=0

	## Build pos-snp freq array

	f3=open(matrix_file,'r')
	fl=f3.readline().strip()
	pos_snp=re.split('\t',fl) # Head line arr
	#print(np.where(np.array(pos_snp)=='8946-T')[0][0])

	# Run jellyfish to get kmer counting result
	
	c=0
	for kf in cls_arr:
		#if c not in id2kmr:continue
		dpsc[dkps[id2kmr[c]]]+=int(kf)
		c+=1

	freq_arr=[]
	carr=[]
	for p in pos_snp:
		c=re.split('-',p)[0]
		if c not in carr:
			carr.append(c)
		if p not in dpsc:
			freq_arr.append(0)
		else:
			freq_arr.append(dpsc[p])

	freq_arr=np.array(freq_arr)


	### Check avg depth from the pos-snp frequency array
	keep=(freq_arr!=0)
	check_arr=freq_arr[keep]
	if len(check_arr)==0:
		print('No kmers matched! No virus strain can be detected!')
		exit()
	min_depth,max_depth=np.percentile(check_arr,[min_depth_percentile,max_depth_percentile])
	keep=np.logical_and.reduce((check_arr>=min_depth,check_arr<=max_depth))
	check_arr2=check_arr[keep]
	# Average depth of the frequency vector
	min_depth_adf=min_depth_rate*np.mean(check_arr2)
	##### !! freq arr filter using 2 or 0.1*avg-depth

	if min_depth_adf<2:
		min_depth_adf=2 # Use 2 to test firstly
	freq_arr[freq_arr<=min_depth_adf]=0
	weighted_freq_arr=freq_arr/np.sum(freq_arr)

	##### Filter done. ########


	pos_freq_map=dict(zip(pos_snp,freq_arr))
	raw_freq_arr=freq_arr
	t=np.array(pos_snp)

	ds_pos={}  # Strain -> 0 1 1 0 0 1 (pos-snp: yes or no vector)
	ds_freq={} # Strain -> frequency vector of this strain
	dmap_rate={} # Strain -> pos-snp map scpre of this strain
	ds_num={} # Strain -> pos-snp map number, raw number
	dmr={}  # Strain -> pos-snp map rate os this strain (map_number/raw_number)
	#These 2 dict will be used to visualize the pos depth figure
	#dscf={} #Strain-> 110-A:110, 111-NA:0, ..
	#dscl={} # Strain-> 110-A:3000, 111-NA:0, ..
	# This dict is used to build the diff snp
	ref_one=ref_dict[db_name]
	ds_ref={} # 574->G,592->C, currently, we set ref as MT745584
	all_ps=[] # Record the matrix array
	count=-1
	while True:
		line=f3.readline().strip()
		if not line:break
		ele=line.split('\t')
		tem=[]
		if ele[0]==ref_one:
			count=0
		else:
			count=-1
		for e in ele[1:]:
			tem.append(int(e))
			if count>=0:
				if int(e)==1:
					snp=re.split('-',pos_snp[count])
					ds_ref[int(snp[0])]=snp[1]
				count+=1
		tem=np.array(tem)
		all_ps.append(tem)
		#dscf[ele[0]]={}
		#dscl[ele[0]]={}
	
		nt=freq_arr*tem # the frequency vector of this strain
		raw_c=len(tem[tem==1])
		map_c=len(nt[nt>0])
		map_rate=np.sum(tem*weighted_freq_arr)
		dmap_rate[ele[0]]=map_rate
		ds_num[ele[0]]=str(map_c)+'/'+str(raw_c)
		dmr[ele[0]]=float(map_c)/float(raw_c)
		ds_pos[ele[0]]=tem
		ds_freq[ele[0]]=nt
	## Get average depth of this strain ##

	all_ps=np.array(all_ps)
	all_sum=np.sum(all_ps,axis=0)
	pos_label=dict(zip(pos_snp,list(all_sum)))

	max_map=sorted(dmr.items(),key=lambda d:d[1],reverse=True)[0][1]
	res=sorted(dmap_rate.items(),key=lambda d:d[1],reverse=True)
	#print(res[:10])
	#exit()
	top10_score_s=res[:10]
	top_map_strain=[]
	for r in res:
		if r[1]==res[0][1]:
			top_map_strain.append(r[0])
		else:break
	#####  Unique nodes scan for all top strains
	snp_arr=[]
	### Pre-calculate the possible strain number, then decide whether should calculate weighted score.
	pre_freq_arr=[]
	for s in top_map_strain:
		snp_arr.append(ds_pos[s])
		pre_pa=ds_pos[s]*(-1)
		pre_pa=np.array(pre_pa)
		pre_pa[pre_pa==0]=1
		pre_freq_arr=freq_arr*pre_pa
		pre_freq_arr[pre_freq_arr<0]=0

	keep=(pre_freq_arr!=0)
	pre_freq_arr=pre_freq_arr[keep]

	pre_pos_snp=np.array(pos_snp)[keep]
	pre_ds_pos={}
	for s in ds_pos:
		pre_ds_pos[s]=ds_pos[s][keep]
	pre_wf_arr=pre_freq_arr/np.sum(pre_freq_arr)
	strain_num={}
	sn=0
	while True:
		if len(pre_freq_arr)==0:break
		smr={}
		for r in ds_pos:
			if r in top_map_strain:continue
			tt=pre_ds_pos[r]
			nt=tt*pre_wf_arr
			mr=np.sum(nt)
			smr[r]=mr
		res=sorted(smr.items(),key=lambda d:d[1],reverse=True)
		ts=[]
		for r in res:
			if r[1]==res[0][1]:
				ts.append(r[0])
		if len(ts)>1:
			rmr={}
			for s in ts:
				rmr[s]=dmap_rate[s]
			res2=sorted(rmr.items(),key=lambda d:d[1],reverse=True)
			strain_num[res2[0][0]]=''
		else:
			strain_num[ts[0]]=''
		vm1=len(pre_freq_arr)
		pre_pa=pre_ds_pos[ts[0]]*(-1)
		pre_pa[pre_pa==0]=1
		pre_freq_arr=pre_freq_arr*pre_pa
		pre_freq_arr[pre_freq_arr<0]=0
		keep=(pre_freq_arr!=0)
		pre_freq_arr=pre_freq_arr[keep]
		if not np.sum(pre_freq_arr)==0:
			pre_wf_arr=pre_freq_arr/np.sum(pre_freq_arr)
		pre_pos_snp=pre_pos_snp[keep]
		for s in pre_ds_pos:
			pre_ds_pos[s]=pre_ds_pos[s][keep]
		vm=vm1-len(pre_freq_arr)
		if vm>1:
			sn+=1
	#print(top_map_strain)
	#exit()
	# Will recalculate the score and select top strain
	
	if sn>1:
		for s in top_map_strain:
			strain_num[s]=''
		sscore={}
		sna=[]
		for s in strain_num:
			sna.append(ds_pos[s])
		sna=np.array(sna)
		ssum=sna.sum(axis=0)
		ssum[ssum==0]=1
		for s in strain_num:
			snt=ds_pos[s]/ssum
			ns=dmap_rate[s]*snt
			ns=ns.sum(axis=0)
			sscore[s]=ns
		res=sorted(sscore.items(),key=lambda d:d[1],reverse=True)
		tem_map_strain=[]
		for r in res:
			if not dmr[r[0]]==max_map:continue
			tem_map_strain.append(r[0])
			break
		if len(tem_map_strain)>0:
			top_map_strain=tem_map_strain
	
	#print(top_map_strain)
	#exit()
	
	snp_arr=np.array(snp_arr)
	pos_sum=snp_arr.sum(axis=0)
	#pos_sum[pos_sum>1]=0
	i=0

	strain_unique={}
	strain_unique_count={}
	su_for_snp={} # 'data':[{},{}],'tichvals':[],ticktext:[]
	for p in pos_sum:
		column=pos_snp[i]
		#print(ds_ref)
		#exit()
		# Get diff SNP to ref
		snp=re.split('-',column)
		#snp_cid=int(snp[0])
		if int(snp[0]) not in ds_ref:
			column_diff=column+'/-'
			ccolor='#D62728'
		else:
			if snp[1]==ds_ref[int(snp[0])]:
				column_diff=column+'/'+snp[1]
				ccolor='#1f77b4'
			else:
				column_diff=column+'/'+ds_ref[int(snp[0])]
				ccolor='#D62728'
		#print(column_diff)
		#exit()
		if p>=1:
			if pos_freq_map[column]<=min_depth_absolute:
				i+=1
				continue
			i2=0
			window=snp_arr[:,i]
			for w in window:
				if w>=1:
					strain=top_map_strain[i2]
					if strain not in strain_unique:
						strain_unique[strain]={column:pos_freq_map[column]}
						strain_unique_count[strain]=1
						#su_for_snp[strain]={'x':[column_diff],'y':[int(pos_freq_map[column])],'marker':{'color':[ccolor]},'name': 'Hit','type':'bar','line':{'color':'rgba(128,0,128,1.0)', 'width':1}}
						#su_for_snp[strain]={'data':[{'x':[],'y':[],'name':'Same base','type':'bar','marker':{'color':''},'line':{'color':'rgba(128,0,128,1.0)'},'width':1},{'x':[],'y':[],'name':'SNV','type':'bar','marker':{'color':''},'line':{'color':'rgba(128,0,128,1.0)'},'width':1}],'tickvals':[],'ticktext':[]}
						su_for_snp[strain]={'data':[{'x':[],'y':[],'name':'Same base','type':'bar','marker':{'color':''},'line':{'color':'rgba(128,0,128,1.0)'},'width':1},{'x':[],'y':[],'name':'SNV','type':'bar','marker':{'color':''},'line':{'color':'rgba(128,0,128,1.0)'},'width':1}],'carr':[]}
						if ccolor=='#1f77b4':
							#su_for_snp[strain]['data'][0]['x'].append(strain_unique_count[strain])
							su_for_snp[strain]['data'][0]['x'].append(column_diff)
							su_for_snp[strain]['data'][0]['y'].append(int(pos_freq_map[column]))
							su_for_snp[strain]['data'][0]['marker']['color']=ccolor
						else:
							#su_for_snp[strain]['data'][1]['x'].append(strain_unique_count[strain])
							su_for_snp[strain]['data'][1]['x'].append(column_diff)
							su_for_snp[strain]['data'][1]['y'].append(int(pos_freq_map[column]))
							su_for_snp[strain]['data'][1]['marker']['color']=ccolor
						#su_for_snp[strain]['tichvals'].append(strain_unique_count[strain])
						su_for_snp[strain]['carr'].append(column_diff)
					else:
						strain_unique[strain][column]=pos_freq_map[column]
						strain_unique_count[strain]+=1
						#su_for_snp[strain]['x'].append(column_diff)
						#su_for_snp[strain]['y'].append(int(pos_freq_map[column]))
						#su_for_snp[strain]['marker']['color'].append(ccolor)
						if ccolor=='#1f77b4':
							#su_for_snp[strain]['data'][0]['x'].append(strain_unique_count[strain])
							su_for_snp[strain]['data'][0]['x'].append(column_diff)
							su_for_snp[strain]['data'][0]['y'].append(int(pos_freq_map[column]))
							su_for_snp[strain]['data'][0]['marker']['color']=ccolor
						else:
							#su_for_snp[strain]['data'][1]['x'].append(strain_unique_count[strain])
							su_for_snp[strain]['data'][1]['x'].append(column_diff)
							su_for_snp[strain]['data'][1]['y'].append(int(pos_freq_map[column]))
							su_for_snp[strain]['data'][1]['marker']['color']=ccolor

						#su_for_snp[strain]['tickvals'].append(strain_unique_count[strain])
						su_for_snp[strain]['carr'].append(column_diff)

				i2+=1
		i+=1

	### Final output report generating part ###
	mp_strain=[]  # Most possible strain
	op_strain=[]  # Other possible strain -> [S1,S2,S3,S5]
	op_strain_batch=[] # Other possible strain ->[[S1,S2],[S3,S5],...]
	if not len(strain_unique)==0:
		for s in strain_unique:
			mp_strain.append(s)
	else:
		### Need to check whether these strains have close depth
		for r in top_map_strain:
			mp_strain.append(r)
	#print(mp_strain)
	#exit()
	## Check nodes of MT419847
	## Iterative function to get other possible strains and other possible pos-snp
	ds_avgd={}
	for m in mp_strain:
		# Get the avg depth of the strain
		keep=(ds_freq[m]!=0)
		min_depth,max_depth=np.percentile(ds_freq[m][keep],[min_depth_percentile,max_depth_percentile])
		keep=np.logical_and.reduce((ds_freq[m]>=min_depth,ds_freq[m]<=max_depth))
		ds_avgd[m]=np.mean(ds_freq[m][keep])

		pos_arr=ds_pos[m]*(-1)
		pos_arr=np.array(pos_arr)
		pos_arr[pos_arr==0]=1
		freq_arr=freq_arr*pos_arr
		freq_arr[freq_arr<0]=0

	keep=(freq_arr!=0)

	left_freq_arr=freq_arr[keep]
	pos_snp=np.array(pos_snp)
	left_pos_snp=pos_snp[keep]
	left_ds_pos={}
	for s in ds_pos:
		left_ds_pos[s]=ds_pos[s][keep]
	left_ps_freq_map=dict(zip(left_pos_snp,left_freq_arr))
	resl=sorted(left_ps_freq_map.items(),key=lambda d:d[1],reverse=True)
	os_strain={} # '221-A-100-10000':['>MT312312.1',....]
	os_arr=[] # ['221-A-100-10000','225-G-100-10000',....]
	left_weighted_freq_arr=left_freq_arr/np.sum(left_freq_arr)
	vmap={} # The dict used to record the valid map rate
	vm1st={} # Valid map of all other strains in the 1st iteration
	#### Start Iterative process ######
	if not len(left_freq_arr)==0:
		max_iter_times=len(left_freq_arr)
		for l in range(max_iter_times):
			if len(left_freq_arr)==0:break
			strain_map_rate={}
			for r in ds_pos:
				if r in mp_strain:continue
				tem=left_ds_pos[r]
				if l==0:
					find_valid=tem*left_freq_arr
					find_valid=np.array(find_valid)
					vm1st[r]=np.sum(find_valid>1)
					ds_avgd[r]=np.mean(find_valid)
				nt=tem*left_weighted_freq_arr
				map_c=len(nt[nt>0])
				map_rate=np.sum(nt)
				strain_map_rate[r]=map_rate
			selected_strain=[] # used to save the selected strains in this round
			res=sorted(strain_map_rate.items(),key=lambda d:d[1],reverse=True)
			top_s=[]
			snp_arr=[]
			for r in res:
				if r[1]==res[0][1]:
					top_s.append(r[0])
					### Calculate avg depth
					nt=left_ds_pos[r[0]]*left_freq_arr
					keep=(nt!=0)
					nt=nt[keep]
					min_depth,max_depth=np.percentile(nt,[min_depth_percentile,max_depth_percentile])
					keep=np.logical_and.reduce((nt>=min_depth,nt<=max_depth))
					if not len(nt[keep])==0:
						nt=nt[keep]
					ds_avgd[r[0]]=np.mean(nt)
					## Done
					snp_arr.append(left_ds_pos[r[0]])
			if len(top_s)>1:
				rank_map_rate={}
				for s in top_s:
					rank_map_rate[s]=dmap_rate[s]
				res=sorted(rank_map_rate.items(),key=lambda d:d[1],reverse=True)
				top_s=[]
				for r in res:
					top_s.append(r[0])
			top_s=np.array(top_s)
			pre=[]
			for r in resl:
				pre.append(r[0]+':'+str(r[1]))
			pre=','.join(pre)
			top_pos_snp=pre+'\t'+str(len(top_s))
			os_arr.append(top_pos_snp)
			os_strain[top_pos_snp]=[]
			for s in top_s:
				os_strain[top_pos_snp].append(s)
				pos_arr=left_ds_pos[s]*(-1)
				pos_arr[pos_arr==0]=1
				left_freq_arr=left_freq_arr*pos_arr
				left_freq_arr[left_freq_arr<0]=0
			keep=(left_freq_arr!=0)
			valid_map=len(left_freq_arr)
			left_freq_arr=left_freq_arr[keep]
			valid_map=valid_map-len(left_freq_arr)
			vmap[top_pos_snp]=valid_map
			if not np.sum(left_freq_arr)==0:
				left_weighted_freq_arr=left_freq_arr/np.sum(left_freq_arr)
			left_pos_snp=left_pos_snp[keep]
			left_ps_freq_map=dict(zip(left_pos_snp,left_freq_arr))
			for s in left_ds_pos:
				left_ds_pos[s]=left_ds_pos[s][keep]
			resl=sorted(left_ps_freq_map.items(),key=lambda d:d[1],reverse=True)
	# All strain cross validation
	#print(mp_strain)
	#exit()

	### Output part
	dc={}

	if os.path.exists(db_dir+'/head_file.txt'):
		fp=open(db_dir+'/head_file.txt','r')
		dc={}
		while True:
			line=fp.readline().strip()
			if not line:break
			ele=line.split('\t')
			#pre=re.split('\|',line)[0].strip()
			#anno=re.split('\|',line)[1].strip()
			dc[ele[0]]={'meta':ele[1],'link':ele[2],'accession':ele[3]}

	#o=open(out_dir,'w+')
	#o.write('\t\tStrain_ID\tCls_info\tSubCls_info\tMap_Score\tValid_Map_Rate\tTotal_Map_Rate\tStrain_Depth\tStrain_info\tUnique_SNP\n')
	#o.write('>>Most possible strains:\n')
	all_s=[]
	vs_sd=[]
	vs_so=[]
	for s in mp_strain:
		all_s.append(s)
		vs_sd.append(s)
	if len(os_arr)>0:
		for s in os_arr:
			all_s.append(os_strain[s][0])
			if vmap[s]>1:
				vs_so.append(os_strain[s][0])
	# Strain-level identification 
	s2cls={} # Used for output cluster info
	s2sub={} # Used for output sub-cluster info
	candidate_cls={}
	s2sub2s={} # Cls_Strain -> Sub_Cls->Strain
	fcls=open(cls_file)
	while True:
		line=fcls.readline().strip()
		if not line:break
		ele=line.split('\t')
		if ele[0] not in all_s:
			s2cls[ele[0]]=ele[2]
			if ele[1] not in s2sub2s:
				s2sub2s[ele[1]]={ele[3]:ele[0]}
			else:
				s2sub2s[ele[1]][ele[3]]=ele[0]
			continue
		if ele[2]==ele[3]:
			s2cls[ele[0]]=ele[2]
			s2sub[ele[0]]='NA'
		else:
			s2cls[ele[0]]=ele[2]
			candidate_cls[ele[2]]=''
			if ele[1] not in s2sub2s:
				s2sub2s[ele[1]]={ele[3]:ele[0]}
			else:
				s2sub2s[ele[1]][ele[3]]=ele[0]
		#s2sub[ele[0]]=''
	#print(s2sub2s)
	#exit()
	if not len(candidate_cls)==0:
		fsk=open(sub_kmr_file,'r')
		ksub={}
		cls_sub={}
		sid2kmr={}  # Sub_kmer_id -> Sub_kmer
		sid=0
		while True:
			line=fsk.readline().strip()
			if not line:break
			ele=line.split('\t')
			kmr=ele[0]
			sid2kmr[sid]=kmr
			sid+=1
			if ele[1] in candidate_cls:
				if kmr not in ksub:
					ksub[kmr]={ele[1]:{}}
				if ele[1] not in ksub[kmr]:
					ksub[kmr][ele[1]]={}
				if ele[1] not in cls_sub:
					cls_sub[ele[1]]={}
				sub=re.split(',',ele[-1])
				for s in sub:
					ksub[kmr][ele[1]][s]=''
					cls_sub[ele[1]][s]=0
		sub_arr=sp.load_npz(npz_2)
		sub_arr=sub_arr.A[0]
		sid=0
		for kf in sub_arr:
			kmr=sid2kmr[sid]
			sid+=1
			if kmr not in ksub:continue
			if int(kf)>=min_depth_adf:
				for c in ksub[kmr]:
					for c2 in ksub[kmr][c]:
						cls_sub[c][c2]+=int(kf)
		for s in all_s:
			if s in s2sub:continue
			if s2cls[s] not in cls_sub:
				s2sub[s]='NA'
			else:
				res=sorted(cls_sub[s2cls[s]].items(),key=lambda d:d[1],reverse=True)
				if len(res)>1:
					if res[0][1]==res[1][1]:
						s2sub[s]='NA'
					else:
						s2sub[s]=res[0][0]
				else:
					s2sub[s]=res[0][0]
	real_s={} # Cls_Strain -> Final Strain
	for s in s2sub:
		if not s2sub[s]=='NA':
			real_s[s]=s2sub2s[s][s2sub[s]]
	#print(real_s)
	#exit()
	# Regression model
	all_ps_strain=[]
	input_x=[]
	y=raw_freq_arr
	for s in mp_strain:
		all_ps_strain.append(s)
		input_x.append(ds_pos[s])
	min_map_num=int(re.split('/',ds_num[mp_strain[0]])[-1])-50
	c=1
	new_op_strain=[]
	if len(os_arr)>0:
		for s in os_arr:
			if int(vmap[s])>=3:
				tem_c=1
				for n in os_strain[s]:
					if tem_c>1:continue
					#print('op_strain',n,vm1st[n])
					if n in mp_strain:continue
					if int(re.split('/',ds_num[n])[-1])<min_map_num:continue
					#if vm1st[n]<5:continue
					if c>1:
						#if dmap_rate[n]<dmap_rate[mp_strain[0]]-0.05:continue
						if dmap_rate[n]<0.8:continue
					new_op_strain.append(n)
					tem_c+=1
					#input_x.append(ds_pos[n])
				c+=1
	#print(new_op_strain)
	#exit()
	'''
	hms={}
	for s in ds_num:
		mn=int(re.split('/',ds_num[s])[0])
		hms[s]=mn
	'''


	'''
	res=sorted(dmr.items(),key=lambda d:d[1],reverse=True)
	top10_s={}
	for t in top10_score_s:
		top10_s[t[0]]=''
	#print(top10_s)
	for r in res:
		if r[1]==res[0][1]:
			if r[0] in mp_strain:continue
			if re.search('JN024100',r[0]):continue
			#print(r,dmap_rate[r[0]],vm1st[r[0]],ds_avgd[r[0]],dmap_rate[r[0]]*ds_avgd[r[0]])
			if r[0] not in all_ps_strain:
				#print(r[0],vm1st[r[0]])
				if r[0] not in top10_s:continue
				if int(re.split('/',ds_num[r[0]])[-1])<min_map_num:continue
				#if vm1st[r[0]]<5:continue
				if int(vmap[r[0]])<3 and db_name=='SCOV2':continue
				all_ps_strain.append(r[0])
				input_x.append(ds_pos[r[0]])
	#print(all_ps_strain)
	#exit()
	input_x_old=np.array(input_x)
	input_x_old=input_x_old.T
	input_x_old=list(input_x_old)
	input_x_old=list(input_x_old)
	y_old=np.array(y)

	c=0
	input_x=[]
	y=[]
	for i in y_old:
		if i==0:
			c+=1
			continue
		input_x.append(input_x_old[c])
		y.append(i)
		c+=1
	input_x=np.array(input_x)
	y=np.array(y)
	
	CV_NITER=20
	NALPHA = 50
	MAX_NITER = 5000
	TEST_SIZE = 0.5
	cv = ShuffleSplit(n_splits=CV_NITER, test_size=TEST_SIZE, random_state=0)
	reg_cv=LassoCV(eps=0.001, n_alphas=NALPHA,fit_intercept=False, normalize=False,precompute='auto', max_iter=MAX_NITER,tol=0.0001, copy_X=True, cv=cv, verbose=False,n_jobs=1, positive=True, random_state=0,selection='cyclic')
	reg_cv.fit(input_x,y)
	reg_cv.fit(input_x, y)
	alpha, mse_ave, mse_std = lasso_mpm(reg_cv.alphas_, reg_cv.mse_path_)
	reg=Lasso(alpha=alpha, fit_intercept=False, normalize=False,precompute=False, copy_X=True, max_iter=MAX_NITER,tol=0.0001, warm_start=False, positive=True,random_state=0, selection='cyclic')
	reg.fit(input_x,y)
	reg_coef=np.atleast_1d(reg.coef_)
	ds_avgd={}
	ds_avgd=dict(zip(all_ps_strain,list(reg_coef)))
	res=sorted(ds_avgd.items(),key=lambda d:d[1],reverse=True)
	new_op_strain=[]
	for r in res:
		if r[0] in mp_strain:continue
		new_op_strain.append(r[0])
	new_op_strain=new_op_strain[:5]
	'''


	# Output part
	out_json={'ref':{'stype':'Ref','sid':'','cls':'','mpscore':'NA','vmr':'NA','tmr':'NA','sdepth':'NA','sinfo':'NA','slink':'NA','sac':'NA'},'mps':{'stype':'MP','sid':'','cls':'','mpscore':'','vmr':'','tmr':'','sdepth':'','sinfo':'NA','slink':'NA','sac':'NA'},'ops':[],'ms_snp':{},'bar_d2':[],'bar_l2':[],'pie_d3':[],'pda':[]}
	target={}
	# Reference strain
	out_json['ref']['sid']=ref_one
	out_json['ref']['cls']=s2cls[ref_one]
	out_json['ref']['sinfo']=dc[ref_one]['meta']
	out_json['ref']['slink']=dc[ref_one]['link']
	out_json['ref']['sac']=dc[ref_one]['accession']
	for s in mp_strain[:1]:
		if s in strain_unique:
			if s not in dc:
				if s in real_s:
					out_json['mps']['sid']=real_s[s]
					target[real_s[s]]='MP Strain'
				else:
					out_json['mps']['sid']=s
					target[s]='MP Strain'
				out_json['mps']['cls']=s2cls[s]
				out_json['mps']['mpscore']=str(dmap_rate[s])
				out_json['mps']['vmr']=str(ds_num[s])
				out_json['mps']['tmr']=str(ds_num[s])
				out_json['mps']['sdepth']=str(ds_avgd[s])
				out_json['mps']['sinfo']='NA'
				#o.write('\t\t'+s+'\t'+s2cls[s]+'\t'+s2sub[s]+'\t'+str(dmap_rate[s])+'\t'+str(ds_num[s])+'\t'+str(ds_num[s])+'\t'+str(ds_avgd[s])+'\t\t\t'+str(strain_unique[s])+'\n')
			else:
				if s in real_s:
					out_json['mps']['sid']=real_s[s]
					target[real_s[s]]='MP Strain'
					out_json['mps']['sinfo']=dc[real_s[s]]['meta']
					out_json['mps']['slink']=dc[real_s[s]]['link']
					out_json['mps']['sac']=dc[real_s[s]]['accession']
				else:
					out_json['mps']['sid']=s
					target[s]='MP Strain'
					out_json['mps']['sinfo']=dc[s]['meta']
					out_json['mps']['slink']=dc[s]['link']
					out_json['mps']['sac']=dc[s]['accession']
				#out_json['mps']['sid']=s
				out_json['mps']['cls']=s2cls[s]
				out_json['mps']['mpscore']=str(dmap_rate[s])
				out_json['mps']['vmr']=str(ds_num[s])
				out_json['mps']['tmr']=str(ds_num[s])
				out_json['mps']['sdepth']=str(ds_avgd[s])
				#out_json['mps']['sinfo']=dc[s]
			out_json['ms_snp']=su_for_snp[s]
				#o.write('\t\t'+s+'\t'+s2cls[s]+'\t'+s2sub[s]+'\t'+str(dmap_rate[s])+'\t'+str(ds_num[s])+'\t'+str(ds_num[s])+'\t'+str(ds_avgd[s])+'\t'+dc[s]+'\t'+str(strain_unique[s])+'\n')
		else:
			if s not in dc:
				if s in real_s:
					out_json['mps']['sid']=real_s[s]
					target[real_s[s]]='MP Strain'
				else:
					out_json['mps']['sid']=s
					target[s]='MP Strain'
				out_json['mps']['cls']=s2cls[s]
				out_json['mps']['mpscore']=str(dmap_rate[s])
				out_json['mps']['vmr']=str(ds_num[s])
				out_json['mps']['tmr']=str(ds_num[s])
				out_json['mps']['sdepth']=str(ds_avgd[s])
				out_json['mps']['sinfo']='NA'
				#o.write('\t\t'+s+'\t'+s2cls[s]+'\t'+s2sub[s]+'\t'+str(dmap_rate[s])+'\t'+str(ds_num[s])+'\t'+str(ds_num[s])+'\t'+str(ds_avgd[s])+'\t\t\tNA\n')
			else:
				if s in real_s:
					out_json['mps']['sid']=real_s[s]
					target[real_s[s]]='MP Strain'
					out_json['mps']['sinfo']=dc[real_s[s]]['meta']
					out_json['mps']['slink']=dc[real_s[s]]['link']
					out_json['mps']['sac']=dc[real_s[s]]['accession']
				else:
					out_json['mps']['sid']=s
					target[s]='MP Strain'
					out_json['mps']['sinfo']=dc[s]['meta']
					out_json['mps']['slink']=dc[s]['link']
					out_json['mps']['sac']=dc[s]['accession']
				#out_json['mps']['sid']=s
				out_json['mps']['cls']=s2cls[s]
				out_json['mps']['mpscore']=str(dmap_rate[s])
				out_json['mps']['vmr']=str(ds_num[s])
				out_json['mps']['tmr']=str(ds_num[s])
				out_json['mps']['sdepth']=str(ds_avgd[s])
				#out_json['mps']['sinfo']=dc[s]
				#o.write('\t\t'+s+'\t'+s2cls[s]+'\t'+s2sub[s]+'\t'+str(dmap_rate[s])+'\t'+str(ds_num[s])+'\t'+str(ds_num[s])+'\t'+str(ds_avgd[s])+'\t'+dc[s]+'\tNA\n')
	#o.write('>>Other possible strains:\n')
	if len(new_op_strain)>0:
		for n in new_op_strain:
			#ele=re.split('\t',s)
			#n=ele[0]
			if int(ds_avgd[n])==0:continue
			dtem={'stype':'OP','sid':'','cls':'','mpscore':'','vmr':'','tmr':'','sdepth':'','sinfo':'NA','slink':'NA','sac':'NA'}
			#ele=re.split('\t',s)
			#all_s.append(os_strain[s][0])
			#for n in os_strain[s]:
			if True:
				#all_s.append(n)
				a=re.split('/',ds_num[n])[-1]
				vm=str(vm1st[n])+'/'+a
				
				if n in s2sub:
					if n not in dc:
						if n in real_s:
							dtem['sid']=real_s[n]
							target[real_s[n]]='OP Strain'
						else:
							dtem['sid']=n
							target[n]='OP Strain'
						dtem['cls']=s2cls[n]
						dtem['mpscore']=str(dmap_rate[n])
						dtem['vmr']=vm
						dtem['tmr']=ds_num[n]
						dtem['sdepth']=str(ds_avgd[n])
						dtem['sinfo']='NA'
						#o.write('\t\t'+n+'\t'+s2cls[n]+'\t'+s2sub[n]+'\t'+str(dmap_rate[n])+'\t'+vm+'\t'+ds_num[n]+'\t'+str(ds_avgd[n])+'\t\t\tNot_record\n')
					else:
						if n in real_s:
							dtem['sid']=real_s[n]
							target[real_s[n]]='OP Strain'
							dtem['sinfo']=dc[real_s[n]]['meta']
							dtem['slink']=dc[real_s[n]]['link']
							dtem['sac']=dc[real_s[n]]['accession']
						else:
							dtem['sid']=n
							target[n]='OP Strain'
							dtem['sinfo']=dc[n]['meta']
							dtem['slink']=dc[n]['link']
							dtem['sac']=dc[n]['accession']
						#dtem['sid']=n
						dtem['cls']=s2cls[n]
						dtem['mpscore']=str(dmap_rate[n])
						dtem['vmr']=vm
						dtem['tmr']=ds_num[n]
						dtem['sdepth']=str(ds_avgd[n])
						#dtem['sinfo']=dc[n]
						#o.write('\t\t'+n+'\t'+s2cls[n]+'\t'+s2sub[n]+'\t'+str(dmap_rate[n])+'\t'+vm+'\t'+ds_num[n]+'\t'+str(ds_avgd[n])+'\t'+dc[n]+'\tNot_record\n')
				else:
					if n not in dc:
						if n in real_s:
							dtem['sid']=real_s[n]
							target[real_s[n]]='OP Strain'
						else:
							dtem['sid']=n
							target[n]='OP Strain'
						dtem['cls']=s2cls[n]
						dtem['mpscore']=str(dmap_rate[n])
						dtem['vmr']=vm
						dtem['tmr']=ds_num[n]
						dtem['sdepth']=str(ds_avgd[n])
						dtem['sinfo']='NA'
						#o.write('\t\t'+n+'\t'+s2cls[n]+'\tNot_record\t'+str(dmap_rate[n])+'\t'+vm+'\t'+ds_num[n]+'\t'+str(ds_avgd[n])+'\t\t\tNot_record\n')
					else:
						if n in real_s:
							dtem['sid']=real_s[n]
							target[real_s[n]]='OP Strain'
							dtem['sinfo']=dc[real_s[n]]['meta']
							dtem['slink']=dc[real_s[n]]['link']
							dtem['sac']=dc[real_s[n]]['accession']
						else:
							dtem['sid']=n
							target[n]='OP Strain'
							dtem['sinfo']=dc[n]['meta']
							dtem['slink']=dc[n]['link']
							dtem['sac']=dc[n]['accession']
						dtem['cls']=s2cls[n]
						dtem['mpscore']=str(dmap_rate[n])
						dtem['vmr']=vm
						dtem['tmr']=ds_num[n]
						dtem['sdepth']=str(ds_avgd[n])
						#dtem['sinfo']=dc[n]
						#o.write('\t\t'+n+'\t'+s2cls[n]+'\tNot_record\t'+str(dmap_rate[n])+'\t'+vm+'\t'+ds_num[n]+'\t'+str(ds_avgd[n])+'\t'+dc[n]+'\tNot_record\n')
			out_json['ops'].append(dtem)
	'''
	else:
		dtem={'sid':'','cls':'','mpscore':'','vmr':'','tmr':'','sdepth':'','sinfo':'','slink':'','sac':''}
		out_json['ops'].append(dtem)
	'''
	# construct json for depth bar and relative abundance pie chart
	if True:
		
		# case-1: only most possible strain
		if len(out_json['ops'])==0:
			out_json['bar_d2'].append({'x':[out_json['mps']['sid']],'y':[float(out_json['mps']['sdepth'])],'marker':{'color': 'rgba(222,45,38,0.8)'},'name': 'Most possible strain','type': 'bar'})
			out_json['bar_l2'].append(out_json['mps']['sid'])
			out_json['pie_d3'].append({'values':[100],'labels':[out_json['mps']['sid']],'type':'pie','hole':0.4})
			out_json['pda'].append({'x':[out_json['mps']['sid']],'y':[float(out_json['mps']['sdepth'])],'marker':{'color': 'rgba(222,45,38,0.8)'},'name': 'Most possible strain','type': 'bar'})
			out_json['pda'].append({'x':[out_json['mps']['sid']],'y':[100],'type':'pie'})
		else:
			out_json['bar_d2'].append({'x':[out_json['mps']['sid']],'y':[out_json['mps']['sdepth']],'marker':{'color': 'rgba(222,45,38,0.8)'},'name': 'Most possible strain','type': 'bar'})
			out_json['pda'].append({'x':[out_json['mps']['sid']],'y':[out_json['mps']['sdepth']],'marker':{'color': 'rgba(222,45,38,0.8)'},'name': 'Most possible strain','type': 'bar'})
			all_s=[]
			all_s.append(out_json['mps']['sid'])
			tem_x=[]
			all_depth=[]
			td=0
			all_depth.append(float(out_json['mps']['sdepth']))
			td+=float(out_json['mps']['sdepth'])
			tem_y=[]
			for tem in out_json['ops']:
				all_s.append(tem['sid'])
				tem_x.append(tem['sid'])
				all_depth.append(float(tem['sdepth']))
				td+=float(tem['sdepth'])
				tem_y.append(float(tem['sdepth']))
			#print(out_json['ops'])
			#print(all_depth,all_s)
			#exit()
			out_json['bar_d2'].append({'x':tem_x,'y':tem_y,'marker':{'color': 'rgba(204,204,204,1)'},'name': 'Other possible strain(s)','type': 'bar'})
			out_json['pda'].append({'x':tem_x,'y':tem_y,'marker':{'color': 'rgba(204,204,204,1)'},'name': 'Other possible strain(s)','type': 'bar'})
			out_json['bar_l2']=all_s
			y_for_rb=[]
		
			csum=0
			for dp in all_depth:
				#print(dp,td)
				current=float(dp/td)*100
				#csum+=current
				y_for_rb.append(current)
			#csum+=all_depth[-1]

			#y_for_rb.append(100-csum)
			#print(all_depth,all_s)
			#print(y_for_rb)
			#exit()
			out_json['pie_d3'].append({'values':y_for_rb,'labels':all_s,'type':'pie','hole':0.4})
			out_json['pda'].append({'y':y_for_rb,'x':all_s,'type':'pie'})
			#print()





	o1=open('tem_json_1.txt','w+')
	o1.write(str(out_json['ms_snp']['data']))
	o2=open('tem_json_2.txt','w+')
	o2.write(str(out_json['ms_snp']['carr']))
	return out_json,target
	'''
	res=sorted(dmr.items(),key=lambda d:d[1],reverse=True)
	o.write('\n>>Highest_Map_Strains (Could be FP):\n')
	final={}
	for r in res:
		if r[1]==res[0][1]:
			if r[0] not in all_s:
				final[r[0]]=dmap_rate[r[0]]
	if not len(final)==0:
		res=sorted(final.items(),key=lambda d:d[1],reverse=True)
		for s in res:
			if s[0] in s2sub:
				if s[0] not in dc:
					o.write('\t\t'+s[0]+'\t'+s2cls[s[0]]+'\t'+s2sub[s[0]]+'\t'+str(dmap_rate[s[0]])+'\t'+ds_num[s[0]]+'\t'+ds_num[s[0]]+'\tNA\tNA\n')
				else:
					o.write('\t\t'+s[0]+'\t'+s2cls[s[0]]+'\t'+s2sub[s[0]]+'\t'+str(dmap_rate[s[0]])+'\t'+ds_num[s[0]]+'\t'+ds_num[s[0]]+'\t'+dc[s[0]]+'\tNA\n')
			else:
				if s[0] not in dc:
					o.write('\t\t'+s[0]+'\t'+s2cls[s[0]]+'\tNot_record\t'+str(dmap_rate[s[0]])+'\t'+ds_num[s[0]]+'\t'+ds_num[s[0]]+'\tNA\tNA\n')
				else:
					o.write('\t\t'+s[0]+'\t'+s2cls[s[0]]+'\tNot_record\t'+str(dmap_rate[s[0]])+'\t'+ds_num[s[0]]+'\t'+ds_num[s[0]]+'\t'+dc[s[0]]+'\tNA\n')

	o.write('>>Top10_Score_Strains:\n')
	for t in top10_score_s:
		if t[0] in s2sub:
			if t[0] not in dc:
				o.write('\t\t'+t[0]+'\t'+s2cls[t[0]]+'\t'+s2sub[t[0]]+'\t'+str(t[1])+'\t'+ds_num[t[0]]+'\t'+ds_num[t[0]]+'\tNA\tNA\n')
			else:
				o.write('\t\t'+t[0]+'\t'+s2cls[t[0]]+'\t'+s2sub[t[0]]+'\t'+str(t[1])+'\t'+ds_num[t[0]]+'\t'+ds_num[t[0]]+'\t'+dc[t[0]]+'\tNA\n')
		else:
			if t[0] not in dc:
				o.write('\t\t'+t[0]+'\t'+s2cls[t[0]]+'\tNot_record\t'+str(t[1])+'\t'+ds_num[t[0]]+'\t'+ds_num[t[0]]+'\tNA\tNA\n')
			else:
				o.write('\t\t'+t[0]+'\t'+s2cls[t[0]]+'\tNot_record\t'+str(t[1])+'\t'+ds_num[t[0]]+'\t'+ds_num[t[0]]+'\t'+dc[t[0]]+'\tNA\n')
	## Remove tem file 
	#os.system('rm Tem_Vs* Tem_VS*')
	## From this line, we will generate strain-level analysis report
	#print('Txt report is done. Now will generate pdf report!')

	vs_so=vs_so[:5]
	for s in ds_freq:
		check=0
		if s  in vs_sd:
			check=1
		if s in vs_so:
			check=2
		if check==0:continue
		i=0
		for c in ds_freq[s]:
			if c==0:
				i+=1
				continue
			current_ps=pos_snp[i]
			column=int(re.split('-',current_ps)[0])
			if column not in dscf[s]:
				dscf[s][column]=c
		
			i+=1
		i2=0
		for c in ds_pos[s]:
			if c==0:
				i2+=1
				continue
			current_ps=pos_snp[i2]
			column=int(re.split('-',current_ps)[0])
			if column not in dscl[s]:
				dscl[s][column]=0
			if c==1:
				dscl[s][column]=pos_label[current_ps]
			i2+=1

	ov1=open('Mps_ps_depth.csv','w+')
	ov2=open('Ops_ps_depth.csv','w+')
	ov1.write('ID,Column_ID')
	#carr=[]
	for s in vs_sd:
		ov1.write(','+s+'_Freq')
		ov1.write(','+s+'_LNum')
	ov1.write('\n')
	#carr=sorted(list(dscf[vs_sd[0]].keys()))
	carr=[]
	for c in pos_snp:
		c=re.split('-',c)[0]
		if int(c) not in carr:
			carr.append(int(c))

	i=1
	for c in carr:
		ov1.write(str(i)+','+str(c))
		check=0
		check1=0
		check2=0
		for s in vs_sd:
			if c not in dscf[s]:
				check+=1
				check1=1
			if c not in dscl[s]:
				check+=1
				check2=1
			if check==0:
				ov1.write(','+str(dscf[s][c])+','+str(dscl[s][c]))
			elif check==1:
				if check1==1:
					ov1.write(',0,'+str(dscl[s][c]))	
		ov1.write('\n')
		i+=1
	
	

	ov2.write('ID,Column_ID')
	if len(vs_so)==0:
		ov2.write(',None,None\n')
	else:
		for s in vs_so:
			ov2.write(','+s+'_Freq')
			ov2.write(','+s+'_LNum')
		ov2.write('\n')
		i=1
		for c in carr:
			ov2.write(str(i)+','+str(c))
			check=0
			check1=0
			check2=0
			for s in vs_so:
				if s not in dscf or s not in dscl:
					print('Warning: ',s,' not in final dict!')
					continue
				if c not in dscf[s]:
					check+=1
					check1=1
				if c not in dscl[s]:
					check+=1
					check2=1
				if check==0:
					ov2.write(','+str(dscf[s][c])+','+str(dscl[s][c]))
				elif check==1:
					if check1==1:
						ov2.write(',0,'+str(dscl[s][c]))
					if check2==1:
						ov2.write(','+str(dscf[s][c])+',0')
				else:
					ov2.write(',0,0')
			ov2.write('\n')
			i+=1
	'''
