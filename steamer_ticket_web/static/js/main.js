/* 导入element-ui样式
*/
import 'element-ui/lib/theme-chalk/index.css'
 
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
 
/* element-ui所有组件
*/
import ElementUI from 'element-ui'
Vue.use(ElementUI)
 
Vue.config.productionTip = false
 
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')