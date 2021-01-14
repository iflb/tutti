<template>
        <v-row class="my-10" justify="center">
            <v-col cols="10" class="text-right">
                <!--<v-btn :loading="button.expireHITs.loading" :disabled="button.expireHITs.disabled" class="mx-2" dark
                       color="warning" v-if="selectedHITIds.length>0" @click="button.expireHITs.loading=true; expireHITs()">Expire ({{ selectedHITIds.length }})</v-btn>
                <v-btn :loading="button.deleteHITs.loading" :disabled="button.deleteHITs.disabled" class="mx-2" dark
                       color="error" v-if="selectedHITIds.length>0" @click="button.deleteHITs.loading=true; deleteHITs()">Delete ({{ selectedHITIds.length }})</v-btn>-->
                <v-btn class="mx-2" dark color="indigo" @click="$refs.dialogSendEmail.shown=true">Create HITs...</v-btn>
            </v-col>
            <v-col cols="10">
                <v-data-table
                  :headers="workerHeaders"
                  :items="workers"
                  item-key="name"
                  class="elevation-1"
                  dense
                  :loading="loadingWorkers"
                  show-select
                  v-model="selectedQualTypes"
                  sort-by="Timestamp"
                  sort-desc
                >
                    <template v-slot:top>
                        <v-card-title>
                            Workers
                            <v-btn icon @click="_evtListWorkers()"><v-icon>mdi-refresh</v-icon></v-btn>
                            <!--<v-btn icon @click="$refs.dlgCreate.shown=true"><v-icon>mdi-plus</v-icon></v-btn>-->
                            <v-spacer></v-spacer>
                            <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
                        </v-card-title>
                    </template>
                </v-data-table>
            </v-col>

            <tutti-snackbar color="success" :timeout="3000" :text="snackbarTexts.success" />
            <tutti-snackbar color="warning" :timeout="3000" :text="snackbarTexts.warning" />
            <tutti-snackbar color="error" :timeout="3000" :text="snackbarTexts.error" />

            <tutti-dialog ref="dialogSendEmail" title="Send Email to Workers" maxWidth="800"
                :actions="[
                    { label: 'Send', color: 'indigo darken-1', dark: true, onclick: sendEmail },
                    { label: 'Cancel', color: 'grey darken-1', text: true }
                ]" >
                <template v-slot:body>
                    <v-textarea v-model="hoge"></v-textarea>
                </template>
            </tutti-dialog>
        </v-row>
</template>
<script>
import { mapGetters, mapActions } from 'vuex'
import Snackbar from '@/views/assets/Snackbar.vue'
import Dialog from '@/views/assets/Dialog.vue'
import { stringifyUnixTime } from '@/lib/utils'

export default {
    components: {
        TuttiSnackbar: Snackbar,
        TuttiDialog: Dialog
    },
    data: () => ({
        selectedQualTypes: [],
        hoge: "",
        search: "",
        expanded: [],
        workerHeaders: [
          { text: 'Worker ID', value: 'wid' },
          { text: 'Worker ID (Platform)', value: 'PlatformWorkerId' },
          { text: 'Created Time', value: 'Timestamp' },
        ],
        workers: [],
        loadingWorkers: false,
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
    }),
    props: ["sharedProps","name"],

    computed: {
        ...mapGetters("ductsModule", [ "duct" ]),
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
        _evtListWorkers() {
            this.loadingWorkers = true;
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.MTURK_LIST_WORKERS,
                data: null
            });
        },

        sendEmail() {
            console.log(this.hoge);
        }
    },
    watch: {
        credentials: {
            handler() { this._evtListWorkers(); },
            deep: true
        }
    },
    mounted() {
        this.onDuctOpen(() => {
            this.duct.addEvtHandler({ tag: this.name, eid: this.duct.EVENT.MTURK_LIST_WORKERS,
                handler: (rid, eid, data) => {
                    this.loadingWorkers = false;
                    if(data["Status"]=="error") return;

                    var workers = [];
                    for(var wid in data["Data"]["Workers"]) {
                        data["Data"]["Workers"][wid]["Timestamp"] = stringifyUnixTime(data["Data"]["Workers"][wid]["Timestamp"]);
                        workers.push({ wid, ...data["Data"]["Workers"][wid] });
                    }
                    this.workers = workers;
                }
            });

            this._evtListWorkers();
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
