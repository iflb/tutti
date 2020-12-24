<template>
    <v-app>
        <div class="text-right ma-3">
        <v-menu offset-y v-if="showWorkerMenu">
            <template v-slot:activator="{ on, attrs }">
            <v-btn text color="primary" class="text-none" v-bind="attrs" v-on="on">
                Your worker ID: {{ platformWorkerId }}
            </v-btn>
            </template>
            <v-list>
                <v-list-item key="logout" @click.stop="dialogLogout = true">
                    <v-list-item-title>Logout</v-list-item-title>
                </v-list-item>
            </v-list>
        </v-menu>
        </div>
        <v-dialog v-model="dialogLogout" max-width="500" >
          <v-card>
            <v-card-title class="headline">Are you sure to logout?</v-card-title>
            <v-card-text>
              Some of your working history may not be saved.
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="grey darken-1" text @click="dialogLogout = false" > Cancel </v-btn>
              <v-btn color="indigo" text @click="dialogLogout = false; logout();" > Logout </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <div class="d-flex flex-column">
        <p class="text-h3 text-center">
            {{ projectTitle }}
        </p>
        <v-row>
            <v-col cols="12" class="text-center">
                <v-btn v-if="instruction.enabled" @click="instruction.shown=true">Show Instruction</v-btn>
            </v-col>
            <!--<v-col cols="12" height="100" class="text-center">
                {{ count }}
            </v-col>-->
        </v-row>
        <v-card flat>
            <v-overlay color="white" :opacity="0.6" absolute :value="loadingNextTemplate">
                <v-progress-circular color="grey" indeterminate size="64"></v-progress-circular>
            </v-overlay>
            <v-row>
                <v-col cols="12" height="100">
                    <v-col class="text-center">
                        <v-btn v-if="pagination" color="white" class="mx-4 pa-2" @click="getTemplate('PREV')" :disabled="!hasPrevTemplate"><v-icon>mdi-chevron-left</v-icon></v-btn>
                        <v-btn v-if="pagination" color="white" class="mx-4 pa-2" @click="getTemplate('NEXT')" :disabled="!hasNextTemplate"><v-icon>mdi-chevron-right</v-icon></v-btn>
                    </v-col>
                </v-col>
                <v-col cols="12">
                    <v-slide-x-reverse-transition hide-on-leave>
                        <component v-if="showTemplate" :is="template" :nano-props="nanoProps" :prev-answer="prevAnswer" @submit="submit" />
                    </v-slide-x-reverse-transition>
                </v-col>
            </v-row>
        </v-card>
        </div>
        <v-dialog v-model="instruction.shown" max-width="1000">
            <v-card>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn icon text @click="instruction.shown = false"><v-icon>mdi-close</v-icon></v-btn>
                </v-card-actions>
                <component :is="instructionTemplate" />
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="green darken-1" text @click="instruction.shown = false" >Close</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-app>
</template>

<script>
import store from '@/store.js'
import { mapActions, mapGetters } from 'vuex'
import { platformConfig } from './platformConfig'

