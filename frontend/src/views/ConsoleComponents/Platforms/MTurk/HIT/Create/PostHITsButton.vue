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
    </div>
</template>

<script>
import Dialog from '@/views/assets/Dialog.vue'

export default {
    components: {
        TuttiDialog: Dialog
    },
    data: () => ({
        loading: false,
        customQualTypes: {},
    }),
    props: [
        "duct",
        "prjName",
        "HITTypeParams",
        "HITParams",
        "numCreateHITs"
    ],
    methods: {
        createHITsWithHITType(HITTypeId) {
            this.duct.controllers.mturk.createHITsWithHITType(
                this.prjName,
                this.numCreateHITs,
                { HITTypeId, ...this.HITParams }
            );
        },
        isTuttiQual(qtid){
            return this.customQualTypes[qtid].name.startsWith("TUTTI_HITTYPE_QUALIFICATION");
        },

        postHITs() {
            this.loading = true;

            this.HITTypeParams.QualificationRequirements.forEach((qr,i) => {
                if(this.isTuttiQual(qr.QualificationTypeId)) {
                    delete this.HITTypeParams.QualificationRequirements[i];
                } else {
                    if(qr.IntegerValues.length>0) {
                        qr.IntegerValues.map((data) => parseInt(data));
                    } else {
                        delete qr.IntegerValues;
                    }
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
                    this.loading = false;
                    this.$refs.snackbar.show("success", "Successfully posted HITs");
                },
                error: (data) => {
                    this.$refs.snackbar.show("error", `Error in posting HITs: ${data["Reason"]}`);
                }
            });
        });
    }
}
</script>
