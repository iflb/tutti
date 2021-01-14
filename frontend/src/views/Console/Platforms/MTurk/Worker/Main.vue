<template>
        <v-row class="my-10" justify="center">
            <v-col cols="10" class="text-right">
                <v-tooltip top>
                    <template #activator="{ on, attrs }">
                        <v-btn v-bind="attrs" v-on="on" class="mx-2" dark color="indigo" @click="$refs.dialogSendEmail.shown=true"><v-icon>mdi-email</v-icon></v-btn>
                    </template>
                    <span>Send email</span>
                </v-tooltip>
            </v-col>
            <v-col cols="10">
                <v-data-table
                  :headers="workerHeaders"
                  :items="workers"
                  item-key="wid"
                  class="elevation-1"
                  dense
                  :loading="loadingWorkers"
                  show-select
                  v-model="selectedWorkers"
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

            <tutti-dialog ref="dialogSendEmail" title="Send Email to Workers" maxWidth="800" persistent
                :actions="[
                    { label: 'Send', color: 'indigo darken-1', dark: true, onclick: sendEmail },
                    { label: 'Cancel', color: 'grey darken-1', text: true }
                ]" >
                <template v-slot:body>
                    <v-combobox dense multiple small-chips outlined hide-selected v-model="sendEmailWorkerIds" :items="workerIds" label="To">
                        <template v-slot:no-data>
                            <v-list-item>
                                <v-list-item-content>
                                    <v-list-item-title>
                                        No results matching "<strong>{{ search }}</strong>". Press <kbd>enter</kbd> to create a new one
                                    </v-list-item-title>
                                </v-list-item-content>
                            </v-list-item>
                        </template>
                    </v-combobox>
                    <v-text-field dense outlined label="Subject" v-model="email.Subject" />
                    <v-textarea outlined label="Message" v-model="email.MessageText"></v-textarea>
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
        hoge: "",
        search: "",
        workerHeaders: [
          { text: 'Worker ID', value: 'wid' },
          { text: 'Worker ID (MTurk)', value: 'PlatformWorkerId' },
          { text: 'Created Time', value: 'Timestamp' },
        ],
        selectedWorkers: [],
        workers: [],
        sendEmailWorkerIds: [],
        loadingWorkers: false,
        snackbarTexts: {
            success: "",
            warning: "",
            error: ""
        },
        email: {
            Subject: "",
            MessageText: ""
        }
    }),
    props: ["sharedProps","name"],

    computed: {
        ...mapGetters("ductsModule", [ "duct" ]),
        selectedWorkerIds() {
            var wids = [];
            for(var i in this.selectedWorkers)
                wids.push(this.selectedWorkers[i]["PlatformWorkerId"]);
            return wids;
        },
        workerIds() {
            var wids = [];
            for(var i in this.workers)
                wids.push(this.workers[i]["PlatformWorkerId"]);
            return wids;
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
        _evtSendEmail() {
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.MTURK_NOTIFY_WORKERS,
                data: { ...this.email, "WorkerIds": this.sendEmailWorkerIds }
            });
        },

        sendEmail() {
            this._evtSendEmail();
        }
    },
    watch: {
        credentials: {
            handler() { this._evtListWorkers(); },
            deep: true
        },
        selectedWorkerIds() {
            this.sendEmailWorkerIds = this.selectedWorkerIds;
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
