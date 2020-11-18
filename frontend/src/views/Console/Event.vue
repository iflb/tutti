<template>
    <v-main class="mt-10 grey lighten-4">
        <v-row justify="center"><v-col cols="11">
            <v-card class="pa-3">
                <v-row class="d-flex">
                    <v-col>
                    <v-select hide-details :items="events" item-text="label" item-value="eid" label="Event" v-model="selectedEventId"></v-select>
                    </v-col>
                    <v-col>
                    <v-combobox v-model="selectedEventArgs" @input.native="selectedEventArgs=$event.srcElement.value" :items="selectedEventArgsHistory" placeholder="Args separated by spaces"></v-combobox>
                    </v-col>
                    <v-col>
                    <v-container>
                    <v-btn color="primary" @keydown.enter="sendEvent" @click="sendEvent">Send</v-btn>
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
import { mapGetters, mapActions } from 'vuex'
import VueJsonPretty from 'vue-json-pretty'
import 'vue-json-pretty/lib/styles.css'

export default {
    store,
    components: {
        VueJsonPretty
    },
    data: () => ({
        selectedEventId: null,
        selectedEventArgs: "",
        //selectedEventArgsHistory: [],
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
                    if(s.eid=="1010") continue;

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
        },
        selectedEventArgsHistory() {
            if(this.sharedProps.evtHistory
                && this.selectedEventId
                && this.selectedEventId.toString() in this.sharedProps.evtHistory) {
                var _hist = this.sharedProps.evtHistory[this.selectedEventId.toString()];
                return _hist.reverse();
            } else {
                return [];
            }
        }
    },
    methods: {
        ...mapActions("ductsModule", [ "onDuctOpen" ]),
        loadEvents() {
            var events = []
            for(var key in this.duct.EVENT) {
                var eid = this.duct.EVENT[key]
                if(eid>=1000){ events.push({eid, label: `${eid}:: ${key}`}) }
            }
            this.events = events
        },
        getEventHistory() {
            this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.EVENT_HISTORY, data: null });
        },
        sendEvent() {
            const histEid = this.duct.EVENT.EVENT_HISTORY;
            this.duct.sendMsg({ tag: this.name, eid: this.selectedEventId, data: this.selectedEventArgs });
            this.duct.sendMsg({ tag: this.name, eid: histEid, data: `${this.selectedEventId} ${this.selectedEventArgs}`});
            this.selectedEventArgs = "";
        }
    },
    mounted() {
        this.onDuctOpen(() => {
            this.loadEvents();
            this.getEventHistory();
        });
    }
}
</script>

<style>
.is-root, .is-root div {
    font-size: 9pt;
}
</style>
