<template>
  <el-form :inline="true" :model="formInline" class="demo-form-inline">
    <el-form-item>
      <el-input v-model="formInline.url" placeholder="Enter URL (ex: google.com)" style="min-width: 500px">
        <template #prepend>
          <el-select v-model="formInline.prefix" placeholder="Prefix" style="width: 90px">
            <el-option label="http://" value="http://" />
            <el-option label="https://" value="https://" />
          </el-select>
        </template>
        <template #append>
          <el-button :icon="Search" type="primary" @click="onSubmit"/>
        </template>
      </el-input>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { sendurl } from '@/apis/subURL'
import { reactive } from 'vue'
import router from '@/router';

const formInline = reactive({
  prefix: '',
  url: '',
})

const onSubmit = () => {
  // if the prefix is empty, we will alert the user
  if (formInline.prefix === '') {
    alert('Please enter a prefix')
    return
  }
  // if the url is empty, we will alert the user
  else if (formInline.url === '') {
    alert('Please enter a url')
    return
  }
  else {
    sendurl(formInline.prefix + formInline.url)
    router.push('/result')
  }
}

</script>


<style>
.input-with-select .el-input-group__prepend {
  background-color: var(--el-fill-color-blank);
}
</style>