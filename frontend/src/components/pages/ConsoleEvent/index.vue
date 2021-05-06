<template>
    <v-main>
        <query-nav-bar :duct="duct" :events="events"></query-nav-bar>
        <query-log-table :logs="queryLogs"></query-log-table>
    </v-main>
</template>

<script>
import QueryNavBar from './QueryNavBar'
import QueryLogTable from './QueryLogTable'

export default {
    components: {
        QueryNavBar,
        QueryLogTable
    },
    data: () => ({
        events: [],
        queryLogs: []
    }),
    props: ["duct"],
    methods: {
        loadEvents() {
            var events = []
            for(var key in this.duct.EVENT) {
                var eid = this.duct.EVENT[key]
                if(eid>=1000){ events.push({eid, label: `${eid}:: ${key}`}) }
            }
            this.events = events
        },
    },
    mounted() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.resource.on("getEventHistory", {
                success: (data) => {
                    this.queryHistoryAll = data["AllHistory"];
                }
            });
            this.duct.eventListeners.resource.on("setEventHistory", {
                success: (data) => {
                    this.$set(this.queryHistoryAll, data["EventId"], data["History"].reverse());
                }
            });

            this.loadEvents();
            this.duct.controllers.resource.getEventHistory();

            setInterval(() => {
                var logs = [];
                const ductLog = this.duct.logger.log;
                for(const rid in ductLog){
                    if( ductLog[rid].eid <= 1010 )  continue;

                    logs.unshift({
                        rid: rid,
                        eid: `${Object.keys(this.duct.EVENT).find(key => this.duct.EVENT[key] === ductLog[rid].eid)} (${ductLog[rid].eid})`,
                        sent: ductLog[rid].sent,
                        received: ductLog[rid].received[0]
                    });
                }
                this.queryLogs = logs;
            }, 1000);
        });
    }
}
</script>
