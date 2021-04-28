<template>
    <v-app>
        <v-app-bar color="indigo" dark app clipped-left clipped-right dense>
            <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
            
            <v-toolbar-title>Tutti Management Console</v-toolbar-title>

            <v-spacer></v-spacer>

            <v-autocomplete v-model="prjName" :items="prjNames" label="Select existing project" hide-details cache-items solo-inverted hide-no-data dense rounded></v-autocomplete>

            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-btn fab dark small icon v-on="on" v-bind="attrs" @click="$refs.dialogCreateProject.show()"><v-icon>mdi-plus</v-icon></v-btn>
                </template>
                <span>Create new project...</span>
            </v-tooltip>

            <v-spacer></v-spacer>

            <v-menu offset-y v-if="srvStatusProfile">
                <template v-slot:activator="{ on, attrs }">
                    <v-btn depressed :color="srvStatusProfile[srvStatus].btn.color" class="text-none" v-bind="attrs" v-on="on">
                        {{ srvStatusProfile[srvStatus].btn.label }}
                        <span v-if="srvStatus == 'connected'" class="text-caption ml-2">(last pinged: {{ lastPinged }})</span>
                        <span v-else-if="srvStatus == 'disconnected'" class="text-caption ml-2">(Auto-retry remaining: {{ retry.maxCnt-retry.cnt }})</span>
                    </v-btn>
                </template>
                <v-list>
                    <v-list-item v-for="(menu, index) in srvStatusProfile[srvStatus].btn.menu" :key="index" @click="menu.handler()">
                        <v-list-item-title>{{ menu.title }}</v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>
            <v-btn icon :plain="!eventNav" @click="eventNav = !eventNav"><v-icon :color="eventNav ? 'yellow darken-2' : ''">mdi-lightning-bolt</v-icon></v-btn>
        </v-app-bar>


        <v-navigation-drawer v-model="drawer" app clipped left>
            <v-list nav dense>
                <v-list-item-group active-class="indigo--text text--accent-4">

                    <v-list-item to="/console/dashboard/">
                        <v-list-item-icon> <v-icon>mdi-view-dashboard</v-icon> </v-list-item-icon>
                        <v-list-item-title>Dashboard</v-list-item-title>
                    </v-list-item>

                </v-list-item-group>

                <v-list-item-group active-class="indigo--text text--accent-4">
                    <v-subheader>DESIGN & TEST</v-subheader>

                    <v-list-item to="/console/template/">
                        <v-list-item-icon> <v-icon>mdi-iframe-outline</v-icon> </v-list-item-icon>
                        <v-list-item-title>Templates</v-list-item-title>
                    </v-list-item>
               
                    <v-list-item to="/console/flow/">
                        <v-list-item-icon> <v-icon>mdi-wrench</v-icon> </v-list-item-icon>
                        <v-list-item-title>Scheme</v-list-item-title>
                    </v-list-item>

                </v-list-item-group>

                <v-list-item-group active-class="indigo--text text--accent-4">
                    <v-subheader>PUBLISH & COLLECT</v-subheader>
 
                    <v-list-item to="/console/response/">
                        <v-list-item-icon> <v-icon>mdi-comment-check-outline</v-icon> </v-list-item-icon>
                        <v-list-item-title>Responses</v-list-item-title>
                    </v-list-item>

                    <v-list-group prepend-icon="mdi-account-group" :value="false">
                        <template v-slot:activator> <v-list-item-title>Worker Platforms</v-list-item-title> </template>

                        <v-list-item class="pl-6" to="/console/platform/mturk/">
                            <v-list-item-icon> <v-icon>mdi-amazon</v-icon> </v-list-item-icon>
                            <v-list-item-title>Amazon MTurk</v-list-item-title>
                        </v-list-item>

                        <v-list-item class="pl-6" to="/console/platform/private/">
                            <v-list-item-icon> <v-icon>mdi-account-supervisor-circle</v-icon> </v-list-item-icon>
                            <v-list-item-title>Partner-Sourcing</v-list-item-title>
                        </v-list-item>

                    </v-list-group>

                </v-list-item-group>

                <v-list-item-group active-class="indigo--text text--accent-4">
                    <v-subheader>OTHERS</v-subheader>

                    <v-list-item to="/console/event/">
                        <v-list-item-icon> <v-icon>mdi-lightning-bolt</v-icon> </v-list-item-icon>
                        <v-list-item-title>Duct Events</v-list-item-title>
                    </v-list-item>

                    <v-list-item href="https://iflb.github.io/tutti/" target="_blank">
                        <v-list-item-icon> <v-icon>mdi-file-document-outline</v-icon> </v-list-item-icon>
                        <v-list-item-title>Documentation</v-list-item-title>
                        <v-list-item-action> <v-icon small>mdi-launch</v-icon> </v-list-item-action>
                    </v-list-item>

                </v-list-item-group>
            </v-list>
        </v-navigation-drawer>

        <v-navigation-drawer v-model="eventNav" app clipped right width="300px">
            <v-data-table :headers="logTableHeaders" :items="serverLogTableRows" :items-per-page="10" hide-default-footer>
                <template v-slot:item.msg="{ item }">
                    <v-icon small v-if="!item.received" color="warning">mdi-clock-outline</v-icon>
                    <v-icon small v-else-if="item.received.Status=='Success'" color="success">mdi-check-circle</v-icon>
                    <v-icon small v-else-if="item.received.Status=='Error'" color="error">mdi-alert</v-icon>
                    <b> {{ item.evtName }} ({{ item.eid }})</b>
                    <div v-if="item.received" style="width:100%;text-align:right"> {{ dateFormat(item.received.Timestamp.Requested*1000, "yyyy-mm-dd HH:MM:ss") }} </div>
                    <vue-json-pretty :data="item.sent" :deep="1"></vue-json-pretty>
                    <div style="display:flex;">
                        <div style="margin-right:5px;">
                            <v-icon x-small>mdi-arrow-right</v-icon>
                        </div>
                        <div v-if="item.received">
                            <vue-json-pretty v-if="item.received.Status=='Success'" :data="item.received.Contents" :deep="1"></vue-json-pretty>
                            <vue-json-pretty v-else :data="item.received.Reason" :deep="1"></vue-json-pretty>
                        </div>
                    </div>
                </template>
            </v-data-table>
            <v-divider></v-divider>
        </v-navigation-drawer>

        <keep-alive>
            <router-view app
                v-if="duct"
                :duct="duct"
                :prj-name="prjName"
                ref="child"
            ></router-view>
        </keep-alive>


        <tutti-dialog ref="dialogCreateProject" title="Create New Project" maxWidth="400" :allowEnter="true"
            :actions="[
                { label: 'Create', color: 'indigo darken-1', disableByRule: true, text: true, onclick: createProject },
                { label: 'Cancel', color: 'grey darken-1', text: true }
            ]" >
            <template v-slot:body>
                <v-text-field autofocus v-model="newProjectName" filled prepend-icon="mdi-pencil" label="Enter Project Name" :rules="rules.createProject"></v-text-field>
            </template>
        </tutti-dialog>

        <tutti-snackbar color="success" :timeout="5000" ref="snackbarSuccess" />
        
    </v-app>
