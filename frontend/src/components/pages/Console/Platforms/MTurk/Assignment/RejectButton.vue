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

        <tutti-snackbar ref="snackbar" />
    </div>
</template>

<script>
import TuttiSnackbar from '@/components/ui/TuttiSnackbar'
import TuttiDialog from '@/components/ui/TuttiDialog'
import rules from '@/lib/input-rules'

export default {
    components: {
        TuttiSnackbar,
        TuttiDialog
    },
    data: () => ({
        rules,

        message: "",
    }),
    props: ["duct", "aids"],
    methods: {
        rejectAssignments() { this.duct.controllers.mturk.rejectAssignments(this.aids, this.message); }
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.mturk.on("rejectAssignments", {
                success: () => {
                    this.$refs.snackbar.show("success", `Successfully rejected ${this.aids.length} assignments`);
                    this.message = "";
                    this.$emit("success");
                }
            });
        });
    }
}
</script>
