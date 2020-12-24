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
                        <v-icon small @click="openNewWindow('https://workersandbox.mturk.com/projects/'+item.groupId+'/tasks');">mdi-open-in-new</v-icon>
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

            <v-snackbar :color="snackbar.success.color" v-model="snackbar.success.shown" :timeout="snackbar.success.timeout">
              {{ snackbar.success.text }}
              <template v-slot:action="{ attrs }">
                  <v-btn dark color="white" text v-bind="attrs" @click="snackbar.success.shown=false">Close</v-btn>
              </template>
            </v-snackbar>
            <v-snackbar :color="snackbar.warning.color" v-model="snackbar.warning.shown" :timeout="snackbar.warning.timeout">
              {{ snackbar.warning.text }}
              <template v-slot:action="{ attrs }">
                  <v-btn dark color="white" text v-bind="attrs" @click="snackbar.warning.shown=false">Close</v-btn>
              </template>
            </v-snackbar>
            <v-snackbar :color="snackbar.error.color" v-model="snackbar.error.shown" :timeout="snackbar.error.timeout">
              {{ snackbar.error.text }}
              <template v-slot:action="{ attrs }">
                  <v-btn dark color="white" text v-bind="attrs" @click="snackbar.error.shown=false">Close</v-btn>
              </template>
            </v-snackbar>
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
        selectedHITTypes: [],
        search: "",
        expanded: [],
        headers: [
          { text: '', value: 'active' },
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
        snackbar: {
            success: {
                shown: false,
                text: "",
                timeout: 5000,
                color: "success"
            },
            warning: {
                shown: false,
                text: "",
                timeout: 5000,
                color: "warning"
            },
            error: {
                shown: false,
                text: "",
                timeout: 5000,
                color: "error"
            }
        }
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
                        this.snackbar.error.text = "Errors occurred in expiring HITs";
                        this.snackbar.error.shown = true;
                    } else {
                        const res = data["Data"]["Results"];
                        var cntSuccess = 0;
                        for(var i in res) {
                            if(("ResponseMetadata" in res[i]) && ("HTTPStatusCode" in res[i]["ResponseMetadata"]) && (res[i]["ResponseMetadata"]["HTTPStatusCode"]==200))
                                cntSuccess++;
                        }
                        if(cntSuccess==res.length) {
                            this.snackbar.success.text = `Successfully expired ${res.length} HITs`;
                            this.snackbar.success.shown = true;
                        } else {
                            this.snackbar.warning.text = `Expired ${cntSuccess} HITs, but errors occurred in expiring ${res.length-cntSuccess} HITs`;
                            this.snackbar.warning.shown = true;
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
                        this.snackbar.error.text = "Errors occurred in deleting HITs";
                        this.snackbar.error.shown = true;
                    } else {
                        const res = data["Data"]["Results"];
                        var cntSuccess = 0;
                        for(var i in res) {
                            if(("ResponseMetadata" in res[i]) && ("HTTPStatusCode" in res[i]["ResponseMetadata"]) && (res[i]["ResponseMetadata"]["HTTPStatusCode"]==200))
                                cntSuccess++;
                        }
                        if(cntSuccess==res.length) {
                            this.snackbar.success.text = `Successfully deleted ${res.length} HITs`;
                            this.snackbar.success.shown = true;
                        } else {
                            this.snackbar.warning.text = `Deleted ${cntSuccess} HITs, but errors occurred in deleting ${res.length-cntSuccess} HITs`;
                            this.snackbar.warning.shown = true;
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
