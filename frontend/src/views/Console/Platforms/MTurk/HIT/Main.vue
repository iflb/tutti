<template>
    <v-main class="mt-10 grey lighten-4">
        <div style="max-width:1000px" class="mx-auto">
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
                >
                    <template v-slot:top>
                        <v-card-title>
                            HITs
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
                                First created at: <b>{{ unixTimeToLocaleString(item.detail.FirstCreationTime) }}</b><br>
                                Expires at: <b>{{ unixTimeToLocaleString(item.detail.Expiration) }}</b><br>
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

export default {
    components: {
        VueJsonPretty
    },
    data: () => ({
      search: "",
      expanded: [],
        headers: [
          { text: 'HITTypeId', value: 'id' },
          { text: 'Title', value: 'title' },
          { text: 'Reward', value: 'reward' },
          { text: '# Posted HITs', value: 'num_hits' },
          { text: '', value: 'data-table-expand' },
        ],
    }),
    props: ["sharedProps","name"],

    computed: {
        ...mapGetters("ductsModule", [ "duct" ]),
        hitTypes() {
            var h = []
            if("HITTypes" in this.sharedProps) {
                for(var htid in this.sharedProps.HITTypes){
                    const _h = this.sharedProps.HITTypes[htid];
                    h.push({
                        "id": htid,
                        "title": _h.info["Title"],
                        "reward": "$"+_h.info["Reward"],
                        "num_hits": _h.cnt,
                        "detail": _h.info
                    });
                }
            }
            return h
        }
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
        }
    },
    mounted() {
        this.onDuctOpen(() => {
            this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.MTURK_HIT, data: "list" });
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
