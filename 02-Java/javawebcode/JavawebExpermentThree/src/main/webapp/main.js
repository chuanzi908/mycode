import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios'
import App from './App.vue'
import router from './router' // 注意：你截图里没看到 router.js，这里也要检查

const app = createApp(App)

// 关键！baseURL 必须和后端 Context Path 一致
axios.defaults.baseURL = 'http://localhost:8080/JavawebExperimentThree'
// 跨域问题：如果 Vue 和 Tomcat 端口不同，必须加这个
axios.defaults.withCredentials = true

app.config.globalProperties.$axios = axios

app.use(ElementPlus).use(router).mount('#app')