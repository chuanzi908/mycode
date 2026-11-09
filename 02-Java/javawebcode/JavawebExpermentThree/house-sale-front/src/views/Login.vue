<template>
  <div class="login-box">
    <el-card shadow="hover" style="width: 400px;">
      <h3 style="text-align:center">房产销售系统登录</h3>
      <el-form ref="loginFormRef" :model="loginForm" label-width="80px">
        <el-form-item label="账号">
          <el-input v-model="loginForm.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="loginForm.password" show-password></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="login" style="width:100%">登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import axios from 'axios'

defineOptions({
  name: 'UserLogin'
})

const router = useRouter()
const loginForm = ref({
  username: '',
  password: ''
})

const login = async () => {
  let res = await axios.post('/JavawebExpermentThree/login', loginForm.value)
  if(res.data.code === 200){
    ElMessage.success("登录成功")
    localStorage.setItem("user",JSON.stringify(res.data.data))
    // 根据角色跳转页面
    if(res.data.data.role === 1){
      router.push("/admin")
    }else{
      router.push("/index")
    }
  }else{
    ElMessage.error(res.data.msg)
  }
}
</script>

<style scoped>
.login-box{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: #f5f5f5;
}
</style>