export default {
    store,
    beforeRouteEnter: (to, from, next) => {
        next(vm => {
            var platformWorkerId = platformConfig.workerId(vm);
            if(platformWorkerId) {
                vm.platformWorkerId = platformWorkerId;
                next();
            } else {
                platformConfig.onWorkerIdNotFound(next, vm.projectName);
            }
        });
    },
    data: () => ({
        projectTitle: "",
        showTemplate: true,
        loadingNextTemplate: false,
        templateName: "",
        count: 0,
        wsid: null,
        nanotaskId: null,
        nsid: "",
        answer: {},
        name: "/private-prod/",
        nanoProps: null,
        workerId: "",
        platformWorkerId: "",
        dialogLogout: false,
        prevAnswer: null,
        pagination: false,
        instruction: {
            enabled: false,
            shown: false
        },

        hasPrevTemplate: false,
        hasNextTemplate: false,
    }),
    computed: {
        ...mapGetters("ductsModule", [
            "duct"
        ]),
        template() {
            try { return require(`@/projects/${this.projectName}/templates/${this.templateName}/Main.vue`).default }
            catch { return null }
        },
        showWorkerMenu() {
            return platformConfig && platformConfig.showWorkerMenu;
        },
        instructionTemplate() {
            console.log(`@/projects/${this.projectName}/templates/Instruction.vue`);
            try { return require(`@/projects/${this.projectName}/templates/Instruction.vue`).default }
            catch { return null }
        }
    },
    props: ["projectName"],
    methods: {
        ...mapActions("ductsModule", [
            "initDuct",
            "openDuct",
            "closeDuct"
        ]),
        getTemplate(direction) {
            if(this.wsid) {
                this.loadingNextTemplate = true;
                this._evtSession({
                    "Command": "Get",
                    "Target": direction,
                    "WorkSessionId": this.wsid,
                    "NodeSessionId": this.nsid
                });
            }
        },
        submit($event) {
            Object.assign(this.answer, $event);
            this._evtSession({
                "Command": "SetAnswer",
                "WorkSessionId": this.wsid,
                "NodeSessionId": this.nsid,
                "Answer": this.answer
            });
        },
        logout() {
            localStorage.removeItem("workerId");
            window.location.href = `../private-prod-login?project=${this.projectName}`;
        },
        
        loadClientToken() {
            return new Promise((resolve, reject) => {
                this.clientToken = platformConfig.clientToken(this);
                if(this.clientToken) resolve();
                else reject();
            });
        },
        _evtSession(data) {
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.SESSION,
                data: data
            });
        }
    },
    created: function(){
        this.loadClientToken().then(() => {
            console.log("clientToken:", this.clientToken);

            this.initDuct( window.ducts = window.ducts || {}).then(() => {
                this.duct.setEventHandler(this.duct.EVENT.SESSION, (rid, eid, data) => {
                    console.log(data);
                    const command = data["Data"]["Command"];
                    if(command=="Create"){
                        if(data["Status"]=="Error") { console.error(`failed to create session ID: ${data["Reason"]}`); return; }

                        console.log(data["Data"]);
                        this.wsid = data["Data"]["WorkSessionId"];
                        this.workerId = data["Data"]["WorkerId"];
                        this.pagination = data["Data"]["Pagination"];
                        this.projectTitle = ("Title" in data["Data"]) ? data["Data"]["Title"] : "";
                        this.instruction.enabled = data["Data"]["InstructionEnabled"];
                        this.getTemplate("NEXT");
                    }
                    else if(command=="Get"){
                        if(data["Status"]=="Error") { console.error(`failed to get from state machine: ${data["Reason"]}`); return; }

                        const d = data["Data"];
                        this.hasPrevTemplate = d["HasPrevTemplate"];
                        this.hasNextTemplate = d["HasNextTemplate"];
                        if(d["Template"]){
                            this.count += 1;
                            this.showTemplate = false;
                            this.$nextTick(() => {
                                this.showTemplate = true;
                                this.templateName = d["Template"];
                                this.nsid = d["NodeSessionId"];
                                if(d["IsStatic"]) {
                                    console.log("loading static task");
                                    this.$set(this, "nanoProps", null);
                                    this.nanotaskId = null;
                                }
                                else {
                                    this.$set(this, "nanoProps", d["Props"]);
                                    this.nanotaskId = d["NanotaskId"];
                                }
                                
                                if("Answers" in d) {
                                    this.$set(this, "prevAnswer", d["Answers"]);
                                }
                            });
                            this.loadingNextTemplate = false;
                        } else {
                            alert(d["TerminateReason"]);
                            platformConfig.onSubmitWorkSession(this);
                        }
                    }
                    else if(command=="SetAnswer"){
                        if(data["Status"]=="Error") { console.error(`failed to send answer: ${data["Reason"]}`); return; }

                        this.answer = {}
                        this.getTemplate("NEXT");
                    }
                });

                this.openDuct().then(() => {
                    this._evtSession({
                        "Command": "Create",
                        "ProjectName": this.projectName,
                        "PlatformWorkerId": this.platformWorkerId,
                        "ClientToken": this.clientToken,
                        "Platform": platformConfig.platformName
                    });
                })
            })

        }).catch(platformConfig.onClientTokenFailure);
    }
}
</script>
