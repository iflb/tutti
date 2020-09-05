<template>
    <v-app>
        <v-app-bar color="indigo" dark app clipped-left dense>
            <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
            
            <v-toolbar-title>DynamicCrowd Management Console</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-autocomplete v-model="project.name" :items="projects" :search-input.sync="searchString" label="Select existing project" hide-details cache-items solo-inverted hide-no-data dense rounded></v-autocomplete>

            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-btn fab dark small icon v-on="on" v-bind="attrs" @click.stop="dialog.createProject = true"><v-icon dark>mdi-plus-box-multiple-outline</v-icon></v-btn>
                </template>
                <span>Create New Project...</span>
            </v-tooltip>

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

        <v-dialog v-model="dialog.createProject" max-width="400">
          <v-card>
            <v-card-title class="headline">Create New Project</v-card-title>
            <v-form v-model="isFormValid.createProject" @submit.prevent="createProject(); dialog.createProject = false">
                <v-card-text>
                    <v-text-field autofocus v-model="newProjectName" filled prepend-icon="mdi-pencil" label="Enter Project Name" :rules="[rules.required, rules.alphanumeric]"></v-text-field>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn text @click="dialog.createProject = false" >Cancel</v-btn>
                  <v-btn color="primary" text :disabled="!isFormValid.createProject" @click="createProject(); dialog.createProject = false" >Create</v-btn>
                </v-card-actions>
            </v-form>
          </v-card>
        </v-dialog>

        <v-navigation-drawer v-model="drawer" app clipped>
            <v-list nav shaped>
                <v-list-item-group active-class="indigo--text text--accent-4">
                    <!--<v-list-item>
                        <v-list-item-content>
                            <v-list-item-title class="title">DynamicCrowd</v-list-item-title>
                            <v-list-item-subtitle>Alpha Version</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>-->

                    <v-list-item to="/console/dashboard/">
                        <v-list-item-icon>
                            <v-icon>mdi-view-dashboard</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Dashboard</v-list-item-title>
                    </v-list-item>
                    
                    <v-list-item to="/console/template/">
                        <v-list-item-icon>
                            <v-icon>mdi-iframe-outline</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Templates</v-list-item-title>
                    </v-list-item>
               
                    <v-list-item to="/console/flow/">
                        <v-list-item-icon>
                            <v-icon>mdi-transit-connection</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Task Flow</v-list-item-title>
                    </v-list-item>
 
                    <v-list-item to="/console/answer/">
                        <v-list-item-icon>
                            <v-icon>mdi-comment-text-multiple-outline</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Answers</v-list-item-title>
                    </v-list-item>
                
                    <v-list-item to="/console/event/">
                        <v-list-item-icon>
                            <v-icon>mdi-lightning-bolt</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Duct Events</v-list-item-title>
                    </v-list-item>

                </v-list-item-group>
            </v-list>
        </v-navigation-drawer>

        <router-view :shared-props="sharedProps" ref="child"></router-view>
        
    </v-app>
</template>

<script>
import dateFormat from 'dateformat'
import store from '@/store.js'
import { mapActions, mapGetters } from 'vuex'

var project = {
    name: "",
    templates: [],
    profile: null,
}

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
        newProjectName: "",

        sharedProps: {
            project,
            answers: {}
        },
        dialog: {
            createProject: false
        },

        isFormValid: {
            createProject: false
        },
        rules: {
            required: value => !!value || "This field is required",
            alphanumeric: value => {
                const pattern = /^[a-zA-Z0-9_-]*$/;
                return pattern.test(value) || 'Alphabets, numbers, "_", or "-" is only allowed';
            }
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
            this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.NANOTASK_SESSION_MANAGER, data: `GET_FLOWS ${val}` })
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
            setTimeout(() => {
                this.items = this.projects.filter(e => { return (e || '').toLowerCase().indexOf((v || '').toLowerCase()) > -1 })
                this.loading = false
            }, 500)
        },
        createProject() {
            this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.CREATE_PROJECT, data: this.newProjectName })
        }
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
            this.duct.setEventHandler(this.duct.EVENT.CREATE_PROJECT, () => {
                this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.LIST_PROJECTS, data: null })
            })
            this.duct.setEventHandler(this.duct.EVENT.CREATE_TEMPLATE, () => {
                this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.LIST_TEMPLATES, data: this.project.name })
            })
            this.duct.setEventHandler(this.duct.EVENT.LIST_PROJECTS, (rid, eid, data) => {
                this.projects = data
            })
            this.duct.setEventHandler(this.duct.EVENT.LIST_TEMPLATES, (rid, eid, data) => {
                this.project.templates = data
                this.sharedProps.project = this.project
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
                    else if(data["Command"]=="GET_FLOWS" || data["Command"]=="LOAD_FLOW"){
                        if(data["Status"]=="error"){
                            this.sharedProps.project.profile = null
                            this.$refs.child.showSnackbar({
                                color: "warning",
                                text: data["Reason"]
                            })
                        } else {
                            this.sharedProps.project.profile = data["Flow"]
                        }
                    }
                }
            })

            this.duct.addEvtHandler({
                tag: "/console/answers/", eid: this.duct.EVENT.ANSWERS,
                handler: (rid, eid, data) => {
                    this.sharedProps.answers = data["Answers"];
                }
            })

            this.openDuct().then(() => {
                this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.LIST_PROJECTS, data: null })
            })
        })
    }
}
</script>
