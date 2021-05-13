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
                    @click="$refs.dialogSendEmail.show()">
                    <v-icon>mdi-email</v-icon>
                </v-btn>
            </template>
            <span>Send email</span>
        </v-tooltip>

        <tutti-dialog
            ref="dialogSendEmail"
            title="Send Email to Workers"
            maxWidth="800"
            persistent
            :actions="[
                {
                    label: 'Send',
                    color: 'indigo darken-1',
                    dark: true,
                    onclick: sendEmail
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
                    v-model="email.WorkerIds"
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
                <v-text-field dense outlined label="Subject" v-model="email.Subject" />
                <v-textarea outlined label="Message" v-model="email.MessageText"></v-textarea>
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
        searchedWorkerId: "",
        email: {
            Subject: "",
            MessageText: "",
            WorkerIds: []
        },
    }),
    props: ["duct", "wids", "selectedWids"],
    methods: {
        sendEmail() {
            this.duct.controllers.mturk.notifyWorkers(this.email.Subject, this.email.MessageText, this.email.WorkerIds);
        }
    },
    watch: {
        selectedWids(val) { this.email.WorkerIds = val; }
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.mturk.on("notifyWorkers", {
                success: () => {
                    this.$refs.snackbar.show("success", "Successfully sent emails!");
                },
                error: (data) => {
                    this.$refs.snackbar.show("error", "Error in sending emails: "+data["Reason"]);
                },
            });
        });
    }
}
</script>
