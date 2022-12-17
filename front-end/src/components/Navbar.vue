<template>
<!--  <b-navbar-brand href="/#" >-->
    <!--        <img src="../assets/logo.png" width="55" height="40" class="d-inline-block align-top" alt="">-->

<!--  </b-navbar-brand>-->
  <div class="nbar">
<!--    <div class="brand"><font   color="#9E426E" size="20px">Strain</font><font color="#667EEA" size="20px">Detect</font></div>-->
<!--    <div class="brand"><font color="white"   size="20px">StrainDetect</font></div>-->
    <div class="mtest">
<!--    <b-navbar toggleable="lg" type="dark" variant="dark" >-->
      <b-navbar toggleable="lg" type="light" variant="light" fixed="top">
      <b-navbar-brand to="/" class="navbar-brand"><img src="../assets/logo.png" width="85" height="55" class="d-inline-block align-top img-logo" alt="">&nbsp;<font   color="#9E426E" size=45px>Strain</font><font color="#667EEA" size=45px>Detect</font></b-navbar-brand>


      <b-navbar-toggle target="nav-collapse" class="mr-auto "></b-navbar-toggle>

      <b-collapse id="nav-collapse"  is-nav>
        <b-navbar-nav class="mr-auto mx-auto baritem">
          <b-nav-item class="bitem" to="/"  exact exact-active-class="active"><i class="fa fa-home" aria-hidden="true"></i>&nbsp;Home&nbsp;&nbsp;&nbsp;</b-nav-item>
          <b-nav-item class="bitem" to="/detect" exact exact-active-class="active"><i class="fa fa-search" aria-hidden="true"></i>&nbsp;Detect&nbsp;&nbsp;&nbsp;</b-nav-item>
          <b-nav-item class="bitem" to="/example" exact exact-active-class="active"><i class="fa fa-file-text-o" aria-hidden="true"></i>&nbsp;Example&nbsp;&nbsp;&nbsp;</b-nav-item>
          <b-nav-item class="bitem" to="/manual" exact exact-active-class="active"><i class="fa fa-info-circle" aria-hidden="true"></i>&nbsp;Manual&nbsp;&nbsp;&nbsp;</b-nav-item>
          <b-nav-item class="bitem" href="https://github.com/liaoherui/StrainDetect"><i class="fa fa-github">&nbsp;GitHub</i></b-nav-item>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
<!--        <b-navbar-nav class="ml-auto">-->
<!--          <b-nav-form>-->
<!--            <b-form-input size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>-->
<!--            <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>-->
<!--          </b-nav-form>-->

<!--          <b-nav-item-dropdown text="Lang" right>-->
<!--            <b-dropdown-item href="#">EN</b-dropdown-item>-->
<!--            <b-dropdown-item href="#">ES</b-dropdown-item>-->
<!--            <b-dropdown-item href="#">RU</b-dropdown-item>-->
<!--            <b-dropdown-item href="#">FA</b-dropdown-item>-->
<!--          </b-nav-item-dropdown>-->

<!--          <b-nav-item-dropdown right>-->
<!--            &lt;!&ndash; Using 'button-content' slot &ndash;&gt;-->
<!--            <template v-slot:button-content>-->
<!--              <em>User</em>-->
<!--            </template>-->
<!--            <b-dropdown-item href="#">Profile</b-dropdown-item>-->
<!--            <b-dropdown-item href="#">Sign Out</b-dropdown-item>-->
<!--          </b-nav-item-dropdown>-->
<!--        </b-navbar-nav>-->
      </b-collapse>
    </b-navbar>
      </div>
  </div>


</template>

<script>

export default {
  name: 'Navbar'  //this is the name of the component
}
</script>

<style  >
@import url('https://fonts.googleapis.com/css2?family=Maven+Pro:wght@500&display=swap');
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css");

.bgwhite{
  background-color: white;
}
.hpink:hover{
  background: #ED64A6;
  color: white;
}
.hblue:hover{
  background: #667EEA;
  color: white;
}

.navbar-brand{
  font-family: 'Maven Pro', sans-serif;
  font-size: 45px;
}
.nav-item a.router-link-exact-active {
  text-shadow: 1px 8px 9px rgb(41, 40, 40);
  font-family: 'Maven Pro', sans-serif;
  /*font-size: 17px;*/
}
.nbar{
  font-size: 24px;
}
.brand{
  background-color: white;
}

/*.mtest{*/
/*  padding:20px;*/
/*}*/
.bitem{
  border-bottom: 0px solid #000;
  padding:20px;
  padding-top: 15px;
  padding-bottom: 10px;
  border-top: 0px solid #000;
}
.img-logo{
  padding-left: 10px;
}
/*.baritem{*/
/*  margin: 20px;*/
/*}*/
/*.navbar-custom{*/
/*  font-color: #212529;*/
/*}*/
/*.b-navbar-default .b-navbar-nav > li > a:hover, .b-navbar-default .b-navbar-nav > li > a:focus {*/
/*  color: #212529; !*Sets the text hover color on navbar*!*/
/*}*/

/*.b-navbar-default .b-navbar-nav > .active > a, .b-navbar-default .b-navbar-nav > .active >*/
/*a:hover, .b-navbar-default .b-navbar-nav > .active > a:focus {*/
/*  color: white; !*BACKGROUND color for active*!*/
/*  background-color: #030033;*/
/*}*/
/*.navbar {*/
/*  */
/*}*/
/*b-navbar-brand {*/
/*  position: absolute;*/
/*  left: 50%;*/
/*  margin-left: -50px !important;  !* 50% of your logo width *!*/
/*  display: block;*/
/*}*/
/*.b-navbar-nav{*/
/*  font-size: 30px;*/
/*}*/
</style>
