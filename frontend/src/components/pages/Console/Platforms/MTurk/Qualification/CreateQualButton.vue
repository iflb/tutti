<template>
    <div>
        <v-btn
            class="mx-2"
            dark
            color="indigo"
            @click="$refs.dialogCreate.shown=true">
            Create Qualification...
        </v-btn>

        <tutti-dialog
            ref="dialogCreate"
            title="Create Qualification Type"
            maxWidth="500"
            :actions="[
                {
                    label: 'Create',
                    color: 'indigo darken-1',
                    disableByRule: true,
                    text: true,
                    onclick: createQualificationType
                },
                {
                    label: 'Cancel',
                    color: 'grey darken-1',
                    text: true
                }
            ]" >
            <template v-slot:body>
                <v-row>
                    <v-col cols="12" class="mb-0 pb-0">
                        <v-text-field
                            filled
                            dense 
                            prepend-icon="mdi-label"
                            v-model="newQualParams.Name"
                            label="Name"
                            :rules="[rules.required]" />
                    </v-col>

                    <v-col cols="12" class="my-0 py-0">
                        <v-text-field
                            filled
                            dense
                            prepend-icon="mdi-message-text"
                            v-model="newQualParams.Description"
                            label="Description"
                            :rules="[rules.required]" />
                    </v-col>

                    <v-col cols="6" class="my-0 py-0">
                        <v-switch
                            hide-details
                            v-model="newQualParams.AutoGranted"
                            color="indigo"
                            label="AutoGranted" />
                    </v-col>
                </v-row>
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
        newQualParams: {
            Name: "",
            Description: "",
            AutoGranted: false,
            QualificationTypeStatus: "Active"
        },
    }),
    props: ["duct"],
    methods: {
        createQualificationType() {
            this.duct.controllers.mturk.createQualification(this.newQualParams);
        }
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.mturk.on("createQualification", {
                success: () => {
                    this.$refs.snackbar.show("success", "Successfully created a qualification");
                    this.$emit("create");
                },
                error: (data) => {
                    this.$refs.snackbar.show("error", `Error in creating a qualification: ${data["Reason"]}`);
                }
            });
        });
    }
}
</script>
