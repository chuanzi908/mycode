import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'

const app = createApp(App)

app.config.globalProperties.$axios = axios
axios.defaults.baseURL = 'http://localhost:8080/JavawebExpermentThree'

app.mount('#app')
