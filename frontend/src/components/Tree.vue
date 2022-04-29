<template>
    <div>
        <!-- Once the page is loaded, a tree is created based on the data returned from the backend -->
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
        /**
         * Gets the data based on the id passed in
         */
        getTree() {
            // Make a request to get the data
            apis.getTree(this.id).then((res) => {
                // Add the data to the tree
                // Set first level of the tree to be the root
                res.data.label = "Root";
                // Add the data to the tree
                this.tree.push(res.data);
                // Emit the id of the root's first child
                this.$emit("label", res.data.children[0].label);
                // This allows the parent component to know that the data has been loaded
            });
        },
        /**
         * Emits the label of the node that was clicked
         * @param {*} nodeobj the node object that was clicked
         * @param {*} node the node that was clicked
         * @param {*} treenode the tree node that was clicked
         */
        emitLabel: function(nodeobj, node, treenode) {
            // Only the nodeobj is needed to get the label
            // console.log(nodeobj.label);
            try {
                // if the nodeobj label is null or is Root, then do nothing
                if (nodeobj.label == null || nodeobj.label == "Root") {
                    return;
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
