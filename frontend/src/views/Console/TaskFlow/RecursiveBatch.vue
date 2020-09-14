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
                            :items="templates"
                            label="Template name"
                            filled hide-details outlined dense />
                </v-col>
                <v-spacer></v-spacer>
                <v-menu bottom left offset-y v-if="!hasChildren">
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn icon v-on="on" v-bind="attrs"><v-icon>mdi-dots-vertical</v-icon></v-btn>
                    </template>
                    <v-list>
                        <v-list-item @click="templateName=node.tag; dialog=true">
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
            </v-row>
            <v-row justify="end" :key="idx" v-for="(child, idx) in children">
                <v-col cols="12" md="11">
                <recursive-batch
                    :template-color="templateColor"
                    :templates="templates"
                    :node="child"
                    :is-last="idx==children.length-1"
                    :depth="depth+1" />
                </v-col>
            </v-row>
        </v-container>
    </v-card>
    <arrow v-if="!isLast" :depth="depth" :color="templateColor" />

    <v-dialog v-model="dialog" max-width="1200" persistent>
      <v-card>
        <v-card-title class="headline">Import Nanotasks for '{{ templateName }}'</v-card-title>
        <v-card-text>
            <v-file-input accept=".csv,.CSV" show-size label="Upload .csv file..." @change="getFileContent"></v-file-input>
        </v-card-text>
        <v-card-text>
            <v-data-table v-if="contents.length>0" dense :headers="headers" :items="contents" class="elevation-1"></v-data-table>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog" > Cancel </v-btn>
          <v-btn color="primary" @click="importNanotasks" :disabled="contents.length==0"> Import </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    </div>
</template>

<script>
import RecursiveBatch from './RecursiveBatch.vue'
import Arrow from './Arrow.vue'
import Papa from 'papaparse'

export default {
    name: "RecursiveBatch",
    props: ["node", "isLast", "depth", "templateColor", "templates"],
    components: { RecursiveBatch, Arrow },
    data: () => ({
        color: "grey",
        templateName: "",

        dialog: false,
        headers: [],
        headerNames: [],
        contents: []
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
    },
    methods: {
        closeDialog() {
            this.contents = [];
            this.headers = [];
            this.dialog = false;
        },
        importNanotasks() {
            this.closeDialog();
        },
        async getFileContent (file) {
          try {
            const content = await this.readFileAsync(file)
            const firstline = content.split("\n").shift();

            this.headerNames = Papa.parse(firstline).data[0];
            this.headers = [];
            for(const i in this.headerNames) this.headers.push({ text: this.headerNames[i], value: this.headerNames[i] });
            this.contents = Papa.parse(content, { header: true }).data;
          } catch (e) {
            console.log(e)
          }
        },
        async readFileAsync (file) {
          return new Promise((resolve, reject) => {
            const reader = new FileReader()
            reader.onload = () => {
              resolve(reader.result);
            }
            reader.onerror = reject;
            reader.readAsText(file);
          })
        }
    }
}
</script>
