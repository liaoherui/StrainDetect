from flask import request
from app.api import bp
import os
import re
#import json

@bp.route('/remove_json',methods=["GET","POST"])
def remove_json():
	nxt_json_dir='/mnt/d/My_Python_Web_development/StrainDetect_Develop/Tree_test/data/'
	data=request.form
	#print(json.dump(data))
	#pre=data['tem_json']
	pre=data.getlist("tem_json")[0]
	os.system('rm '+nxt_json_dir+pre+'.json')
