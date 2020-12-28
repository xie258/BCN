import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'


// 引入element-ui组件
import './plugins/element.js'
//引入自定义ico
import '../public/icon/iconfont.css'
//引入滚动条组件
import vuescroll from 'vuescroll';

Vue.config.productionTip = false

Vue.prototype.$axios = axios

Vue.use(vuescroll); // install the vuescroll first
Vue.prototype.$vuescrollConfig = {
  bar: {
    background: ' #1296db'  //滚动条颜色
  }
}
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
