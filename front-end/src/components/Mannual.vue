<template>

  <div class="container3">



    <div class="inner-container-mannual">
      <h3 class="heading4 fw-bold mt-5 text-pink " >Step-by-Step instructions</h3>
      <p class="fontpartm">- The usage of StrainDetect consists of two steps. Here, we use test fastq data contained in <router-link :to="{name: 'Detect'}" style="text-decoration: none">StrainKmer</router-link> to illustrate. After knowing each step, you can run StrainDetect with your own fastq data.  <br><br>- For fast test of "Detect" component, you can download the "Example data" in "Detect" page and submit the data directly.</p>
<!--      <br><br>- We also provide a video for the instructions. To watch it, click here.-->
      <h3 class="heading5 fw-bold mt-5 text-pink " >Step 1 - Run StrainKmer to extract featur files from raw sequencing data</h3>
      <p></p>

      <div class="pic-m1">
        <img src="../assets/mannual_pages_1.png" width="800px" height="400px"  class=" imgwf" alt="Step1">
        <img src="../assets/mannual_pages_2.png" width="800px" height="400px"  class=" imgwf" alt="Step1">
      </div>

      <h3 class="heading5 fw-bold mt-5 text-pink " >Step 2 - Upload feature files to "Detect" component to obtain the analysis report</h3>
      <div class="pic-m1">
        <img src="../assets/mannual_pages_3.png" width="800px" height="410px"  class=" imgwf" alt="Step2">
      </div>

      <h3 class="heading5 fw-bold mt-5 text-pink " >The explaination about the analysis report</h3>
      <div class="pic-m1">
        <img src="../assets/mannual_pages_4.png" width="800px" height="410px"  class=" imgwf" alt="Report">
        <img src="../assets/mannual_pages_5.png" width="810px" height="390px"  class=" imgwf" alt="Report">
        <img src="../assets/mannual_pages_6.png" width="830px" height="340px"  class=" imgwf" alt="Report">
      </div>
    </div>
    <!--<p>Mannual page</p>-->
    <!--    <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>-->
    <!--    <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>-->
  </div>
</template>

<script>
export default {
  name: 'Mannual',
  methods: {
    //锚点跳转
    goAnchor(selector) {/*参数selector是id选择器（#anchor14）*/
      document.querySelector(selector).scrollIntoView({
        behavior: "smooth"
      });
    },
  }
}
</script>

<style>

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
.inner-container-mannul{
  /*width: 90%;*/
  padding-left: 90px;
  padding-right: 90px;
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


</style>
