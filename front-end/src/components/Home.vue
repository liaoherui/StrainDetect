<template>



  <div class="container-fluid">
    <div class="inner-container-home">
    <div class="banner-2 ">
      <h3 class="heading3 fw-bold mt-5 text-pink " >What can StrainDetect do?</h3>
      <div class="card">
        <div class="fontpart">
          <h3 class="project-title fw-bold  item">Introduction</h3>
          <p class="font-work_sans ppart">
            StrainDetect is an online extension of <b><a href="https://github.com/liaoherui/VirStrain" style="text-decoration: none">VirStrain</a></b>, which can identify viral strains from sequencing data efficiently and accurately.
            There are two major components of StrainDetect. The first component is a GUI tool called <b><font  color="#9E426E" class="cfont">StrainKmer</font></b>, which allows the user to extract features from raw sequencing data on a personal PC. After acquiring the feature files, the user can upload the files to the second component, the <b><font class="cfont" color="#667EEA">Detect</font></b> page of StrainDetect, to perform viral strain detection. <br/><b>(Statement: This website is free and open to all users and there is no login requirement.)</b>
                      </p>
          <h3 class="project-title fw-bold  item">The workflow of StrainDetect</h3>
          <div class="pic">
          <img src="../assets/images/background.png"  class=" imgwf" alt="The workflow of StrainDetects">
            </div>
          <router-link :to="{name: 'Detect'}">
                      <button type="button" class="btn btn-dark text-uppercase  text-light fw-bold px-sm-4 py-sm-3 Stars" >

                       Start your detection!

                      </button>
          </router-link>
        <div>&nbsp;</div>
                    </div>
            <!--        <div class="card-image bg-green-100">-->
<!--          <img-->

<!--            src="../assets/logo.png"-->
<!--          />-->
<!--        </div>-->
      </div>
      </div>

<!--      Database statistics-->
      <h2 class="heading6 fw-bold mt-5 text-pink " >Statistics of strains in pre-built databases</h2>
      <div class="inner-container-home3">

        <div class="banner-2 ">
          <p class="font-work_sans ppart">Currently, there are 22530 strains covering 8 different human-related viruses in our pre-built databases.
            These strains are downloaded from <a href="https://www.ncbi.nlm.nih.gov/" style="text-decoration: none">NCBI</a>, <a href="https://gisaid.org/" style="text-decoration: none">GISAID</a>, and <a href="https://www.hiv.lanl.gov/" style="text-decoration: none">HIVdb</a>, respectively. </p>
          <div >
            <img src="../assets/db_statistics.png"  class=" imgwf" width="850px" height="450px" alt="The database statistics">
          </div>
          <p></p>
          <p class="font-work_sans ppart">For each virus, there is an <a href="https://docs.nextstrain.org/projects/auspice/en/stable/" style="text-decoration: none">auspice</a> dashboard provided by <a href="https://nextstrain.org/" style="text-decoration: none">Nextstrain team</a>, you can check these auspice pages via:
            <a href="https://strain.ee.cityu.edu.hk/ncov/open/global/all-time" style="text-decoration: none">SARS-CoV-2</a>,
            <a href="https://strain.ee.cityu.edu.hk/HIV?c=subtype" style="text-decoration: none">HIV</a>,
            <a href="https://strain.ee.cityu.edu.hk/H1N1" style="text-decoration: none">H1N1</a>,
            <a href="https://strain.ee.cityu.edu.hk/HBV" style="text-decoration: none">HBV</a>,
            <a href="https://strain.ee.cityu.edu.hk/Dengue" style="text-decoration: none">DENV</a>,
            <a href="https://strain.ee.cityu.edu.hk/Zika" style="text-decoration: none">Zika</a>,
            <a href="https://strain.ee.cityu.edu.hk/Ebola" style="text-decoration: none">Ebola</a>,
            <a href="https://strain.ee.cityu.edu.hk/Entero" style="text-decoration: none">EV-D68</a>.
          </p>
        </div>
      </div>


    <!-- Other tools -->
    <div class="row mt-5 ">
      <h1 class="fw-bold mt-5 text-pink sp" >Other tools you may be interested</h1>
