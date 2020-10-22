<template>
    <v-main class="mt-10 grey lighten-4">
        <div style="max-width:1000px" class="mx-auto">
            <v-card>
                <v-data-table
                  :headers="qualHeaders"
                  :items="quals"
                  :single-expand="false"
                  :expanded.sync="expanded"
                  item-key="name"
                  show-expand
                  class="elevation-1"
                  dense
                >
                    <template v-slot:top>
                        <v-card-title>
                            Qualifications
                            <v-spacer></v-spacer>
                            <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
                        </v-card-title>
                    </template>
                    <template v-slot:expanded-item="{ headers, item }">
                        <td :colspan="headers.length">
                            <div class="my-2">
                                <div class="d-flex flex-row-reverse">
                                    <v-btn icon color="grey lighten-1"><v-icon>mdi-pencil</v-icon></v-btn>
                                    <v-btn icon color="grey lighten-1"><v-icon>mdi-account-edit</v-icon></v-btn>
                                </div>
                                Description: <b>{{ item.detail.Description }}</b><br>
                                Created at: <b>{{ unixTimeToLocaleString(item.detail.CreationTime) }}</b><br>
                                Automatically grant on submission: <b>{{ item.detail.AutoGranted }}</b><br>
                                # of assigned workers: <b>{{ item.detail.workers ? item.detail.workers.length : 'retrieving...' }}</b><br>
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

export default {
    components: {
        VueJsonPretty
    },
    data: () => ({
      search: "",
      expanded: [],
        qualHeaders: [
          { text: 'Name', value: 'name' },
          { text: 'Status', value: 'status' },
          { text: 'QualificationTypeId', value: 'qualificationId' },
          { text: '', value: 'data-table-expand' },
        ],
    }),
    props: ["sharedProps","name"],

    //components: { DialogCreate },
    computed: {
        ...mapGetters("ductsModule", [ "duct" ]),
        quals() {
            var q = []
            if("mTurkQuals" in this.sharedProps) {
                for(var qid in this.sharedProps.mTurkQuals){
                    const _q = this.sharedProps.mTurkQuals[qid];
                    q.push({
                        "name": _q["Name"],
                        "status": _q["QualificationTypeStatus"],
                        "qualificationId": _q["QualificationTypeId"],
                        "detail": _q
                    });
                }
            }
            return q
        }
    },
    methods: {
        ...mapActions("ductsModule", [ "onDuctOpen" ]),
        unixTimeToLocaleString(unixTime) {
            var dt = new Date(unixTime*1000);
            return dt.toLocaleDateString() + " " + dt.toLocaleTimeString();
        }
    },
    mounted() {
        this.onDuctOpen(() => {
            if(Object.keys(this.sharedProps.mTurkAccount).length==0) {
                this.duct.addEvtHandler({ tag: this.name, eid: this.duct.EVENT.MTURK_QUALIFICATION, handler: (rid, eid, data) => {
                        const command = data["Data"]["Command"];
                        if(data["Status"]=="error") return;

                        if(command=="list"){
                            var qids = [];
                            for(var i in data["Data"]["QualificationTypes"]){
                                qids.push(data["Data"]["QualificationTypes"][i]["QualificationTypeId"]);
                            }
                            this.duct.sendMsg({
                                tag: this.name, eid: this.duct.EVENT.MTURK_QUALIFICATION,
                                data: "get_workers "+qids.join(" ")
                            });
                        }
                    }
                });
                this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.MTURK_QUALIFICATION, data: "list" });
                //this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.MTURK_REQUESTER_INFO, data: null });
            }
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
