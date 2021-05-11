<template>
    <v-navigation-drawer
        app
        clipped
        right
        class="grey lighten-4 pt-4"
        width="400">
        <v-list>

            <v-list-item class="py-2">
                <v-autocomplete
                    outlined
                    dense
                    hide-details
                    :items="events"
                    item-text="label"
                    item-value="eid"
                    label="Event"
                    v-model="eid">
                </v-autocomplete>
            </v-list-item>

            <v-list-item>Requested JSON:</v-list-item>

            <v-list-item>
                <v-autocomplete
                    outlined
                    dense
                    v-model="queryHistoryItem"
                    :items="queryHistory"
                    :disabled="queryHistory.length==0"
                    :placeholder="queryHistory.length>0 ? `Select from history ... (${queryHistory.length})` : 'No history found'">
                </v-autocomplete>
            </v-list-item>

            <v-list-item>
                <codemirror
                    v-model="query"
                    :options="cmOptions"
                    width="100%">
                </codemirror>
            </v-list-item>

            <v-list-item>
                <v-container>
                    <v-btn
                        color="primary"
                        @keydown.enter="sendEvent"
                        @click="sendEvent">
                        Send
                    </v-btn>
                </v-container>
            </v-list-item>

        </v-list>
    </v-navigation-drawer>
</template>

<script>
import { codemirror } from 'vue-codemirror'
import 'codemirror/lib/codemirror.css'

export default {
    components: {
        codemirror
    },
    data: () => ({
        eid: "",
        query: "",
        queryHistoryItem: "",
        cmOptions: {
            styleActiveLine: true,
            lineNumbers: true,
            line: true,
            mode: 'text/javascript',
            lineWrapping: true,
            theme: 'base16-dark',
            indentWithTabs: true
        },
    }),
    props: ["duct", "events"],
    computed: {
        queryHistory() {
            try { return [ ...this.queryHistoryAll[this.eid.toString()] ].reverse(); }
            catch { return []; }
        }
    },
    methods: {
        sendEvent() {
            var args;
            try { args = JSON.parse(this.query); }
            catch { args = this.query!=="" ? this.query : null; }

            this.duct.send(this.duct.next_rid(), this.eid, args);
            this.duct.controllers.resource.setEventHistory(this.eid, this.query);
            this.query = "";
        },
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
