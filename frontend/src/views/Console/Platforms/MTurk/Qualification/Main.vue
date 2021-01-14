<template>
        <v-row class="my-10" justify="center">
            <v-col class="text-right" cols="10">
                <v-btn :loading="button.deleteQuals.loading" :disabled="button.deleteQuals.disabled" class="mx-2" dark
                       color="error" v-if="selectedQualTypeIds.length>0" @click="button.deleteQuals.loading=true; deleteQuals()">Delete ({{ selectedQualTypeIds.length }})</v-btn>
                <v-btn class="mx-2" dark color="indigo" @click="$refs.dialogCreate.shown=true">Create Qualification...</v-btn>
            </v-col>
            <v-col cols="10">
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
                                Created at: <b>{{ item.detail.CreationTime }}</b><br>
                                Automatically grant on submission: <b>{{ item.detail.AutoGranted }}</b><br>
                                # of assigned workers: <b>{{ item.detail.workers ? item.detail.workers.length : 'retrieving...' }}</b><br>
                                Raw data:
                                <vue-json-pretty :data="item.detail" :deep="1" style="font-size:0.6em;"></vue-json-pretty>
                            </div>
                        </td>
                    </template>
                </v-data-table>
            </v-col>

            <tutti-snackbar color="success" :timeout="3000" :text="snackbarTexts.success" />
            <tutti-snackbar color="warning" :timeout="3000" :text="snackbarTexts.warning" />
            <tutti-snackbar color="error" :timeout="3000" :text="snackbarTexts.error" />

            <tutti-dialog ref="dialogCreate" title="Create Qualification Type" maxWidth="500"
                :actions="[
                    { label: 'Create', color: 'indigo darken-1', dark: true, onclick: createQualificationType },
                    { label: 'Cancel', color: 'grey darken-1', text: true }
                ]" >
                <template v-slot:body>
                    <v-row>
                        <v-col cols="12">
                            <v-text-field prepend-icon="mdi-label" v-model="newQualParams.Name" filled label="Name" dense hide-details/>
                        </v-col>
                        <v-col cols="12">
                            <v-text-field prepend-icon="mdi-message-text" v-model="newQualParams.Description" filled label="Description" dense hide-details/>
                        </v-col>
                        <v-col cols="6"><v-switch v-model="newQualParams.AutoGranted" color="indigo" hide-details label="AutoGranted" /></v-col>
                    </v-row>
                </template>
            </tutti-dialog>
        </v-row>
</template>
<script>
import Snackbar from '@/views/assets/Snackbar.vue'
import Dialog from '@/views/assets/Dialog.vue'
import { mapGetters, mapActions } from 'vuex'
import VueJsonPretty from 'vue-json-pretty'
import 'vue-json-pretty/lib/styles.css'
import { stringifyUnixTime } from '@/lib/utils'

export default {
    components: {
        VueJsonPretty,
        TuttiSnackbar: Snackbar,
        TuttiDialog: Dialog
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
        snackbarTexts: {
            success: "",
            warning: "",
            error: ""
        },
            newQualParams: {
            Name: "",
            Description: "",
            AutoGranted: false,
            QualificationTypeStatus: "Active"
        }
    }),
    props: ["credentials", "sharedProps","name"],

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
                        "creationTime": stringifyUnixTime(_q["CreationTime"]),
                        "detail": _q
                    };
                    q.push(data);
                }
            }
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
        },
        createQualificationType() {
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.MTURK_CREATE_QUALIFICATION,
                data: this.newQualParams
            });
        }
    },
    watch: {
        credentials: {
            handler() {
                this._evtGetQualificationTypeIds();
            },
            deep: true
        }
    },
    mounted() {
        this.onDuctOpen(() => {
            this.duct.addEvtHandler({ tag: this.name, eid: this.duct.EVENT.MTURK_LIST_QUALIFICATIONS,
                handler: (rid, eid, data) => {
                    if(data["Status"]=="error") return;

                    var qids = [];
                    this.$set(this.sharedProps, "mTurkQuals", {});
                    for(var i in data["Data"]["QualificationTypes"]){
                        const qtype = data["Data"]["QualificationTypes"][i];
                        const qid = qtype["QualificationTypeId"];
                        qids.push(qtype["QualificationTypeId"]);
                        this.$set(this.sharedProps.mTurkQuals, qid, qtype);
                    }
                    this.selectedQualTypes = [];
                    this.loadingQuals = false;
                    this._evtGetWorkersForQualificationTypeIds(qids);
                }
            });

            this.duct.addEvtHandler({ tag: this.name, eid: this.duct.EVENT.MTURK_CREATE_QUALIFICATION,
                handler: (rid, eid, data) => {
                    if(data["Status"]=="Error") {
                        this.snackbarTexts.error = "Error in creating a qualification";
                    } else {
                        this.snackbarTexts.success = "Successfully created a qualification";
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

            this.duct.addEvtHandler({
                tag: this.name, eid: this.duct.EVENT.MTURK_DELETE_QUALIFICATIONS,
                handler: (rid, eid, data) => {
                    if(data["Status"]=="Error") {
                        this.snackbarTexts.error = "Errors occurred in deleting qualifications";
                    } else {
                        const res = data["Data"]["Results"];
                        var cntSuccess = 0;
                        for(var i in res) {
                            if(("ResponseMetadata" in res[i]) && ("HTTPStatusCode" in res[i]["ResponseMetadata"]) && (res[i]["ResponseMetadata"]["HTTPStatusCode"]==200))
                                cntSuccess++;
                        }
                        if(cntSuccess==res.length) {
                            this.snackbarTexts.success = `Successfully deleted ${res.length} qualifications`;
                        } else {
                            this.snackbarTexts.warning = `Deleted ${cntSuccess} qualifications, but errors occurred in deleting ${res.length-cntSuccess} qualifications`;
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
