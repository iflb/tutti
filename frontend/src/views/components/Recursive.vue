<template>
    <div>
    <v-card class="ma-3 mt-0 px-3" :color="cardColor" :tile="hasChildren">
        <v-container>
            <v-row>
                <v-col cols="8" class="pb-0">
                        <v-text-field
                            v-if="hasChildren"
                            v-model="node.tag"
                            label="Batch name"
                            prepend-inner-icon="mdi-pencil"
                            outlined filled hide-details dense />
                        <v-select
                            v-if="!hasChildren"
                            v-model="node.tag"
                            :items="templates"
                            label="Template name"
                            filled hide-details outlined dense />
                </v-col>
                <v-spacer></v-spacer>
                <v-col align="right">
                    <v-btn text icon><v-icon>mdi-dots-vertical</v-icon></v-btn>
                </v-col>
            </v-row>
            <v-row class="text-caption">
                <v-col cols="12" class="pb-0" v-if="node.cond_if">
                    <v-icon>mdi-comment-question-outline</v-icon>
                    IF condition = <b>{{ node.cond_if }}</b>
                </v-col>
                <v-col cols="12" class="pb-0" v-if="node.cond_while">
                    <v-icon>mdi-repeat</v-icon>
                    LOOP condition = <b>{{ node.cond_while }}</b>
                </v-col>
                <v-col cols="12" class="pb-0" v-if="node.is_skippable">
                    <v-icon>mdi-transit-skip</v-icon>
                    Skippable
                </v-col>
            </v-row>
            <v-row justify="end" :key="idx" v-for="(child, idx) in children">
                <v-col cols="11">
                <recursive
                    :template-color="templateColor"
                    :templates="templates"
                    :node="child"
                    :is-last="idx==children.length-1"
                    :depth="depth+1" />
                </v-col>
            </v-row>
        </v-container>
    </v-card>
    <flow-arrow v-if="!isLast" :depth="depth" :color="templateColor" />
    </div>
</template>

<script>
import Recursive from './Recursive.vue'
import FlowArrow from './FlowArrow.vue'

export default {
    name: "Recursive",
    props: ["node", "isLast", "depth", "templateColor", "templates"],
    components: { Recursive, FlowArrow },
    data: () => ({
        color: "grey",
    }),
    computed: {
        cardColor() {
            if(this.hasChildren) return `${this.color} lighten-${this.depth+2}`;
            else return this.templateColor;
        },
        children() {
            if(this.node) return this.node.children;
            else return [];
        },
        hasChildren() {
            if(this.children) return this.children.length>0;
            else return false;
        }
    }
}
</script>
