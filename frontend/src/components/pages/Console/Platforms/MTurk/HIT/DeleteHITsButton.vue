<template>
    <div>
        <v-btn
            dark
            :loading="loading"
            class="mx-2"
            color="error"
            v-if="hids.length>0"
            @click="deleteHITs()">
            Delete ({{ hids.length }})
        </v-btn>

        <tutti-snackbar ref="snackbar" />
    </div>
</template>

<script>
import TuttiSnackbar from '@/components/ui/TuttiSnackbar'

export default {
    components: {
        TuttiSnackbar
    },
    data: () => ({
        loading: false,
    }),
    props: ["duct", "hids"],
    methods: {
        deleteHITs(){
            this.loading = true;
            this.duct.controllers.mturk.deleteHITs(this.hids);
        },
    },
    mounted() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.mturk.on("deleteHITs", {
                success: (data) => {
                    const cntSuccess = data["Results"].filter((r) => (
                            ("ResponseMetadata" in r) &&
                            ("HTTPStatusCode" in r["ResponseMetadata"]) &&
                            (r["ResponseMetadata"]["HTTPStatusCode"]==200)
                        )).length;

                    if(cntSuccess==data["Results"].length) {
                        this.$refs.snackbar.show("success", `Deleted ${cntSuccess} HITs`);
                    } else {
                        this.$refs.snackbar.show("warning", `Deleted ${cntSuccess} HITs, but errors occurred in deleting ${data["Results"].length-cntSuccess} HITs`);
                    }
                },
                error: (data) => {
                    this.$refs.snackbar.show("error", `Errors occurred in deleting HITs: ${data["Reason"]}`);
                },
                complete: () => {
                    this.loading = false;
                }
            });
        });
    }
}
</script>
