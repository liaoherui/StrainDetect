from flask import jsonify,request
from app.api import bp,md5random,run_virstrain,run_virstrain_regression,modify_data,generate_msa
import os
import re
#import md5random.sjs

@bp.route('/detect',methods=["GET","POST"])
def detect():
	msa_html_dir='../../../front-end/static'
	data=request.form
	vtype=data['vtype']
	files=request.files
	dirs=md5random.sjs()
	os.mkdir(dirs)
	#print(dirs)
	# Save files in tem folder
	file_name=[]
	for file in files.values():	
		dst=dirs+"/"+file.name
		file.save(dst)
		file_name.append(dirs+"/"+file.name)
	#print(file_name)
	
	res_json,target=run_virstrain.detect(file_name[0],file_name[1],vtype)

	#print(res_json)
	#print(target)
	#exit()
	
	ts='?s='
	ts2='?c=subtype&s='
	tem=[]
	for r in target:
		nr=re.sub('>','',r)
		tem.append(nr)
	ts+=','.join(tem)
	ts2+=','.join(tem)
	if vtype=='SCOV2':
		res_json['nxt']='https://strain.ee.cityu.edu.hk/ncov/open/global/all-time'+ts
	elif vtype=='HIV':
		res_json['nxt']='https://strain.ee.cityu.edu.hk/'+vtype+ts2
	else:
		res_json['nxt']='https://strain.ee.cityu.edu.hk/'+vtype+ts
	generate_msa.gmsa(res_json,dirs,msa_html_dir,vtype)

	os.system('rm -rf '+dirs)
	
	return jsonify(res_json)
