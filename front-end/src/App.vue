<template>
  <div class="overallbox">
    <div class="inbox">
  <div id="app">
    <navbar></navbar>
    <div>&ndash;</div>
    <div>&ndash;</div>
    <div>&ndash;</div>
    <router-view/>

<div class="foot">
  <MainFooter></MainFooter>
</div>
    </div>
    </div>
  </div>


</template>


<script>
import Navbar from './components/Navbar'
import MainFooter from './components/MainFooter'


export default {
  name: 'App',
  components: {
    navbar: Navbar,
    'MainFooter': MainFooter
  }
}
</script>

<style>
/*.overallbox{*/
/*  background-color: white;*/

/* padding: 40px;*/
/*  padding-top: 10px;*/
/*}*/
/*.inbox{*/
/*  box-shadow: 0px 0.5px 10px  rgb(180, 180, 180);*/
/*  border: 2px solid #D5DFE6;*/
/*}*/
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;




  /*font-size: 10px;*/
  /*background-color: #F3F3F3;*/

}
body{
  padding: 0;
  margin: 0;
  /*font-size: 10px;*/
  /*height: 100%;*/
  /*position:absolute;*/
  /*top: 0;*/
  /*bottom:0;*/
}
.foot{
  bottom:0;
}
</style>
