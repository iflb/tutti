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

        <tutti-snackbar v-for="type in Object.keys(snackbarTexts)" :key="type" :color="type" :text="snackbarTexts[type]" :timeout="2000" />

    </v-main>
</template>

<script>
import Arrow from './Arrow.vue'
import RecursiveBatch from './RecursiveBatch.vue'
import Snackbar from '@/views/assets/Snackbar.vue'

export default {
    data: () => ({
        snackbarTexts: {
            success: "",
            error: ""
        },
        templateColor: "blue-grey lighten-4",
        flow: null,
    }),
    components: {
        Arrow, RecursiveBatch,
        TuttiSnackbar: Snackbar
    },
    props: ["duct", "prjName", "name"],
    methods: {
        showSnackbar(info){
            Object.assign(this.snackbar, info)
            this.snackbar.visible = true
        },
        loadFlow(){
            if(this.prjName){
                this.duct.sendMsg({
                    tag: this.name,
                    eid: this.duct.EVENT.GET_PROJECT_SCHEME,
                    data: { "ProjectName": this.prjName, "Cached": false }
                });
            }
        }
    },
    watch: {
        prjName() { this.loadFlow(); }
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.addTuttiEvtHandler({
                eid: this.duct.EVENT.GET_PROJECT_SCHEME,
                success: ({ data }) => {
                    this.flow = data["Flow"];
                    this.snackbarTexts.success = "successfully loaded flow";
                },
                error: ({ data }) => {
                    this.snackbarTexts.error = "Error in loading flow: " + data["Reason"];
                }
            });
            this.loadFlow();
        });
    }
}
</script>
