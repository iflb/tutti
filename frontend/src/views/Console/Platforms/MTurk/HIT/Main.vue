<template>
    <v-main class="mt-10 grey lighten-4">
        <div style="max-width:1200px" class="mx-auto">
            <v-row>
                <v-col class="text-right">
                    <v-btn :loading="button.expireHITs.loading" :disabled="button.expireHITs.disabled" class="mx-2" dark
                           color="warning" v-if="selectedHITIds.length>0" @click="button.expireHITs.loading=true; expireHITs()">Expire ({{ selectedHITIds.length }})</v-btn>
                    <v-btn :loading="button.deleteHITs.loading" :disabled="button.deleteHITs.disabled" class="mx-2" dark
                           color="error" v-if="selectedHITIds.length>0" @click="button.deleteHITs.loading=true; deleteHITs()">Delete ({{ selectedHITIds.length }})</v-btn>
                    <v-btn class="mx-2" dark color="indigo" to="/console/platform/mturk/hit/create/">Create HITs...</v-btn>
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
                  show-select
                  v-model="selectedHITTypes"
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
                    <template v-slot:item.active="{ item }">
                        <v-icon v-if="item.detail.HITStatusCount.Assignable>0" color="success">mdi-circle-medium</v-icon>
                    </template>
                    <template v-slot:item.id="{ item }">
                        {{ item.id }}
                        <v-icon v-if="item.detail.HITStatusCount.Assignable>0" small @click="openNewWindow('https://workersandbox.mturk.com/projects/'+item.groupId+'/tasks');">mdi-open-in-new</v-icon>
                    </template>
                    <template v-slot:expanded-item="{ headers, item }">
                        <td :colspan="headers.length">
                            <div class="my-2">
                                <div class="d-flex flex-row-reverse">
                                    <v-btn icon color="grey lighten-1"><v-icon>mdi-pencil</v-icon></v-btn>
                                    <v-btn icon color="grey lighten-1"><v-icon>mdi-account-edit</v-icon></v-btn>
                                </div>
                                Keywords: <b>{{ item.detail.Props.Keywords }}</b><br>
                                Description: <b>{{ item.detail.Props.Description }}</b><br>
                                Auto-approval delay: <b>{{ secondsToTimeString(item.detail.Props.AutoApprovalDelayInSeconds) }}</b><br>
                                Assignment duration: <b>{{ secondsToTimeString(item.detail.Props.AssignmentDurationInSeconds) }}</b><br>
                                Raw data:
                                <vue-json-pretty :data="item.detail" :deep="1" style="font-size:0.6em;"></vue-json-pretty>
                            </div>
                        </td>
                    </template>
                </v-data-table>
            </v-card>

            <tutti-snackbar color="success" :timeout="3000" :text="snackbarTexts.success" />
            <tutti-snackbar color="warning" :timeout="3000" :text="snackbarTexts.warning" />
            <tutti-snackbar color="error" :timeout="3000" :text="snackbarTexts.error" />
        </div>
    </v-main>
</template>
<script>
//import DialogCreate from './DialogCreate.vue'
import { mapGetters, mapActions } from 'vuex'
import VueJsonPretty from 'vue-json-pretty'
import 'vue-json-pretty/lib/styles.css'
import Snackbar from '@/views/assets/Snackbar.vue'
//import { codemirror } from 'vue-codemirror'
//import 'codemirror/lib/codemirror.css'

