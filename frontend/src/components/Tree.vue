<template>
    <div>
        <!-- Once the page is loaded, create a tree based on the data returned from the backend -->
        <el-tree :data="tree" :props="defaultProps" />
    </div>
</template>

<script>
import * as apis from "@/apis/getResults";
import { forEach } from "lodash";
import { root } from "postcss";

export default {
    props: {
        id: {
            required: true,
        },
    },
    data() {
        return {
            data: [],
            tree: [],
            defaultProps: {
                label: "label",
                children: "children",
            },
        };
    },
    methods: {
        getTree() {
            apis.getTree(this.id).then((res) => {
                // Recursively create a tree structure
                console.log(res.data);
                this.tree.push(res.data);
            });
        },
    },
    mounted() {
        this.getTree()
    },
};
</script>

<style scoped>
</style>
