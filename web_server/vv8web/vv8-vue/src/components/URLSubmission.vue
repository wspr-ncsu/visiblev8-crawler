<template>
    <!-- <form class="index-search-container" id="search-container">
        <el-input v-model="input" name="request" type="text" placeholder="Enter URL here" />
        <button type="submit" @click="passText"><i class="fa fa-search"></i></button>
    </form>     -->
    <div class="index-search-container" id="search-container">
    <el-input
      v-model="input"
      placeholder="Enter URL here"
      class="input-with-select"
      name="request"
      type="text"
    >
      <template #prepend>
        <el-select v-model="select" placeholder="Select" style="width: 110px">
          <el-option label="http://" value="http://" />
          <el-option label="https://" value="http://" />
        </el-select>
      </template>
      <template #append>
        <el-button :icon="Search" type="submit" @click="passText"/>
      </template>
    </el-input>
  </div>
</template>

<script setup lang="ts">
import { defineComponent, ref } from 'vue'
import { Search } from '@element-plus/icons-vue'
const input = ref('')
const select = ref('')

import { sendurl } from '../apis/subURL'
const passText = () => {
  sendurl(input).then(res => console.log(res)).catch(err => console.log(err))
}


</script>


<style>
.input-with-select .el-input-group__prepend {
  background-color: var(--el-fill-color-blank);
}
</style>