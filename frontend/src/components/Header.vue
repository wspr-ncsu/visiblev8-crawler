<template>
    <el-header>
        <ul class="navigation">
            <li class="history-link">
                <router-link to="/history">History</router-link>
            </li>

            <li class="title">
                <h1>
                    <router-link to="/">Visible V8</router-link>
                </h1>
            </li>

            <li class="about-link">
                <router-link to="/about">About</router-link>
            </li>
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