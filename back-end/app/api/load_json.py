from flask import request,jsonify
from app.api import bp
import os
import re
import json

@bp.route('/load_json',methods=["GET","POST"])
def load_json():
	#nxt_json_dir='/mnt/d/My_Python_Web_development/StrainDetect_Develop/Tree_test/data/'
	data=request.form
	jid=data['jid']
	#print(jid+'/res.json')
	#print(json.dump(data))
	#pre=data['tem_json']
	#pre=data.getlist("tem_json")[0]
	#os.system('rm '+nxt_json_dir+pre+'.json')
	if os.path.exists(jid+'/error.log'):
		f=open(jid+'/error.log','r')
		line=f.read()
		return jsonify({'error':line})
	elif not os.path.exists(jid+'/res.json'):
		return jsonify({})
	elif os.path.exists(jid+'/res.json'):
		f=open(jid+'/res.json',"r")
		#res=f.read()
		res=json.load(f)
		#print(res)
		#exit()
		return jsonify(res)

