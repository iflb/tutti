<template>
    <v-main>
        <v-navigation-drawer app clipped right class="grey lighten-4 pt-4" width="400">
            <v-list>
                <v-list-item class="py-2">
                    <v-autocomplete outlined dense hide-details :items="events" item-text="label" item-value="eid" label="Event" v-model="eid"></v-autocomplete>
                </v-list-item>
                <v-list-item>
                    Requested JSON:
                </v-list-item>
                <v-list-item>
                    <v-autocomplete outlined dense v-model="queryHistoryItem" :items="queryHistory" :disabled="queryHistory.length==0" :placeholder="queryHistory.length>0 ? `Select from history ... (${queryHistory.length})` : 'No history found'"></v-autocomplete>
                </v-list-item>
                <v-list-item>
                    <codemirror v-model="query" :options="cmOptions" width="100%"></codemirror>
                </v-list-item>
                <v-list-item>
                    <v-container>
                        <v-btn color="primary" @keydown.enter="sendEvent" @click="sendEvent">Send</v-btn>
                    </v-container>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>

        <v-card-title>
            Tutti-Duct Event Logs (Advanced)
            <v-spacer></v-spacer>
            <!--<v-text-field v-model="searchStr" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>-->
        </v-card-title>
        <v-data-table :headers="logTableHeaders" :items="serverLogTableRows" :items-per-page="10" :search="searchStr">
            <template v-slot:item.sent="{ item }">
                {{ item.eid }}
                <vue-json-pretty :data="item.sent" :deep="1" style="font-size:0.6em;"></vue-json-pretty>
            </template>
            <template v-slot:item.received="{ item }">
                <vue-json-pretty :data="item.received" :deep="1" style="font-size:0.6em;"></vue-json-pretty>
            </template>
        </v-data-table>
    </v-main>
</template>

<script>
import { codemirror } from 'vue-codemirror'
import 'vue-json-pretty/lib/styles.css'
import 'codemirror/lib/codemirror.css'

export default {
    components: {
        VueJsonPretty: () => import("vue-json-pretty/lib/vue-json-pretty"),
        codemirror
    },
    data: () => ({
        eid: "",
        query: "",
        events: [],
        logTableHeaders: [
            { text: "Request ID", value: "rid" },
            { text: "Tag", value: "tag" },
            { text: "Sent Message", value: "sent" },
            { text: "Received Message", value: "received" },
        ],
        searchStr: "",
        cmOptions: {
            styleActiveLine: true,
            lineNumbers: true,
            line: true,
            mode: 'text/javascript',
            lineWrapping: true,
            theme: 'base16-dark',
            indentWithTabs: true
        },
        queryHistoryItem: ""
    }),
    props: ["duct", "sharedProps","name"],
    computed: {
        serverLogTableRows() {
            var rows = [];
            if(this.duct){
                const sentAll = this.duct.log.sent;
                for(const i in sentAll){
                    const s = sentAll[i];
                    if(s.eid=="1010") continue;

                    const rid = s.rid;
                    const tag = s.tag;
                    const sent = s.data;
                    const eid = `${Object.keys(this.duct.EVENT).find(key => this.duct.EVENT[key] === s.eid)} (${s.eid})`;
                    const received = null;
                    rows.unshift({ rid, tag, eid, sent, received })
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
        queryHistory() {
            try { return [ ...this.queryHistoryAll[this.eid.toString()] ].reverse(); }
            catch { return []; }
        }
    },
    methods: {
        loadEvents() {
            var events = []
            for(var key in this.duct.EVENT) {
                var eid = this.duct.EVENT[key]
                if(eid>=1000){ events.push({eid, label: `${eid}:: ${key}`}) }
            }
            this.events = events
        },
        sendEvent() {
            var args;
            try { args = JSON.parse(this.query); }
            catch { args = this.query!=="" ? this.query : null; }

            this.duct.sendMsg({ tag: this.name, eid: this.eid, data: args });
            this.duct.controllers.resource.setEventHistory(this.end, this.query);
            this.query = "";
        }
    },
    watch: {
        queryHistoryItem(val) {
            if(val.length>0){
                this.query = val.slice();
                this.$nextTick(() => {
                    this.queryHistoryItem = "";
                });
            }
        }
    },
    mounted() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.addTuttiEvtHandler({
                eid: this.duct.EVENT.EVENT_HISTORY,
                success: ({ data }) => {
                    if("AllHistory" in data)    this.queryHistoryAll = data["AllHistory"];
                    //else if("History" in data)  this.queryHistory = data["History"].reverse();
                }
            });

            this.loadEvents();
            this.duct.controllers.resource.getEventHistory();
        });
    }
}
</script>

<style>
.is-root, .is-root div {
    font-size: 9pt;
}
.vue-codemirror {
    width: 100%;
}
.CodeMirror {
    font-size: 12px;
    height: 150px;
}
</style>
