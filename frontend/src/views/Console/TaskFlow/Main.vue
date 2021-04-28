<template>
    <v-main class="grey lighten-4">
        <v-row class="justify-center"><v-col cols="11" lg="8">
            <v-card class="mt-10">
                <v-card-title> Config Parameters </v-card-title>
                <v-data-table
                    dense
                    hide-default-footer
                    :headers="[
                        { width: '40%', text: 'Property', value: 'key' },
                        { width: '60%', text: 'Value', value: 'val' }
                    ]"
                    :items="configArray"
                >
                    <template v-slot:item.val="{ item }">
                        <v-icon v-if="item.val===true" color="success">mdi-check-circle-outline</v-icon>
                        <v-icon v-else-if="item.val===false" color="error">mdi-cancel</v-icon>
                        <b v-else>{{ item.val }}</b>
                    </template>
                </v-data-table>
            </v-card>
        </v-col></v-row>
        <v-row class="justify-center"><v-col cols="11" lg="8">
            <v-card class="mt-10">
                <v-card-title>
                    Task Flow
                    <v-btn text icon @click="loadFlow()"><v-icon>mdi-refresh</v-icon></v-btn>
                </v-card-title>
                <v-container>
                    <v-row>
                        <v-col align="right">
                        </v-col>
                    </v-row>
                    <v-card align="center" class="mx-auto py-2 text-h6" color="grey lighten-2" width="200">Start</v-card>

                    <arrow :color="templateColor" depth="1" />

                    <div v-if="scheme.Flow">
                        <recursive-batch
                            :duct="duct"
                            :name="name"
                            :parent-params="{
                                prjName, templateColor,
                                node: scheme.Flow,
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
        scheme: {
            Flow: null,
            Config: null
        },
    }),
    components: {
        Arrow: () => import("./Arrow"),
        RecursiveBatch: () => import("./RecursiveBatch"),
        TuttiSnackbar: () => import("@/views/assets/Snackbar")
    },
    props: ["duct", "prjName", "name"],
    computed: {
        configArray() {
            if(!this.scheme.Config) return [];
            let arr = [];
            for(const [key,val] of Object.entries(this.scheme.Config)){
                arr.push({ key, val });
            }
            return arr;
        }
    },
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
                    this.scheme = data;
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
