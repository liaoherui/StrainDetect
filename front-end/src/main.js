// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'

import BootstrapVue from 'bootstrap-vue'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import locale from '../node_modules/element-ui/lib/locale/lang/en'
// import VueSmoothScroll from 'vue3-smooth-scroll'



Vue.config.productionTip = false
Vue.use(ElementUI,{locale})
Vue.use(BootstrapVue)
// Vue.use(VueSmoothScroll)
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
