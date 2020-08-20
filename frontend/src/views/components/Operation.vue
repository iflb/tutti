<template>
    <v-main>
        <v-container justify="center">
            <v-row class="d-flex justify-center">
                <v-col>
                <v-select :items="events" item-text="label" item-value="eid" label="Event" v-model="selectedEventId"></v-select>
                </v-col>
                <v-col>
                <v-text-field id="input-args" type="text" v-model="selectedEventArgs" placeholder="Args separated by spaces"></v-text-field>
                </v-col>
                <v-col>
                <v-btn color="primary" @click="duct.sendMsg({ tag: name, eid: selectedEventId, data: selectedEventArgs })">Send</v-btn>
                </v-col>
            </v-row>
            <v-card>
                <v-card-title>
                    Communication Logs
                    <v-spacer></v-spacer>
                    <v-text-field v-model="searchStr" append-icon="mdi-magnify" label="Search" single-line hide-details>
                    </v-text-field>
                </v-card-title>
                <v-data-table :headers="logTableHeaders" :items="serverLogTableRows" :items-per-page="10" :search="searchStr"></v-data-table>
                <!--<v-col>
                    <v-simple-table>
                        <template v-slot:default>
                            <thead><tr><th class="text-left">Sent Messages</th></tr></thead>
                            <tbody><tr v-for="m in sentMsg" :key="m"><td>{{ m }}</td></tr></tbody>
                        </template>
                    </v-simple-table>
                </v-col>
                <v-col>
                    <v-simple-table>
                        <template v-slot:default>
                            <thead><tr><th class="text-left">Received Messages</th></tr></thead>
                            <tbody><tr v-for="m in receivedMsg" :key="m"><td>{{ m }}</td></tr></tbody>
                        </template>
                    </v-simple-table>
                </v-col>
                -->
            </v-card>
        </v-container>
    </v-main>
</template>

<script>
import store from '@/store.js'
import { mapGetters } from 'vuex'

export default {
    store,
    data: () => ({
        selectedEventId: "",
        selectedEventArgs: "",
        events: [],
        serverLog: {},
        logTableHeaders: [
            { text: "Request ID", value: "rid" },
            { text: "Tag", value: "tag" },
            { text: "Sent Message", value: "sent" },
            { text: "Received Message", value: "received" },
        ],
        serverLogTableRows: [],
        searchStr: ""
    }),
    props: ["sharedProps","name"],
    computed: {
        ...mapGetters("ductsModule", [
            "duct"
        ]),
        sentMsg() {
            if(!this.duct) return []
            var msg = []
            for(var i in this.duct.log.sent){
                var l = this.duct.log.sent[i]
                msg.push(`${l.tag}__${l.rid}__${l.eid}__${l.data}`)
            }
            return msg
        },
        receivedMsg() {
            if(!this.duct) return []
            var msg = []
            for(var i in this.duct.log.received){
                var l = this.duct.log.received[i]
                msg.push(`${l.rid}__${l.eid}__${JSON.stringify(l.data)}`)
            }
            return msg
        },
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
        },
        aggregateLogs(log) {
            const lastLog = log[log.length-1]
            var key = "tag" in lastLog ? "sent" : "received";
            if(lastLog){
                if(!(lastLog.rid in this.serverLog)) this.serverLog[lastLog.rid] = {}
                this.serverLog[lastLog.rid][key] = lastLog;
            }
            var rows = [];
            for(const rid in this.serverLog){
                const tag = this.serverLog[rid].sent.tag;
                const s = this.serverLog[rid].sent;
                const sent = s ? `${s.eid}__${s.data}` : ""
                const r = this.serverLog[rid].received;
                const received = r ? `${r.eid}__${JSON.stringify(r.data)}` : ""
                rows.push({ rid, tag, sent, received })
            }
            this.serverLogTableRows = rows;
        }
    },
    mounted() {
        this.loadEvents()
    },
    watch: {
        "duct.EVENT": function() { this.loadEvents() },
        "duct.log.sent": function(newVal){ if(newVal.length) this.aggregateLogs(newVal); },
        "duct.log.received": function(newVal){ if(newVal.length) this.aggregateLogs(newVal); },
    }
}
</script>
