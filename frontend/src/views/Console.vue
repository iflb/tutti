<template>
    <v-app>
        <v-app-bar color="indigo" dark app clipped-left>
            <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
            
            <v-toolbar-title>DynamicCrowd Management Console</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-menu offset-y>
                <template v-slot:activator="{ on, attrs }">
                    <v-btn depressed :color="srvBtns[srvStatus].color" class="text-none" v-bind="attrs" v-on="on">
                        {{ srvBtns[srvStatus].label }}
                        <span v-if="srvStatus == 'connected'" class="text-caption ml-2">(last pinged: {{ lastPinged }})</span>
                    </v-btn>
                </template>
                <v-list>
                    <v-list-item v-for="(menu, index) in srvBtns[srvStatus].menu" :key="index" @click="menu.handler()">
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
                    
                    <v-list-item to="/console/inspector/">
                        <v-list-item-icon>
                            <v-icon>mdi-iframe-braces-outline</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Nanotask Inspector</v-list-item-title>
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

        <v-sheet><router-view :duct="duct" ref="child"></router-view></v-sheet>
        
    </v-app>
</template>

<script>
import dateFormat from 'dateformat'

export default {
    data: () => ({
        drawer: true,
        lastPinged: "",
        duct: null,
        srvStatus: "connecting",
        srvBtns: null,
    }),
    methods: {
        init() {
            this.srvBtns = {
                connected: {
                    color: "success",
                    label: `Connected to server`,
                    menu: [ { title: "Disconnect", handler: this.closeDuct } ]
                },
                connecting: {
                    color: "warning",
                    label: "Connecting to server..."
                },
                disconnected: {
                    color: "error",
                    label: "No connection to server",
                    menu: [ { title: "Connect", handler: this.openDuct } ]
                }
            }
        },
        main(wsd){
            this.duct = new window.ducts.dynamiccrowd.Duct(wsd);

            this.duct.catchall_event_handler = (rid, eid) => {console.log('on_message eid='+eid)};
            this.duct.uncaught_event_handler = (rid, eid) => {console.log('uncaught_message eid='+eid)};
            this.duct.event_error_handler = (rid, eid, data, error) => {console.error(error);};

            this.duct._connection_listener.on("onopen", () => {
                this.srvStatus = "connected"
                this.lastPinged = dateFormat(new Date(), "HH:MM:ss")
            })
            this.duct._connection_listener.on(["onclose", "onerror"], () => {
                this.srvStatus = "disconnected"
            })
            this.duct.setEventHandler(this.duct.EVENT.ALIVE_MONITORING, () => {
                this.lastPinged = dateFormat(new Date(), "HH:MM:ss")
            })

            this.openDuct()
        },
        initDucts(ducts) {
            ducts.user = 'guest';
            ducts.context_url = '/ducts';
            ducts.libs_plugin = [ducts.context_url + '/libs/libcrowd.js'];
            ducts.main = this.main;
                                                
            let lib_script = document.createElement('script');
            lib_script.src = ducts.context_url+'/libs/main.js';
            document.body.appendChild(lib_script);
        },
        openDuct(){
            return new Promise((resolve, reject) => {
                this.duct.open().then(() => {
                    if(this.$refs.child.onDuctOpen) this.$refs.child.onDuctOpen();
                    resolve();
                }).catch(reject);
            })
        },
        closeDuct(){
            this.duct.close()
            if(this.$refs.child.onDuctClose) this.$refs.child.onDuctClose();
        }
    },
    created: function(){
        this.init()
        this.initDucts( window.ducts = window.ducts || {})
    }
}
</script>
