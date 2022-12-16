<template>
  <div class="containerr1">
    <div class="inner-containerr1">

      <div class="titler1"><h1 class="text-center fw-bold mt-6 text-pink">Result</h1></div>
      <div class="px-7"><hr class="mt-2"/></div>

      <div class="abundance1 rpc" style="margin-top:20px;">
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

      <div class="info1 rpc" style="margin-top:20px;">
        <h5> 2. Detailed information about identified strain(s)</h5>

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


      <div class="hist1 rpc" style="margin-top:18px;">
        <h5> 3. Histogram of site coverage of the most possible strain &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          <vue-json-to-csv :json-data="data1" :csv-title="'siteInfo'">
            <b-button style="width: 10%; font-size: 15px !important;" variant="primary">
              <i class="fa fa-download"></i>&nbsp;<b>Download</b>
            </b-button>
          </vue-json-to-csv> </h5>
        <Plotly :data="data1" :layout="layout1" ></Plotly>
      </div>

      <div class="msa1 rpc" style="margin-top:18px;">
        <h5> 4. The msa alignment visualization of identified strain(s)</h5>
        <div>
          <!--          <iframe  src="/static/SRR961514.html" scrolling="auto" frameborder="0" style="width: 100%;height: 200px;"></iframe>-->
          <iframe v-bind:src="msaSrc" scrolling="auto" frameborder="0" style="width: 100%;height: 200px;"></iframe>
        </div>
      </div>

      <div class="auspice1 rpc" style="margin-top:18px; margin-bottom:18px;">
        <h5> 5. The auspice page of identified strain(s)</h5>
        <iframe src="https://strain.ee.cityu.edu.hk/H1N1?s=A/Hunan-Wuling/1468/2018" scrolling="auto" frameborder="0" style="width: 100%;height: 700px;"></iframe>
        <!--        &nbsp;&nbsp;&nbsp;&nbsp;<b-button style="width: 10%; font-size: 18px !important;" variant="primary" v-on:click="gotosite_nextstrain()"> <i class="fa fa-arrow-right"></i>&nbsp;Go!</b-button>-->
      </div>



      <!--                <b-card class="text-left" bg-variant="dark" text-variant="white">-->
      <!--                  <div >-->
      <!--                <b>Download the report</b>-->
      <!--                   </div>-->
      <!--                 </b-card>-->
      <!--                  <button type="button" class="download-btn" v-on:click="download">Download</button>-->
    </div>
  </div>
</template>

<script>


import { BTable } from 'bootstrap-vue'
import { Plotly } from 'vue-plotly'
import XLSX from 'xlsx';
import VueJsonToCsv from 'vue-json-to-csv'
// import '../modules/msa.min';

