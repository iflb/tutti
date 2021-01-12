<template>
    <v-main class="mt-10 grey lighten-4">
        <div style="max-width:1200px" class="mx-auto">
            <v-row>
                <v-col class="text-right">
                    <v-btn :loading="button.deleteQuals.loading" :disabled="button.deleteQuals.disabled" class="mx-2" dark
                           color="error" v-if="selectedQualTypeIds.length>0" @click="button.deleteQuals.loading=true; deleteQuals()">Delete ({{ selectedQualTypeIds.length }})</v-btn>
                    <v-btn class="mx-2" dark color="indigo" @click="$refs.dlgCreate.shown=true">Create Qualification...</v-btn>
                </v-col>
            </v-row>
            <v-data-table
              :headers="qualHeaders"
              :items="quals"
              :single-expand="false"
              :expanded.sync="expanded"
              item-key="name"
              show-expand
              class="elevation-1"
              dense
              :loading="loadingQuals"
              show-select
              v-model="selectedQualTypes"
              sort-by="creationTime"
              sort-desc
            >
                <template v-slot:top>
                    <v-card-title>
                        Qualifications
                        <v-btn icon @click="_evtGetQualificationTypeIds()"><v-icon>mdi-refresh</v-icon></v-btn>
                        <!--<v-btn icon @click="$refs.dlgCreate.shown=true"><v-icon>mdi-plus</v-icon></v-btn>-->
                        <v-spacer></v-spacer>
                        <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
                    </v-card-title>
                </template>
                <template v-slot:expanded-item="{ headers, item }">
                    <td :colspan="headers.length">
                        <div class="my-2">
                            <div class="d-flex flex-row-reverse">
                                <v-btn icon color="grey lighten-1"><v-icon>mdi-pencil</v-icon></v-btn>
                                <v-btn icon color="grey lighten-1"><v-icon>mdi-account-edit</v-icon></v-btn>
                            </div>
                            Description: <b>{{ item.detail.Description }}</b><br>
                            Created at: <b>{{ unixTimeToLocaleString(item.detail.CreationTime) }}</b><br>
                            Automatically grant on submission: <b>{{ item.detail.AutoGranted }}</b><br>
                            # of assigned workers: <b>{{ item.detail.workers ? item.detail.workers.length : 'retrieving...' }}</b><br>
                            Raw data:
                            <vue-json-pretty :data="item.detail" :deep="1" style="font-size:0.6em;"></vue-json-pretty>
                        </div>
                    </td>
                </template>
            </v-data-table>
            <dialog-create ref="dlgCreate"></dialog-create>

            <v-snackbar :color="snackbar.success.color" v-model="snackbar.success.shown" :timeout="snackbar.success.timeout">
              {{ snackbar.success.text }}
              <template v-slot:action="{ attrs }">
                  <v-btn dark color="white" text v-bind="attrs" @click="snackbar.success.shown=false">Close</v-btn>
              </template>
            </v-snackbar>
            <v-snackbar :color="snackbar.warning.color" v-model="snackbar.warning.shown" :timeout="snackbar.warning.timeout">
              {{ snackbar.warning.text }}
              <template v-slot:action="{ attrs }">
                  <v-btn dark color="white" text v-bind="attrs" @click="snackbar.warning.shown=false">Close</v-btn>
              </template>
            </v-snackbar>
            <v-snackbar :color="snackbar.error.color" v-model="snackbar.error.shown" :timeout="snackbar.error.timeout">
              {{ snackbar.error.text }}
              <template v-slot:action="{ attrs }">
                  <v-btn dark color="white" text v-bind="attrs" @click="snackbar.error.shown=false">Close</v-btn>
              </template>
            </v-snackbar>

        </div>
    </v-main>
</template>
<script>
import DialogCreate from './DialogCreate.vue'
import { mapGetters, mapActions } from 'vuex'
import VueJsonPretty from 'vue-json-pretty'
import 'vue-json-pretty/lib/styles.css'

