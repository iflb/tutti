<template>
    <v-main class="mt-10 grey lighten-4">
        <div style="max-width:1200px" class="mx-auto">
            <!--<v-card class="my-3">
                <v-card-text class="py-1">
                    <v-row align="center">
                        <v-col class="pa-0">
                            <v-list-item two-line>
                                <v-list-item-content>
                                    <v-list-item-title>Create HIT Type</v-list-item-title>
                                    <v-list-item-subtitle>HIT Metadata (title, reward, time limit, etc.) is required before posting.</v-list-item-subtitle>
                                </v-list-item-content>
                            </v-list-item>
                        </v-col>
                        <v-col class="text-end py-0">
                            <v-btn>Create HIT Type</v-btn>
                        </v-col>
                    </v-row>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-text class="py-1">
                    <v-row align="center">
                        <v-col class="pa-0">
                            <v-list-item two-line>
                                <v-list-item-content>
                                    <v-list-item-title>Create HIT Type</v-list-item-title>
                                    <v-list-item-subtitle>HIT Metadata (title, reward, time limit, etc.) is required before posting.</v-list-item-subtitle>
                                </v-list-item-content>
                            </v-list-item>
                        </v-col>
                        <v-col class="text-end py-0">
                            <v-btn>Create HIT Type</v-btn>
                        </v-col>
                    </v-row>
                </v-card-text>
            </v-card>-->
            <v-row>
                <v-col class="text-right">
                    <v-btn dark color="indigo" to="/console/platform/mturk/hit/create/">Create HITs</v-btn>
                </v-col>
            </v-row>
            <v-card>
                <v-data-table
                  :headers="headers"
                  :items="hitTypes"
                  :single-expand="false"
                  :expanded.sync="expanded"
                  item-key="id"
                  show-expand
                  class="elevation-1"
                  dense
                  :loading="loadingHITs"
                >
                    <template v-slot:top>
                        <v-card-title>
                            HITs
                            <v-btn icon @click="_evtListHITs(false)"><v-icon>mdi-refresh</v-icon></v-btn>
                            <v-spacer></v-spacer>
                            <v-spacer></v-spacer>
                            <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
                        </v-card-title>
                        <v-card-subtitle>
                        (Last retrieved: {{ unixTimeToLocaleString(listLastRetrieved) }})
                        </v-card-subtitle>
                    </template>
                    <template v-slot:expanded-item="{ headers, item }">
                        <td :colspan="headers.length">
                            <div class="my-2">
                                <div class="d-flex flex-row-reverse">
                                    <v-btn icon color="grey lighten-1"><v-icon>mdi-pencil</v-icon></v-btn>
                                    <v-btn icon color="grey lighten-1"><v-icon>mdi-account-edit</v-icon></v-btn>
                                </div>
                                Keywords: <b>{{ item.detail.Keywords }}</b><br>
                                Description: <b>{{ item.detail.Description }}</b><br>
                                Auto-approval delay: <b>{{ secondsToTimeString(item.detail.AutoApprovalDelayInSeconds) }}</b><br>
                                Assignment duration: <b>{{ secondsToTimeString(item.detail.AssignmentDurationInSeconds) }}</b><br>
                                Raw data:
                                <vue-json-pretty :data="item.detail" :deep="1" style="font-size:0.6em;"></vue-json-pretty>
                            </div>
                        </td>
                    </template>
                </v-data-table>
            </v-card>
        </div>
    </v-main>
</template>
<script>
//import DialogCreate from './DialogCreate.vue'
import { mapGetters, mapActions } from 'vuex'
import VueJsonPretty from 'vue-json-pretty'
import 'vue-json-pretty/lib/styles.css'
//import { codemirror } from 'vue-codemirror'
//import 'codemirror/lib/codemirror.css'

export default {
    components: {
        VueJsonPretty,
        //codemirror
    },
    data: () => ({
        search: "",
        expanded: [],
        headers: [
          { text: 'HIT Type ID', value: 'id' },
          { text: 'Title', value: 'title' },
          { text: 'Reward', value: 'reward' },
          { text: '# Posted HITs', value: 'num_hits' },
          { text: 'Creation Time', value: 'creation_time' },
          { text: '', value: 'data-table-expand' },
        ],
        listLastRetrieved: null,
        hitTypes: [],
        cmOptions: {
            styleActiveLine: true,
            lineNumbers: true,
            line: true,
            mode: 'text/javascript',
            lineWrapping: true,
            theme: 'base16-dark',
            indentWithTabs: true
        },
        hitTypeParams: "",
        loadingHITs: false
    }),
    props: ["sharedProps","name"],

    computed: {
        ...mapGetters("ductsModule", [ "duct" ]),
    },
    methods: {
        ...mapActions("ductsModule", [ "onDuctOpen" ]),
        unixTimeToLocaleString(unixTime) {
            var dt = new Date(unixTime*1000);
            return dt.toLocaleDateString() + " " + dt.toLocaleTimeString();
        },
        secondsToTimeString(seconds) {
            var hours = Math.floor(seconds / 3600);
            seconds -= hours*3600;
            var minutes = Math.floor(seconds / 60);
            seconds -= minutes*60;
            return `${hours}:${("00"+minutes).slice(-2)}:${("00"+seconds).slice(-2)}`;
        },
        _evtListHITs(cached){
            this.loadingHITs = true;
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.MTURK_HIT,
                data: {
                    "Command": "List",
                    "Cached": cached
                }
            });
        }
    },
    mounted() {
        this.onDuctOpen(() => {
            this.duct.addEvtHandler({
                tag: this.name, eid: this.duct.EVENT.MTURK_HIT,
                handler: (rid, eid, data) => {
                    if(data["Status"]=="Error") return;

                    const command = data["Data"]["Command"];
                    switch(command) {
                        case "List": {
                            this.loadingHITs = false;
                            this.listLastRetrieved = data["Data"]["Result"]["LastRetrieved"];
                            const hits = data["Data"]["Result"]["HITTypes"];
                            this.hitTypes = [];
                            for(var i in hits){
                                this.hitTypes.push({
                                    id: i,
                                    title: hits[i]["Props"]["Title"],
                                    reward: hits[i]["Props"]["Reward"],
                                    creation_time: this.unixTimeToLocaleString(hits[i]["CreationTime"]),
                                    num_hits: hits[i]["Count"],
                                    detail: hits[i]["Props"]
                                });
                            }
                            break;
                        }
                    }
                }
            });

            this._evtListHITs(true);
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