</template>

<script>
//import tutti from '@/lib/tutti-js/lib/tutti'
import tutti from '@iflb/tutti'
import dateFormat from 'dateformat'
import rules from '@/lib/input-rules'
import 'vue-json-pretty/lib/styles.css'

export default {
    components: { 
        VueJsonPretty: () => import("vue-json-pretty/lib/vue-json-pretty"),
        TuttiSnackbar: () => import('@/views/assets/Snackbar'),
        TuttiDialog: () => import('@/views/assets/Dialog')
    },
    data: () => ({
        duct: null,
        retry: {
            enabled: true,
            cnt: 0,
            maxCnt: 5,
            interval: null
        },
        wsdPath: "/ducts/wsd",
        drawer: true,
        eventNav: true,
        logTableHeaders: [
            { text: "Message", value: "msg" },
        ],
        serverLogTableRows: [],

        lastPinged: "",
        srvStatus: "connecting",
        srvStatusProfile: null,

        prjNames: [],
        prjName: "",

        newProjectName: "",

        rules: {
            createProject: [rules.required, rules.alphanumeric]
        },
        dateFormat: dateFormat
    }),
    watch: {
        prjName (name) { if(name){ localStorage.setItem("tuttiProject", name); } },
    },
    methods: {
        createProject() { this.duct.controllers.resource.createProject(this.newProjectName); },

        setEventHandlers() {
            this.duct.eventListeners.resource.on("listProjects", {
                success: (data) => {
                    this.prjNames = data["Projects"].map((value) => (value.name));
                    this.prjName = localStorage.getItem("tuttiProject") || null;
                }
            });
            this.duct.eventListeners.resource.on("createProject", {
                success: (data) => {
                    this.$refs.snackbarSuccess.show(`Successfully created project '${data["ProjectName"]}'`);
                    this.duct.controllers.resource.listProjects();
                }
            });
        },
        initDuct() {
            this.duct = new tutti.Duct();

            this.duct.logger = new tutti.DuctEventLogger(this.duct);

            this.duct.addOnOpenHandler(() => {
                this.srvStatus = "connected"
                this.lastPinged = dateFormat(new Date(), "HH:MM:ss")


                this.setEventHandlers();
                this.duct.controllers.resource.listProjects();


                setInterval(() => {
                    var rows = [];
                    const ductLog = this.duct.logger.log;
                    for(const rid in ductLog){
                        if( ductLog[rid].eid <= 1010 )  continue;

                        rows.unshift({
                            rid,
                            eid: ductLog[rid].eid,
                            evtName: Object.keys(this.duct.EVENT).find(key => this.duct.EVENT[key] === ductLog[rid].eid),
                            sent: ductLog[rid].sent,
                            received: ductLog[rid].received[0]
                        });
                    }
                    this.serverLogTableRows = rows;
                }, 1000);

            });

            this.duct._connection_listener.on(["onclose", "onerror"], () => { this.srvStatus = "disconnected"; } );

            this.duct.open(this.wsdPath);

        },
        reconnect() {
            console.log("trying to reconnect");
            this.initDuct();
            if(this.duct){
                try {
                    this.duct.reconnect().then(() => {
                        this.retry.enabled = true;
                        this.srvStatus = "connected";
                        this.retry.cnt = 0;
                    }).catch(() => { 
                        if(++this.retry.cnt>=this.retry.maxCnt) {
                            console.error("failed reconnection 5 times");
                            clearInterval(this.retry.interval);
                            this.retry.interval = null;
                        }
                    });
                } catch (e) {
                    console.log(e);
                }
            } else {
                if(++this.retry.cnt>=this.retry.maxCnt) {
                    console.error("failed reconnection 5 times");
                    clearInterval(this.retry.interval);
                    this.retry.interval = null;
                }
            }
        },
        disconnect() {
            this.retry.enabled = false;
            this.duct.close();
        }
    },

    created: function(){
        this.initDuct();

        this.srvStatusProfile = {
            connected: {
                btn: {
                    color: "success",
                    label: "Connected to server",
                    menu: [ { title: "Disconnect", handler: this.disconnect } ]
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
                    menu: [ { title: "Connect", handler: this.reconnect } ]
                }
            }
        }

        this.retry.interval = setInterval(() => {
            if(this.srvStatus=="disconnected" && this.retry.enabled) { this.reconnect(); }
        }, 3000);
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

.vjs-tree {
    font-size: 10px;
}
</style>
