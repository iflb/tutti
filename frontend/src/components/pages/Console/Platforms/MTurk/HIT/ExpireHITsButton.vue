<template>
    <div>
        <v-btn
            dark
            :loading="loading"
            class="mx-2"
            color="warning"
            v-if="hids.length>0"
            @click="expireHITs()">
            Expire ({{ hids.length }})
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
        expireHITs(){
            this.loading = true;
            this.duct.controllers.mturk.expireHITs(this.hids);
        },
    },
    watch: {
    },
    mounted() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.mturk.on("expireHITs", {
                success: (data) => {
                    const cntSuccess = data["Results"].filter((r) => (
                            ("ResponseMetadata" in r) &&
                            ("HTTPStatusCode" in r["ResponseMetadata"]) &&
                            (r["ResponseMetadata"]["HTTPStatusCode"]==200)
                        )).length;

                    if(cntSuccess==data["Results"].length) {
                        this.$refs.snackbar.show("success", `Expired ${cntSuccess} HITs`);
                    } else {
                        this.$refs.snackbar.show("warning", `Expired ${cntSuccess} HITs, but errors occurred in expiring ${data["Results"].length-cntSuccess} HITs`);
                    }
                },
                error: (data) => {
                    this.$refs.snackbarError.show("error", `Errors occurred in expiring HITs: ${data["Reason"]}`);
                },
                complete: () => {
                    this.loading = false;
                }
            });
        });
    }
}
</script>
