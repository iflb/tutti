<template>
    <div class="mt-10">
        <v-row justify="center">
            <v-col cols="10" class="text-right">
                <v-btn :loading="button.expireHITs.loading" :disabled="button.expireHITs.loading" class="mx-2" dark
                       color="warning" v-if="selectedHITIds.length>0" @click="button.expireHITs.loading=true; expireHITs()">Expire ({{ selectedHITIds.length }})</v-btn>
                <v-btn :loading="button.deleteHITs.loading" :disabled="button.deleteHITs.loading" class="mx-2" dark
                       color="error" v-if="selectedHITIds.length>0" @click="button.deleteHITs.loading=true; deleteHITs()">Delete ({{ selectedHITIds.length }})</v-btn>
                <v-btn class="mx-2" dark color="indigo" to="/console/platform/mturk/hit/create/">Create HITs...</v-btn>
            </v-col>
            <v-col cols="10">
                <v-card cols="10">
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
                      sort-by="creation_time"
                      sort-desc
                    >
                        <template v-slot:top>
                            <v-card-title>
                                HITs
                                <v-btn icon @click="listHITs(false)"><v-icon>mdi-refresh</v-icon></v-btn>
                                <v-spacer></v-spacer>
                                <v-spacer></v-spacer>
                                <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
                            </v-card-title>
                            <v-card-subtitle>
                            (Last retrieved: {{ listLastRetrieved }})
                            </v-card-subtitle>
                        </template>
                        <template v-slot:item.active="{ item }">
                            <v-icon v-if="item.detail.HITStatusCount.Assignable>0" color="success">mdi-circle-medium</v-icon>
                        </template>
                        <template v-slot:item.id="{ item }">
                            <div class="text-truncate" style="max-width:100px;">
                            {{ item.id }}
                            </div>
                            <v-icon v-if="item.detail.HITStatusCount.Assignable>0" small @click="openNewWindow('https://worker.mturk.com/projects/'+item.groupId+'/tasks');">mdi-open-in-new</v-icon>
                            <v-icon v-if="item.detail.HITStatusCount.Assignable>0" small @click="openNewWindow('https://workersandbox.mturk.com/projects/'+item.groupId+'/tasks');">mdi-open-in-new</v-icon>
                        </template>
                        <template v-slot:item.title="{ item }">
                            <div class="text-truncate" style="max-width:100px;">
                            {{ item.title }}
                            </div>
                        </template>
                        <template v-slot:item.project_names="{ item }">
                            <div v-if="item.project_names && item.project_names.length==1"> {{ item.project_names[0] }} </div>
                            <v-tooltip bottom>
                                <template #activator="{ on, attrs }">
                                    <div v-if="item.project_names && item.project_names.length>1" v-html="item.project_names.join(',<br>')" v-bind="attrs" v-on="on" style="font-weight:bold; color:red;"> </div>
                                </template>
                                <span><v-icon color="white">mdi-alert</v-icon> Multiple projects are bound to one HIT Type</span>
                            </v-tooltip>
                        </template>
                        <template v-slot:item.num_hits="{ item }">
                            {{ item.num_hits }} ( {{ item.num_assignable }} / {{ item.num_reviewable }} )
                        </template>
                        <template v-slot:item.reward="{ item }">
                            ${{ item.reward }}
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
            </v-col>
        </v-row>

        <tutti-snackbar ref="snackbarSuccess" color="success" :timeout="3000" />
        <tutti-snackbar ref="snackbarWarning" color="warning" :timeout="3000" />
        <tutti-snackbar ref="snackbarError" color="error" :timeout="3000" />
    </div>
</template>
<script>
import 'vue-json-pretty/lib/styles.css'
import { stringifyUnixTime } from '@/lib/utils'

