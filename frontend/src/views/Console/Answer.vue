<template>
    <v-main class="mt-10 grey lighten-4">
        <v-row justify="center">
            <v-col cols="11">
            <v-card class="pa-3">
                <v-row class="justify-space-around">
                <v-col cols="12" md="7" align="center">
                <v-select width="80%" hide-details :items="templateNames" v-model="templateName" label="Template name" :disabled="isTemplateSelectDisabled"></v-select>
                </v-col>
                </v-row>
            </v-card>
            </v-col>
            <v-col cols="11">
                <v-card>
                    <v-card-title>
                        Answers
                        <v-spacer></v-spacer>
                        <v-text-field v-model="searchStr" append-icon="mdi-magnify" label="Search" single-line hide-details>
                        </v-text-field>
                    </v-card-title>
                    <v-data-table :headers="ansTableHeaders" :items="ansTableRows" :items-per-page="10" :search="searchStr">
                    </v-data-table>
                </v-card>
            </v-col>
        </v-row>
    </v-main>
</template>

<script>
// https://zukucode.com/2017/04/javascript-date-format.html
function formatDate (date, format) {
    format = format.replace(/yyyy/g, date.getFullYear());
    format = format.replace(/MM/g, ('0' + (date.getMonth() + 1)).slice(-2));
    format = format.replace(/dd/g, ('0' + date.getDate()).slice(-2));
    format = format.replace(/HH/g, ('0' + date.getHours()).slice(-2));
    format = format.replace(/mm/g, ('0' + date.getMinutes()).slice(-2));
    format = format.replace(/ss/g, ('0' + date.getSeconds()).slice(-2));
    format = format.replace(/SSS/g, ('00' + date.getMilliseconds()).slice(-3));
    return format;
}

import store from '@/store.js'
import { mapGetters } from 'vuex'

export default {
    store,
    data: () => ({
        templateName: null,
        ansTableHeaderValues: [],
        ansTableHeaders: [],
        searchStr: ""
    }),
    props: ["sharedProps","name"],
    computed: {
        ...mapGetters("ductsModule", ["duct"]),
        project() { return this.sharedProps.project },

        isTemplateSelectDisabled() {
            return !this.project.templates || Object.keys(this.project.templates).length==0
        },
        templateNames() {
            if(this.project.templates) return Object.keys(this.project.templates);
            else return [];
        },
        answers() { return this.sharedProps.answers },
        ansTableRows() {
            var rows = [];
            if(this.duct){
                const ansAll = this.sharedProps.answers;
                for(const i in ansAll){
                    const a = ansAll[i];
                    const sid = a.sessionId;
                    const wid = a.workerId;
                    const nid = a.nanotaskId;
                    const timestamp = a.timestamp ? formatDate(new Date(a.timestamp*1000), "yyyy-MM-dd HH:mm:ss") : "";
                    const ans = a.answers;
                    var row = { sid, wid, nid, timestamp };
                    Object.assign(row, ans);
                    rows.push(row);
                }
            }
            return rows;
        }
    },
    watch: {
        "project.name"() { this.templateName = null },
        templateName() {
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.ANSWERS,
                data: `get ${this.project.name} ${this.templateName}`
            })
        },
        answers(val) {
            const ansAll = val;
            var headerValues = ["sid","wid","nid","timestamp"];
            var headers = [
                { text: "Session ID", value: "sid" },
                { text: "Worker ID", value: "wid" },
                { text: "Nanotask ID", value: "nid" },
                { text: "Submitted time", value: "timestamp" },
            ];
            for(const i in ansAll){
                const ans = ansAll[i].answers;
                for(const key in ans){
                    if(headerValues.indexOf(key)==-1) {
                        headerValues.push(key);
                        headers.push({ text: key, value: key });
                    }
                }
            }
            this.ansTableHeaderValues = headerValues;
            this.ansTableHeaders = headers;
        }
    }
}
</script>
