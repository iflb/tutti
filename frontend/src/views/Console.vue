<template>
    <v-app>
        <v-app-bar color="indigo" dark app clipped-left>
            <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
            
            <v-toolbar-title>DynamicCrowd Management Console</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-menu offset-y>
                <template v-slot:activator="{ on, attrs }">
                    <v-btn depressed :color="srvStatusProfile[srvStatus].btn.color" class="text-none" v-bind="attrs" v-on="on">
                        {{ srvStatusProfile[srvStatus].btn.label }}
                        <span v-if="srvStatus == 'connected'" class="text-caption ml-2">(last pinged: {{ lastPinged }})</span>
                    </v-btn>
                </template>
                <v-list>
                    <v-list-item v-for="(menu, index) in srvStatusProfile[srvStatus].btn.menu" :key="index" @click="menu.handler()">
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

        <v-sheet><router-view :child-props="childProps" ref="child"></router-view></v-sheet>
        
    </v-app>
</template>

<script>
import dateFormat from 'dateformat'
import store from '@/store.js'
import { mapActions, mapGetters } from 'vuex'

export default {
    store,
    data: () => ({
        drawer: true,

        lastPinged: "",
        srvStatus: "connecting",
        srvStatusProfile: null,

        childProps: {
            "/console/inspector/": {
                projects: [],
                templates: []
            },
            "/console/events/": {
                events: []
            }
        }
    }),
    props: ["name"],
    computed: {
        ...mapGetters("ductsModule", [
            "duct"
        ])
    },
    methods: {
        ...mapActions("ductsModule", [
            "initDuct",
            "openDuct",
            "closeDuct"
        ])
    },
    created: function(){
        var self = this
        this.srvStatusProfile = {
            connected: {
                handler() {
                    self.srvStatus = "connected"
                    self.lastPinged = dateFormat(new Date(), "HH:MM:ss")
                },
                btn: {
                    color: "success",
                    label: "Connected to server",
                    menu: [ { title: "Disconnect", handler: self.closeDuct } ]
                }
            },
            connecting: {
                handler() {
                },
                btn: {
                    color: "warning",
                    label: "Connecting to server..."
                }
            },
            disconnected: {
                handler() {
                    self.srvStatus = "disconnected"
                },
                btn: {
                    color: "error",
                    label: "No connection to server",
                    menu: [ { title: "Connect", handler: self.openDuct } ]
                }
            }
        }
        this.initDuct(window.ducts = window.ducts || {}).then(() => {
            this.duct._connection_listener.on("onopen", this.srvStatusProfile.connected.handler)
            this.duct._connection_listener.on(["onclose", "onerror"], this.srvStatusProfile.disconnected.handler)
            this.duct.setEventHandler(this.duct.EVENT.ALIVE_MONITORING, this.srvStatusProfile.connected.handler)


            this.duct.addEvtHandler({
                tag: "/console/inspector/", eid: this.duct.EVENT.LIST_PROJECTS,
                handler: (rid, eid, data) => { this.childProps["/console/inspector/"].projects = data }
            })
            this.duct.addEvtHandler({
                tag: "/console/inspector/", eid: this.duct.EVENT.LIST_TEMPLATES,
                handler: (rid, eid, data) => { this.childProps["/console/inspector/"].templates = data }
            })


            var events = []
            for(var key in this.duct.EVENT) {
                var eid = this.duct.EVENT[key]
                if(eid>=1000){ events.push({id: eid, key: key, label: `${eid}:: ${key}`}) }
            }
            this.childProps["/console/events/"].events = events

            this.openDuct().then(() => {
                this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.LIST_PROJECTS, data: null })
            })
        })
    }
}
</script>
