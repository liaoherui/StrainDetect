<template>
  <div class="container4">
    <div class="inner-container4 ">

      <div class="titler"><h1 class="text-center fw-bold mt-6 text-pink">Result</h1></div>
      <div class="px-7"><hr class="mt-2"/></div>
      <div class="abundance rpc" style="margin-top:20px;">
        <h5>1. Predicted depth and relative abundance of identified strain(s)&nbsp;&nbsp; <vue-json-to-csv :json-data="pda" :csv-title="'abundInfo'">
          <b-button style="width: 10%; font-size: 15px !important;" variant="primary">
            <i class="fa fa-download"></i>&nbsp;<b>Download</b>
          </b-button>
        </vue-json-to-csv></h5>
        <div class="row">
          <div  style="width:700px; height:auto; float:left; display:inline"><Plotly :data="data2" :layout="layout2" ></Plotly></div>
          <div  style="width:500px; height:auto; float:left; display:inline"><Plotly :data="data3" :layout="layout3" ></Plotly></div>
        </div>
      </div>


      <div class="info rpc" style="margin-top:20px;">
        <h5> 2. Detailed information about identified strain(s)</h5>
<!--	<b-card class="text-left" bg-variant="light">-->
        <div >
          <br>
          <p style=" font-size: 20px;"> The reference strain (Ref), most possible strain (MP) and other possible strains (OP).&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <vue-json-to-csv :json-data="items1" :csv-title="'strainInfo'">
              <b-button style="width: 10%; font-size: 15px !important;" variant="primary">
                <i class="fa fa-download"></i>&nbsp;<b>Download</b>
              </b-button>
            </vue-json-to-csv></p>

        </div>

        <b-table style="background-color: #FFFFFF; width: 100%; font-size: 13px !important;" small striped hover :items="items1" :fields="fields1" label-sort-asc="" label-sort-desc="" label-sort-clear="">
          <template #cell(slink)="data">
            <b-button style="width: 50%; font-size: 8px !important;" variant="primary" v-on:click="gotosite(data.value)"><i class="fa fa-download"></i></b-button>
          </template>
        </b-table>


      </div>


      <div class="hist rpc" style="margin-top:20px;">
        <h5> 3. Histogram of site coverage of the most possible strain &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          <vue-json-to-csv :json-data="data1" :csv-title="'siteInfo'">
            <b-button style="width: 10%; font-size: 15px !important;" variant="primary">
              <i class="fa fa-download"></i>&nbsp;<b>Download</b>
            </b-button>
          </vue-json-to-csv>

        </h5>
      <Plotly :data="data1" :layout="layout1" ></Plotly>
        </div>
<!--	<b-card class="text-left" bg-variant="dark" text-variant="white">-->

      <div class="msa rpc" style="margin-top:18px;">
        <h5> 4. The msa alignment visualization of identified strain(s)</h5>
        <div>
          <iframe v-bind:src="msaSrc"  scrolling="auto" frameborder="0" style="width: 100%;height: 200px;"></iframe>
        </div>
      </div>


      <div class="auspice rpc" style="margin-top:18px; margin-bottom:18px;">
        <h5> 5. The auspice page of identified strain(s)</h5>
        <iframe v-bind:src="nxtSrc" scrolling="auto" frameborder="0" style="width: 100%;height: 700px;"></iframe>
        <!--        &nbsp;&nbsp;&nbsp;&nbsp;<b-button style="width: 10%; font-size: 18px !important;" variant="primary" v-on:click="gotosite_nextstrain()"> <i class="fa fa-arrow-right"></i>&nbsp;Go!</b-button>-->
      </div>

<!--      <div class="auspice rpc" style="margin-top:20px;">-->
<!--                <h5> 5. The auspice dashboard of viral strains</h5>-->
<!--        &nbsp;<iframe src="http://localhost:4000/ncov/SRR15224359" scrolling="auto" frameborder="0" style="width: 100%;height: 700px;"></iframe>-->
<!--                  </div>-->
<!--                 </b-card>-->



      <!--                <b-card class="text-left" bg-variant="dark" text-variant="white">-->


<!--                 </b-card>-->
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    </div>
</div>

</template>

<script>

import axios from 'axios'
import { BTable } from 'bootstrap-vue'
import { Plotly } from 'vue-plotly'
import XLSX from 'xlsx';
import VueJsonToCsv from 'vue-json-to-csv'
// import { VuePhylogram } from 'vue-phylogram';