export default {
    components: {
        VueJsonPretty,
        DialogCreate
    },
    data: () => ({
        selectedQualTypes: [],
        search: "",
        expanded: [],
        qualHeaders: [
          { text: 'Name', value: 'name' },
          { text: 'Status', value: 'status' },
          { text: 'QualificationTypeId', value: 'qualificationId' },
          { text: 'CreationTime', value: 'creationTime' },
          { text: '', value: 'data-table-expand' },
        ],
        loadingQuals: false,
        button: {
            deleteQuals: {
                loading: false,
                disabled: false
            },
        },
        snackbar: {
            success: {
                shown: false,
                text: "",
                timeout: 5000,
                color: "success"
            },
            warning: {
                shown: false,
                text: "",
                timeout: 5000,
                color: "warning"
            },
            error: {
                shown: false,
                text: "",
                timeout: 5000,
                color: "error"
            }
        }
    }),
    props: ["sharedProps","name"],

    computed: {
        ...mapGetters("ductsModule", [ "duct" ]),
        quals() {
            var q = []
            if("mTurkQuals" in this.sharedProps) {
                for(var qid in this.sharedProps.mTurkQuals){
                    const _q = this.sharedProps.mTurkQuals[qid];
                    const data = {
                        "name": _q["Name"],
                        "status": _q["QualificationTypeStatus"],
                        "qualificationId": _q["QualificationTypeId"],
                        "creationTime": this.unixTimeToLocaleString(_q["CreationTime"]),
                        "detail": _q
                    };
                    q.push(data);
                }
            }
            console.log(q);
            return q
        },
        selectedQualTypeIds() {
            var qtids = [];
            for(var i in this.selectedQualTypes)
                qtids.push(this.selectedQualTypes[i]["detail"]["QualificationTypeId"]);
            return qtids;
        }
    },
    methods: {
        ...mapActions("ductsModule", [ "onDuctOpen" ]),
        unixTimeToLocaleString(unixTime) {
            var dt = new Date(unixTime*1000);
            return dt.toLocaleDateString() + " " + dt.toLocaleTimeString();
        },
        deleteQuals() {
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.MTURK_DELETE_QUALIFICATIONS,
                data: {
                    "QualificationTypeIds": this.selectedQualTypeIds
                }
            });
        },
        _evtGetQualificationTypeIds() {
            this.loadingQuals = true;
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.MTURK_LIST_QUALIFICATIONS,
                data: null
            });
        },
        _evtGetWorkersForQualificationTypeIds(qids){
            for(var i in qids){
                this.duct.sendMsg({
                    tag: this.name,
                    eid: this.duct.EVENT.MTURK_LIST_WORKERS_WITH_QUALIFICATION_TYPE,
                    data: {
                        "QualificationTypeId": qids[i]
                    }
                });
            }
        }
    },
    mounted() {
        this.onDuctOpen(() => {
            this.duct.addEvtHandler({ tag: this.name, eid: this.duct.EVENT.MTURK_LIST_QUALIFICATIONS,
                handler: (rid, eid, data) => {
                    if(data["Status"]=="error") return;

                    var qids = [];
                    for(var i in data["Data"]["QualificationTypes"]){
                        qids.push(data["Data"]["QualificationTypes"][i]["QualificationTypeId"]);
                    }
                    this.$set(this.sharedProps, "mTurkQuals", data["Data"]["QualificationTypes"]);
                    this.selectedQualTypes = [];
                    this.loadingQuals = false;
                    this._evtGetWorkersForQualificationTypeIds(qids);
                }
            });

            this.duct.addEvtHandler({ tag: this.name, eid: this.duct.EVENT.MTURK_CREATE_QUALIFICATION,
                handler: (rid, eid, data) => {
                    if(data["Status"]=="Error") {
                        this.snackbar.error.text = "Successfully created a qualification";
                        this.snackbar.error.shown = true;
                        console.log(data["Reason"]);
                    } else {
                        this.snackbar.success.text = "Successfully created a qualification";
                        this.snackbar.success.shown = true;
                        this._evtGetQualificationTypeIds();
                    }
                }
            });

            this.duct.addEvtHandler({ tag: this.name, eid: this.duct.EVENT.MTURK_LIST_WORKERS_WITH_QUALIFICATION_TYPE,
                handler: (rid, eid, data) => {
                    const qid = data["Data"]["Results"][0]["QualificationTypeId"];
                    var quals = data["Data"]["Results"];
                    this.$set(this.sharedProps.mTurkQuals[qid], "workers", quals);
                }
            });

            //this.duct.addEvtHandler({ tag: this.name, eid: this.duct.EVENT.MTURK_QUALIFICATION, handler: (rid, eid, data) => {
            //        const command = data["Data"]["Command"];
            //        if(data["Status"]=="error") return;

            //        //if(command=="List"){
            //        //    var qids = [];
            //        //    for(var i in data["Data"]["QualificationTypes"]){
            //        //        qids.push(data["Data"]["QualificationTypes"][i]["QualificationTypeId"]);
            //        //    }
            //        //    this.$set(this.sharedProps, "mTurkQuals", data["Data"]["QualificationTypes"]);
            //        //    this.selectedQualTypes = [];
            //        //    this.loadingQuals = false;
            //        //    this._evtGetWorkersForQualificationTypeIds(qids);
            //        //}
            //        //else
            //        if(command=="Create"){
            //            this.snackbar.success.text = "Successfully created a qualification";
            //            this.snackbar.success.shown = true;
            //            this._evtGetQualificationTypeIds();
            //        }
            //        //else if(command=="GetWorkers"){
            //        //}
            //    }
            //});

            this.duct.addEvtHandler({
                tag: this.name, eid: this.duct.EVENT.MTURK_DELETE_QUALIFICATIONS,
                handler: (rid, eid, data) => {
                    if(data["Status"]=="Error") {
                        this.snackbar.error.text = "Errors occurred in deleting qualifications";
                        this.snackbar.error.shown = true;
                    } else {
                        const res = data["Data"]["Results"];
                        var cntSuccess = 0;
                        for(var i in res) {
                            if(("ResponseMetadata" in res[i]) && ("HTTPStatusCode" in res[i]["ResponseMetadata"]) && (res[i]["ResponseMetadata"]["HTTPStatusCode"]==200))
                                cntSuccess++;
                        }
                        if(cntSuccess==res.length) {
                            this.snackbar.success.text = `Successfully deleted ${res.length} qualifications`;
                            this.snackbar.success.shown = true;
                        } else {
                            this.snackbar.warning.text = `Deleted ${cntSuccess} qualifications, but errors occurred in deleting ${res.length-cntSuccess} qualifications`;
                            this.snackbar.warning.shown = true;
                        }

                    }
                    this.button.deleteQuals.loading = false;
                    this.button.deleteQuals.disabled = false;
                    this._evtGetQualificationTypeIds();
                }
            });

            this._evtGetQualificationTypeIds();
        });
    }
}
</script>
<style>
.v-data-table tbody tr.v-data-table__expanded__content {
    box-shadow: none;
    background-color: #f5f5f5;
}
.is-root, .is-root div {
    font-size: 9pt;
}
</style>
