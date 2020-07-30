<template>
    <v-app>
        <router-view></router-view>
    </v-app>
</template>

<script>
import dateFormat from 'dateformat'
export default {
    data: () => ({
        drawer: true,
        wsStatus: "connecting",
        wsStatusLabels: {
            connected: {
                color: "success",
                label: `Connected to websocket`
            },
            connecting: {
                color: "warning",
                label: "Connecting to websocket..."
            },
            closed: {
                color: "error",
                label: "No connection to websocket"
            }
        },
        wsBtnMenu: {},
        lastPinged: ""
    }),
    computed: {
        ws() { return this.$store.getters.ws },
        wsd() { return this.$store.getters.wsd },
    },
    methods: {
        connectWS(){
            const self = this
            self.$store.dispatch("connectDuctsWebSocket").then(function(){
                self.$store.dispatch("setOnMessageHandler", [
                    self.wsd.EVENT["ALIVE_MONITORING"],
                    function(){
                        self.lastPinged = dateFormat(new Date(), "HH:MM:ss")
                        self.wsStatus = "connected"
                    }
                ])
                self.$store.dispatch("setOnCloseHandler", function(){ self.wsStatus = "closed" })
            })
        }
    },
    created: function(){
        this.connectWS()
        this.wsBtnMenu = {
            connected: [
                {
                    title: "Disconnect",
                    handler: () => {
                        this.ws._ws.close()
                    }
                }
            ],
            closed: [
                {
                    title: "Connect",
                    handler: () => {
                        this.connectWS()
                    }
                }
            ]
        }
    }
}
</script>