export default {
  name: 'Mannual',

  data(){
    return{
      msaViewer: null,
      msaSrc: null,
      fields0:[
        {key: 'stype',sortable: false,'label':'Strain \nType'},
        {key: 'sid',sortable: false,'label':'Strain \nID'},
        {key: 'sinfo',sortable: false,'label':'Metadata'},
        {key: 'slink',sortable: false,'label':'Download\n Link'},
        {key: 'sac',sortable: false,'label':'Accession'},
      ],
      items0:[],
      fields1:[
        {key: 'stype',sortable: false,'label':'Strain Type'},
        {key: 'sid',sortable: false,'label':'Strain ID'},
        {key: 'cls',sortable: false,'label':'Strain Cls'},
        {key: 'mpscore',sortable: true,'label':'Mapping score'},
        {key: 'vmr',sortable: true,'label':'Valid map rate'},
        {key: 'tmr',sortable: true,'label':'Total  map rate'},
        {key: 'sdepth',sortable: true,'label':'Predicted depth'},
        {key: 'sinfo',sortable: false,'label':'Metadata'},
        {key: 'slink',sortable: false,'label':'Download Link'},
        {key: 'sac',sortable: false,'label':'Accession'},
      ],
      items1:[],
      fields2:[
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
      items2:[],
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
  },
  methods:{
    getMessage(){
      let ref={
        "stype": "Ref",
        "sac": "GISAID:EPI705910",
        "sid": ">A/California/7/2009",
        "sinfo": "Region:California|Date:2009",
        "slink": "https://gisaid.org",
        "cls": "Cluster26_2",
        "mpscore": "NA",
        "sdepth": "NA",
        "tmr": "NA",
        "vmr": "NA"
      };
      // let arr0=[];
      // arr0.push(ref);
      //this.items0=arr0;

      let mps={
        "stype": "MP",
        "cls": "Cluster164_2",
        "mpscore": "0.9907353849472063",
        "sac": "GISAID:EPI1312145",
        "sdepth": "2795.4367816091954",
        "sid": ">A/Hunan-Wuling/1468/2018",
        "sinfo": "Region:Hunan-Wuling|Date:2018|Clade:6B.1A",
        "slink": "https://gisaid.org",
        "tmr": "109/119",
        "vmr": "109/119"
      };
      let ops=[
      ];
      let arr1=[];
      arr1.push(ref);
      arr1.push(mps);
      this.items1=arr1;
      this.msaSrc="/static/SRR15011445.html";

      for (var i in ops){
        this.items1.push(ops[i]);
      }

      //this.items2=ops;

      let ms_data=[{'x': ['881-G/G', '882-G/G', '883-G/G', '886-A/A', '889-G/G', '890-A/A', '891-A/A', '892-C/C', '893-T/T', '894-A/A', '895-T/T', '896-T/T', '898-C/C', '902-A/A', '903-C/C', '904-A/A', '905-C/C', '907-A/A', '908-G/G', '910-A/A', '911-G/G', '912-A/A', '913-G/G', '914-C/C', '917-G/G', '919-A/A', '922-C/C', '924-A/A', '925-A/A', '926-A/A', '928-A/A', '929-A/A', '930-C/C', '931-A/A', '932-T/T', '934-C/C', '937-A/A', '938-G/G', '939-C/C', '940-A/A', '943-T/T', '946-A/A', '947-A/A', '949-T/T', '950-C/C', '952-A/A', '953-G/G', '955-G/G', '956-G/G', '957-T/T', '958-A/A', '961-G/G', '964-A/A', '965-T/T', '966-A/A', '967-T/T', '968-G/G', '969-C/C', '970-A/A', '973-C/C', '975-C/C', '976-A/A', '977-A/A', '979-G/G', '980-G/G', '981-A/A', '982-A/A', '983-A/A', '984-G/G', '985-A/A', '986-A/A', '987-A/A', '988-T/T', '989-G/G', '990-C/C', '991-T/T', '992-G/G', '993-G/G', '994-A/A', '995-T/T', '996-C/C', '997-T/T', '1002-T/T', '1003-T/T', '1004-A/A', '1006-C/C', '1007-A/A', '1008-T/T', '1009-T/T', '1012-A/A', '1013-G/G', '1014-A/A', '1015-T/T', '1016-A/A', '1017-C/C', '1018-A/A', '1019-C/C', '1020-C/C', '1021-A/A', '1022-G/G', '1037-A/A', '1039-A/A', '1041-C/C', '1042-T/T', '1045-T/T'], 'y': [2688, 2680, 2684, 2713, 2643, 2643, 2639, 2610, 2612, 2625, 2633, 2630, 2649, 2553, 2483, 2465, 2435, 2443, 2447, 2457, 2462, 2491, 2499, 2506, 2796, 2839, 2832, 2856, 2867, 2863, 2846, 2853, 2852, 2864, 2870, 2874, 2904, 2876, 2851, 2843, 2845, 2848, 2844, 2848, 2828, 2853, 2802, 2776, 2779, 2790, 2775, 2730, 2734, 2739, 2737, 2760, 2885, 2890, 2901, 2928, 2989, 2987, 2998, 2995, 2989, 2970, 2976, 2962, 2953, 2947, 2952, 2946, 2944, 2946, 2916, 2898, 2904, 2893, 2901, 2803, 2802, 2794, 2813, 2804, 2812, 2826, 2822, 2794, 2779, 2795, 2775, 2731, 2739, 2733, 2735, 2751, 2727, 2727, 2736, 2735, 2832, 2836, 2830, 2808, 2808], 'name': 'Same base', 'type': 'bar', 'marker': {'color': '#1f77b4'}, 'line': {'color': 'rgba(128,0,128,1.0)'}, 'width': 1}, {'x': ['916-A/G', '974-A/G', '1023-C/T', '1048-G/A'], 'y': [2624, 2953, 2748, 2762], 'name': 'SNV', 'type': 'bar', 'marker': {'color': '#D62728'}, 'line': {'color': 'rgba(128,0,128,1.0)'}, 'width': 1}]
      this.data1=ms_data;

      let ms_carr=['881-G/G', '882-G/G', '883-G/G', '886-A/A', '889-G/G', '890-A/A', '891-A/A', '892-C/C', '893-T/T', '894-A/A', '895-T/T', '896-T/T', '898-C/C', '902-A/A', '903-C/C', '904-A/A', '905-C/C', '907-A/A', '908-G/G', '910-A/A', '911-G/G', '912-A/A', '913-G/G', '914-C/C', '916-A/G', '917-G/G', '919-A/A', '922-C/C', '924-A/A', '925-A/A', '926-A/A', '928-A/A', '929-A/A', '930-C/C', '931-A/A', '932-T/T', '934-C/C', '937-A/A', '938-G/G', '939-C/C', '940-A/A', '943-T/T', '946-A/A', '947-A/A', '949-T/T', '950-C/C', '952-A/A', '953-G/G', '955-G/G', '956-G/G', '957-T/T', '958-A/A', '961-G/G', '964-A/A', '965-T/T', '966-A/A', '967-T/T', '968-G/G', '969-C/C', '970-A/A', '973-C/C', '974-A/G', '975-C/C', '976-A/A', '977-A/A', '979-G/G', '980-G/G', '981-A/A', '982-A/A', '983-A/A', '984-G/G', '985-A/A', '986-A/A', '987-A/A', '988-T/T', '989-G/G', '990-C/C', '991-T/T', '992-G/G', '993-G/G', '994-A/A', '995-T/T', '996-C/C', '997-T/T', '1002-T/T', '1003-T/T', '1004-A/A', '1006-C/C', '1007-A/A', '1008-T/T', '1009-T/T', '1012-A/A', '1013-G/G', '1014-A/A', '1015-T/T', '1016-A/A', '1017-C/C', '1018-A/A', '1019-C/C', '1020-C/C', '1021-A/A', '1022-G/G', '1023-C/T', '1037-A/A', '1039-A/A', '1041-C/C', '1042-T/T', '1045-T/T', '1048-G/A']
      this.layout1.xaxis.categoryarray=ms_carr;

      this.data2=[{
        'x': ['>A/Hunan-Wuling/1468/2018'],
        'y': [ 2795.4367816091954],
        'marker': {'color': 'rgba(222,45,38,0.8)'},
        'name': 'Most possible strain',
        'type': 'bar'
      }
      ];
      this.layout2.xaxis.categoryarray=['>A/Hunan-Wuling/1468/2018'];

      this.data3=[
        {
          'values': [100],
          'labels': ['>A/Hunan-Wuling/1468/2018'],
          'type': 'pie',
          'hole': 0.4
        }

      ]
      this.pda=[{
        'x': ['>A/Hunan-Wuling/1468/2018'],
        'y': [ 2795.4367816091954],
        'marker': {'color': 'rgba(222,45,38,0.8)'},
        'name': 'Most possible strain',
        'type': 'bar'
      },
        {
          'values': [100],
          'labels': ['>A/Hunan-Wuling/1468/2018'],
          'type': 'pie',
          'hole': 0.4
        }

      ]



    },
    gotosite(producturl){
      //window.location.href = producturl
      window.open(producturl)
    },
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
/*@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css");*/
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
.containerr1 {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  padding-top: 40px;
  /*height: 340vh;*/
  /*background-color: #F3F3F3;*/
}
.inner-containerr1 {
  border: 0px solid black;
  width: 90%;
  height: 92%;
  text-align: justify;
}
.titler1{
  padding:20px;
}
.abundance1{
  background-color: white;
  box-shadow: 0px 0.5px 10px  rgb(180, 180, 180);
  border: 1px solid #D5DFE6;
}
.info1{
  background-color: white;
  box-shadow: 0px 0.5px 10px  rgb(180, 180, 180);
  border: 1px solid #D5DFE6;
}

.hist1{
  background-color: white;
  box-shadow: 0px 0.5px 10px  rgb(180, 180, 180);
  border: 1px solid #D5DFE6;
}
.msa1{
  background-color: white;
  box-shadow: 0px 0.5px 10px  rgb(180, 180, 180);
  border: 1px solid #D5DFE6;
}

.auspice1{
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
