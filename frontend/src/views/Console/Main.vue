<template>
    <v-app>
        <v-app-bar color="indigo" dark app clipped-left clipped-right dense>
            <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
            
            <v-toolbar-title>Tutti Management Console</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-autocomplete v-model="prjName" :items="prjNames" :search-input.sync="searchString" label="Select existing project" hide-details cache-items solo-inverted hide-no-data dense rounded></v-autocomplete>

            <v-menu bottom left offset-y>
                <template v-slot:activator="{ on, attrs }">
                    <v-btn fab dark small icon v-on="on" v-bind="attrs"><v-icon>mdi-dots-vertical</v-icon></v-btn>
                </template>
                <v-list>
                    <v-list-item @click="$refs.dialogCreateProject.show()">
                        <v-list-item-title>Create New Project...</v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>

            <tutti-dialog ref="dialogCreateProject" title="Create New Project" maxWidth="400"
                :actions="[
                    { label: 'Create', color: 'indigo darken-1', text: true, onclick: createProject },
                    { label: 'Cancel', color: 'grey darken-1', text: true }
                ]" >
                <template v-slot:body>
                    <v-text-field autofocus v-model="newProjectName" filled prepend-icon="mdi-pencil" label="Enter Project Name" :rules="[rules.required, rules.alphanumeric]"></v-text-field>
                </template>
            </tutti-dialog>

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

        <v-navigation-drawer v-model="drawer" app clipped left>
            <v-list nav dense>
                <v-list-item-group active-class="indigo--text text--accent-4">
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
 
                    <v-list-item :href="`/vue/private-prod/${this.prjName}`" target="_blank">
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

        <transition name="fade" mode="out-in">
            <keep-alive>
                <router-view app
                    v-if="duct"
                    :duct="duct"
                    :prj-name="prjName"
                    :shared-props="sharedProps"
                    ref="child"
                ></router-view>
            </keep-alive>
        </transition>

        <tutti-snackbar color="success" :timeout="5000" :text="snackbarTexts.success" />
        
    </v-app>
</template>

<script>
import { DuctsLoader } from '@/lib/ducts-loader'
import dateFormat from 'dateformat'
import Snackbar from '@/views/assets/Snackbar.vue'
import Dialog from '@/views/assets/Dialog.vue'

var Project = class {
    constructor(name, path) {
        this.name = name;
        this.templates = {};
        this.profile = null;
        this.path = path;
    }
};

export default {
    components: { 
        TuttiSnackbar: Snackbar,
        TuttiDialog: Dialog
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

        prjNames: [],
        projects: {},
        project: new Project("", null),
        prjName: "",

        answers: {},

        sharedProps: {},

        newProjectName: "",

        rules: {
            required: value => !!value || "This field is required",
            alphanumeric: value => {
                const pattern = /^[a-zA-Z0-9_-]*$/;
                return pattern.test(value) || 'Alphabets, numbers, "_", or "-" is only allowed';
            }
        }
    }),
    watch: {
        searchString (val) {
            val && val !== this.select && this.querySelections(val)
        },
        prjName (name) {  // called when project name is selected on the app bar
            if(name){
                localStorage.setItem("tuttiProject", name);
                this.project = this.projects[name];
                this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.GET_PROJECT_SCHEME, data: { "ProjectName": name } })
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
        launchProductionMode(){ window.open(`/vue/private-prod/${this.prjName}`); },
        createProject() {
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.CREATE_PROJECT,
                data: {
                    "ProjectName": this.newProjectName
                }
            });
        },
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
                this.prjNames = data["Projects"].map((value) => (value.name));
                this.prjName = localStorage.getItem("tuttiProject") || null;
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
                this.listTemplates(this.prjName);
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
                        this.projects[ProjectName].templates[TemplateName].nanotask.data = data["Nanotasks"];
                        this.projects[ProjectName].templates[TemplateName].nanotask.cnt = cnt;
                        break;
                    }
                }
            });

            this.duct.setTuttiEventHandler(this.duct.EVENT.GET_PROJECT_SCHEME,
                ({ data }) => {
                    this.project.profile = data["Flow"]
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
        //this.$set(this.sharedProps, "answers", this.answers);

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
<style>
.fade-enter-active,
.fade-leave-active {
  transition-duration: 0.5s;
  transition-property: opacity;
  transition-timing-function: ease-in;
}

.fade-enter-active {
  transition-duration: 0.5s;
}

.fade-enter,
.fade-leave-active {
  opacity: 0
}
</style>
