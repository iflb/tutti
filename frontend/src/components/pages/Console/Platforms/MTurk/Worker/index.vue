<template>
        <v-row class="my-10" justify="center">
            <v-col cols="10">
                <div style="display:flex;justify-content:flex-end;">
                    <send-email-button :duct="duct" :wids="workerIds" :selected-wids="selectedWorkerIds"></send-email-button>
                    <grant-qual-button :duct="duct" :wids="workerIds" :selected-wids="selectedWorkerIds"></grant-qual-button>
                </div>
            </v-col>
            <v-col cols="10">
                <v-data-table
                  dense
                  show-select
                  sort-desc
                  :headers="headers"
                  :items="workers"
                  item-key="wid"
                  class="elevation-1"
                  :loading="loading"
                  v-model="selectedWorkers"
                  sort-by="Timestamp"
                  :search="search"
                >
                    <template v-slot:top>
                        <v-card-title>
                            Workers
                            <v-btn icon @click="listWorkers()"><v-icon>mdi-refresh</v-icon></v-btn>

                            <v-spacer></v-spacer>

                            <v-text-field
                                single-line
                                hide-details
                                v-model="search"
                                append-icon="mdi-magnify"
                                label="Search">
                            </v-text-field>
                        </v-card-title>
                    </template>
                    <template v-slot:item.Projects="{ item }">
                        {{ item.Projects.join(", ") }}
                    </template>
                </v-data-table>
            </v-col>
        </v-row>
</template>
<script>
import GrantQualButton from './GrantQualButton'
import SendEmailButton from './SendEmailButton'
import { stringifyUnixTime } from '@/lib/utils'

export default {
    components: {
        GrantQualButton,
        SendEmailButton,
    },
    data: () => ({
        loading: false,

        search: "",
        headers: [
          { text: 'Worker ID', value: 'wid' },
          { text: 'Worker ID (MTurk)', value: 'PlatformWorkerId' },
          { text: 'Visited Projects', value: 'Projects' },
          { text: 'Created Time', value: 'Timestamp' },
        ],
        selectedWorkers: [],
        workers: [],
    }),
    props: ["duct", "credentials"],

    computed: {
        selectedWorkerIds() {
            var wids = [];
            for(var i in this.selectedWorkers)
                wids.push(this.selectedWorkers[i]["PlatformWorkerId"]);
            return wids;
        },
        workerIds() {
            var wids = [];
            for(var i in this.workers)
                wids.push(this.workers[i]["PlatformWorkerId"]);
            return wids;
        },
    },
    methods: {
        listWorkers() {
            this.loading = true;
            this.duct.controllers.mturk.listWorkers();
        },
    },
    watch: {
        credentials: {
            handler() { this.listWorkers(); },
            deep: true
        },
    },
    mounted() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.mturk.on("listWorkers", {
                success: (data) => {
                    this.loading = false;

                    var workers = [];
                    for(var wid in data["Workers"]) {
                        data["Workers"][wid]["Timestamp"] = stringifyUnixTime(data["Workers"][wid]["Timestamp"]);
                        workers.push({ wid, ...data["Workers"][wid] });
                    }
                    this.workers = workers;
                },
                error: (data) => {
                    console.log("error", data);
                }
            });

            this.listWorkers();
        });
    }
}
</script>
<style>
.v-data-table tbody tr.v-data-table__expanded__content {
    box-shadow: none;
    background-color: #f5f5f5;
}
.is-root, .is-root div {
    font-size: 9pt;
}
</style>