<!--      <div class="px-5"><hr class="mt-5"/></div>-->

      <div class="col-sm m-sm-5 p-sm-4">
        <div class="pt-3" >
          <!-- Bootstrap -->
          <div class="col-sm ">
            <!--                    <div class="col-sm fs-3 d-inline p-2 shadow bg-light rounded-circle">-->
            <!--                      <fa :icon="['fab','bootstrap']" class="text-other"/>-->
            <img src="../assets/sc.png" width="55" height="40" class="img-thumbnail text-other" alt="">
            <!--                    </div>-->
            <div class="pt-3" >
              <h5 class="fw-bold">StrainScan</h5>
              <p class="fs-6 text-secondary"><a href="https://github.com/liaoherui/StrainScan" style="text-decoration: none">StrainScan</a> is an efficient, accurate and high-resolution strain-level microbiome composition analysis tool based on reference genomes and k-mers. StrainScan takes reference database and sequencing data as input, outputs strain-level microbiome compistion analysis report.</p>
            </div>
          </div>
        </div>
      </div>

      <div class="col-sm m-sm-5 p-sm-4">
        <div class="pt-3" >
          <!-- Bootstrap -->
          <div class="col-sm ">
            <!--                    <div class="col-sm fs-3 d-inline p-2 shadow bg-light rounded-circle">-->
            <!--                      <fa :icon="['fab','bootstrap']" class="text-other"/>-->
            <img src="../assets/gd.png" width="55" height="40" class="img-thumbnail text-other" alt="">
            <!--                    </div>-->
            <div class="pt-3" >
              <h5 class="fw-bold">GDmicro</h5>
              <p class="fs-6 text-secondary"><a href="https://github.com/liaoherui/GDmicro" style="text-decoration: none">GDmicro</a> is a computational tool that uses GCN and Deep adaptation network to classify host disease status based on microbiome data. You can use GDmicro to: 1. Clssify host disease status for your metagenomic samples. 2. Explore disease-related species. 3. Explore the sample relationship of your metagenomic samples through the knn graph constructed by GDmicro.</p>
            </div>
          </div>
        </div>
      </div>

      <!--    <div class="col-sm m-sm-5 p-sm-4">-->
      <!--      <div>-->
      <!--        &lt;!&ndash; comment image &ndash;&gt;-->
      <!--&lt;!&ndash;        <img :src="p1" alt="" class="img-thumbnail rounded-circle">&ndash;&gt;-->
      <!--        <img src="../assets/logo.png" width="55" height="40" class="img-thumbnail text-other" alt="">-->
      <!--      </div>-->

      <!--      <div class="pt-3" >-->
      <!--      &lt;!&ndash; User Name &ndash;&gt;-->
      <!--      <h5 class="fw-bold">GDmicro</h5>-->
      <!--      &lt;!&ndash; comment text &ndash;&gt;-->
      <!--      <p class="fs-6 text-secondary"> GDmicro is a computational tool that uses GCN and Deep adaptation network to predict disease based on microbiome data. You can use GCN to: 1. Predict disease for your test samples. 2. Explore disease-related species. 3. Explore the sample relationship of your metagenomic samples through the knn graph constructed by GDmicro.</p>-->
      <!--    </div>-->
      <!--    </div>-->
    </div>

      <!--      Website statistics-->
      <h2 class="heading3 fw-bold mt-5 text-pink " >Website Statistics</h2>
      <div class="inner-container-home2">

        <div class="banner-2 ">
          <p class="font-work_sans ppart">This page is provided by <a href="https://clustrmaps.com/" style="text-decoration: none">ClustrMaps</a>.</p>
