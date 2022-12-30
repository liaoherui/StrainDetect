from flask import jsonify,request
from app.api import bp,run_virstrain,generate_msa
import os
import re
import json
import traceback
#import md5random.sjs

@bp.route('/detect',methods=["GET","POST"])
def detect():
	try:
		#msa_html_dir='/home/www/static'
		msa_html_dir='../../../front-end/static'
		data=request.form
		vtype=data['vtype']
		files=request.files
		#dirs=md5random.sjs()
		dirs=data['randcode']
		os.mkdir(dirs)
		#print(dirs)
		#exit()
		# Save files in tem folder
		file_name=[]
		for file in files.values():	
			dst=dirs+"/"+file.name
			file.save(dst)
			file_name.append(dirs+"/"+file.name)
		#print(file_name)
	
		res_json,target=run_virstrain.detect(file_name[0],file_name[1],vtype)
		
		if len(res_json)==0:
			res_json={'nov':1}
			return jsonify(res_json)
		
		'''
		else:
			res_json,target=run_virstrain_regression.detect(file_name[0],file_name[1],vtype)
		'''
		#print(res_json)
		#print(target)
		#exit()
		#if vtype=='SCOV2':
		#modify_data.modify_scov2(nxt_json_dir+'/herui_ncov_rebuild.json',target,nxt_json_dir+'/'+dirs+'.json')
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
		#res_json['msa_link']=msa_dir
		#print(msa_dir)
		o=open(dirs+'/res.json','w+')
		json.dump(res_json,o)
		o.close()
	
		os.system('rm '+dirs+'/*.npz')
		#exit()
	except Exception as e:
		o=open(dirs+'/error.log','w+')
		error=traceback.format_exc()
		o.write(str(error))
		o.close()
		return {}
	else:
		return jsonify(res_json)
