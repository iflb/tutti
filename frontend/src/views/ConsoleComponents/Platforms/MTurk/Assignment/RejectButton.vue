<template>
    <div>
        <v-tooltip top>
            <template #activator="{ on, attrs }">
                <v-btn
                    dark
                    v-bind="attrs"
                    v-on="on"
                    class="mx-2"
                    color="error"
                    @click="$refs.dialog.show()">
                    <v-icon>mdi-close-thick</v-icon>
                </v-btn>
            </template>
            <span>Reject assignment(s)</span>
        </v-tooltip>

        <tutti-dialog
            persistent
            ref="dialog"
            title="Reject Assignment(s)"
            maxWidth="500"
            :actions="[
                {
                    label: 'Confirm',
                    color: 'indigo darken-1',
                    disableByRule: true,
                    text: true,
                    onclick: rejectAssignments
                },
                {
                    label: 'Cancel',
                    color: 'grey darken-1',
                    text: true
                }
            ]" >
            <template v-slot:body>
                Reject {{ aids.length }} assignments?<br>
                Caution: You must be careful when rejecting workers.
                <v-text-field
                    autofocus
                    v-model="message"
                    label="Reason for rejection (required)"
                    :rules="[rules.required]" />
            </template>
        </tutti-dialog>

        <tutti-snackbar v-for="type in Object.keys(snackbarTexts)"
            :key="type"
            :ref="'snackbar'+type"
            color="type"
            :texts="snackbarTexts[type]"
            :timeout="3000" />
    </div>
</template>

<script>
import Snackbar from '@/views/assets/Snackbar.vue'
import Dialog from '@/views/assets/Dialog.vue'
import rules from '@/lib/input-rules'

export default {
    components: {
        TuttiSnackbar: Snackbar,
        TuttiDialog: Dialog
    },
    data: () => ({
        rules,

        message: "",
        snackbarTexts: {
            success: "",
            warning: "",
            error: ""
        },
    }),
    props: ["duct", "aids"],
    methods: {
        rejectAssignments() { this.duct.controllers.mturk.rejectAssignments(this.aids, this.message); }
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.mturk.on("rejectAssignments", {
                success: () => {
                    this.$refs.snackbarsuccess.show(`Successfully rejected ${this.aids.length} assignments`);
                    this.message = "";
                    this.$emit("success");
                }
            });
        });
    }
}
</script>
