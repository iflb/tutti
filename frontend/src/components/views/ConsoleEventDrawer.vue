<template>
    <v-navigation-drawer
        app
        clipped
        right
        v-model="drawer"
        width="300px">
        <v-data-table
            :headers="headers"
            :items="logs"
            :items-per-page="10"
            hide-default-footer>
            <template v-slot:item.msg="{ item }">
                <v-icon
                    v-if="!item.received"
                    small
                    color="warning">
                    mdi-clock-outline
                </v-icon>

                <v-icon
                    v-else-if="item.received.Status=='Success'"
                    small
                    color="success">
                    mdi-check-circle
                </v-icon>

                <v-icon
                    v-else-if="item.received.Status=='Error'"
                    small
                    color="error">
                    mdi-alert
                </v-icon>

                <b> {{ item.evtName }} ({{ item.eid }})</b>

                <div
                    v-if="item.received"
                    style="width:100%;text-align:right">
                    {{ dateFormat(item.received.Timestamp.Requested*1000, "yyyy-mm-dd HH:MM:ss") }}
                </div>
                <vue-json-pretty :data="item.sent" :deep="1"></vue-json-pretty>
                <div style="display:flex;">
                    <div style="margin-right:5px;">
                        <v-icon x-small>mdi-arrow-right</v-icon>
                    </div>
                    <div v-if="item.received">
                        <vue-json-pretty
                            v-if="item.received.Status=='Success'"
                            :data="item.received.Contents"
                            :deep="1">
                        </vue-json-pretty>

                        <vue-json-pretty
                            v-else
                            :data="item.received.Reason"
                            :deep="1">
                        </vue-json-pretty>
                    </div>
                </div>
            </template>
        </v-data-table>
        <v-divider></v-divider>
    </v-navigation-drawer>
</template>

<script>
import 'vue-json-pretty/lib/styles.css'
import VueJsonPretty from "vue-json-pretty/lib/vue-json-pretty"
import dateFormat from 'dateformat'

export default {
    components: {
        VueJsonPretty
    },
    data: () => ({
        dateFormat,
        logs: [],
        headers: [
            { text: "Message", value: "msg" },
        ],
    }),
    props: ["duct", "drawer"],
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            setInterval(() => {
                var rows = [];
                const ductLog = this.duct.logger.log;
                for(const rid in ductLog){
                    if( ductLog[rid].eid <= 1010 )  continue;

                    rows.unshift({
                        rid,
                        eid: ductLog[rid].eid,
                        evtName: Object.keys(this.duct.EVENT).find(key => this.duct.EVENT[key] === ductLog[rid].eid),
                        sent: ductLog[rid].sent,
                        received: ductLog[rid].received[0]
                    });
                }
                this.logs = rows;
            }, 1000);
        });
    }
}
</script>
