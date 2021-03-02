<template>
        <v-row class="my-10" justify="center">
            <v-col cols="10" class="text-right">
                <v-tooltip top>
                    <template #activator="{ on, attrs }">
                        <v-btn v-bind="attrs" v-on="on" class="mx-2" dark color="indigo" @click="$refs.dialogSendEmail.shown=true"><v-icon>mdi-email</v-icon></v-btn>
                    </template>
                    <span>Send email</span>
                </v-tooltip>
                <v-tooltip top>
                    <template #activator="{ on, attrs }">
                        <v-btn v-bind="attrs" v-on="on" class="mx-2" dark color="indigo" @click="$refs.dialogAssociateQuals.shown=true; if(!quals) listQualifications();"><v-icon>mdi-account-star</v-icon></v-btn>
                    </template>
                    <span>Grant qualification</span>
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
                  :search="search"
                >
                    <template v-slot:top>
                        <v-card-title>
                            Workers
                            <v-btn icon @click="listWorkers()"><v-icon>mdi-refresh</v-icon></v-btn>
                            <!--<v-btn icon @click="$refs.dlgCreate.shown=true"><v-icon>mdi-plus</v-icon></v-btn>-->
                            <v-spacer></v-spacer>
                            <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
                        </v-card-title>
                    </template>
                    <template v-slot:item.Projects="{ item }">
                        {{ item.Projects.join(", ") }}
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
                    <v-combobox dense multiple small-chips outlined hide-selected v-model="sendEmailWorkerIds" :items="workerIds" label="To" :search-input.sync="searchedWorkerId">
                        <template v-slot:no-data>
                            <v-list-item>
                                <v-list-item-content>
                                    <v-list-item-title>
                                        No results matching "<strong>{{ searchedWorkerId }}</strong>". Press <kbd>enter</kbd> to create a new one
                                    </v-list-item-title>
                                </v-list-item-content>
                            </v-list-item>
                        </template>
                    </v-combobox>
                    <v-text-field dense outlined label="Subject" v-model="email.Subject" />
                    <v-textarea outlined label="Message" v-model="email.MessageText"></v-textarea>
                </template>
            </tutti-dialog>

            <tutti-dialog ref="dialogAssociateQuals" title="Associate Qualifications to Workers" maxWidth="800" persistent
                :actions="[
                    { label: 'Send', color: 'indigo darken-1', dark: true, onclick: associateQuals },
                    { label: 'Cancel', color: 'grey darken-1', text: true }
                ]" >
                <template v-slot:body>
                    <v-combobox dense multiple small-chips outlined hide-selected v-model="newAssociateQual.WorkerIds" :items="workerIds" label="To" :search-input.sync="searchedWorkerId">
                        <template v-slot:no-data>
                            <v-list-item>
                                <v-list-item-content>
                                    <v-list-item-title>
                                        No results matching "<strong>{{ searchedWorkerId }}</strong>". Press <kbd>enter</kbd> to create a new one
                                    </v-list-item-title>
                                </v-list-item-content>
                            </v-list-item>
                        </template>
                    </v-combobox>
                    <v-select v-model="newAssociateQual.QualificationTypeId" :items="qualificationTypes" label="QualificationTypeId" dense outlined></v-select>
                    <v-text-field dense outlined v-model.number="newAssociateQual.IntegerValue" label="IntegerValue"></v-text-field>
                    <v-switch v-model="newAssociateQual.SendNotification" label="SendNotification"/>
                </template>
            </tutti-dialog>
        </v-row>
</template>
<script>
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
        searchedWorkerId: "",
        workerHeaders: [
          { text: 'Worker ID', value: 'wid' },
          { text: 'Worker ID (MTurk)', value: 'PlatformWorkerId' },
          { text: 'Visited Projects', value: 'Projects' },
          { text: 'Created Time', value: 'Timestamp' },
        ],
        selectedWorkers: [],
        workers: [],
        sendEmailWorkerIds: [],
        newAssociateQual: {
            WorkerIds: [],
            QualificationTypeId: "",
            IntegerValue: null,
            SendNotification: true
        },
        loadingWorkers: false,
        snackbarTexts: {
            success: "",
            warning: "",
            error: ""
        },
        email: {
            Subject: "",
            MessageText: ""
        },
        quals: null
    }),
    props: ["duct", "sharedProps","name"],

    computed: {
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
        },
        qualificationTypes() {
            var wids = [];
            for(var i in this.quals) {
                const id = this.quals[i]["QualificationTypeId"];
                const name = this.quals[i]["Name"];
                wids.push({ text: `${name} - ${id}`, value: this.quals[i]["QualificationTypeId"] });
            }
            return wids;
        }
    },
    methods: {
        unixTimeToLocaleString(unixTime) {
            var dt = new Date(unixTime*1000);
            return dt.toLocaleDateString() + " " + dt.toLocaleTimeString();
        },
        associateQuals() {
            this.duct.controllers.mturk.associateQualificationsWithWorkers(this.newAssociateQual);
        },
        listWorkers() {
            this.loadingWorkers = true;
            this.duct.controllers.mturk.listWorkers();
        },
        listQualifications() {
            this.duct.controllers.mturk.listQualifications();
        },
        sendEmail() {
            this.duct.controllers.mturk.notifyWorkers(this.email.Subject, this.email.MessageText, this.sendEmailWorkerIds);
        }
    },
    watch: {
        credentials: {
            handler() { this.listWorkers(); },
            deep: true
        },
        selectedWorkerIds() {
            this.sendEmailWorkerIds = this.selectedWorkerIds;
            this.newAssociateQual.WorkerIds = this.selectedWorkerIds;
        }
    },
    mounted() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.mturk.on("listWorkers", {
                success: (data) => {
                    this.loadingWorkers = false;

                    var workers = [];
                    for(var wid in data["Workers"]) {
                        data["Workers"][wid]["Timestamp"] = stringifyUnixTime(data["Workers"][wid]["Timestamp"]);
                        workers.push({ wid, ...data["Workers"][wid] });
                    }
                    this.workers = workers;
                },
                error: (data) => {
                    console.log("error", data);
                }
            });
            this.duct.eventListeners.mturk.on("listQualifications", {
                success: (data) => {
                    this.quals = data["QualificationTypes"];
                }
            });

            this.listWorkers();
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
