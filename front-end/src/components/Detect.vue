<template>

    <div class="container1">
      <!-- Comments -->
      <div class="inner-container1">

        <div class="center">
          <h1 class="text-center fw-bold mt-5 text-pink"><font   color="#9E426E">StrainKmer</font></h1>
          <div class="px-6"><hr class="mt-6"/></div>
          <div class="off-center">
            <p>To use StrainDetect, you may need to obtain the feature files from your sequencing data firstly.
              Thus, We have provided a user-friendly GUI tool named StrainKmer for your usage.
              All you need to do is download StrainKmer and the associated species-specific database. Then run StrainKmer and you can easily get two required feature files (*.npz and *_sub.npz).
              Finally, you can upload these feature files to "Detect" componnet to obtain your viral strain composition analysis report. </p>

            <h6><b>Download GUI tools</b> </h6>
            <p>(Tools, test fastq data and all pre-built databases are packed in the same zip file.)</p>
            <a href="https://strain.ee.cityu.edu.hk/strainkmer/StrainKmer_Windows.zip" style="text-decoration: none;"> Windows version (GUI tool)</a> <a href="https://strain.ee.cityu.edu.hk/strainkmer/StrainKmer_Mac.zip" style="margin-left:20px; text-decoration: none;"> Mac version (GUI tool)</a> <a href="https://github.com/liaoherui/StrainKmer" style="margin-left:20px; text-decoration: none;"> Linux version (cmd tool)</a>
            <p></p>
            <p>You can also download StrainKmer via Google drive if the link above fails.</p>
            <a href="https://drive.google.com/file/d/1xg5Vd6KajFB9CG53JNl75e8Mb-iwmEcH/view?usp=sharing" style="text-decoration: none;"> Windows version (GUI tool, Google drive)</a> <a href="https://drive.google.com/file/d/1cAzu1wjGW2Z6qE7A8VbyJetdH4MUOdwp/view?usp=sharing" style="margin-left:20px; text-decoration: none;"> Mac version (GUI tool, Google drive)</a>
            <p></p>
            <p>1. Note that opening the GUI tool may take some time, be patient please.<br>2. Note that Mac users need to open terminal and modify "~/.zshrc" file before running KMC in the StrainKmer:</p>
            <p> - vi ~/.zshrc<br>- add "ulimit -n 2048" to this file, save and quit.<br>- bash ~/.zshrc</p>
            <p>More details about this step can be found via <a href="https://github.com/refresh-bio/KMC" style="text-decoration: none;">KMC github page</a></p>
          </div>
          <div class="px-6"><hr class="mt-6"/></div>

          <h1 class="text-center fw-bold mt-5 text-pink"><font color="#667EEA">Detect</font></h1>
          <div class="px-6"><hr class="mt-6"/></div>
          <h5>Step 1 - Upload the feature files</h5>
          <p >Please upload files via the buttons below.</p>
          <form @submit.prevent="onSubmit" enctype="multipart/form-data">
            <div class="form-outline form-white mb-3">
              <input type="file" id="formfile1" class="form-control form-control-lg" />
              <label class="form-label" for="typeFile">&nbsp;Feature file 1 (named *.npz) &nbsp;&nbsp;  </label>
              <a  href="/static/SRR15224359.npz" download="SRR15224359.npz" style="text-decoration: none"> Example data (SCOV2) &nbsp;</a>
              <a  href="/static/SRR961514.npz" download="SRR961514.npz" style="text-decoration: none"> Example data (HIV) </a>
            </div>
            <div class="form-outline form-white mb-3">
              <input type="file" id="formfile2" class="form-control form-control-lg" />
              <label class="form-label" for="typeFile">&nbsp;Feature file 2 (named *_sub.npz) &nbsp;&nbsp; </label>
              <a  href="/static/SRR15224359_sub.npz" download="SRR15224359_sub.npz" style="text-decoration: none"> Example data (SCOV2) &nbsp;</a>
              <a  href="/static/SRR961514_sub.npz" download="SRR961514_sub.npz" style="text-decoration: none"> Example data (HIV) </a>
            </div >
            <h5>Step 2 - Choose targeted species <br><br></h5>
            <p >Please select which strain of virus you would like to identify. </p>
            <div class="form-outline form-white mb-3">
              <select class="form-select" aria-label="Default select example" id="vtype">
                <option selected>Select the species type</option>
                <option value="SCOV2">SCOV2</option>
                <option value="H1N1">H1N1</option>
                <option value="HIV">HIV</option>
                <option value="HBV">HBV</option>
                <option value="Ebola">Ebola</option>
                <option value="Dengue">Dengue</option>
                <option value="Zika">Zika</option>
                <option value="Entero">Entero</option>

              </select>
            </div>

            <h5>Step 3 - Submit <br><br></h5>
            <button   class="btn btn-outline-secondary btn-lg px-5" type="submit" >Detect</button>

            <div v-if="seen==1">
              <p><br><img src="../assets/Loading.gif" width="40" height="40" alt="">&nbsp;&nbsp;&nbsp;The job is running. Please wait or you can access the result via <b>https://strain.ee.cityu.edu.hk/#/res</b> later.</p>
            </div>
            <div v-else-if="seen==2">
              <p> <br><img src="../assets/error.png" width="40" height="40" alt=""> &nbsp;Something wrong. The job is failed. Please check or send emails to heruiliao2-c@my.cityu.edu.hk! </p>
            </div>
            <div v-else-if="seen==3">
              <p> <br><img src="../assets/error.png" width="40" height="40" alt=""> &nbsp;Please fill out all required items in the form and click "Detect" again! </p>
            </div>
            <div v-else>
              <p><br>The identification process usually takes 1~3 mins. You can also access the result via the given link later...</p>
            </div>



          </form>

        </div>
      </div>
    </div>


</template>

<script>
import axios from 'axios'
//import {Loading} from 'element-ui'



export default {
name: 'Detect',
  data(){
    return{
      seen: 0
    }
  },
methods: {

onSubmit(e){
var formData = new FormData();
var file1 = document.querySelector('#formfile1');
var file2 = document.querySelector('#formfile2');

var sel=document.querySelector("#vtype");
var ind=sel.selectedIndex;
var val=sel[ind].value;

try{
formData.append(file1.files[0].name, file1.files[0]);
formData.append(file2.files[0].name,file2.files[0]);
formData.append("vtype",val);
if (val!="Select the species type") {
    this.seen = 1;
  }else{
    this.seen=3;
  }
}catch(error) {
    //window.alert('');
    this.seen=3;
    //console.error(error);
  }

const path="https://strain.ee.cityu.edu.hk/api/detect"

//let loadingInstance = Loading.service(
// {
// text: 'Loading... Can access your results via http://localhost:8080/#/res later...',
// spinner: 'el-icon-loading',
// background: 'rgba(0,0,0,0.7)',
// fullscreen: true
// }
// );

axios.post(path, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
}).then( (response) =>{
       //loadingInstance.close()
       localStorage.setItem('store',JSON.stringify(response.data))
       this.$router.push({name:"Result",params: response.data})
}).catch ((error)=>{
  console.log(error);
  //window.alert(11);
  if  (this.seen!=3){
    this.seen=2;
  }
})

}
}
}

</script>

<style>

body {
  margin: 10;
}

.container1 {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  padding-top: 10px;
  /*height: 180vh;*/
}


.inner-container1 {
  border: 0px solid black;
  width: 60%;
  height: 90%;
  text-align: justify;
}


</style>
