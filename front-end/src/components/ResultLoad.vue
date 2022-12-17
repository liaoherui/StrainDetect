<template>
  <div class="container42">
    <div class="inner-container4 ">

      <div class="titler"><h1 class="text-center fw-bold mt-6 text-pink">Job status</h1></div>
      <div v-if="seen==1">
        <p class="pfontrl"><br><img src="../assets/Loading.gif" width="40" height="40" alt="">&nbsp;&nbsp;&nbsp;The job is still running. Please wait patiently.</p>
      </div>
      <div v-else-if="seen==2">
        <p class="pfontrl"> <br><img src="../assets/error.png" width="40" height="40" alt=""> &nbsp;Something wrong. The job is failed, and error log is shown below. Please check your input files or send emails to heruiliao2-c@my.cityu.edu.hk! </p>
        <p class="pfontrl">{{error}}</p>
      </div>

    </div>
  </div>

</template>

<script>

import axios from 'axios'
// import { BTable } from 'bootstrap-vue'
// import { Plotly } from 'vue-plotly'
// import XLSX from 'xlsx';
// import VueJsonToCsv from 'vue-json-to-csv'
// import { VuePhylogram } from 'vue-phylogram';



export default {
  name: 'ResultLoad',
  data(){
    return{
      seen: 0,
      error: 'Fail to load error log'
    }
  },

  methods:{

    getMessage(){
      var seen=0;
      let id=this.$route.params.id
      const path="https://strain.ee.cityu.edu.hk/api/load_json"
      //window.alert(id)
      //this.msg=this.$route.params
      var formData = new FormData();
      formData.append("jid",id);
      axios.post(path, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then((response) =>{
        //loadingInstance.close()
        this.msg=response.data
        if (typeof(this.msg.error)!="undefined"){
          this.seen=2;
          this.error=this.msg.error;
        }else if (typeof(this.msg.mps)=="undefined"){
          this.seen=1;
        }
          else {
          localStorage.setItem('store', JSON.stringify(response.data))
          this.$router.push({name: "Result", params: response.data})
        }
        // this.msg=response.data
      }).catch ((error)=>{
        console.log(error);
        //window.alert(11);
        this.seen=2;

      })


      // if (typeof(this.msg.mps)=="undefined"){
      //   this.msg=JSON.parse(localStorage.getItem("store"))
      // }
      // let arr0=[];
      // arr0.push(this.msg.ref);
      // this.items0=arr0;
      // console.log(this.msg);
      // let arr1=[];
      // arr1.push(this.msg.ref);
      // arr1.push(this.msg.mps);
      // this.items1=arr1;
      // //this.items1.push(this.msg.ops)
      // //this.items2=this.msg.ops;
      // for (var i in this.msg.ops) {
      //   this.items1.push(this.msg.ops[i]);
      // }
      // this.data1=this.msg.ms_snp.data;
      // this.layout1.xaxis.categoryarray=this.msg.ms_snp.carr;
      //
      //
      // // let arr2=[];
      // // for (var i in this.msg.ops) {
      // //   arr2.push(this.msg.bar_d2[i])
      // // }
      // this.data2=this.msg.bar_d2;
      // this.layout2.xaxis.categoryarray=this.msg.bar_l2;
      // this.data3=this.msg.pie_d3;
      // this.pda=this.msg.pda;
      // this.msaSrc=this.msg.msa_link;
      // this.nxtSrc=this.msg.nxt;
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
.inner-container42 {
  border: 0px solid black;
  width: 90%;
  height: 92%;
  text-align: justify;
  padding-bottom: 1000px;

}
.titler{
  padding:20px;
}

.pfontrl{
  font-size: 20px;
}
</style>
