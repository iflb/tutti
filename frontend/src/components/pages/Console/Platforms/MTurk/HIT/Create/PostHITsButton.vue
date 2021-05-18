<template>
    <div>
        <v-btn
            dark
            :loading="loading"
            color="indigo"
            @click.stop="credentials.Sandbox ? postHITs() : $refs.dialog.show();">
            Post HITs
        </v-btn>

        <tutti-dialog
            ref="dialog"
            title="Post HITs in Production mode?"
            maxWidth="800"
            persistent
            :actions="[
                {
                    label: 'Proceed',
                    color: 'indigo darken-1',
                    dark: true,
                    onclick: postHITs
                },
                {
                    label: 'Cancel',
                    color: 'grey darken-1',
                    text: true
                }
            ]" >
            <template v-slot:body>
                You are currently in production mode, which will hire MTurk workers and pay them real money. Are you sure to proceed?
            </template>
        </tutti-dialog>
        <tutti-snackbar ref="snackbar" />
    </div>
</template>

<script>
import TuttiDialog from '@/components/ui/TuttiDialog'
import TuttiSnackbar from '@/components/ui/TuttiSnackbar'

export default {
    components: {
        TuttiDialog,
        TuttiSnackbar
    },
    data: () => ({
        loading: false,
    }),
    props: [
        "duct",
        "prjName",
        "HITTypeParams",
        "HITParams",
        "numCreateHITs",
        "credentials",
        "createNew",
        "chosenExstHITTypeId"
    ],
    methods: {
        createHITsWithHITType(HITTypeId) {
            this.duct.controllers.mturk.createHITsWithHITType(
                this.prjName,
                this.numCreateHITs,
                { HITTypeId, ...this.HITParams }
            );
        },
        postHITs() {
            this.loading = true;

            this.HITTypeParams.QualificationRequirements.forEach((qr) => {
                if(qr.IntegerValues && qr.IntegerValues.length>0) {
                    qr.IntegerValues = qr.IntegerValues.map((data) => parseInt(data));
                } else {
                    delete qr.IntegerValues;
                }
            });

            if(this.createNew){
                this.duct.controllers.mturk.createTuttiHITBatch(
                    this.prjName,
                    this.numCreateHITs,
                    this.HITTypeParams,
                    this.HITParams
                );
            }
            else {
                this.createHITsWithHITType(this.chosenExstHITTypeId);
            }
        },
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.mturk.on(["createTuttiHITBatch", "createHITsWithHITType"], {
                success: () => {
                    this.$refs.snackbar.show("success", "Successfully posted HITs");
                },
                error: (data) => {
                    this.$refs.snackbar.show("error", `Error in posting HITs: ${data["Reason"]}`);
                },
                complete: () => {
                    console.log("complete");
                    this.loading = false;
                }
            });
        });
    }
}
</script>
