<template>
    <div>
        <v-btn
            dark
            :loading="loading"
            :disabled="qtids.length==0"
            class="mx-2"
            color="error"
            @click="deleteQualifications">
            Delete ({{ qtids.length }})
        </v-btn>

        <tutti-snackbar ref="snackbar" />
    </div>
</template>

<script>
import Snackbar from '@/views/assets/Snackbar.vue'

export default {
    components: {
        TuttiSnackbar: Snackbar,
    },
    data: () => ({
        loading: false,
        disabled: false,
    }),
    props: ["duct", "qtids"],
    methods: {
        deleteQualifications() {
            this.loading = true;
            this.duct.controllers.mturk.deleteQualifications( this.qtids );
        },
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.mturk.on("deleteQualifications", {
                success: (data) => {
                    const res = data["Results"];
                    var cntSuccess = 0;
                    for(var i in res) {
                        if(("ResponseMetadata" in res[i]) &&
                            ("HTTPStatusCode" in res[i]["ResponseMetadata"]) &&
                            (res[i]["ResponseMetadata"]["HTTPStatusCode"]==200))
                            cntSuccess++;
                    }
                    if(cntSuccess==res.length) {
                        this.$refs.snackbar.show("success", `Successfully deleted ${res.length} qualifications`);
                    } else {
                        this.$refs.snackbar.show("success", `Deleted ${cntSuccess} qualifications, but errors occurred in deleting ${res.length-cntSuccess} qualifications`);
                    }

                    this.loading = false;
                    this.$emit("delete");
                },
                error: (data) => {
                    this.$refs.snackbar.show("error", `Errors occurred in deleting qualifications: ${data["Reason"]}`);

                    this.loading = false;
                }
            });
        });
    }
}
</script>
