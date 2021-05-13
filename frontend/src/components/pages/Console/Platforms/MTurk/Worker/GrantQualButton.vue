<template>
    <div>
        <v-tooltip top>
            <template #activator="{ on, attrs }">
                <v-btn
                    dark
                    v-bind="attrs"
                    v-on="on"
                    class="mx-2"
                    color="indigo"
                    @click="$refs.dialogAssociateQuals.shown=true; if(!quals) listQuals();">
                    <v-icon>mdi-account-star</v-icon>
                </v-btn>
            </template>
            <span>Grant qualification</span>
        </v-tooltip>

        <tutti-dialog
            ref="dialogAssociateQuals"
            title="Associate Qualifications to Workers"
            maxWidth="800"
            persistent
            :actions="[
                {
                    label: 'Send',
                    color: 'indigo darken-1',
                    dark: true,
                    onclick: associateQuals
                },
                {
                    label: 'Cancel',
                    color: 'grey darken-1',
                    text: true
                }
            ]" >
            <template v-slot:body>
                <v-combobox
                    dense
                    multiple
                    small-chips
                    outlined
                    hide-selected
                    v-model="newAssociateQual.WorkerIds"
                    :items="wids"
                    label="To"
                    :search-input.sync="searchedWorkerId">
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
                <v-select
                    v-model="newAssociateQual.QualificationTypeId"
                    :items="qualificationTypes"
                    label="QualificationTypeId"
                    dense
                    outlined>
                    </v-select>
                <v-text-field
                    dense
                    outlined
                    v-model.number="newAssociateQual.IntegerValue"
                    label="IntegerValue">
                </v-text-field>
                <v-switch
                    v-model="newAssociateQual.SendNotification"
                    label="SendNotification">
                </v-switch>
            </template>
        </tutti-dialog>

        <tutti-snackbar ref="snackbar" />
    </div>
</template>

<script>
import TuttiSnackbar from '@/components/ui/TuttiSnackbar'
import TuttiDialog from '@/components/ui/TuttiDialog'

export default {
    components: {
        TuttiSnackbar,
        TuttiDialog
    },
    data: () => ({
        quals: null,
        searchedWorkerId: "",
        newAssociateQual: {
            WorkerIds: [],
            QualificationTypeId: "",
            IntegerValue: null,
            SendNotification: true
        },
    }),
    props: ["duct", "wids", "selectedWids"],
    computed: {
        qualificationTypes() {
            var qids = [];
            for(var i in this.quals) {
                const id = this.quals[i]["QualificationTypeId"];
                const name = this.quals[i]["Name"];
                qids.push({ text: `${name} - ${id}`, value: this.quals[i]["QualificationTypeId"] });
            }
            return qids;
        }
    },
    methods: {
        associateQuals() {
            this.duct.controllers.mturk.associateQualificationsWithWorkers(this.newAssociateQual);
        },
        listQuals() {
            this.duct.controllers.mturk.listQualifications();
        },
    },
    watch: {
        selectedWids(val) { this.newAssociateQual.WorkerIds = val; }
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.mturk.on("listQualifications", {
                success: (data) => {
                    this.quals = data["QualificationTypes"];
                }
            });
            this.duct.eventListeners.mturk.on("associateQualificationsWithWorkers", {
                success: () => {
                    this.$refs.snackbar.show("success", "Successfully granted a qualification!");
                },
                error: (data) => {
                    this.$refs.snackbar.show("error", "Error in granting a qualification: "+data["Reason"]);
                },
            });
        });
    }
}
</script>
