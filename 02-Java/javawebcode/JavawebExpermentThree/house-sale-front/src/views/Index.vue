<template>
  <div class="container">
    <h2>房源列表</h2>
    <el-table :data="houseList" border style="width:100%">
      <el-table-column prop="title" label="房源标题"/>
      <el-table-column prop="area" label="所在区域"/>
      <el-table-column prop="houseType" label="户型"/>
      <el-table-column prop="price" label="价格"/>
      <el-table-column prop="address" label="地址"/>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

defineOptions({
  name: 'HouseIndex'
})

const houseList = ref([])

const getHouseList = async () => {
  let res = await axios.get('/JavawebExpermentThree/house/list')
  if(res.data.code === 200){
    houseList.value = res.data.data
  }
}

onMounted(()=>{
  getHouseList()
})
</script>