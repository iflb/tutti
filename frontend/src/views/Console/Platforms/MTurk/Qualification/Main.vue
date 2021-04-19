<template>
        <v-row class="my-10" justify="center">
            <v-col class="text-right" cols="10">
                <v-btn :loading="button.deleteQuals.loading" :disabled="button.deleteQuals.disabled" class="mx-2" dark
                       color="error" v-if="selectedQualTypeIds.length>0" @click="button.deleteQuals.loading=true; deleteQualifications()">Delete ({{ selectedQualTypeIds.length }})</v-btn>
                <v-btn class="mx-2" dark color="indigo" @click="$refs.dialogCreate.shown=true">Create Qualification...</v-btn>
            </v-col>
            <v-col cols="10">
                <v-data-table
                  :headers="qualHeaders"
                  :items="qualsList"
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
                            <v-btn icon @click="getQualificationTypeIds()"><v-icon>mdi-refresh</v-icon></v-btn>
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

            <tutti-snackbar ref="snackbarSuccess" color="success" :timeout="3000" />
            <tutti-snackbar ref="snackbarWarning" color="warning" :timeout="3000" />
            <tutti-snackbar ref="snackbarError" color="error" :timeout="3000" />

            <tutti-dialog ref="dialogCreate" title="Create Qualification Type" maxWidth="500"
                :actions="[
                    { label: 'Create', color: 'indigo darken-1', disableByRule: true, text: true, onclick: createQualificationType },
                    { label: 'Cancel', color: 'grey darken-1', text: true }
                ]" >
                <template v-slot:body>
                    <v-row>
                        <v-col cols="12" class="mb-0 pb-0">
                            <v-text-field prepend-icon="mdi-label" v-model="newQualParams.Name" filled label="Name" :rules="[rules.required]" dense/>
                        </v-col>
                        <v-col cols="12" class="my-0 py-0">
                            <v-text-field prepend-icon="mdi-message-text" v-model="newQualParams.Description" filled label="Description" :rules="[rules.required]" dense/>
                        </v-col>
                        <v-col cols="6" class="my-0 py-0"><v-switch v-model="newQualParams.AutoGranted" color="indigo" hide-details label="AutoGranted" /></v-col>
                    </v-row>
                </template>
            </tutti-dialog>
        </v-row>
</template>
<script>
import 'vue-json-pretty/lib/styles.css'
import { stringifyUnixTime } from '@/lib/utils'
import rules from '@/lib/input-rules'

export default {
    components: {
        VueJsonPretty: () => import('vue-json-pretty/lib/vue-json-pretty'),
        TuttiSnackbar: () => import('@/views/assets/Snackbar'),
        TuttiDialog: () => import('@/views/assets/Dialog')
    },
    data: () => ({
        rules,

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
        newQualParams: {
            Name: "",
            Description: "",
            AutoGranted: false,
            QualificationTypeStatus: "Active"
        },
        quals: {},

        button: {
            deleteQuals: {
                loading: false,
                disabled: false
            },
        },
    }),
    props: ["duct", "credentials", "sharedProps","name"],

    computed: {
        selectedQualTypeIds() {
            var qtids = [];
            for(var i in this.selectedQualTypes)
                qtids.push(this.selectedQualTypes[i]["detail"]["QualificationTypeId"]);
            return qtids;
        },
        qualsList() {
            return Object.entries(this.quals).map((val) => (val[1]));
        }
    },
    methods: {
        deleteQualifications() {
            this.duct.controllers.mturk.deleteQualifications( this.selectedQualTypeIds );
        },
        getQualificationTypeIds() {
            this.loadingQuals = true;
            this.duct.controllers.mturk.listQualifications(false);
        },
        _evtGetWorkersForQualificationTypeIds(qids){
            for(var i in qids){
                this.duct.controllers.mturk.listWorkersWithQualificationType(qids[i]);
            }
        },
        createQualificationType() {
            this.duct.controllers.mturk.createQualification(this.newQualParams);
        }
    },
    mounted() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.mturk.on("listQualifications", {
                success: (data) => {
                    this.quals = {};
                    const qtypes = data["QualificationTypes"];
                    for(const qtype of qtypes){
                        this.$set(this.quals, qtype.QualificationTypeId, {
                            "name": qtype["Name"],
                            "status": qtype["QualificationTypeStatus"],
                            "qualificationId": qtype["QualificationTypeId"],
                            "creationTime": stringifyUnixTime(qtype["CreationTime"]),
                            "detail": qtype
                        });
                    }

                    this.selectedQualTypes = [];
                    this.loadingQuals = false;
                    this._evtGetWorkersForQualificationTypeIds( Object.keys(this.quals) );
                }
            });

            this.duct.eventListeners.mturk.on("createQualification", {
                success: () => {
                    this.$refs.snackbarSuccess.show("Successfully created a qualification");
                    this.getQualificationTypeIds();
                },
                error: (data) => {
                    this.$refs.snackbarError.show(`Error in creating a qualification: ${data["Reason"]}`);
                }
            });

            this.duct.eventListeners.mturk.on("listWorkersWithQualificationType", {
                success: (data) => {
                    const qid = data["QualificationTypeId"];
                    var quals = data["Results"];
                    this.$set(this.quals[qid].detail, "workers", quals);
                }
            });

            this.duct.eventListeners.mturk.on("deleteQualifications", {
                success: (data) => {
                    const res = data["Results"];
                    var cntSuccess = 0;
                    for(var i in res) {
                        if(("ResponseMetadata" in res[i]) && ("HTTPStatusCode" in res[i]["ResponseMetadata"]) && (res[i]["ResponseMetadata"]["HTTPStatusCode"]==200))
                            cntSuccess++;
                    }
                    if(cntSuccess==res.length) {
                        this.$refs.snackbarSuccess.show(`Successfully deleted ${res.length} qualifications`);
                    } else {
                        this.$refs.snackbarSuccess.show(`Deleted ${cntSuccess} qualifications, but errors occurred in deleting ${res.length-cntSuccess} qualifications`);
                    }

                    this.button.deleteQuals.loading = false;
                    this.button.deleteQuals.disabled = false;
                },
                error: (data) => {
                    this.$refs.snackbarError.show(`Errors occurred in deleting qualifications: ${data["Reason"]}`);

                    this.button.deleteQuals.loading = false;
                    this.button.deleteQuals.disabled = false;
                }
            });

            this.getQualificationTypeIds();
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