export default {
    components: {
        VueJsonPretty,
        TuttiSnackbar: Snackbar
        //codemirror
    },
    data: () => ({
        snackbarTexts: {
            success: "",
            warning: "",
            error: ""
        },
        selectedHITTypes: [],
        search: "",
        expanded: [],
        headers: [
          { text: '', value: 'active' },
          { text: 'HIT Type ID', value: 'id' },
          { text: 'Title', value: 'title' },
          { text: 'Reward', value: 'reward' },
          { text: '# HITs', value: 'num_hits' },
          { text: '# Open HITs', value: 'num_assignable' },
          { text: '# Closed HITs', value: 'num_reviewable' },
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
        loadingHITs: false,
        button: {
            expireHITs: {
                loading: false,
                disabled: false
            },
            deleteHITs: {
                loading: false,
                disabled: false
            },
        },
    }),
    props: ["sharedProps","name"],

    computed: {
        ...mapGetters("ductsModule", [ "duct" ]),
        selectedHITIds() {
            var hitIds = [];
            for(var i in this.selectedHITTypes){
                hitIds = [...hitIds, ...this.selectedHITTypes[i]["detail"]["HITIds"]];
            }
            return hitIds;
        }
    },
    methods: {
        ...mapActions("ductsModule", [ "onDuctOpen" ]),
        openNewWindow(url) {
            window.open(url, "_blank");
        },
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
        expireHITs(){
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.MTURK_EXPIRE_HITS,
                data: {
                    "HITIds": this.selectedHITIds
                }
            });
        },
        deleteHITs(){
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.MTURK_DELETE_HITS,
                data: {
                    "HITIds": this.selectedHITIds
                }
            });
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
                                    groupId: hits[i]["HITGroupId"],
                                    title: hits[i]["Props"]["Title"],
                                    reward: hits[i]["Props"]["Reward"],
                                    creation_time: this.unixTimeToLocaleString(hits[i]["CreationTime"]),
                                    num_hits: hits[i]["Count"],
                                    num_assignable: hits[i]["HITStatusCount"]["Assignable"],
                                    num_reviewable: hits[i]["HITStatusCount"]["Reviewable"],
                                    detail: hits[i]
                                });
                            }
                            this.selectedHITTypes = [];
                            break;
                        }
                    }
                }
            });

            this.duct.addEvtHandler({
                tag: this.name, eid: this.duct.EVENT.MTURK_EXPIRE_HITS,
                handler: (rid, eid, data) => {
                    if(data["Status"]=="Error") {
                        this.snackbarTexts.error = "Errors occurred in expiring HITs";
                    } else {
                        const res = data["Data"]["Results"];
                        var cntSuccess = 0;
                        for(var i in res) {
                            if(("ResponseMetadata" in res[i]) && ("HTTPStatusCode" in res[i]["ResponseMetadata"]) && (res[i]["ResponseMetadata"]["HTTPStatusCode"]==200))
                                cntSuccess++;
                        }
                        if(cntSuccess==res.length) {
                            this.snackbarTexts.success = `Successfully expired ${res.length} HITs`;
                        } else {
                            this.snackbarTexts.warning = `Expired ${cntSuccess} HITs, but errors occurred in expiring ${res.length-cntSuccess} HITs`;
                        }

                    }
                    this.button.expireHITs.loading = false;
                    this.button.expireHITs.disabled = false;
                    this._evtListHITs(false);
                }
            });

            this.duct.addEvtHandler({
                tag: this.name, eid: this.duct.EVENT.MTURK_DELETE_HITS,
                handler: (rid, eid, data) => {
                    if(data["Status"]=="Error") {
                        this.snackbarTexts.error = "Errors occurred in deleting HITs";
                    } else {
                        const res = data["Data"]["Results"];
                        var cntSuccess = 0;
                        for(var i in res) {
                            if(("ResponseMetadata" in res[i]) && ("HTTPStatusCode" in res[i]["ResponseMetadata"]) && (res[i]["ResponseMetadata"]["HTTPStatusCode"]==200))
                                cntSuccess++;
                        }
                        if(cntSuccess==res.length) {
                            this.snackbarTexts.success = `Successfully deleted ${res.length} HITs`;
                        } else {
                            this.snackbarTexts.warning = `Deleted ${cntSuccess} HITs, but errors occurred in deleting ${res.length-cntSuccess} HITs`;
                        }

                    }
                    this.button.deleteHITs.loading = false;
                    this.button.deleteHITs.disabled = false;
                    this._evtListHITs(false);
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