<!--            More details about the website statistics can be found via <a href="https://clustrmaps.com/site/1bry1" style="text-decoration: none">here</a>-->
          <div >
            <a href="https://clustrmaps.com/site/1bry1" title="Visit tracker"><img src="//clustrmaps.com/map_v2.png?cl=ffffff&w=800&t=tt&d=PhL_54NoSVmt8afCuQwe5AleWcS0eCP4YUIJ9-99vx4&co=2d78ad&ct=ffffff" /></a>
          </div>
        </div>
      </div>

</div>
  </div>

</template>

<script>


//import righthead from '../layouts/header/righthead.vue'
</script>

<style>

@import url('https://fonts.googleapis.com/css2?family=Festive&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Festive&family=Varela+Round&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Eczar&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Work+Sans&display=swap');

.ttile{
  color: #667EEA;
}
.cfont{
  font-family: "cavolini";
}
/*p:first-child {*/
/*  color: #667EEA;*/

/*}*/
/*.news{*/
/*  !*display:inline-block;*!*/
/*  border:1px solid #000;*/
/*  padding:50px;*/

/*}*/
.inner-container-home{
  /*width: 90%;*/
  padding-left: 90px;
  padding-right: 90px;
}
.inner-container-home2{
  /*width: 90%;*/
  padding-left: 90px;
  padding-right: 90px;
  padding-bottom: 20px;
}
.inner-container-home3{
  /*width: 90%;*/
  padding-left: 90px;
  padding-right: 90px;
  /*padding-bottom: 20px;*/
}
.ttile{
  font-size: 20px;
}
/*.hp1{*/
/*  text-align: left;*/
/*  padding: 20px;*/
/*}*/



.text-secondary{
  font-size: 21px;
  font-family: arial;
}

.Stars{
  background-color: #334155;
}


.text-pin{
  color: #334155;
}
.text-other{
  color: #7952B3;
}
.contp{
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
}
.cont1{
  border: 2px solid #dddddd;
  width: 40%;
  height: 90%;
  text-align: justify;
  padding: 20px;
}
.tt{
  padding: 20px;
}
.heading3{
  text-align: left;
  font-size: 35px;
  padding: 30px;
  padding-left: 0px;

}
.heading6{
  text-align: left;
  font-size: 35px;
  padding: 30px;
  padding-left: 0px;

}
.project-title{
  padding-top: 20px;
  font-size: 30px;
}
/*.banner-2 {*/
/*  @apply px-5  pt-5 md:pt-10 3xl:px-36 2xl:px-36 xl:px-28 lg:px-24 md:px-16;*/
/*  background-color: #ffddbf;*/
/*}*/
/*.card {*/
/*  @apply bg-white rounded-2xl md:flex place-items-center my-20 shadow-md;*/
/*}*/
/*.card-image {*/
/*  @apply md:w-1/2 md:rounded-r-2xl md:rounded-l-none rounded-b-2xl flex;*/
/*}*/
/*.heading3 {*/
/*  color: #403930;*/
/*  @apply md:text-5xl text-xl font-bold font-work_sans tracking-wide;*/
/*}*/
/*.project-title {*/
/*  @apply text-gray-700 text-3xl md:text-4xl font-work_sans tracking-wide font-bold;*/
/*}*/
.ppart{
  font-size: 20px;
  text-align: left;
  padding-left: 20px;
  padding-right: 20px;
}
.Stars{
  padding: 20px;
  font-size: 20px;

}
.sp{
  text-align: left;
  font-size: 35px;
}
.pic {
  width: 80%;
  height: 100%;
  margin: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: 10%;
  margin-right: 10%;
  /*border: 2px solid;*/
}
.pic img {
  max-width: 100%;
  max-height: 100%;

  /*margin-right: auto;*/
}
/*.imgwf{*/
/*  padding-left: 50px;*/
/*}*/
</style>
