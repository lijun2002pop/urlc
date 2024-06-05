import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import 'ant-design-vue/dist/reset.css'
import Antd from 'ant-design-vue'
import * as echarts from 'echarts';

axios.defaults.baseURL='http://127.0.0.1:8000'
const app = createApp(App)
app.config.globalProperties.$http = axios
app.config.globalProperties.$echarts = echarts
app.use(store).use(Antd).use(router).mount('#app')
