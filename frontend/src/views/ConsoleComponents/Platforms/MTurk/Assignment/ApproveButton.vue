<template>
    <div>
        <v-tooltip top>
            <template #activator="{ on, attrs }">
                <v-btn
                    dark
                    v-bind="attrs"
                    v-on="on"
                    class="mx-2"
                    color="success"
                    @click="$refs.dialog.show()">
                    <v-icon>mdi-check-bold</v-icon>
                </v-btn>
            </template>
            <span>Approve assignment(s)</span>
        </v-tooltip>

        <tutti-dialog
            persistent
            ref="dialog"
            title="Approve Assignment(s)"
            maxWidth="500"
            :actions="[
                {
                    label: 'Confirm',
                    color: 'indigo darken-1',
                    text: true,
                    onclick: approveAssignments
                },
                {
                    label: 'Cancel',
                    color: 'grey darken-1',
                    text: true
                }
            ]" >
            <template v-slot:body>
                Approve {{ aids.length }} assignments?
                <v-text-field v-model="message" label="Message to workers (optional)"></v-text-field>
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

export default {
    components: {
        TuttiSnackbar: Snackbar,
        TuttiDialog: Dialog
    },
    data: () => ({
        message: "",
        snackbarTexts: {
            success: "",
            warning: "",
            error: ""
        },
    }),
    props: ["duct", "aids"],
    methods: {
        approveAssignments() { this.duct.controllers.mturk.approveAssignments(this.aids, this.message); },
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.mturk.on("approveAssignments", {
                success: () => {
                    this.$refs.snackbarsuccess.show(`Successfully approved ${this.aids.length} assignments`);
                    this.message = "";
                    this.$emit("success");
                }
            });
        });
    }
}
</script>