export default {
    components: {
        VueJsonPretty: () => import('vue-json-pretty/lib/vue-json-pretty'),
        TuttiSnackbar: () => import('@/views/assets/Snackbar')
    },
    data: () => ({
        selectedHITTypes: [],
        search: "",
        expanded: [],
        headers: [
          { text: '', value: 'active' },
          { text: 'HIT Type ID', value: 'id' },
          { text: 'Title', value: 'title' },
          { text: 'Project', value: 'project_names' },
          { text: 'Reward', value: 'reward' },
          { text: '# HITs (Open/Closed)', value: 'num_hits' },
          { text: 'Creation Time', value: 'creation_time' },
          { text: 'Expiration Time', value: 'expiration_time' },
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
            },
            deleteHITs: {
                loading: false,
            },
        },
    }),
    props: ["duct", "prjName", "credentials", "name"],

    computed: {
        selectedHITIds() {
            var hitIds = [];
            for(var i in this.selectedHITTypes){
                hitIds = [...hitIds, ...this.selectedHITTypes[i]["detail"]["HITIds"]];
            }
            return hitIds;
        }
    },
    methods: {
        openNewWindow(url) {
            window.open(url, "_blank");
        },
        secondsToTimeString(seconds) {
            var hours = Math.floor(seconds / 3600);
            seconds -= hours*3600;
            var minutes = Math.floor(seconds / 60);
            seconds -= minutes*60;
            return `${hours}:${("00"+minutes).slice(-2)}:${("00"+seconds).slice(-2)}`;
        },
        expireHITs(){
            this.button.expireHITs.loading = false;
            this.duct.controllers.mturk.expireHITs(this.selectedHITIds);
        },
        deleteHITs(){
            this.button.deleteHITs.loading = false;
            this.duct.controllers.mturk.deleteHITs(this.selectedHITIds);
        },
        listHITs(cached){
            this.loadingHITs = true;
            this.duct.controllers.mturk.listHITs(cached);
        }
    },

    watch: {
        credentials: {
            handler() {
                this.listHITs(true);
            },
            deep: true
        }
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.mturk.on("listHITs", {
                success: (data) => {
                    this.loadingHITs = false;
                    this.listLastRetrieved = stringifyUnixTime(data["Results"]["LastRetrieved"]);
                    const hits = data["Results"]["HITTypes"];

                    this.hitTypes = [];
                    for(var i in hits){
                        this.hitTypes.push({
                            id: i,
                            groupId: hits[i]["HITGroupId"],
                            title: hits[i]["Props"]["Title"],
                            project_names: hits[i]["ProjectNames"],
                            reward: hits[i]["Props"]["Reward"],
                            creation_time: stringifyUnixTime(hits[i]["CreationTime"]),
                            expiration_time: stringifyUnixTime(hits[i]["Expiration"]),
                            num_hits: hits[i]["Count"],
                            num_assignable: hits[i]["HITStatusCount"]["Assignable"],
                            num_reviewable: hits[i]["HITStatusCount"]["Reviewable"],
                            detail: hits[i]
                        });
                    }
                    this.selectedHITTypes = [];
                }
            });

            for(const opr of ["expire", "delete"]){
                this.duct.eventListeners.mturk.on(`${opr}HITs`, {
                    success: (data) => {
                        const cntSuccess = data["Results"].reduce((cnt,res) => ((("ResponseMetadata" in res) && ("HTTPStatusCode" in res["ResponseMetadata"]) && (res["ResponseMetadata"]["HTTPStatusCode"]==200)) ? cnt+1 : cnt));

                        if(cntSuccess==data["Results"].length) {
                            this.$refs.snackbarSuccess.show(`${opr[0].toUpperCase()+opr.slice(1)}d ${cntSuccess} HITs`);
                        } else {
                            this.$refs.snackbarWarning.show(`${opr[0].toUpperCase()+opr.slice(1)}d ${cntSuccess} HITs, but errors occurred in ${opr.slice(0,-1)}ing ${data["Results"].length-cntSuccess} HITs`);
                        }

                        this.listHITs(false);
                    },
                    error: (data) => {
                        this.$refs.snackbarError.show(`Errors occurred in ${opr.slice(0,-1)}ing HITs: ${data["Reason"]}`);

                        this.listHITs(false);
                    }
                });
            }

            this.listHITs(true);
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
