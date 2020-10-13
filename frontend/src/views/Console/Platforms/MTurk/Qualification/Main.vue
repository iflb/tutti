<template>
    <v-main class="mt-10 grey lighten-4">
        <div style="max-width:1000px" class="mx-auto">
            <v-card>
              <v-data-table
                :headers="qualHeaders"
                :items="quals"
                :single-expand="singleExpand"
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
                      <v-text-field
                        v-model="search"
                        append-icon="mdi-magnify"
                        label="Search"
                        single-line
                        hide-details
                      ></v-text-field>
                    </v-card-title>
                </template>
                <template v-slot:expanded-item="{ headers, item }">
                  <td :colspan="headers.length">
                    More info about {{ item.name }}
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

export default {
    data: () => ({
      search: "",
      expanded: [],
        singleExpand: false,
        qualHeaders: [
          { text: 'Name', value: 'name' },
          { text: 'Status', value: 'status' },
          { text: '', value: 'data-table-expand' },
        ],
    }),
    props: ["sharedProps","name"],

    //components: { DialogCreate },
    computed: {
        ...mapGetters("ductsModule", [ "duct" ]),
        quals() {
            console.log(this.sharedProps);
            var q = []
            if("mTurkQuals" in this.sharedProps) {
                for(var i in this.sharedProps.mTurkQuals){
                    const _q = this.sharedProps.mTurkQuals[i];
                    q.push({
                        "name": _q["Name"],
                        "status": _q["QualificationTypeStatus"],
                        "detail": _q
                    });
                }
            }
            return q
        }
    },
    methods: {
        ...mapActions("ductsModule", [ "onDuctOpen" ]),
    },
    mounted() {
        this.onDuctOpen(() => {
            if(Object.keys(this.sharedProps.mTurkAccount).length==0) {
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
</style>
