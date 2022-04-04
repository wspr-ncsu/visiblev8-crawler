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
      ref="getURL"
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

<script>
import { defineComponent } from 'vue'
import { sendurl } from '../apis/subURL'
import { Search } from '@element-plus/icons-vue'
export default {
  setup(){
    return {
      Search
    }
  },
  data(){
    return {
      input: '',
    }    
  },
  methods: {
    passText(){
      sendurl(this.input).then(res => console.log(res)).catch(err => console.log(err))
      this.$router.push('/result')
    }
    
  }
}

</script>


<style>
.input-with-select .el-input-group__prepend {
  background-color: var(--el-fill-color-blank);
}
</style>