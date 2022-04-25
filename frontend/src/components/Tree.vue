<template>
    <div>
        <!-- Once the page is loaded, create a tree based on the data returned from the backend -->
        <el-tree :data="tree" :props="defaultProps" @node-click="emitLabel"  />
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
                // console.log(res.data);
                this.tree.push(res.data);
            });
        },
        emitLabel: function(nodeobj, node, treenode) {
            // console.log(nodeobj.label);
            try {
                // if the nodeobj label is null, then throw an error
                if (nodeobj.label == null) {
                    throw new Error("nodeobj.label is null");
                }
                this.$emit("clicked", nodeobj.label);
            } catch (e) {
                console.log(e);
            }
        }
    },
    mounted() {
        this.getTree()
    },
};
</script>

<style scoped>
</style>
