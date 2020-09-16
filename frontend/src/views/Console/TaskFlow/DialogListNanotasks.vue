<template>
    <v-dialog v-model="show" max-width="1200" persistent>
      <v-card>
        <v-card-title class="headline">
            Import Nanotasks for '{{ template }}'
        </v-card-title>
        <v-card-text>
            <v-file-input accept=".csv,.CSV" show-size label=".csv file to upload" @change="getFileContent"></v-file-input>
        </v-card-text>
        <v-card v-if="contents.length>0" class="mx-6">
            <v-card-title>
                CSV File Parsing Results
                <v-spacer></v-spacer>
                <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details />
            </v-card-title>
            <v-data-table dense :headers="headers" :items="contents" :search="search"></v-data-table>
        </v-card>
        <v-container v-if="contents.length>0">
            <v-row>
                <v-col><v-text-field v-model="tagName" label="Tag Name" :min="1" /></v-col>
                <v-col><v-text-field v-model="numAssignments" type="number" label="# Assignments" :min="1" /></v-col>
                <v-col><v-text-field v-model="priority" type="number" label="Priority" :min="1" /></v-col>
                <v-spacer/>
            </v-row>
        </v-container>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog" > Cancel </v-btn>
          <v-btn color="primary" @click="importNanotasks" :disabled="contents.length==0"> Import </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
</template>

<script>
import Papa from 'papaparse'

import store from '@/store.js'
import { mapGetters } from 'vuex'

export default {
    store,
    data: () => ({
        show: false,
        headers: [],
        headerNames: [],
        contents: [],
        search: "",

        tagName: "",
        numAssignments: 1,
        priority: 1
    }),
    props: ["project", "template"],
    computed: {
        ...mapGetters("ductsModule", [ "duct" ]),
    },
    methods: {
        closeDialog() {
            this.contents = [];
            this.headers = [];
            this.show = false;
        },
        importNanotasks() {
            const data = {
                projectName: this.project.name,
                templateName: this.template,
                tag: this.tagName,
                numAssignable: this.numAssignments,
                priority: this.priority,
                props: this.contents
            }
            this.duct.sendMsg({ tag: "recursive", eid: this.duct.EVENT.UPLOAD_NANOTASKS, data: data });
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
