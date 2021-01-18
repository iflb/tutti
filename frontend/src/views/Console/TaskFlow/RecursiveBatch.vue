<template>
    <div>
    <v-card class="pa-3 ma-3" :color="cardColor" :tile="hasChildren" :shaped="!hasChildren">
        <v-container>
            <v-row>
                <v-col cols="10" md="6">
                        <v-text-field
                            v-if="hasChildren"
                            v-model="node.name"
                            label="Batch name"
                            prepend-inner-icon="mdi-pencil"
                            outlined filled hide-details dense />
                        <v-select
                            v-if="!hasChildren"
                            v-model="node.name"
                            :items="Object.keys(project.templates)"
                            label="Template name"
                            filled hide-details outlined dense />
                </v-col>

                <v-spacer></v-spacer>

                <v-menu bottom left offset-y v-if="!hasChildren">
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn icon v-on="on" v-bind="attrs"><v-icon>mdi-dots-vertical</v-icon></v-btn>
                    </template>
                    <v-list>
                        <v-list-item @click="$refs.dlgImport.show=true">
                            <v-list-item-title>Import Nanotasks...</v-list-item-title>
                        </v-list-item>
                    </v-list>
                </v-menu>
            </v-row>

            <v-row class="text-caption">
                <v-col cols="12" class="pb-0" v-if="node.statement==duct.APP_WSD.enums.Statement.IF">
                    <v-icon>mdi-comment-question-outline</v-icon>
                    IF condition
                    <v-card height=100><codemirror v-model="node.condition" :options="cmOptions" /></v-card>
                </v-col>
                <v-col cols="12" class="pb-0" v-if="node.statement==duct.APP_WSD.enums.Statement.WHILE">
                    <v-icon>mdi-repeat</v-icon>
                    LOOP condition
                    <v-card height=100><codemirror v-model="node.condition" :options="cmOptions" /></v-card>
                </v-col>
                <v-col cols="12" class="pb-0" v-if="node.skippable">
                    <v-icon>mdi-transit-skip</v-icon>
                    Skippable
                </v-col>
                <v-col cols="12" class="pb-0" v-if="hasNanotask">
                    <v-chip dark label outlined color="indigo" @click="$refs.dlgList.show=true">
                        <v-icon left>mdi-file-document-multiple-outline</v-icon>
                        Nanotasks ({{ project.templates[node.name].nanotask.cnt }})
                    </v-chip>
                </v-col>
            </v-row>

            <v-row justify="end" :key="idx" v-for="(child, idx) in children">
                <v-col cols="12" md="11">
                <recursive-batch
                    :template-color="templateColor"
                    :project="project"
                    :node="child"
                    :is-last="idx==children.length-1"
                    :depth="depth+1" />
                </v-col>
            </v-row>

        </v-container>
    </v-card>
    <arrow v-if="!isLast" :depth="depth" :color="templateColor" />

    <dialog-import :project="project" :template="node.name" ref="dlgImport" />
    <dialog-list :project="project" :template="node.name" :nanotasks="nanotasks" ref="dlgList" />

    </div>
</template>

<script>
import RecursiveBatch from './RecursiveBatch.vue'
import Arrow from './Arrow.vue'
import DialogImport from './DialogImportNanotasks.vue'
import DialogList from './DialogListNanotasks.vue'
import { codemirror } from 'vue-codemirror/src/codemirror'
import 'codemirror/lib/codemirror.css'
import 'codemirror/mode/python/python'
import 'codemirror/theme/base16-light.css'

import store from '@/store.js'
import { mapGetters } from 'vuex'

export default {
    store,
    name: "RecursiveBatch",
    props: ["name", "node", "isLast", "depth", "templateColor", "project"],
    components: { RecursiveBatch, Arrow, DialogImport, DialogList, codemirror },
    data: () => ({
        color: "grey",
        cmOptions: {
            tabSize: 4,
            mode: 'text/x-python',
            //theme: 'base16-light',
            lineNumbers: true,
            line: true,
            readOnly: true
            // more CodeMirror options...
        }
    }),
    computed: {
        ...mapGetters("ductsModule", [ "duct" ]),
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
        },
        hasNanotask() {
            return !this.hasChildren && this.project.templates[this.node.name].nanotask.cnt>0;
        },
        nanotasks() {
            try { return this.project.templates[this.node.name].nanotask.data; }
            catch { return []; }
        }
    },
}
</script>
<style>
.CodeMirror {
    height: 100px;
}
.CodeMirror-vscrollbar, .CodeMirror-hscrollbar, .CodeMirror-scrollbar-filler, .CodeMirror-gutter-filler {
    z-index: 3;
}
</style>
