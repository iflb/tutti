<template>
    <v-app>
        <v-app-bar color="indigo" dark app clipped-left dense>
            <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
            
            <v-toolbar-title>Tutti Management Console</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-autocomplete v-model="projectName" :items="projectNames" :search-input.sync="searchString" label="Select existing project" hide-details cache-items solo-inverted hide-no-data dense rounded></v-autocomplete>

            <v-menu bottom left offset-y>
                <template v-slot:activator="{ on, attrs }">
                    <v-btn fab dark small icon v-on="on" v-bind="attrs"><v-icon>mdi-dots-vertical</v-icon></v-btn>
                </template>
                <v-list>
                    <v-list-item @click="$refs.dlgCreateProject.shown=true">
                        <v-list-item-title>Create New Project...</v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>

            <dialog-create-project ref="dlgCreateProject" />

            <v-spacer></v-spacer>
            <v-menu offset-y v-if="srvStatusProfile">
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
 
                    <v-list-item :href="`/vue/private-prod/${this.projectName}`" target="_blank">
                        <v-list-item-icon>
                            <v-icon>mdi-monitor</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Task UI</v-list-item-title>
                        <v-list-item-action>
                            <v-icon small>mdi-launch</v-icon>
                        </v-list-item-action>
                    </v-list-item>
                    <v-list-item to="/console/answer/">
                        <v-list-item-icon>
                            <v-icon>mdi-database-arrow-left-outline</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Answers</v-list-item-title>
                    </v-list-item>
                    <v-list-group prepend-icon="mdi-account-group" :value="false">
                        <template v-slot:activator><v-list-item-title>Worker Platforms</v-list-item-title></template>
                        <v-list-item to="/console/platform/mturk/">
                            <v-list-item-icon><v-icon>mdi-amazon</v-icon></v-list-item-icon>
                            <v-list-item-content>
                            <v-list-item-title>Amazon MTurk</v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                        <v-list-item to="/console/platform/private/">
                            <v-list-item-icon><v-icon>mdi-account-supervisor-circle</v-icon></v-list-item-icon>
                            <v-list-item-content>
                            <v-list-item-title>Partner-Sourcing</v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </v-list-group>
                </v-list-item-group>
                <v-list-item-group active-class="indigo--text text--accent-4">
                    <v-subheader>OTHERS</v-subheader>
                    <v-list-item to="/console/event/">
                        <v-list-item-icon>
                            <v-icon>mdi-lightning-bolt</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Duct Events</v-list-item-title>
                    </v-list-item>
                    <v-list-item href="https://iflb.github.io/tutti/" target="_blank">
                        <v-list-item-icon>
                            <v-icon>mdi-file-document-outline</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Documentation</v-list-item-title>
                        <v-list-item-action>
                            <v-icon small>mdi-launch</v-icon>
                        </v-list-item-action>
                    </v-list-item>

                </v-list-item-group>
            </v-list>
        </v-navigation-drawer>

        <v-slide-x-transition hide-on-leave>
            <router-view v-if="duct" :duct="duct" :shared-props="sharedProps" ref="child"></router-view>
        </v-slide-x-transition>

        <tutti-snackbar color="success" :timeout="5000" :text="snackbarTexts.success" />
        
    </v-app>
</template>

