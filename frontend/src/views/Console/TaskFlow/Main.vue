<template>
    <v-main class="grey lighten-4">
        <v-row class="justify-center"><v-col cols="11" md="8" lg="6">
            <v-card class="pa-3 mt-10">
            <v-container>
                <v-row>
                    <v-col align="right">
                        <v-btn text icon @click="loadFlow()"><v-icon>mdi-refresh</v-icon></v-btn>
                    </v-col>
                </v-row>
                <v-card align="center" class="mx-auto py-2 text-h6" color="grey lighten-2" width="200">Start</v-card>

                <arrow :color="templateColor" depth="1" />

                <div v-if="flow">
                    <recursive-batch
                        :duct="duct"
                        :name="name"
                        :parent-params="{
                            prjName, templateColor,
                            node: flow,
                            depth: 1,
                            isLast: true,
                        }" />
                </div>

                <arrow :color="templateColor" depth="1" />

                <v-card align="center" class="mx-auto py-2 text-h6" color="grey lighten-2" width="200">End</v-card>
            </v-container>
            </v-card>
        </v-col></v-row>

        <tutti-snackbar ref="snackbarSuccess" color="success" :timeout="2000" />
        <tutti-snackbar ref="snackbarError" color="error" :timeout="2000" />

    </v-main>
</template>

<script>
export default {
    data: () => ({
        templateColor: "blue-grey lighten-4",
        flow: null,
    }),
    components: {
        Arrow: () => import("./Arrow"),
        RecursiveBatch: () => import("./RecursiveBatch"),
        TuttiSnackbar: () => import("@/views/assets/Snackbar")
    },
    props: ["duct", "prjName", "name"],
    methods: {
        loadFlow(){
            if(this.prjName)  this.duct.controllers.resource.getProjectScheme(this.prjName, false);
        }
    },
    watch: {
        prjName() { this.loadFlow(); }
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.resource.on("getProjectScheme", {
                success: (data) => {
                    this.flow = data["Flow"];
                    this.$refs.snackbarSuccess.show("successfully loaded flow");
                },
                error: (data) => {
                    this.$refs.snackbarError.show("Error in loading flow: " + data["Reason"]);
                }
            });
            this.loadFlow();
        });
    }
}
</script>
