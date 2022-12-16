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
        <iframe src="https://strain.ee.cityu.edu.hk/HBV?s=MK720631.1，MK720628.1" scrolling="auto" frameborder="0" style="width: 100%;height: 700px;"></iframe>
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
    "sac": "Genbank:NC_003977",
    "sid": ">NC_003977.2",
    "sinfo": "Region:USA|Date:1987-06-07",
    "slink": "https://www.ncbi.nlm.nih.gov/nuccore/NC_003977",
       "cls": "Cluster20_60",
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
    "cls": "Cluster537_3",
    "mpscore": "0.988338356349242",
    "sac": "Genbank:MK720631",
    "sdepth": "531.6627906976744",
    "sid": ">MK720631.1",
    "sinfo": "Region:United Kingdom|Date:2019-10-26",
    "slink": "https://www.ncbi.nlm.nih.gov/nuccore/MK720631",
    "tmr": "321/321",
    "vmr": "321/321"
  };
     let ops=[
       {
         "stype": "OP",
         "cls": "Cluster535_4",
         "mpscore": "0.9732074580540687",
         "sac": "Genbank:MK720628",
         "sdepth": "59.23529411764706",
         "sid": ">MK720628.1",
         "sinfo": "Region:United Kingdom|Date:2019-10-26",
         "slink": "https://www.ncbi.nlm.nih.gov/nuccore/MK720628",
         "tmr": "321/321",
         "vmr": "23/321"
       }
     ];
     let arr1=[];
     arr1.push(ref);
     arr1.push(mps);
     this.items1=arr1;
     this.msaSrc="/static/ERR3253398.html";

      for (var i in ops){
        this.items1.push(ops[i]);
      }

     //this.items2=ops;

     let ms_data=[{'x': ['2688-C/C', '2689-T/T', '2690-A/A', '2691-G/G', '2692-G/G', '2693-A/A', '2768-T/T', '2769-T/T', '2770-G/G', '2772-T/T', '2773-G/G', '2774-A/A', '2775-C/C', '2776-A/A', '2779-A/A', '2780-A/A', '2781-T/T', '2782-C/C', '2783-C/C', '2784-T/T', '2785-C/C', '2807-A/A', '2808-C/C', '2810-A/A', '2811-T/T', '2820-G/G', '2821-T/T', '2822-C/C', '2823-T/T', '2824-A/A', '2825-G/G', '2826-A/A', '2827-C/C', '2828-T/T', '2829-C/C', '2830-G/G', '2831-T/T', '2832-G/G', '2843-G/G', '2844-G/G', '2845-A/A', '2846-C/C', '3089-C/C', '3090-T/T', '3091-C/C', '3092-A/A', '3093-T/T', '3094-C/C', '3095-T/T', '3096-T/T', '3101-C/C', '3102-T/T', '3103-T/T', '3104-G/G', '3105-T/T', '3106-T/T', '3107-G/G', '3108-G/G', '3110-T/T', '3111-C/C', '3112-T/T', '3113-T/T', '3114-C/C', '3115-T/T', '3116-G/G', '3117-G/G', '3118-A/A', '3119-C/C', '3120-T/T', '3121-A/A', '3122-T/T', '3123-C/C', '3178-A/A', '3377-G/G', '3378-A/A', '3379-C/C', '3380-G/G', '3381-G/G', '3382-A/A', '3383-A/A', '3392-T/T', '3393-G/G', '3394-T/T', '3395-A/A', '3396-T/T', '3397-T/T', '3398-C/C', '3414-T/T', '3415-G/G', '3416-G/G', '3417-G/G', '3418-C/C', '3419-T/T', '3420-T/T', '3436-C/C', '3437-T/T', '3439-T/T', '3441-G/G', '3442-G/G', '3446-G/G', '3447-G/G', '3448-G/G', '3450-C/C', '3472-A/A', '3473-G/G', '3475-T/T', '3552-T/T', '3553-G/G', '3567-G/G', '3568-C/C', '3569-T/T', '3570-T/T', '3571-T/T', '3572-C/C', '3573-A/A', '3574-G/G', '3575-T/T', '3576-T/T', '3577-A/A', '3578-T/T', '3610-G/G', '3611-G/G', '3612-G/G', '3613-G/G', '3614-C/C', '3615-C/C', '3616-A/A', '3617-A/A', '3618-G/G', '3619-T/T', '3620-C/C', '3621-T/T', '3622-G/G', '3623-T/T', '3624-A/A', '3625-C/C', '3626-A/A', '3628-C/C', '3629-A/A', '3668-G/G', '3669-A/A', '3670-G/G', '3671-T/T', '3673-C/C', '3674-C/C', '3694-T/T', '3696-T/T', '3698-T/T', '3699-A/A', '3700-C/C', '3701-C/C', '3703-C/C', '3704-T/T', '3705-G/G', '3706-T/T', '3707-T/T', '3753-C/C', '3754-A/A', '3755-T/T', '3756-T/T', '3757-T/T', '3758-A/A', '3759-A/A', '3760-A/A', '3762-C/C', '3766-A/A', '3767-C/C', '3774-C/C', '3776-A/A', '3777-A/A', '3779-A/A', '3780-G/G', '3781-A/A', '3782-T/T', '3800-G/G', '3801-G/G', '3802-G/G', '3803-G/G', '3805-T/T', '3806-A/A', '3808-T/T', '3809-C/C', '3811-C/C', '3812-T/T', '3814-A/A', '3815-A/A', '3816-T/T', '3817-T/T', '3822-T/T', '3824-A/A', '3825-T/T', '3826-G/G', '3827-G/G', '3828-G/G', '3829-T/T', '3830-T/T', '3831-A/A', '3832-T/T', '3833-G/G', '3834-T/T', '3836-A/A', '3837-T/T', '3838-T/T', '3839-G/G', '3840-G/G', '3841-A/A', '3887-C/C', '3888-C/C', '3889-A/A', '3890-C/C', '3891-A/A', '3893-G/G', '3894-A/A', '3895-A/A', '3897-A/A', '3898-C/C', '3908-A/A', '3909-A/A', '3947-T/T', '3949-C/C', '3951-T/T', '3953-T/T', '3955-A/A', '3956-A/A', '3957-C/C', '3959-G/G', '3960-G/G', '3961-C/C', '3962-C/C', '3963-T/T', '3989-A/A', '3990-A/A', '3991-A/A', '4004-A/A', '4005-T/T', '4006-G/G', '4007-T/T', '4008-C/C', '4073-C/C', '4075-T/T', '4076-T/T', '4077-T/T', '4078-T/T', '4080-G/G', '4081-G/G', '4083-T/T', '4084-T/T', '4085-T/T', '4087-C/C', '4088-T/T', '4089-G/G', '4090-C/C', '4091-C/C', '4204-A/A', '4205-G/G', '4206-C/C', '4207-A/A', '4221-G/G', '4222-C/C', '4293-A/A', '4294-C/C', '4295-A/A', '4320-C/C', '4321-C/C', '4323-T/T', '4324-T/T', '4325-C/C', '4326-T/T', '4327-G/G', '4328-T/T', '4329-G/G', '4330-T/T', '4332-A/A', '4333-A/A', '4334-C/C', '4335-A/A', '4336-A/A', '4337-T/T', '4338-A/A', '4348-T/T', '4349-G/G', '4350-A/A', '4412-T/T', '4413-G/G', '4414-C/C', '4415-C/C', '4416-C/C', '4417-G/G', '4418-G/G', '4436-G/G', '4437-G/G', '4438-C/C', '4439-C/C', '4440-A/A', '4441-G/G', '4442-G/G', '4443-T/T', '4444-C/C', '4445-T/T', '4447-T/T', '4448-G/G', '4449-C/C', '4469-C/C'], 'y': [1062, 1061, 1062, 1058, 1060, 2190, 1089, 1095, 1095, 1103, 1103, 1101, 1107, 1087, 1062, 1048, 1031, 1026, 1009, 973, 977, 966, 953, 934, 939, 903, 935, 954, 948, 965, 959, 965, 961, 963, 966, 955, 1029, 1047, 1037, 1038, 1029, 1030, 1122, 1113, 1104, 1100, 1116, 1128, 1126, 1125, 1140, 1145, 1146, 1140, 1142, 1134, 1142, 1131, 1103, 1102, 1114, 1108, 1110, 1118, 1077, 1063, 1041, 1003, 1003, 1000, 695, 1033, 1117, 1137, 1144, 792, 1128, 1123, 1120, 1114, 998, 994, 984, 990, 976, 974, 978, 1018, 1033, 1055, 1070, 1074, 1081, 1083, 1038, 1039, 1025, 1041, 1046, 1085, 1109, 1119, 1119, 961, 965, 961, 715, 718, 717, 716, 705, 659, 624, 622, 614, 604, 602, 598, 602, 595, 440, 443, 443, 445, 421, 385, 389, 355, 356, 345, 339, 336, 319, 318, 319, 311, 301, 293, 291, 285, 283, 271, 261, 202, 200, 198, 194, 191, 185, 181, 181, 178, 180, 103, 175, 178, 110, 105, 103, 103, 103, 52, 111, 111, 111, 109, 53, 110, 105, 101, 45, 105, 51, 106, 100, 101, 103, 101, 97, 94, 91, 95, 93, 94, 99, 98, 58, 98, 99, 94, 92, 94, 95, 93, 62, 92, 97, 99, 99, 99, 101, 101, 115, 119, 122, 123, 149, 149, 109, 146, 153, 162, 172, 166, 174, 137, 211, 217, 286, 288, 289, 293, 295, 293, 249, 298, 254, 310, 322, 324, 334, 331, 339, 346, 349, 350, 353, 347, 393, 401, 401, 400, 400, 405, 402, 402, 405, 417, 419, 418, 418, 378, 377, 408, 407, 405, 403, 408, 413, 417, 414, 407, 400, 404, 396, 383, 383, 384, 385, 387, 387, 391, 388, 389, 389, 374, 370, 369, 371, 405, 401, 396, 486, 487, 479, 477, 475, 477, 479, 467, 471, 324, 456, 453, 452, 450, 452, 434, 431, 429, 430, 428, 439], 'name': 'Same base', 'type': 'bar', 'marker': {'color': '#1f77b4'}, 'line': {'color': 'rgba(128,0,128,1.0)'}, 'width': 1}, {'x': ['2778-A/G', '3391-T/C', '3627-A/G', '3697-A/T', '3702-T/G', '3761-T/C', '3775-T/A', '3804-A/T', '3810-C/T', '3823-C/T', '3835-A/C', '3892-G/A', '3906-T/A', '3907-G/A', '3948-C/T', '3952-G/A', '3958-C/A', '4082-C/T'], 'y': [741, 1003, 295, 117, 175, 54, 51, 47, 94, 95, 101, 117, 208, 166, 239, 293, 249, 400], 'name': 'SNV', 'type': 'bar', 'marker': {'color': '#D62728'}, 'line': {'color': 'rgba(128,0,128,1.0)'}, 'width': 1}]
     this.data1=ms_data;

     let ms_carr=['2688-C/C', '2689-T/T', '2690-A/A', '2691-G/G', '2692-G/G', '2693-A/A', '2768-T/T', '2769-T/T', '2770-G/G', '2772-T/T', '2773-G/G', '2774-A/A', '2775-C/C', '2776-A/A', '2778-A/G', '2779-A/A', '2780-A/A', '2781-T/T', '2782-C/C', '2783-C/C', '2784-T/T', '2785-C/C', '2807-A/A', '2808-C/C', '2810-A/A', '2811-T/T', '2820-G/G', '2821-T/T', '2822-C/C', '2823-T/T', '2824-A/A', '2825-G/G', '2826-A/A', '2827-C/C', '2828-T/T', '2829-C/C', '2830-G/G', '2831-T/T', '2832-G/G', '2843-G/G', '2844-G/G', '2845-A/A', '2846-C/C', '3089-C/C', '3090-T/T', '3091-C/C', '3092-A/A', '3093-T/T', '3094-C/C', '3095-T/T', '3096-T/T', '3101-C/C', '3102-T/T', '3103-T/T', '3104-G/G', '3105-T/T', '3106-T/T', '3107-G/G', '3108-G/G', '3110-T/T', '3111-C/C', '3112-T/T', '3113-T/T', '3114-C/C', '3115-T/T', '3116-G/G', '3117-G/G', '3118-A/A', '3119-C/C', '3120-T/T', '3121-A/A', '3122-T/T', '3123-C/C', '3178-A/A', '3377-G/G', '3378-A/A', '3379-C/C', '3380-G/G', '3381-G/G', '3382-A/A', '3383-A/A', '3391-T/C', '3392-T/T', '3393-G/G', '3394-T/T', '3395-A/A', '3396-T/T', '3397-T/T', '3398-C/C', '3414-T/T', '3415-G/G', '3416-G/G', '3417-G/G', '3418-C/C', '3419-T/T', '3420-T/T', '3436-C/C', '3437-T/T', '3439-T/T', '3441-G/G', '3442-G/G', '3446-G/G', '3447-G/G', '3448-G/G', '3450-C/C', '3472-A/A', '3473-G/G', '3475-T/T', '3552-T/T', '3553-G/G', '3567-G/G', '3568-C/C', '3569-T/T', '3570-T/T', '3571-T/T', '3572-C/C', '3573-A/A', '3574-G/G', '3575-T/T', '3576-T/T', '3577-A/A', '3578-T/T', '3610-G/G', '3611-G/G', '3612-G/G', '3613-G/G', '3614-C/C', '3615-C/C', '3616-A/A', '3617-A/A', '3618-G/G', '3619-T/T', '3620-C/C', '3621-T/T', '3622-G/G', '3623-T/T', '3624-A/A', '3625-C/C', '3626-A/A', '3627-A/G', '3628-C/C', '3629-A/A', '3668-G/G', '3669-A/A', '3670-G/G', '3671-T/T', '3673-C/C', '3674-C/C', '3694-T/T', '3696-T/T', '3697-A/T', '3698-T/T', '3699-A/A', '3700-C/C', '3701-C/C', '3702-T/G', '3703-C/C', '3704-T/T', '3705-G/G', '3706-T/T', '3707-T/T', '3753-C/C', '3754-A/A', '3755-T/T', '3756-T/T', '3757-T/T', '3758-A/A', '3759-A/A', '3760-A/A', '3761-T/C', '3762-C/C', '3766-A/A', '3767-C/C', '3774-C/C', '3775-T/A', '3776-A/A', '3777-A/A', '3779-A/A', '3780-G/G', '3781-A/A', '3782-T/T', '3800-G/G', '3801-G/G', '3802-G/G', '3803-G/G', '3804-A/T', '3805-T/T', '3806-A/A', '3808-T/T', '3809-C/C', '3810-C/T', '3811-C/C', '3812-T/T', '3814-A/A', '3815-A/A', '3816-T/T', '3817-T/T', '3822-T/T', '3823-C/T', '3824-A/A', '3825-T/T', '3826-G/G', '3827-G/G', '3828-G/G', '3829-T/T', '3830-T/T', '3831-A/A', '3832-T/T', '3833-G/G', '3834-T/T', '3835-A/C', '3836-A/A', '3837-T/T', '3838-T/T', '3839-G/G', '3840-G/G', '3841-A/A', '3887-C/C', '3888-C/C', '3889-A/A', '3890-C/C', '3891-A/A', '3892-G/A', '3893-G/G', '3894-A/A', '3895-A/A', '3897-A/A', '3898-C/C', '3906-T/A', '3907-G/A', '3908-A/A', '3909-A/A', '3947-T/T', '3948-C/T', '3949-C/C', '3951-T/T', '3952-G/A', '3953-T/T', '3955-A/A', '3956-A/A', '3957-C/C', '3958-C/A', '3959-G/G', '3960-G/G', '3961-C/C', '3962-C/C', '3963-T/T', '3989-A/A', '3990-A/A', '3991-A/A', '4004-A/A', '4005-T/T', '4006-G/G', '4007-T/T', '4008-C/C', '4073-C/C', '4075-T/T', '4076-T/T', '4077-T/T', '4078-T/T', '4080-G/G', '4081-G/G', '4082-C/T', '4083-T/T', '4084-T/T', '4085-T/T', '4087-C/C', '4088-T/T', '4089-G/G', '4090-C/C', '4091-C/C', '4204-A/A', '4205-G/G', '4206-C/C', '4207-A/A', '4221-G/G', '4222-C/C', '4293-A/A', '4294-C/C', '4295-A/A', '4320-C/C', '4321-C/C', '4323-T/T', '4324-T/T', '4325-C/C', '4326-T/T', '4327-G/G', '4328-T/T', '4329-G/G', '4330-T/T', '4332-A/A', '4333-A/A', '4334-C/C', '4335-A/A', '4336-A/A', '4337-T/T', '4338-A/A', '4348-T/T', '4349-G/G', '4350-A/A', '4412-T/T', '4413-G/G', '4414-C/C', '4415-C/C', '4416-C/C', '4417-G/G', '4418-G/G', '4436-G/G', '4437-G/G', '4438-C/C', '4439-C/C', '4440-A/A', '4441-G/G', '4442-G/G', '4443-T/T', '4444-C/C', '4445-T/T', '4447-T/T', '4448-G/G', '4449-C/C', '4469-C/C']
     this.layout1.xaxis.categoryarray=ms_carr;

     this.data2=[{
       'x': ['>MK720631.1'],
       'y': [ 531.6627906976744],
       'marker': {'color': 'rgba(222,45,38,0.8)'},
       'name': 'Most possible strain',
       'type': 'bar'
     },{
       'x': ['>MK720628.1'],
       'y': [ 59.23529411764706],
       'marker': {'color': 'rgba(204,204,204,1)'},
       'name': 'Other possible strain(s)',
       'type': 'bar'
     }
     ];
     this.layout2.xaxis.categoryarray=['>MK720631.1','>MK720628.1'];

     this.data3=[
       {
         'values': [89.97537889530301, 10.024621104696994],
         'labels': ['>MK720631.1','>MK720628.1'],
         'type': 'pie',
         'hole': 0.4
       }

     ]
     this.pda=[{
       'x': ['>MK720631.1'],
       'y': [ 531.6627906976744],
       'marker': {'color': 'rgba(222,45,38,0.8)'},
       'name': 'Most possible strain',
       'type': 'bar'
     },{
       'x': ['>MK720628.1'],
       'y': [ 59.23529411764706],
       'marker': {'color': 'rgba(204,204,204,1)'},
       'name': 'Other possible strain(s)',
       'type': 'bar'
     },
       {
         'values': [89.97537889530301, 10.024621104696994],
         'labels': ['>MK720631.1','>MK720628.1'],
         'type': 'pie'
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
