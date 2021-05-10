<template>
    <v-row class="my-10" justify="center">
        <v-col class="text-right" cols="10">
            <div style="display:flex;justify-content:flex-end;">
                <delete-qual-button :duct="duct" :qtids="selectedQualTypeIds" @delete="getQualificationTypeIds()" />
                <create-qual-button :duct="duct" @create="getQualificationTypeIds()" />
            </div>
        </v-col>

        <v-col cols="10">
            <v-data-table
                dense
                show-expand
                show-select
                sort-desc
                :headers="qualHeaders"
                :items="qualsList"
                :single-expand="false"
                :expanded.sync="expanded"
                item-key="name"
                class="elevation-1"
                :loading="loading"
                v-model="selectedQualTypes"
                sort-by="creationTime">

                <template v-slot:item.qualificationId="{ item }">
                    <div class="text-truncate" style="max-width:100px;">
                        {{ item.qualificationId }}
                    </div>
                </template>

                <template v-slot:item.num_workers="{ item }">
                    <v-btn
                        text
                        :loading="item.num_workers==-2"
                        @click="item.num_workers=-2; listWorkersWithQualificationType(item.qualificationId);">
                        <span v-if="item.num_workers>=0"> {{ item.num_workers }} </span>
                        <span v-else> ... </span>
                    </v-btn>
                </template>

                <template v-slot:top>
                    <v-card-title>
                        Qualifications
                        <v-btn icon @click="getQualificationTypeIds()"><v-icon>mdi-refresh</v-icon></v-btn>

                        <v-spacer></v-spacer>

                        <v-text-field
                            single-line
                            hide-details 
                            v-model="search"
                            append-icon="mdi-magnify"
                            label="Search" />
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
                            Created at: <b>{{ item.detail.CreationTime }}</b><br>
                            Automatically grant on submission: <b>{{ item.detail.AutoGranted }}</b><br>
                            # of assigned workers: <b>{{ item.detail.workers ? item.detail.workers.length : 'retrieving...' }}</b><br>
                            Raw data:
                            <vue-json-pretty :data="item.detail" :deep="1" style="font-size:0.6em;"></vue-json-pretty>
                        </div>
                    </td>
                </template>

            </v-data-table>
        </v-col>

    </v-row>
</template>
<script>
import 'vue-json-pretty/lib/styles.css'
import { stringifyUnixTime } from '@/lib/utils'
import CreateQualButton from './CreateQualButton'
import DeleteQualButton from './DeleteQualButton'

export default {
    components: {
        CreateQualButton,
        DeleteQualButton,
        VueJsonPretty: () => import('vue-json-pretty/lib/vue-json-pretty'),
    },
    data: () => ({

        selectedQualTypes: [],
        search: "",
        expanded: [],
        qualHeaders: [
          { text: 'Name', value: 'name' },
          { text: 'Status', value: 'status' },
          { text: 'QualificationTypeId', value: 'qualificationId' },
          { text: '# Workers', value: 'num_workers' },
          { text: 'CreationTime', value: 'creationTime' },
          { text: '', value: 'data-table-expand' },
        ],
        loading: false,
        quals: {},
    }),
    props: ["duct", "credentials", "sharedProps","name"],

    computed: {
        selectedQualTypeIds() {
            var qtids = [];
            for(var i in this.selectedQualTypes)
                qtids.push(this.selectedQualTypes[i]["detail"]["QualificationTypeId"]);
            return qtids;
        },
        qualsList() {
            return Object.entries(this.quals).map((val) => (val[1]));
        }
    },
    methods: {
        getQualificationTypeIds() {
            this.loading = true;
            this.duct.controllers.mturk.listQualifications(false);
        },
        listWorkersWithQualificationType(qid) {
            this.duct.controllers.mturk.listWorkersWithQualificationType(qid);
        },
    },
    mounted() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.mturk.on("listQualifications", {
                success: (data) => {
                    this.quals = {};
                    const qtypes = data["QualificationTypes"];
                    for(const qtype of qtypes){
                        this.$set(this.quals, qtype.QualificationTypeId, {
                            "name": qtype["Name"],
                            "status": qtype["QualificationTypeStatus"],
                            "qualificationId": qtype["QualificationTypeId"],
                            "num_workers": -1,
                            "creationTime": stringifyUnixTime(qtype["CreationTime"]),
                            "detail": qtype
                        });
                    }

                    this.selectedQualTypes = [];
                    this.loading = false;
                }
            });

            this.duct.eventListeners.mturk.on("listWorkersWithQualificationType", {
                success: (data) => {
                    const qid = data["QualificationTypeId"];
                    var quals = data["Results"];
                    this.$set(this.quals[qid], "num_workers", quals.length);
                }
            });

            this.getQualificationTypeIds();
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
