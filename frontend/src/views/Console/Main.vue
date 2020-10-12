<template>
    <v-app>
        <v-app-bar color="indigo" dark app clipped-left dense>
            <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
            
            <v-toolbar-title>DynamicCrowd Management Console</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-autocomplete v-model="project.name" :items="projectNames" :search-input.sync="searchString" label="Select existing project" hide-details cache-items solo-inverted hide-no-data dense rounded></v-autocomplete>

            <v-menu bottom left offset-y>
                <template v-slot:activator="{ on, attrs }">
                    <v-btn fab dark small icon v-on="on" v-bind="attrs"><v-icon>mdi-dots-vertical</v-icon></v-btn>
                </template>
                <v-list>
                    <v-list-item @click="$refs.dlgCreateProject.shown=true">
                        <v-list-item-title>Create New Project...</v-list-item-title>
                    </v-list-item>
                    <v-list-item :disabled="project.name==''" @click="launchProductionMode()">
                        <v-list-item-title>Launch in Production Mode (Private)</v-list-item-title>
                        <v-list-item-action>
                            <v-icon>mdi-open-in-new</v-icon>
                        </v-list-item-action>
                    </v-list-item>
                    <v-list-item @click="copyProjectPath">
                        <v-list-item-content>
                            <v-list-item-title>Project Path (Click to Copy)</v-list-item-title>
                            <v-list-item-subtitle>{{ this.project.path }}</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
            </v-menu>

            <dialog-create-project ref="dlgCreateProject" />

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
            <v-list nav dense>
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
                </v-list-item-group>
                <v-list-item-group active-class="indigo--text text--accent-4">
                    <v-subheader>DESIGN & TEST</v-subheader>
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
                </v-list-item-group>
                <v-list-item-group active-class="indigo--text text--accent-4">
                    <v-subheader>PUBLISH & COLLECT</v-subheader>
 
                    <v-list-group prepend-icon="mdi-account-group" :value="false">
                        <template v-slot:activator><v-list-item-title>Worker Platforms</v-list-item-title></template>
                        <v-list-item to="/console/platform/mturk/">
                            <v-list-item-icon></v-list-item-icon>
                            <v-list-item-content>
                            <v-list-item-title>Amazon MTurk</v-list-item-title>
                            </v-list-item-content>
                            <v-list-item-icon><v-icon>mdi-amazon</v-icon></v-list-item-icon>
                        </v-list-item>
                        <v-list-item to="/console/platform/private/">
                            <v-list-item-icon></v-list-item-icon>
                            <v-list-item-content>
                            <v-list-item-title>Partner-Sourcing</v-list-item-title>
                            </v-list-item-content>
                            <v-list-item-icon><v-icon>mdi-account-supervisor-circle</v-icon></v-list-item-icon>
                        </v-list-item>
                    </v-list-group>
                    <v-list-item to="/console/answer/">
                        <v-list-item-icon>
                            <v-icon>mdi-comment-text-multiple-outline</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Answers</v-list-item-title>
                    </v-list-item>
                </v-list-item-group>
                <v-list-item-group active-class="indigo--text text--accent-4">
                    <v-subheader>OTHERS</v-subheader>
                    <v-list-item to="/console/event/">
                        <v-list-item-icon>
                            <v-icon>mdi-lightning-bolt</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Duct Events</v-list-item-title>
                    </v-list-item>

                </v-list-item-group>
            </v-list>
        </v-navigation-drawer>

        <v-slide-x-transition hide-on-leave>
            <router-view :shared-props="sharedProps" ref="child"></router-view>
        </v-slide-x-transition>
        
    </v-app>
</template>

<script>
import dateFormat from 'dateformat'
import store from '@/store.js'
import { mapActions, mapGetters } from 'vuex'
import DialogCreateProject from './DialogCreateProject.vue'

var Project = class {
    constructor(name, path) {
        this.name = name;
        this.templates = {};
        this.profile = null;
        this.path = path;
    }
};

var Template = class {
    constructor(name) {
        this.name = name;
        this.nanotask = {
            cnt: 0,
            data: []
        };
    }
};

