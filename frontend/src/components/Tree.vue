<template>
    <div>
        <!-- Once the page is loaded, create a tree based on the data returned from the backend -->
        <el-tree :data="tree" :props="defaultProps" />
    </div>
</template>

<script>
import * as apis from "@/apis/getResults";

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
            testData: [
                {
                    label: "Level one 1",
                    children: [
                        {
                            label: "Level two 1-1",
                            children: [
                                {
                                    label: "Level three 1-1-1",
                                },
                            ],
                        },
                    ],
                },
                {
                    label: "Level one 2",
                    children: [
                        {
                            label: "Level two 2-1",
                            children: [
                                {
                                    label: "Level three 2-1-1",
                                },
                            ],
                        },
                        {
                            label: "Level two 2-2",
                            children: [
                                {
                                    label: "Level three 2-2-1",
                                },
                            ],
                        },
                    ],
                },
                {
                    label: "Level one 3",
                    children: [
                        {
                            label: "Level two 3-1",
                            children: [
                                {
                                    label: "Level three 3-1-1",
                                },
                            ],
                        },
                        {
                            label: "Level two 3-2",
                            children: [
                                {
                                    label: "Level three 3-2-1",
                                },
                            ],
                        },
                    ],
                },
            ],
        };
    },
    methods: {
        getTree() {
            apis.getTree(this.id).then((res) => {
                // Using the data, recursively create a tree structure
                console.log(res.data);
                this.tree = res.data;
            });
        },
        createTree(data) {
            // Create a tree structure based on the data returned from the backend
            let tree = [];
            for (let i = 0; i < data.length; i++) {
                let node = data[i];
                let children = [];
                if (node.children) {
                    children = this.createTree(node.children);
                }
                tree.push({
                    id: node.id,
                    label: node.label,
                    children: children,
                });
            }
            this.tree = tree;
            console.log(this.tree);
            console.log(this.testData);
            return tree;
        },
    },
    mounted() {
        this.getTree();
    },
};
</script>

<style scoped>
</style>
