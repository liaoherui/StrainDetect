<template>


  <div class="container3">

    <div style="position:fixed;top:160px;left:30px;background-color: white;"  class="list-group">
      <a href="#" class="list-group-item list-group-item-action ">
        Top
      </a>
      <a href="javascript:void(0)" @click="goAuchor('#div2')" class="list-group-item list-group-item-action">Step1</a>
      <a href="javascript:void(0)" @click="goAuchor('#div3')" class="list-group-item list-group-item-action">Step2</a>
      <a href="javascript:void(0)" @click="goAuchor('#div4')" class="list-group-item list-group-item-action">Output</a>
      <a href="javascript:void(0)" @click="goAuchor('#div5')" class="list-group-item list-group-item-action " >Compatibility</a>
    </div>

<!--    <div style="position:fixed;top:160px;left:30px;background-color: white;" class="ancle">-->
<!--      <p>-->
<!--        <a href="#div1" style="text-decoration: none">- Top -</a>-->
<!--      </p>-->
<!--      <p>-->
<!--        <a href="#div2" style="text-decoration: none">- Step 1 -</a>-->
<!--      </p>-->
<!--      <p>-->
<!--        <a href="#div3" style="text-decoration: none">- Step 2 -</a>-->
<!--      </p>-->
<!--      <p>-->
<!--        <a href="#div4" style="text-decoration: none">- Output -</a>-->
<!--      </p>-->
<!--      <p>-->
<!--        <a href="#div5" style="text-decoration: none">- Compatibility -</a>-->
<!--      </p>-->
<!--    </div>-->

    <div class="inner-container-mannual">
      <div class="banner_ma">
<!--        <div id="div1"></div>-->
      <h3 class="heading4 fw-bold mt-5 text-pink " id="div1">Step-by-Step instructions</h3>
      <p class="fontpartm" id="div2">- The usage of StrainDetect consists of two steps. Here, we use test fastq data contained in <router-link :to="{name: 'Detect'}" style="text-decoration: none">StrainKmer</router-link> to illustrate. You can download the StrainKmer GUI tool and follow each step. After knowing each step, you can run StrainDetect with your own fastq data.  <br><br>- For fast test of "Detect" component, you can download the "Example data" in "Detect" page and submit the data directly.</p>
      <!--      <br><br>- We also provide a video for the instructions. To watch it, click here.-->
<!--        <div id="div2"></div>-->
      <h3 class="heading5 fw-bold mt-5 text-pink " >Step 1 - Run StrainKmer to extract featur files from raw sequencing data</h3>
      <p></p>

      <div class="pic-m1" >
        <img src="../assets/mannual_pages_1.png" width="800px" height="400px"  class=" imgwf" alt="Step1">
        <img src="../assets/mannual_pages_2.png" width="800px" height="400px"  class=" imgwf" alt="Step1" id="div3">
      </div>

      <h3 class="heading5 fw-bold mt-5 text-pink " >Step 2 - Upload feature files to "Detect" component to obtain the analysis report</h3>
      <div class="pic-m1">
        <img src="../assets/mannual_pages_3.png" width="800px" height="410px"  class=" imgwf" alt="Step2" id="div4">
      </div>

      <h3 class="heading5 fw-bold mt-5 text-pink " >The explaination about the analysis report</h3>
      <p class="fontpartm">To check the output report of real data, you can go to <router-link :to="{name: 'Example'}" style="text-decoration: none">Example</router-link> page. All datasets tested in Example are downloaded from <a href="https://www.ncbi.nlm.nih.gov/sra/" style="text-decoration: none">NCBI SRA database</a>.</p>
      <div class="pic-m1">
        <img src="../assets/mannual_pages_4.png" width="800px" height="410px"  class=" imgwf" alt="Report">
        <img src="../assets/mannual_pages_5.png" width="810px" height="390px"  class=" imgwf" alt="Report">
        <img src="../assets/mannual_pages_6.png" width="830px" height="340px"  class=" imgwf" alt="Report">
      </div>

        <h3 class="heading5 fw-bold mt-5 text-pink " id="div5">Compatibility test</h3>

        <div class="pic-m2">
          <p >Browser compatibility</p>
          <b-table :items="items" :fields="fields" style="width: 100%;" ></b-table>
          <p >StrainKmer compatibility</p>
          <b-table :items="items2" :fields="fields2" style="width: 100%;" ></b-table>
        </div>

        </div>

    </div>

    <!--<p>Mannual page</p>-->
    <!--    <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>-->
    <!--    <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>-->
  </div>
</template>

<script>
export default {
  data(){
    return {
      fields: ['OS','Version', 'Chrome', 'Firefox','MicrosoftEdge','Safari'],
      items: [
        {  OS: 'Linux',Version:'pop-os 18.04 LTS',Chrome: '108.0.5359.94', Firefox: '108.0.1', MicrosoftEdge:'n/a', Safari:'n/a'},
        { OS: 'MacOs',Version:'Monterey',Chrome: "108.0.5359.124" , Firefox: '108.0.1', MicrosoftEdge:'n/a', Safari:'16.0' },
        { OS: 'Windows',Version:10,Chrome: ' 108.0.5359.125', Firefox: '108.0.1', MicrosoftEdge:'108.0.1462.46', Safari:'n/a'}
      ],
      fields2: ['OS','Version','Disk', 'Memory', 'Number_of_CPUs'],
      items2: [
        {  OS: 'Linux',Version:'pop-os 18.04 LTS',Disk: '512G', Memory: '32G', Number_of_CPUs:'8'},
        { OS: 'MacOs',Version:'Monterey',Disk: "512G" , Memory: '16G', Number_of_CPUs:'10'},
        { OS: 'Windows',Version:10,Disk: '512G', Memory: '16G', Number_of_CPUs:'6'}
      ]
    }
  },
  methods:{
    goAuchor(id){
      console.log(id)
      document.querySelector(id).scrollIntoView(true)
      var auchor=this.$el.querySelector(id)
      // console.log(auchor)
      // console.log(auchor.getBoundingClientRect().top)
      // document.body.scrollTop=auchor.offsetTop
    }
  }
};

</script>

<style>
.banner_ma{
  padding-left: 120px;
  text-align: left;
}
/*.container3 {*/
/*  display: flex;*/
/*  !*align-items: center;*!*/
/*  !*justify-content: center;*!*/
/*  flex-wrap: wrap;*/
/*  !*height: 100vh;*!*/
/*}*/
.pic-m1 {
  width: 50%;
  height: 40%;
  margin: 50px;
  /*display: flex;*/
  /*justify-content: left;*/
  /*align-items: left;*/
  margin-left: 10%;
  margin-right: 10%;
  padding-left:100px;
  /*border: 2px solid;*/
}
.pic-m2{
  width: 70%;
  height: 40%;
  margin: 50px;
  /*display: flex;*/
  /*justify-content: left;*/
  /*align-items: left;*/
  margin-left: 10%;
  margin-right: 10%;
  padding-left:100px;
  padding-bottom: 30px;
}
.inner-container-mannul{
  /*width: 90%;*/
  padding-left: 120px;
  /*padding-right: 90px;*/
  padding-bottom: 20px;
}

.heading4{
  text-align: center;
  font-size: 35px;
  padding: 30px;
  /*padding-left: 90px;*/

}
.fontpartm{
  text-align: left;
  padding-left: 90px;
  padding-right: 90px;
  font-size: 20px;
}
.heading5{
  text-align: left;
  padding-left: 90px;
  font-size: 25px;
  /*padding: 30px;*/
}

.ancle{
  padding-right: 70px;
}
</style>
