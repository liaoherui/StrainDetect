import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Detect from '@/components/Detect'
import Manual from '@/components/Manual'
import Result from '@/components/Result'
import ResultLoad from '@/components/ResultLoad'
import Example from '@/components/Example'
import SRR10971381 from '../Report/SRR10971381'
import SRR15224359 from '../Report/SRR15224359'
import SRR961514 from '../Report/SRR961514'
import SRR15011445 from '../Report/SRR15011445'
import ERR3253398 from '../Report/ERR3253398'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
	{
	   path: '/detect',
	   name: 'Detect',
	   component: Detect
	},
	{
		path:'/manual',
		name: 'Manual',
		component: Manual

	},
	{
		path: '/res',
		name: 'Result',
		component: Result
	},
    ,
    {
      path: '/resload/:id/',
      name: 'ResultLoad',
      component: ResultLoad
    },
	{
		path: '/example',
		name: 'Example',
		component: Example
	},
	{
		path: '/SRR10971381',
		name: 'SRR10971381',
		component: SRR10971381

	},
	{
		path: '/SRR15224359',
		name: 'SRR15224359',
		component: SRR15224359

	},
	{
		path: '/SRR961514',
		name: 'SRR961514',
		component: SRR961514

	},
    {
      path: '/SRR15011445',
      name: 'SRR15011445',
      component: SRR15011445
    },
    {
      path: '/ERR3253398',
      name: 'ERR3253398',
      component: ERR3253398
    }

  ]
})
router.afterEach((to,from,next)=>{
  window.scrollTo(0,0)
})
export default router
