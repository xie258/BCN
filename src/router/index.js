import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'


Vue.use(VueRouter)

const routes = [{
	path: '/',
	redirect: '/homemain'
}, {
	path: '/',
	name: 'Home',
	component: Home,
	children: [{
		path: '/homemain',
		name: 'HomeMain',
		component: () => import('../components/HomeMain.vue'),
	},{
		path: '/rename',
		name: 'Rename',
		component: () => import('../components/rename.vue'),
	},{
		path: '/createPdf',
		name: 'CreatePdf',
		component: () => import('../components/createPdf.vue'),
	},{
		path: '/sendemail',
		name: 'Sendemail',
		component: () => import('../components/sendemail.vue'),
	},{
		path: '/any',
		name: 'Any',
		component: () => import('../components/any.vue'),
	}]
	// children: [
	//   {
	//     path: 'homeheader',
	//     name: 'homeheader',
	//     component: () => import(/* webpackChunkName: "HomeHeader" */ '../components/HomeHeader.vue'),
	//   },
	//   {
	//     path: 'homemain',
	//     name: 'homemain',
	//     component: () => import(/* webpackChunkName: "HomeMain" */ '../components/HomeMain.vue'),
	//   },
	//   {
	//     path: 'homefooter',
	//     name: 'homeheader',
	//     component: () => import(/* webpackChunkName: "HomeFooter" */ '../components/HomeFooter.vue'),
	//   },
	//   ]
}]

const router = new VueRouter({
	routes
})

export default router
