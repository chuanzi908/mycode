<template>
  <div class="app-container">
    <!-- 登录页 -->
    <div v-if="!isLoggedIn" class="login-page">
      <div class="login-card">
        <div class="login-header">
          <h1>🏠 房产销售管理系统</h1>
          <p>请登录您的账号</p>
        </div>

        <div class="login-form">
          <div class="form-item">
            <label>账号</label>
            <input
              type="text"
              v-model="loginForm.username"
              placeholder="请输入账号"
              class="form-input"
            />
          </div>
          <div class="form-item">
            <label>密码</label>
            <input
              type="password"
              v-model="loginForm.password"
              placeholder="请输入密码"
              class="form-input"
            />
          </div>
          <button
            class="login-btn"
            @click="handleLogin"
            :disabled="loading"
          >
            {{ loading ? '登录中...' : '登 录' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 主页面（房源列表） -->
    <div v-else class="main-page">
      <div class="header-bar">
        <div class="header-left">
          <h2>🏠 房源列表</h2>
        </div>
        <div class="header-right">
          <span>欢迎您，{{ userInfo.username }}</span>
          <button class="logout-btn" @click="handleLogout">退出登录</button>
        </div>
      </div>

      <div class="table-container">
        <table class="house-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>房源标题</th>
              <th>区域</th>
              <th>户型</th>
              <th>价格(元)</th>
              <th>地址</th>
              <th>状态</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="house in houseList" :key="house.id">
              <td>{{ house.id }}</td>
              <td>{{ house.title }}</td>
              <td>{{ house.area }}</td>
              <td>{{ house.houseType }}</td>
              <td>{{ house.price.toLocaleString() }}</td>
              <td>{{ house.address }}</td>
              <td>
                <span :class="house.status === 1 ? 'status-tag success' : 'status-tag warning'">
                  {{ house.status === 1 ? '已发布' : '未审核' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

// 配置代理和跨域
axios.defaults.baseURL = ''
axios.defaults.withCredentials = true

const isLoggedIn = ref(false)
const loading = ref(false)
const loginForm = ref({
  username: 'admin',
  password: '123456'
})
const userInfo = ref({})
const houseList = ref([])

// 登录（关键：用表单格式提交，适配后端getParameter）
const handleLogin = async () => {
  if (!loginForm.value.username || !loginForm.value.password) {
    alert('请输入账号和密码')
    return
  }
  loading.value = true
  try {
    // 用URLSearchParams转成表单格式，后端才能正常读取
    const params = new URLSearchParams()
    params.append('username', loginForm.value.username)
    params.append('password', loginForm.value.password)

    const res = await axios.post('/backend/login', params)
    if (res.data.code === 200) {
      alert('登录成功')
      isLoggedIn.value = true
      userInfo.value = res.data.data
      getHouseList()
    } else {
      alert(res.data.msg || '登录失败')
    }
  } catch (err) {
    console.error('登录请求失败:', err)
    alert('网络错误，请检查后端服务是否启动')
  } finally {
    loading.value = false
  }
}

// 获取房源列表
const getHouseList = async () => {
  try {
    const res = await axios.get('/backend/house/list')
    if (res.data.code === 200) {
      houseList.value = res.data.data
    }
  } catch (err) {
    console.error('获取房源失败:', err)
    alert('获取房源列表失败')
  }
}

// 退出登录
const handleLogout = () => {
  alert('已退出登录')
  isLoggedIn.value = false
  userInfo.value = {}
  loginForm.value = { username: '', password: '' }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
}

.app-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 400px;
  padding: 40px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h1 {
  color: #333;
  font-size: 24px;
  margin-bottom: 10px;
}

.login-header p {
  color: #999;
  font-size: 14px;
}

.form-item {
  margin-bottom: 20px;
}

.form-item label {
  display: block;
  margin-bottom: 8px;
  color: #666;
  font-size: 14px;
}

.form-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
}

.login-btn {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.main-page {
  padding: 20px;
}

.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 0 20px;
  height: 60px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
}

.header-left h2 {
  color: #333;
  font-size: 20px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
  color: #666;
}

.logout-btn {
  padding: 6px 12px;
  background: #f56c6c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.table-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.house-table {
  width: 100%;
  border-collapse: collapse;
}

.house-table th, .house-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.house-table th {
  background-color: #f8f9fa;
  color: #333;
}

.status-tag {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.status-tag.success {
  background: #e6f7ef;
  color: #52c41a;
}

.status-tag.warning {
  background: #fff7e6;
  color: #faad14;
}
</style>