<template>
    <v-main class="grey lighten-4">
        <v-row class="justify-center">
            <v-col cols="11" lg="8" class="text-right mt-10">
                <v-btn
                    color="indigo"
                    dark
                    @click="loadFlow()">
                    <v-icon>mdi-refresh</v-icon>
                </v-btn>
            </v-col>
        </v-row>

        <v-row class="justify-center">
            <v-col cols="11" lg="8">
                <config-table :config="config" />
            </v-col>
        </v-row>

        <v-row class="justify-center">
            <v-col cols="11" lg="8">
                <task-flow-card
                    :duct="duct"
                    :prjName="prjName"
                    :flow="flow"
                    template-color="blue-grey lighten-4"
                    />
            </v-col>
        </v-row>

        <tutti-snackbar ref="snackbar" />

    </v-main>
</template>

<script>
import ConfigTable from './ConfigTable'
import TaskFlowCard from './TaskFlowCard'
import TuttiSnackbar from '@/components/ui/TuttiSnackbar'

export default {
    components: {
        ConfigTable,
        TaskFlowCard,
        TuttiSnackbar
    },
    data: () => ({
        templateColor: "blue-grey lighten-4",
        flow: null,
        config: null
    }),
    props: ["duct", "prjName"],
    methods: {
        loadFlow(){
            if(this.prjName)
                this.duct.controllers.resource.getProjectScheme(this.prjName, false);
        }
    },
    watch: {
        prjName() { this.loadFlow(); }
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.resource.on("getProjectScheme", {
                success: (data) => {
                    this.flow = data.Flow;
                    this.config = data.Config;
                    this.$refs.snackbar.show("success", "successfully loaded flow");
                },
                error: (data) => {
                    this.$refs.snackbar.show("error", "Error in loading flow: " + data["Reason"]);
                }
            });
            this.loadFlow();
        });
    }
}
</script>
