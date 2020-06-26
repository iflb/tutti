<template>
    <v-app>
        <v-app-bar color="indigo" dark app clipped-left>
            <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
            
            <v-toolbar-title>DynamicCrowd Management Console</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-menu offset-y>
                <template v-slot:activator="{ on, attrs }">
                    <v-btn depressed :color="wsStatusLabels[wsStatus].color" class="text-none" v-bind="attrs" v-on="on">
                        {{ wsStatusLabels[wsStatus].label }}
                        <span v-if="wsStatus == 'connected'" class="text-caption ml-2">(last pinged: {{ lastPinged }})</span>
                    </v-btn>
                </template>
                <v-list>
                    <v-list-item v-for="(menu, index) in wsBtnMenu[wsStatus]" :key="index" @click="menu.handler()">
                        <v-list-item-title>{{ menu.title }}</v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>
        </v-app-bar>

        <v-navigation-drawer v-model="drawer" app clipped>
            <v-list nav>
                <v-list-item-group active-class="indigo--text text--accent-4">
                    <v-list-item>
                        <v-list-item-content>
                            <v-list-item-title class="title">DynamicCrowd</v-list-item-title>
                            <v-list-item-subtitle>Beta Version</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>

                    <v-list-item to="/console/dashboard/">
                        <v-list-item-icon>
                            <v-icon>mdi-home</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Home</v-list-item-title>
                    </v-list-item>
                    
                    <v-list-item to="/console/tester/">
                        <v-list-item-icon>
                            <v-icon>mdi-iframe-braces-outline</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Nanotask Tester</v-list-item-title>
                    </v-list-item>

                    <v-list-item to="/console/events/">
                        <v-list-item-icon>
                            <v-icon>mdi-puzzle</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Event Handlers</v-list-item-title>
                    </v-list-item>
                
                </v-list-item-group>
            </v-list>
        </v-navigation-drawer>

        <v-sheet><router-view></router-view></v-sheet>
        
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
