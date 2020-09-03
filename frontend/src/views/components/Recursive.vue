<template>
    <div>
    <v-card class="ma-3" :color="color+' lighten-'+(depth+2)">
        <v-container>
            <v-row><v-col cols="4">
                <v-text-field v-if="hasChildren" v-model="node.tag" label="Batch name" prepend-inner-icon="mdi-pencil" dense />
                <v-select v-if="!hasChildren" :items="[node.tag]" v-model="node.tag" label="Template name" outlined dense />
            </v-col></v-row>
            {{ node.cond_while }}
            <recursive :key="idx" v-for="(child, idx) in children" :node="child" :is-last="idx==children.length-1" :depth="depth+1"></recursive>
        </v-container>
    </v-card>
    <flow-arrow v-if="!isLast" :depth="depth" :color="color" />
    </div>
</template>

<script>
import Recursive from './Recursive.vue'
import FlowArrow from './FlowArrow.vue'

export default {
    name: "Recursive",
    props: ["node", "isLast", "depth"],
    components: { Recursive, FlowArrow },
    data: () => ({
        color: "indigo"
    }),
    computed: {
        children() {
            if(this.node) return this.node.children;
            else return [];
        },
        hasChildren() {
            if(this.children) return this.children.length;
            else return false;
        }
    }
}
</script>