export default {
name: 'Result',
data(){
return{
   _beforeUnload_time:0,
   _gap_time:0,
   tem_json:'',
  msaSrc: null,
  nxtSrc: null,
  // labelStyles: {
  //   EPI_ISL_4036644: {
  //     color: 'white',
  //     background: 'red',
  //     borderWidth: 0
  //   },
  //   EPI_ISL_416632: {
  //     color: 'white',
  //     background: 'blue',
  //     borderWidth: 0
  //   }
  // },
  // nodeStyles: {
  //   EPI_ISL_4036644: {
  //     size: 5,
  //     fill: 'red'
  //   },
  //   EPI_ISL_416632: {
  //     size: 5,
  //     fill: 'blue'
  //   }
  // },
//    fields0:[
//      {key: 'sid',sortable: false,'label':'Strain ID'},
//      {key: 'sinfo',sortable: false,'label':'Metadata'},
//      {key: 'slink',sortable: false,'label':'Download Link'},
//      {key: 'sac',sortable: false,'label':'Accession'},
// ],
// items0:[],
   fields1:[
     {key: 'stype',sortable: false,'label':'Strain Type'},
     {key: 'sid',sortable: false,'label':'Strain ID'},
     {key: 'cls',sortable: false,'label':'Strain Cls'},
     {key: 'mpscore',sortable: true,'label':'Mapping score'},
     {key: 'vmr',sortable: true,'label':'Valid map rate'},
     {key: 'tmr',sortable: true,'label':'Total map rate'},
     {key: 'sdepth',sortable: true,'label':'Predicted depth'},
     {key: 'sinfo',sortable: false,'label':'Metadata'},
     {key: 'slink',sortable: false,'label':'Download Link'},
     {key: 'sac',sortable: false,'label':'Accession'},
],
items1:[],
//  fields2:[
//      {key: 'sid',sortable: false,'label':'Strain ID'},
//      {key: 'cls',sortable: false,'label':'Strain Cls'},
//      {key: 'mpscore',sortable: true,'label':'Mapping score'},
//      {key: 'vmr',sortable: true,'label':'Valid map rate'},
//      {key: 'tmr',sortable: true,'label':'Total map rate'},
//      {key: 'sdepth',sortable: true,'label':'Predicted depth'},
//      {key: 'sinfo',sortable: false,'label':'Metadata'},
//      {key: 'slink',sortable: false,'label':'Download Link'},
//      {key: 'sac',sortable: false,'label':'Accession'},
// ],
// items2:[],
data1:[],

layout1:{
showlegend:true,
title:'K-mer hits of most possible strain',
xaxis:{
	tickangle:60,
	tickfont:{size: 8,color: '#bc6f98'},
                 type: "category",
	categoryorder: "array",
	categoryarray:[]
},
yaxis:{title:'Hit'}
},
  data2:[],
    layout2:{
    showlegend:true,
      title:'Predicted depth of identified strain(s)',
      xaxis:{
      tickangle:60,
        tickfont:{size: 12,color: '#bc6f98'},
      categoryorder: "array",
        categoryarray:[]
    },
    yaxis:{title:'Sequencing depth'}
  },
  data3:[],
    layout3:{
    title:'Relative abundance of identified strain(s)'
  }
}
},
components:{
 'b-table':BTable,
  Plotly,
  'vue-json-to-csv':VueJsonToCsv
  // 'Phylogram':VuePhylogram
},
mounted(){
window.addEventListener('beforeunload', e=>this.beforeunloadHandler(e));
window.addEventListener('unload', e=>this.set());
},
destroyed(){
window.removeEventListener('beforeunload', e=>this.beforeunloadHandler(e));
window.removeEventListener('unload', e=>this.set());
},

methods:{
   set(){
     const path="https://strain.ee.cityu.edu.hk/api/remove_json"
     this.tem_json=this.$route.params.nxt
     var val= this.tem_json
     var formData = new FormData()
     formData.append("tem_json", val)
     this._gap_time=new Date().getTime() - this._beforeUnload_time
     if (this._gap_time<=5){
      axios.post(path,formData,{headers:{'Content-Type': 'multipart/form-data'}})
     }
    },
    beforeunloadHandler(){
     this._beforeUnload_time= new Date().getTime();
    },
   getMessage(){
     this.msg=this.$route.params

     if (typeof(this.msg.mps)=="undefined"){
      this.msg=JSON.parse(localStorage.getItem("store"))
     }
     // let arr0=[];
     // arr0.push(this.msg.ref);
     // this.items0=arr0;
     console.log(this.msg);
     let arr1=[];
     arr1.push(this.msg.ref);
     arr1.push(this.msg.mps);
     this.items1=arr1;
     //this.items1.push(this.msg.ops)
     //this.items2=this.msg.ops;
     for (var i in this.msg.ops) {
       this.items1.push(this.msg.ops[i]);
     }
     this.data1=this.msg.ms_snp.data;
     this.layout1.xaxis.categoryarray=this.msg.ms_snp.carr;


     // let arr2=[];
     // for (var i in this.msg.ops) {
     //   arr2.push(this.msg.bar_d2[i])
     // }
     this.data2=this.msg.bar_d2;
     this.layout2.xaxis.categoryarray=this.msg.bar_l2;
     this.data3=this.msg.pie_d3;
     this.pda=this.msg.pda;
     this.msaSrc=this.msg.msa_link;
     this.nxtSrc=this.msg.nxt;
     //this.layout1.xaxis.tickvals=this.msg.ms_snp.tichvals;
     //this.layout1.xaxis.ticktext=this.msg.ms_snp.ticktext;
},
gotosite(producturl){
        //window.location.href = producturl
         window.open(producturl)
},
// gotosite_nextstrain(){
// 	this.tem_json=this.$route.params.nxt
// 	window.open("http://localhost:4000/"+this.tem_json)
// },
// download(){
// 	var ws = XLSX.utils.aoa_to_sheet([["The reference strain"]])
// 	const header0=["sid","sinfo","slink","sac"]
// 	const d0=this.items0
// 	const hd0={"sid":"Strain ID","sinfo":"Strain Metadata","slink":"Download Link","sac":"Aceession"}
// 	const nd0 =[hd0,...d0]
// 	XLSX.utils.sheet_add_json(ws,nd0,{origin: "A2",header:header0,skipHeader:true})
// 	XLSX.utils.sheet_add_aoa(ws,[["Most possible strain and other possible strains"]],{origin: "A4"})
// 	const header1=["sid","cls","mpscore","vmr","tmr","sdepth","sinfo","slink","sac"]
// 	const d1=this.items1
// 	const hd1={"sid":"Strain ID","cls":"Strain Cls","mpscore":"Mapping score","vmr":"Valid map rate","tmr":"Total map rate","sdepth":"Predicted depth","sinfo":"Strain Metadata","slink":"Download Link","sac":"Aceession"}
// 	const nd1=[hd1,...d1]
// 	XLSX.utils.sheet_add_json(ws,nd1,{origin: "A5", header:header1,skipHeader:true})
// 	// XLSX.utils.sheet_add_aoa(ws,[["Other possible strains (Top5)"]],{origin: "A7"})
// 	// const header2=["sid","cls","mpscore","vmr","tmr","sdepth","sinfo","slink","sac"]
// 	// const d2=this.items2
// 	// const hd2={"sid":"Strain ID","cls":"Strain Cls","mpscore":"Mapping score","vmr":"Valid map rate","tmr":"Total map rate","sdepth":"Predicted depth","sinfo":"Strain Metadata","slink":"Download Link","sac":"Aceession"}
// 	// const nd2=[hd1,...d2]
// 	// XLSX.utils.sheet_add_json(ws,nd2,{origin: "A8",header:header2,skipHeader:true})
// 	const wb = XLSX.utils.book_new()
// 	XLSX.utils.book_append_sheet(wb, ws, 'data')
// 	XLSX.writeFile(wb,'report.xlsx')
// }
},

created() {
      this.getMessage()
 }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Roboto:300,400,500,700');
.download-btn {
  background-color: DodgerBlue;
  border: none;
  color: white;
  padding: 12px 30px;
  margin: 12px 0;
  cursor: pointer;
  font-size: 20px;
}
.download-btn:hover {
  background-color: RoyalBlue;
}

.container4 {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  padding-top: 40px;
  /*height: 250vh;*/
  /*height: 350vh;*/
  /*background-color: #F3F3F3;*/
}
.inner-container4 {
  border: 0px solid black;
  width: 90%;
  height: 92%;
  text-align: justify;

}
.titler{
  padding:20px;
}

.abundance{
  background-color: white;
  box-shadow: 0px 0.5px 10px  rgb(180, 180, 180);
  border: 1px solid #D5DFE6;
}
.info{
  background-color: white;
  box-shadow: 0px 0.5px 10px  rgb(180, 180, 180);
  border: 1px solid #D5DFE6;
}
.hist{
  background-color: white;
  box-shadow: 0px 0.5px 10px  rgb(180, 180, 180);
  border: 1px solid #D5DFE6;
}
.msa{
  background-color: white;
  box-shadow: 0px 0.5px 10px  rgb(180, 180, 180);
  border: 1px solid #D5DFE6;
}
.auspice{
  background-color: white;
  box-shadow: 0px 0.5px 10px  rgb(180, 180, 180);
  border: 1px solid #D5DFE6;
}
.download{
  background-color: white;
  box-shadow: 0px 0.5px 10px  rgb(180, 180, 180);
  border: 1px solid #D5DFE6;
}
.rpc{
  padding: 20px;
  font-family: 'Roboto';
  color: black;
}
</style>
