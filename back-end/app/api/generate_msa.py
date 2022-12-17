import re
import os

def gmsa(in_json,md5_code,odir,vtype):
	in_json['msa_link']='/static/'+md5_code+'.html'
	msa_dir='/static/'+md5_code+'.html'
	o=open(odir+'/'+md5_code+'.html','w+')
	tstrain=[] # Ref+MP+OP
	tstrain.append(in_json['ref']['sid'])
	tstrain.append(in_json['mps']['sid'])
	for s in in_json['ops']:
		tstrain.append(s['sid'])

	abs_file=__file__
	abs_dir=abs_file[:abs_file.rfind("/")]
	msa_file=abs_dir+'/DB/'+vtype+'/msa.aln'
	#msa_file='DB/'+vtype+'/msa.aln'
	f=open(msa_file,'r')
	dout={}
	out_str=''
	while True:
		line=f.readline().strip()
		if not line:break
		if re.search('>',line):
			if line in tstrain:
				record=1
				#out_str+=line+'\\n'
				tems=line
				dout[tems]=''
			else:
				record=0
		else:
			if record==1:
				#out_str+=line+'\\n'
				dout[tems]+=line
	for s in tstrain:
		if s in dout:
			out_str+=s+'\\n'+dout[s]+'\\n'
	p1='''
	<!-- Original project: https://github.com/wilzbach/msa -->
	<!-- optional: tinier menu -->

	<div id="menuDiv"></div>
	<div id="yourDiv">Loading...</div>

	<!DOCTYPE html>
	<html lang="en-US">
	<meta name="description" content="Simple BioJS example" />


	<head>
	  <meta charset="UTF-8">
	    <meta name="viewport" content="width=device-width, initial-scale=1">
		  <title>MSAviewer</title>
		  </head>

		  <body>


		  <!-- include MSA js + css -->
		  <script src="https://s3-eu-west-1.amazonaws.com/biojs/msa/latest/msa.js"></script>
		  <!--<link type=text/css rel=stylesheet href=https://s3-eu-west-1.amazonaws.com/biojs/msa/latest/msa.css />-->


		  <!-- optional: menubar -->
		  <!--<link type=text/css rel=stylesheet href=  https://raw.githubusercontent.com/greenify/biojs-vis-msa/master/external/jquery.dropdown.css />-->

		  <!--<script src="script.js"></script>-->
		  <script>
		    // Original project: https://github.com/wilzbach/msa
			  var opts = {};

			    // set your custom properties
				  // @see: https://github.com/greenify/biojs-vis-msa/tree/master/src/g
				 

	'''
	p2='''
	

	  var seqs = msa.io.fasta.parse(fasta);
	    //opts.seqs = msa.utils.seqgen.getDummySequences(1000,300);
		  var m = msa({
			      el: document.getElementById("yourDiv"),
				      seqs: seqs,
					      zoomer: { labelNameLength: 250},
						      colorscheme: {scheme: "nucleotide"},
							      vis: {conserv: true}

								    });
		    var menuOpts = {};
			  menuOpts.el = document.getElementById('div');
			    // menuOpts.vis = {conserv: false, overviewbox: false}
				  menuOpts.msa = m;
				    var defMenu =  new msa.menu.defaultmenu(menuOpts);
					  m.addView("menu", defMenu);
					    // var defMenu=
						  m.render();

						    // opts.seqs=seqs;
							  // opts.el = document.getElementById("yourDiv");
							    // opts.vis = {conserv: false, overviewbox: false}
								  // height = window.screen.height - 250;
								    // console.log(height)
									  // opts.zoomer = {alignmentHeight: height, labelWidth: 110,labelFontsize: "13px",labelIdLength: 50}
									    //
										  // // init msa
										    // var m = new msa.msa(opts);
											  //
											    // // the menu is independent to the MSA container
												  // var menuOpts = {};
												    // menuOpts.el = document.getElementById('div');
													  // menuOpts.msa = m;
													    // var defMenu = new msa.menu.defaultmenu(menuOpts);
														  // m.addView("menu", defMenu);
														    //
															  // // call render at the end to display the whole MSA
															    // m.render();
																</script>

																</body>

																</html>

	'''
	o.write(p1+'\nvar fasta="'+out_str+'";\n'+p2)
	o.close()
	#return msa_dir

#gmsa({'ref':{'sid':'>EPI_ISL_416632'},'mps':{'sid':'>EPI_ISL_4036644'},'ops':[]},'test','./','SCOV2')
