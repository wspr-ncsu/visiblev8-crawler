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
          <el-button :icon="Search" type="primary" @click="onSubmit">
            <el-icon class="el-input__icon"><search /></el-icon>
          </el-button>
        </template>
      </el-input>
    </el-form-item>
  </el-form>
</template>

<script lang="ts">
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { sendurl } from '@/apis/subURL'
import { submiturl } from '@/apis/subURL'
import { reactive } from 'vue'
import router from '@/router';

export default {
  name: "submitURL",
  components: {
    Search
  },
  props: {
    // leave here for future use
    txt: String
  },
  setup(props, { emit }) {
    const formInline = reactive({
      prefix: "https://",
      url: '',
    })

    /**
     * When the submit button is clicked, send the URL to the server
     */
    function onSubmit () {
      // if the prefix is empty, alert the user
      if (formInline.prefix === '') {
        alert('Please enter a prefix')
        return
      }
      // if the url is empty, alert the user
      else if (formInline.url === '') {
        alert('Please enter a url')
        return
      }
      else {
        try {
          var url = formInline.prefix + formInline.url
          // console.log(url)
          emit('loading', true)
          // send the url to the server
          sendurl(url).then(function (response) { 
            // if response.data.valid is false, alert the user
            if (response.data.valid === false) {
              alert('Invalid URL')
              emit('loading', false)
            }
            // Check to see if the URL is cached
            else if (response.data.cached) {
              var rerun = true
              // If the URL is cached, prompt the user to see if they want to go to the cached URL
              if (confirm('This URL is cached. Do you want to go to the cached URL?')) {
                rerun = false
              }
              // If the user does not want to go to the cached URL,
              // Submit the URL to the server
              submiturl(url, rerun).then(function (res) {
                // get the submission id from the response
                var submission_id = res.data.submission_id
                // redirect the user to the submission page
                router.push({
                  path: '/result/' + submission_id,
                })
              })
            }
            else {
              // If the URL is not cached, submit the URL to the server
              // Submit the URL to the server
              submiturl(url, true).then(function (res) {
                // get the submission id from the response
                var submission_id = res.data.submission_id
                // redirect the user to the submission page
                router.push({
                  path: '/result/' + submission_id,
                })
              })
            }
          })
        }
        catch (e) {
          alert(e)
        }
      }
    }

    return {formInline, onSubmit}

  }
}


</script>


<style>
.input-with-select .el-input-group__prepend {
  background-color: var(--el-fill-color-blank);
}
</style>