<template>
    <v-app>
        <v-app-bar color="indigo" dark app clipped-left>
            <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
            
            <v-toolbar-title>DynamicCrowd Management Console</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-autocomplete v-model="project.name" :items="projects" :search-input.sync="searchString" label="Project name" cache-items solo-inverted hide-no-data></v-autocomplete>
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
                            <v-list-item-subtitle>Alpha Version</v-list-item-subtitle>
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
               
                    <v-list-item to="/console/flow/">
                        <v-list-item-icon>
                            <v-icon>mdi-puzzle</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Task Flow Designer</v-list-item-title>
                    </v-list-item>
 
                    <v-list-item to="/console/events/">
                        <v-list-item-icon>
                            <v-icon>mdi-lightning-bolt</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Event Handlers</v-list-item-title>
                    </v-list-item>
                
                </v-list-item-group>
            </v-list>
        </v-navigation-drawer>

        <router-view :child-props="childProps" ref="child"></router-view>
        
    </v-app>
</template>

<script>
import dateFormat from 'dateformat'
import store from '@/store.js'
import { mapActions, mapGetters } from 'vuex'

var project = {
    name: "",
    templates: [],
    profile: null
}

//var connection = {
//    status: "connecting",
//    lastPinged: null,
//    btnInfo() {
//        switch(this.status){
//            case "connected":
//                return {
//                    color: "success",
//                    label: "Connected to server",
//                    menu: [ { title: "Disconnect", handler: self.closeDuct } ]
//                }
//            case "connecting":
//                return {
//                    color: "warning",
//                    label: "Connecting to server..."
//                }
//            case "disconnected":
//                return {
//                    color: "error",
//                    label: "No connection to server",
//                    menu: [ { title: "Connect", handler: self.openDuct } ]
//                }               
//            default:
//                return null
//        }
//    }
//}




export default {
    store,
    data: () => ({
        drawer: true,
        name: "/console/",

        lastPinged: "",
        srvStatus: "connecting",
        srvStatusProfile: null,

        searchString: "",

        projects: [],
        project,

        childProps: {
            project,
            "/console/events/": {
                events: []
            },
            "/console/flow/": {
                projects: [],
                templates: [],
                projectName: "",
                profile: ""
            },
        }
    }),
    computed: {
        ...mapGetters("ductsModule", [
            "duct"
        ])
    },
    watch: {
        searchString (val) {
            val && val !== this.select && this.querySelections(val)
        },
        "project.name" (val) {
            this.project = project

            this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.LIST_TEMPLATES, data: val })
        }
    },
    methods: {
        ...mapActions("ductsModule", [
            "initDuct",
            "openDuct",
            "closeDuct"
        ]),
        querySelections (v) {
            this.loading = true
            // Simulated ajax query
            setTimeout(() => {
                this.items = this.projects.filter(e => {
                    return (e || '').toLowerCase().indexOf((v || '').toLowerCase()) > -1
                })
                this.loading = false
            }, 500)
        },
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
            this.duct.setEventHandler(this.duct.EVENT.LIST_PROJECTS, (rid, eid, data) => {
                this.projects = data
                this.childProps["/console/flow/"].projects = data
            })
            this.duct.setEventHandler(this.duct.EVENT.LIST_TEMPLATES, (rid, eid, data) => {
                this.project.templates = data
                this.childProps.project = this.project

                this.childProps["/console/flow/"].templates = data
            })


            this.duct.addEvtHandler({
                tag: "/console/flow/", eid: this.duct.EVENT.NANOTASK_SESSION_MANAGER,
                handler: (rid, eid, data) => {
                    if(data["Command"]=="REGISTER_SM"){
                        this.$refs.child.showSnackbar({
                            color: "success",
                            text: "Successfully registered a state machine"
                        })
                    }
                    else if(data["Command"]=="GET_SM_PROFILE"){
                        if(data["Status"]=="error"){
                            this.childProps.project.profile = null
                            this.$refs.child.showSnackbar({
                                color: "warning",
                                text: "Profile is not set"
                            })
                        } else {
                            this.childProps.project.profile = data["Profile"]
                        }
                    }
                }
            })

            this.openDuct().then(() => {
                this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.LIST_PROJECTS, data: null })
            })
        })
    }
}
</script>
