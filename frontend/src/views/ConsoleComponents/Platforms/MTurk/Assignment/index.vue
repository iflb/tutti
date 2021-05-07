<template>
    <v-row class="my-10" justify="center">
        <v-col cols="10" class="text-right">
            <div style="display:flex;justify-content:flex-end;">
                <approve-button :duct="duct" :aids="selectedIds" @success="clearSelection();" />
                <reject-button :duct="duct" :aids="selectedIds" @success="clearSelection();" />
            </div>
        </v-col>

        <v-col cols="10">
            <v-data-table
              dense
              sort-desc
              show-select
              :headers="headers"
              :items="assignments"
              item-key="AssignmentId"
              class="elevation-1"
              :loading="loading"
              v-model="selected"
              sort-by="Timestamp"
              :items-per-page="100"
              :footer-props="{ itemsPerPageOptions: [10,30,50,100,300] }"
              :search="searchQuery">

                <template v-slot:top>
                    <v-card-title>
                        Assignments
                        <v-btn icon @click="listAssignments(false)"><v-icon>mdi-refresh</v-icon></v-btn>

                        <v-spacer></v-spacer>

                        <v-select
                            hide-details 
                            :loading="loadingHITTypes"
                            v-model="HITTypeId"
                            :items="Object.keys(HITIds)"
                            label="HITTypeId" />

                        <v-spacer></v-spacer>

                        <v-text-field
                            single-line
                            hide-details
                            v-model="searchQuery"
                            append-icon="mdi-magnify"
                            label="Search"
                            >
                        </v-text-field>
                    </v-card-title>
                </template>

                <template v-slot:item.WorkerId="{ item }">
                    {{ `${item.PlatformWorkerId}\n(${item.WorkerId})` }}
                </template>

                <template v-slot:item.AssignmentId="{ item }">
                    <div class="text-truncate" style="max-width:100px;">
                        {{ item.AssignmentId }}
                    </div>
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

    </v-row>
</template>
<script>
import { stringifyUnixTime } from '@/lib/utils'
import ApproveButton from './ApproveButton'
import RejectButton from './RejectButton'

export default {
    components: {
        ApproveButton,
        RejectButton
    },
    data: () => ({
        stringifyUnixTime,

        headers: [
            { text: "Assignment ID", value: "AssignmentId" },
            { text: "Worker ID", value: "WorkerId" },
            { text: "Status", value: "AssignmentStatus" },
            { text: "Accepted at", value: "AcceptTime" },
            { text: "Submitted at", value: "SubmitTime" },
            { text: "Auto-approve at", value: "AutoApprovalTime" },
        ],
        searchQuery: "",
        HITTypeId: "",

        selected: [],
        assignments: [],
        HITIds: {},

        loading: false,
        loadingHITTypes: false,
    }),
    props: ["duct", "sharedProps","name"],

    computed: {
        selectedIds() {
            return this.selected.map((s)=>(s["AssignmentId"]));
        }
    },
    methods: {
        listHITsForHITType() {
            this.loadingHITTypes = true;
            this.duct.controllers.mturk.listHITsForHITType();
        },
        listAssignmentsForHITType() {
            this.loading = true;
            this.duct.controllers.mturk.listAssignmentsForHITs(this.HITIds[this.HITTypeId]);
        },
        clearSelection() {
            this.selected = [];
        }
    },
    watch: {
        credentials: {
            handler() { this.listWorkers(); },
            deep: true
        },
        HITTypeId() {
            this.listAssignmentsForHITType();
        }
    },
    mounted() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.mturk.on("listHITsForHITType", {
                success: (data) => {
                    for(const HITTypeId in data.Results){
                        this.$set(this.HITIds, HITTypeId, data.Results[HITTypeId].HITIds);
                    }
                },
                complete: () => {
                    this.loadingHITTypes = false;
                }
            });
            this.duct.eventListeners.mturk.on("listAssignmentsForHITs", {
                success: (data) => {
                    this.assignments = data["Assignments"];
                },
                complete: () => {
                    this.loading = false;
                }
            });

            this.listHITsForHITType();
        });
    }
}
</script>
<style>
</style>
