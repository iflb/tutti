<template>
    <div>
    <v-card class="pa-1 mt-0 px-3" :color="cardColor" :tile="hasChildren" :shaped="!hasChildren">
        <v-container>
            <v-row>
                <v-col cols="10" md="6" class="pb-0">
                        <v-text-field
                            v-if="hasChildren"
                            v-model="node.tag"
                            label="Batch name"
                            prepend-inner-icon="mdi-pencil"
                            outlined filled hide-details dense />
                        <v-select
                            v-if="!hasChildren"
                            v-model="node.tag"
                            :items="Object.keys(templates)"
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
                <v-col cols="12" class="pb-0" v-if="node.is_skippable">
                    <v-chip dark label outlined color="indigo" @click="$refs.dlgList.show=true">
                        <v-icon left>mdi-file-document-multiple-outline</v-icon>
                        Nanotasks set (320)
                    </v-chip>
                </v-col>
            </v-row>

            <v-row justify="end" :key="idx" v-for="(child, idx) in children">
                <v-col cols="12" md="11">
                <recursive-batch
                    :template-color="templateColor"
                    :project="project"
                    :templates="templates"
                    :node="child"
                    :is-last="idx==children.length-1"
                    :depth="depth+1" />
                </v-col>
            </v-row>

        </v-container>
    </v-card>
    <arrow v-if="!isLast" :depth="depth" :color="templateColor" />

    <dialog-import :project="project" :template="node.template" ref="dlgImport" />
    <dialog-list :project="project" :template="node.template" ref="dlgList" />

    </div>
</template>

<script>
import RecursiveBatch from './RecursiveBatch.vue'
import Arrow from './Arrow.vue'
import DialogImport from './DialogImportNanotasks.vue'
import DialogList from './DialogListNanotasks.vue'

export default {
    name: "RecursiveBatch",
    props: ["node", "isLast", "depth", "templateColor", "project", "templates"],
    components: { RecursiveBatch, Arrow, DialogImport, DialogList },
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
