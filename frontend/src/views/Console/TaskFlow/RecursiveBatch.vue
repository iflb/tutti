<template>
    <div>
    <v-card class="pa-3 ma-3" :color="cardColor" :tile="isBatch" :shaped="!isBatch">
        <v-container>
            <v-row>
                <v-col cols="10" md="6">
                        <v-text-field v-model="node.name" :label="isBatch ? 'Batch name' : 'Template name'" prepend-inner-icon="mdi-pencil" outlined filled hide-details dense />
                </v-col>

                <v-spacer></v-spacer>

                <v-menu bottom left offset-y v-if="!isBatch">
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
                        Nanotasks ({{ nanotasks.length }})
                    </v-chip>
                </v-col>
            </v-row>

            <v-row justify="end" :key="idx" v-for="(child, idx) in children">
                <v-col cols="12" md="11">
                <recursive-batch
                    :duct="duct"
                    :name="name"
                    :parent-params="{
                        prjName, templateColor,
                        node: child,
                        isLast: idx==children.length-1,
                        depth: depth+1
                    }" />
                </v-col>
            </v-row>

        </v-container>
    </v-card>
    <arrow v-if="!isLast" :depth="depth" :color="templateColor" />

    <dialog-import :duct="duct" :prj-name="prjName" :template="node.name" ref="dlgImport" />
    <dialog-list :duct="duct" :prj-name="prjName" :template="node.name" :nanotasks="nanotasks" ref="dlgList" />

    </div>
</template>

<script>
import { codemirror } from 'vue-codemirror'
import 'codemirror/lib/codemirror.css'
import 'codemirror/mode/python/python'
import 'codemirror/theme/base16-light.css'

export default {
    name: "RecursiveBatch",
    props: ["duct", "name", "parentParams"],
    components: {
        RecursiveBatch: () => import("./RecursiveBatch"),
        Arrow: () => import("./Arrow"),
        DialogImport: () => import("./DialogImportNanotasks"),
        DialogList: () => import("./DialogListNanotasks"),
        codemirror
    },
    data: () => ({
        color: "grey",
        cmOptions: {
            tabSize: 4,
            mode: 'text/x-python',
            //theme: 'base16-light',
            lineNumbers: true,
            line: true,
            readOnly: true
        },
        nanotasks: []
    }),
    computed: {
        cardColor() { return this.isBatch ? `${this.color} lighten-${this.depth+2}` : this.templateColor; },
        children() { return this.node ? this.node.children : []; },
        isBatch() { return this.children ? this.children.length>0 : false; },
        hasNanotask() { return !this.isBatch && this.nanotasks.length>0; },

        prjName() { return this.parentParams.prjName; },
        node() { return this.parentParams.node; },
        templateColor() { return this.parentParams.templateColor; },
        depth() { return this.parentParams.depth; },
        isLast() { return this.parentParams.isLast; },
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.addTuttiEvtHandler({
                eid: this.duct.EVENT.GET_NANOTASKS,
                success: ({ data }) => {
                    if(data["ProjectName"]==this.prjName && data["TemplateName"]==this.node.name)
                        this.nanotasks = data["Nanotasks"];
                }
            });
            this.duct.addTuttiEvtHandler({
                eid: this.duct.EVENT.UPLOAD_NANOTASKS,
                success: ({ data }) => {
                    if(data["ProjectName"]==this.prjName && data["TemplateName"]==this.node.name)
                        this.duct.controllers.resource.getNanotasks();
                }
            });
            this.duct.addTuttiEvtHandler({
                eid: this.duct.EVENT.DELETE_NANOTASKS,
                success: () => {
                    this.duct.controllers.resource.getNanotasks();
                }
            });

            if(!this.isBatch){ this.duct.controllers.resource.getNanotasks(); }
        });

    }
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
