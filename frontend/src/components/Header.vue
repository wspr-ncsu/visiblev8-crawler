<template>
    <el-header>
        <ul class="navigation">
            <li class="history-link"><a href="/history">History</a></li>
            <li class="title"><h1><a href="/">Visible V8</a></h1></li>
            <li class="about-link"><a href="/about">About</a></li>
        </ul>
      </el-header>
</template>

<script setup>
import { useRouter, useRoute } from "vue-router";
import { ref } from "vue";

const router = useRouter();

</script>


<style scoped>

</style>