export default {
    store,
    components: { DialogCreateProject },
    data: () => ({
        drawer: true,
        name: "/console/",

        lastPinged: "",
        srvStatus: "connecting",
        srvStatusProfile: null,

        searchString: "",

        projects: {},
        project: new Project("", null),

        answers: {},

        sharedProps: {}

    }),
    computed: {
        ...mapGetters("ductsModule", [ "duct" ]),
        projectNames() {
            return Object.keys(this.projects);
        }
    },
    watch: {
        searchString (val) {
            val && val !== this.select && this.querySelections(val)
        },
        "project.name" (name) {  // called when project name is selected on the app bar
            this.project = this.projects[name];
            this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.LIST_TEMPLATES, data: name })
            this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.NANOTASK_SESSION_MANAGER, data: `LOAD_FLOW ${name}` })
        },
        project: {
            handler: function(val) {
                this.sharedProps.project = val
            },
            deep: true
        },
        answers: {
            handler: function(val) {
                this.sharedProps.answers = val
            },
            deep: true
        },
    },
    methods: {
        ...mapActions("ductsModule", [
            "initDuct",
            "openDuct",
            "closeDuct"
        ]),
        launchProductionMode(){ window.open(`/vue/private-prod/${this.project.name}`); },
        querySelections (v) {
            this.loading = true
            setTimeout(() => {
                this.items = Object.keys(this.projects).filter(e => { return (e || '').toLowerCase().indexOf((v || '').toLowerCase()) > -1 })
                this.loading = false
            }, 500)
        },
        copyProjectPath() {
            this.copyText = this.project.path;
            document.addEventListener("copy" , this.copyListener);
            document.execCommand("copy");
        },
        copyListener(e) {
            e.clipboardData.setData("text/plain" , this.copyText);
            e.preventDefault();
            document.removeEventListener("copy", this.copyListener);
        }
    },

    created: function(){
        this.$set(this.sharedProps, "project", this.project);
        this.$set(this.sharedProps, "answers", this.answers);

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
            this.duct._connection_listener.on("onopen", this.srvStatusProfile.connected.handler);
            this.duct._connection_listener.on(["onclose", "onerror"], this.srvStatusProfile.disconnected.handler);
            this.duct.setEventHandler(this.duct.EVENT.ALIVE_MONITORING, this.srvStatusProfile.connected.handler);
            this.duct.setEventHandler(this.duct.EVENT.CREATE_PROJECT, () => {
                this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.LIST_PROJECTS, data: null });
            });
            this.duct.setEventHandler(this.duct.EVENT.CREATE_TEMPLATE, () => {
                this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.LIST_TEMPLATES, data: this.project.name });
            });
            this.duct.setEventHandler(this.duct.EVENT.LIST_PROJECTS, (rid, eid, data) => {
                if(data["Status"]==="Success"){
                    var projects = data["Data"]["Projects"];
                    for(const i in projects){
                        const name = projects[i].name;
                        const path = projects[i].path;
                        var project = new Project(name, path);
                        this.$set(this.projects, name, project);
                    }
                }
            });
            this.duct.setEventHandler(this.duct.EVENT.LIST_TEMPLATES, (rid, eid, data) => {
                if(data["Status"]=="Error") return;

                const pn = data["Data"]["Project"];
                const tns = data["Data"]["Templates"];
                var templates = {};
                for(const i in tns){
                    var template = new Template(tns[i]);
                    templates[tns[i]] = template;

                    this.duct.sendMsg({
                        tag: this.name,
                        eid: this.duct.EVENT.GET_NANOTASKS,
                        data: `COUNT ${pn} ${tns[i]}`
                    });
                }
                this.$set(this.project, "templates", templates);
            });

            this.duct.setEventHandler(this.duct.EVENT.UPLOAD_NANOTASKS, (rid, eid, data) => {
                if(data["Status"]=="Error") return;

                const project = data["Data"]["Project"];
                const template = data["Data"]["Template"];
                this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.GET_NANOTASKS, data: `COUNT ${project} ${template}` });
            });

            this.duct.setEventHandler(this.duct.EVENT.GET_NANOTASKS, (rid, eid, data) => {
                if(data["Status"]=="Error") return;

                const command = data["Data"]["Command"];
                const project = data["Data"]["Project"];
                const template = data["Data"]["Template"];
                if(command=="NANOTASKS"){
                    const d = data["Data"]["Nanotasks"];
                    this.projects[project].templates[template].nanotask.data = d;
                }
                else if(command=="COUNT") {
                    const cnt = data["Data"]["Count"];
                    this.projects[project].templates[template].nanotask.cnt = cnt;
                }
            });

            this.duct.addEvtHandler({
                tag: "/console/flow/", eid: this.duct.EVENT.NANOTASK_SESSION_MANAGER,
                handler: (rid, eid, data) => {
                    const command = data["Data"]["Command"];
                    if(command=="REGISTER_SM"){
                        this.$refs.child.showSnackbar({
                            color: "success",
                            text: "Successfully registered a state machine"
                        })
                    }
                    else if(command=="LOAD_FLOW"){
                        if(data["Status"]=="Error"){
                            this.project.profile = null
                            this.$refs.child.showSnackbar({
                                color: "warning",
                                text: data["Reason"]
                            })
                        } else {
                            this.project.profile = data["Data"]["Flow"]
                        }
                    }
                }
            })

            this.duct.addEvtHandler({
                tag: "/console/answers/", eid: this.duct.EVENT.ANSWERS,
                handler: (rid, eid, data) => {
                    this.answers = data["Data"]["Answers"];
                }
            })

            this.openDuct().then(() => {
                this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.LIST_PROJECTS, data: null })
            })
        })
    }
}
</script>