<script>
import { DuctsLoader } from '@/lib/ducts-loader'
import dateFormat from 'dateformat'
import DialogCreateProject from './DialogCreateProject.vue'
import Snackbar from '@/views/assets/Snackbar.vue'

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
    components: { 
        TuttiSnackbar: Snackbar,
        DialogCreateProject
    },
    data: () => ({
        duct: null,
        snackbarTexts: {
            success: ""
        },
        drawer: true,
        name: "/console/",

        lastPinged: "",
        srvStatus: "connecting",
        srvStatusProfile: null,

        searchString: "",

        projects: {},
        project: new Project("", null),
        projectName: "",

        answers: {},

        sharedProps: {}
    }),
    computed: {
        projectNames() {
            return Object.keys(this.projects);
        },
    },
    watch: {
        searchString (val) {
            val && val !== this.select && this.querySelections(val)
        },
        projectName (name) {  // called when project name is selected on the app bar
            if(name){
                localStorage.setItem("tuttiProject", name);
                this.project = this.projects[name];
                this.listTemplates(name);
                this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.SESSION, data: { "Command": "LoadFlow", "ProjectName": name } })
            } 
        },
        project: {
            handler: function(val) {
                this.$set(this.sharedProps, "project", val)
            },
            deep: true
        },
        answers: {
            handler: function(val) {
                this.$set(this.sharedProps, "answers", val)
            },
            deep: true
        },
    },
    methods: {
        launchProductionMode(){ window.open(`/vue/private-prod/${this.projectName}`); },
        listTemplates(pn) {
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.LIST_TEMPLATES,
                data: {
                    "ProjectName": pn
                }
            });
        },
        querySelections (v) {
            this.loading = true
            setTimeout(() => {
                this.items = Object.keys(this.projects).filter(e => { return (e || '').toLowerCase().indexOf((v || '').toLowerCase()) > -1 })
                this.loading = false
            }, 500)
        },

        setEventHandlers() {
            this.duct.setTuttiEventHandler(this.duct.EVENT.EVENT_HISTORY, ({ data }) => {
                if("AllHistory" in data)    this.$set(this.sharedProps, "evtHistory", data["AllHistory"])
                else if("History" in data)  this.$set(this.sharedProps.evtHistory, data["EventId"], data["History"])
            });

            this.duct.setTuttiEventHandler(this.duct.EVENT.LIST_PROJECTS, ({ data }) => {
                var projects = data["Projects"];
                for(const i in projects){
                    const name = projects[i].name;
                    const path = projects[i].path;
                    var project = new Project(name, path);
                    this.$set(this.projects, name, project);
                }
                var selected = localStorage.getItem("tuttiProject");   
                if(selected)  this.$set(this, "projectName", selected);
            },
            ({ reason }) => { console.error(reason); });

            this.duct.setTuttiEventHandler(this.duct.EVENT.CREATE_PROJECT, ({ data }) => {
                this.snackbarTexts.success = `Successfully created project '${data["ProjectName"]}'`;
                this.duct.sendMsg({
                    tag: this.name,
                    eid: this.duct.EVENT.LIST_PROJECTS
                });
            });

            this.duct.setTuttiEventHandler(this.duct.EVENT.CREATE_TEMPLATES, () => {
                this.listTemplates(this.projectName);
            });

            this.duct.setTuttiEventHandler(this.duct.EVENT.LIST_TEMPLATES, ({ data }) => {
                const pn = data["Project"];
                const tns = data["Templates"];
                var templates = {};
                for(const i in tns){
                    var template = new Template(tns[i]);
                    templates[tns[i]] = template;

                    this.duct.sendMsg({
                        tag: this.name,
                        eid: this.duct.EVENT.NANOTASK,
                        data: {
                            "Command": "Get",
                            "ProjectName": pn,
                            "TemplateName": tns[i]
                        }
                    });
                }
                this.$set(this.project, "templates", templates);
            });

            this.duct.setTuttiEventHandler(this.duct.EVENT.NANOTASK, ({ data }) => {
                const Command = data["Command"];
                const ProjectName = data["ProjectName"];
                const TemplateName = data["TemplateName"];

                switch(Command){
                    case "Upload": {
                        this.duct.sendMsg({
                            tag: this.name,
                            eid: this.duct.EVENT.NANOTASK,
                            data: { Command, ProjectName, TemplateName }
                        });
                        break;
                    }
                    case "Get": {
                        const cnt = data["Count"];
                        this.projects[ProjectName].templates[TemplateName].nanotask.cnt = cnt;
                        break;
                    }
                }
            });

            this.duct.setTuttiEventHandler(this.duct.EVENT.SESSION,
                ({ data }) => {
                    if(data["Command"]=="LoadFlow"){
                        this.project.profile = data["Flow"]
                    }
                },
                ({ reason }) => {
                    this.project.profile = null
                    this.$refs.child.showSnackbar({
                        color: "warning",
                        text: reason
                    })
                }
            );

            this.duct.setTuttiEventHandler(this.duct.EVENT.GET_ANSWERS_FOR_TEMPLATE, ({ data }) => {
                this.answers = data["Answers"];
            });
        }
    },

    created: function(){
        this.$set(this.sharedProps, "project", this.project);
        this.$set(this.sharedProps, "answers", this.answers);

        new DuctsLoader().initDuct("guest").then( ({ loader, duct }) => {
            this.duct = duct;

            this.srvStatusProfile = {
                connected: {
                    btn: {
                        color: "success",
                        label: "Connected to server",
                        menu: [ { title: "Disconnect", handler: () => { loader.closeDuct(); } } ]
                    }
                },
                connecting: {
                    btn: {
                        color: "warning",
                        label: "Connecting to server..."
                    }
                },
                disconnected: {
                    btn: {
                        color: "error",
                        label: "No connection to server",
                        menu: [ { title: "Connect", handler: () => { loader.openDuct(); } } ]
                    }
                }
            }

            duct.addOnOpenHandler(() => {
                console.log("onopen");
                this.srvStatus = "connected"
                this.lastPinged = dateFormat(new Date(), "HH:MM:ss")

                this.setEventHandlers();
                this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.LIST_PROJECTS });
            });
            duct._connection_listener.on(["onclose", "onerror"], () => { this.srvStatus = "disconnected"; } );

            loader.openDuct();
        });
    }
}
</script>
