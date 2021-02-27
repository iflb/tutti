<template>
        <v-row class="my-10" justify="center">
            <v-col cols="10" class="text-right">
                <v-tooltip top>
                    <template #activator="{ on, attrs }">
                        <v-btn v-bind="attrs" v-on="on" class="mx-2" dark color="success" @click="$refs.dialogApprove.show()"><v-icon>mdi-check-bold</v-icon></v-btn>
                    </template>
                    <span>Approve assignment(s)</span>
                </v-tooltip>
                <v-tooltip top>
                    <template #activator="{ on, attrs }">
                        <v-btn v-bind="attrs" v-on="on" class="mx-2" dark color="error" @click="$refs.dialogReject.show()"><v-icon>mdi-close-thick</v-icon></v-btn>
                    </template>
                    <span>Reject assignment(s)</span>
                </v-tooltip>
            </v-col>
            <v-col cols="10">
                <v-data-table
                  :headers="headers"
                  :items="assignments"
                  item-key="AssignmentId"
                  class="elevation-1"
                  dense
                  :loading="loading"
                  show-select
                  v-model="selected"
                  sort-by="Timestamp"
                  sort-desc
                  :items-per-page="100"
                  :footer-props="{ itemsPerPageOptions: [10,30,50,100,300] }"
                  :search="searchAssignments"
                >
                    <template v-slot:top>
                        <v-card-title>
                            Assignments
                            <v-btn icon @click="listAssignments(false)"><v-icon>mdi-refresh</v-icon></v-btn>
                            <!--<v-btn icon @click="$refs.dlgCreate.shown=true"><v-icon>mdi-plus</v-icon></v-btn>-->
                            <v-spacer></v-spacer>
                            <v-text-field v-model="searchAssignments" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
                        </v-card-title>
                        <v-card-subtitle>
                        (Last retrieved: {{ listLastRetrieved }})
                        </v-card-subtitle>
                    </template>
                    <template v-slot:item.AssignmentId="{ item }">
                        <div class="text-truncate" style="max-width:100px;">
                            {{ item.AssignmentId }}
                        </div>
                    </template>
                    <template v-slot:item.WorkerId="{ item }">
                        {{ item.PlatformWorkerId }}<br>
                        ({{ item.WorkerId }})
                    </template>
                    <template v-slot:item.AcceptTime="{ item }">
                        {{ stringifyUnixTime(item.AcceptTime*1000) }}
                    </template>
                    <template v-slot:item.SubmitTime="{ item }">
                        {{ stringifyUnixTime(item.SubmitTime*1000) }}
                    </template>
                    <template v-slot:item.AutoApprovalTime="{ item }">
                        {{ stringifyUnixTime(item.AutoApprovalTime*1000) }}
                    </template>
                </v-data-table>
            </v-col>

            <tutti-snackbar ref="snackbarSuccess" color="success" :timeout="3000" />
            <tutti-snackbar ref="snackbarWarning" color="warning" :timeout="3000" />
            <tutti-snackbar ref="snackbarError" color="error" :timeout="3000" />

            <tutti-dialog ref="dialogApprove" title="Approve Assignment(s)" maxWidth="500" persistent
                :actions="[
                    { label: 'Confirm', color: 'indigo darken-1', text: true, onclick: approveAssignments },
                    { label: 'Cancel', color: 'grey darken-1', text: true }
                ]" >
                <template v-slot:body>
                    Approve {{ selectedIds.length }} assignments?
                    <v-text-field v-model="message" label="Message to workers (optional)"></v-text-field>
                </template>
            </tutti-dialog>

            <tutti-dialog ref="dialogReject" title="Reject Assignment(s)" maxWidth="500" persistent
                :actions="[
                    { label: 'Confirm', color: 'indigo darken-1', disableByRule: true, text: true, onclick: rejectAssignments },
                    { label: 'Cancel', color: 'grey darken-1', text: true }
                ]" >
                <template v-slot:body>
                    Reject {{ selectedIds.length }} assignments?<br>
                    Caution: You must be careful when rejecting workers.
                    <v-text-field autofocus v-model="message" label="Reason for rejection (required)" :rules="[rules.required]"></v-text-field>
                </template>
            </tutti-dialog>

        </v-row>
</template>
<script>
import Snackbar from '@/views/assets/Snackbar.vue'
import Dialog from '@/views/assets/Dialog.vue'
import { stringifyUnixTime } from '@/lib/utils'
import rules from '@/lib/input-rules'

export default {
    components: {
        TuttiSnackbar: Snackbar,
        TuttiDialog: Dialog
    },
    data: () => ({
        rules,

        stringifyUnixTime,
        headers: [
            { text: "Assignment ID", value: "AssignmentId" },
            { text: "Worker ID", value: "WorkerId" },
            { text: "Status", value: "AssignmentStatus" },
            { text: "Accepted at", value: "AcceptTime" },
            { text: "Submitted at", value: "SubmitTime" },
            { text: "Auto-approve at", value: "AutoApprovalTime" },
        ],
        search: "",
        searchAssignments: "",
        selected: [],
        workers: [],
        sendEmailWorkerIds: [],
        loading: false,
        snackbarTexts: {
            success: "",
            warning: "",
            error: ""
        },
        email: {
            Subject: "",
            MessageText: ""
        },
        listLastRetrieved: null,
        assignments: [],
        message: "",
    }),
    props: ["duct", "sharedProps","name"],

    computed: {
        selectedIds() {
            return this.selected.map((s)=>(s["AssignmentId"]));
        }
    },
    methods: {
        unixTimeToLocaleString(unixTime) {
            var dt = new Date(unixTime*1000);
            return dt.toLocaleDateString() + " " + dt.toLocaleTimeString();
        },
        listAssignments(Cached=true) {
            this.loading = true;
            this.duct.controllers.mturk.listAssignments(Cached);
        },
        approveAssignments() { this.duct.controllers.mturk.approveAssignments(this.selectedIds, this.message); },
        rejectAssignments() { this.duct.controllers.mturk.rejectAssignments(this.selectedIds, this.message); }
    },
    watch: {
        credentials: {
            handler() { this.listWorkers(); },
            deep: true
        }
    },
    mounted() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.mturk.on("listAssignments", {
                success: (data) => {
                    this.loading = false;
                    this.listLastRetrieved = stringifyUnixTime(data["Assignments"]["LastRetrieved"]);
                    this.assignments = data["Assignments"]["Assignments"];
                }
            });
            //this.duct.eventListeners.mturk.on("getAssignments", {
            //    success: (data) => {
            //        const assignments = data["Assignments"];
            //        for(const asmt of assignments){
            //            const asmtId = asmt["Assignment"]["AssignmentId"];
            //            for(const a in this.assignments){
            //                if(a.AssignmentId==asmtId) {
            //                    a = asmt["Assignment"]
            //                }
            //        }
            //    }
            //});
            for(const opr of ["approve", "reject"]) {
                this.duct.eventListeners.mturk.on(`${opr}Assignments`, {
                    success: () => {
                        //this.duct.controllers.mturk.getAssignments(this.selectedIds);
                        this.$refs.snackbarSuccess.show(`Successfully ${opr.split(6)}ed ${this.selectedIds.length} assignments`);
                        this.selected = [];
                        this.message = "";
                    }
                });
            }

            this.listAssignments();
        });
    }
}
</script>
<style>
</style>
