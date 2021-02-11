<template>
    <v-main>
        <v-toolbar class="grey lighten-4">
            <v-row justify="center" align="end"><v-col cols="8">
                <v-select width="80%" hide-details :items="tmplNames" v-model="tmplName" label="Template name" :disabled="tmplNames.length==0"></v-select>
            </v-col></v-row>
        </v-toolbar>

        <v-card-title>
            Answers
            <v-spacer></v-spacer>
            <v-text-field v-model="searchStr" append-icon="mdi-magnify" label="Search" single-line hide-details>
            </v-text-field>
        </v-card-title>
        <v-data-table :headers="answerHeaders" :items="answerRows" :items-per-page="50" :footer-props="{ itemsPerPageOptions: [10,30,50,100,300] }" :search="searchStr">
        </v-data-table>
    </v-main>
</template>

<script>
import { stringifyUnixTime } from '@/lib/utils'

export default {
    data: () => ({
        tmplNames: [],
        tmplName: null,

        answerHeaders: [],
        answers: [],

        searchStr: "",
    }),
    props: ["duct", "prjName","name"],
    computed: {
        answerRows() {
            var rows = [];
            if(this.duct){
                const ansAll = this.answers;
                for(const i in ansAll){
                    const a = ansAll[i];
                    const wsid = a.WorkSessionId;
                    const wid = a.WorkerId;
                    const nid = a.NanotaskId;
                    const timestamp = stringifyUnixTime(a.Timestamp) || "";
                    const ans = a.Answers;
                    var row = { wsid, wid, nid, timestamp };
                    Object.assign(row, ans);
                    rows.push(row);
                }
            }
            return rows;
        }
    },
    methods: {
        listTemplates() {
            this.tmplName = null;
            this.duct.controllers.resource.listTemplates(this.prjName);
        }
    },
    watch: {
        prjName() {
            this.listTemplates();
        },
        tmplName() {
            this.duct.controllers.resource.getAnswersForTemplate(this.prjName, this.tmplName);
        },
        answers(val) {
            const ansAll = val;
            var headers = [
                { text: "Session ID", value: "wsid" },
                { text: "Worker ID", value: "wid" },
                { text: "Nanotask ID", value: "nid" },
                { text: "Submitted time", value: "timestamp" },
            ];
            var headerValues = headers.map((item) => (item.value));
            for(const i in ansAll){
                for(const key in ansAll[i].Answers){
                    if(!headerValues.includes(key)) {
                        headers.push({ text: key, value: key });
                        headerValues.push(key);
                    }
                }
            }
            this.answerHeaders = headers;
        }
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.resource.on("listTemplates", {
                success: (data) => {
                    this.tmplNames = data["Templates"];
                }
            });

            this.duct.eventListeners.resource.on("getAnswersForTemplate", {
                success: (data) => {
                    this.answers = data["Answers"];
                }
            });

            if(this.prjName) this.listTemplates();
        });
    }
}
</script>
