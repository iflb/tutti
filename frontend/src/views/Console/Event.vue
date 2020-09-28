<template>
    <v-main class="mt-10 grey lighten-4">
        <v-row justify="center"><v-col cols="11">
            <v-card class="pa-3">
                <v-row class="d-flex">
                    <v-col>
                    <v-select hide-details :items="events" item-text="label" item-value="eid" label="Event" v-model="selectedEventId"></v-select>
                    </v-col>
                    <v-col>
                    <v-text-field hide-details id="input-args" type="text" v-model="selectedEventArgs" placeholder="Args separated by spaces"></v-text-field>
                    </v-col>
                    <v-col>
                    <v-container>
                    <v-btn color="primary" @click="duct.sendMsg({ tag: name, eid: selectedEventId, data: selectedEventArgs })">Send</v-btn>
                    </v-container>
                    </v-col>
                </v-row>
            </v-card>
        </v-col>
        <v-col cols="11">
            <v-card>
                <v-card-title>
                    Communication Logs
                    <v-spacer></v-spacer>
                    <v-text-field v-model="searchStr" append-icon="mdi-magnify" label="Search" single-line hide-details>
                    </v-text-field>
                </v-card-title>
                <v-data-table :headers="logTableHeaders" :items="serverLogTableRows" :items-per-page="10" :search="searchStr">
                    <template v-slot:item.received="{ item }">
                        <vue-json-pretty :data="item.received" :deep="1" style="font-size:0.6em;"></vue-json-pretty>
                    </template>
                </v-data-table>
            </v-card>
        </v-col></v-row>
    </v-main>
</template>

<script>
import store from '@/store.js'
import { mapGetters } from 'vuex'
import VueJsonPretty from 'vue-json-pretty'

export default {
    store,
    components: {
        VueJsonPretty
    },
    data: () => ({
        selectedEventId: "",
        selectedEventArgs: "",
        events: [],
        logTableHeaders: [
            { text: "Request ID", value: "rid" },
            { text: "Tag", value: "tag" },
            { text: "Sent Message", value: "sent" },
            { text: "Received Message", value: "received" },
        ],
        searchStr: ""
    }),
    props: ["sharedProps","name"],
    computed: {
        ...mapGetters("ductsModule", [
            "duct"
        ]),
        serverLogTableRows() {
            var rows = [];
            if(this.duct){
                const sentAll = this.duct.log.sent;
                for(const i in sentAll){
                    const s = sentAll[i];
                    const rid = s.rid;
                    const tag = s.tag;
                    const sent = `${s.eid}__${s.data}`;
                    const received = null;
                    rows.unshift({ rid, tag, sent, received })
                }
    
                const receivedAll = this.duct.log.received;
                for(const i in receivedAll){
                    const r = receivedAll[i];
                    const rid = r.rid;
                    var row = rows.find(e => e.rid==rid);
                    if(row) row.received = r.data;
                }
            }
            return rows;
        }
    },
    methods: {
        loadEvents() {
            if(!this.duct){ return }

            var events = []
            for(var key in this.duct.EVENT) {
                var eid = this.duct.EVENT[key]
                if(eid>=1000){ events.push({eid, label: `${eid}:: ${key}`}) }
            }
            this.events = events
        }
    },
    mounted() {
        this.loadEvents()
    },
    watch: {
        "duct.EVENT": function() { this.loadEvents() },
    }
}
</script>

<style>
.is-root, .is-root div {
    font-size: 9pt;
}
</style>
