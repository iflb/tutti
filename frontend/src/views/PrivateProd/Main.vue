<template>
    <v-app>
        <div class="text-right ma-6">
            <v-menu offset-y v-if="showWorkerMenu && platformWorkerId">
                <template v-slot:activator="{ on, attrs }">
                    <v-btn text color="indigo" class="text-none" v-bind="attrs" v-on="on">
                        Worker ID: {{ platformWorkerId }}
                    </v-btn>
                </template>
                <v-list>
                    <v-list-item key="logout" @click="$refs.dialogLogout.shown=true">
                        <v-list-item-title>Log out</v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>
            <v-btn v-if="showWorkerMenu && !platformWorkerId" dark color="indigo" :href="`../private-prod-login?project=${projectName}`">
                Log in
            </v-btn>
        </div>

        <div class="d-flex flex-column">
        <v-row>
            <v-col v-if="showTitle" cols="12" class="text-center text-h3 my-3">
                {{ projectTitle }}
            </v-col>
            <v-col cols="12" class="text-center">
                <v-btn v-if="instruction.enabled" @click="$refs.dialogInstruction.shown=true">Show Instruction</v-btn>
            </v-col>
        </v-row>
        <v-card flat>
            <v-overlay color="white" :opacity="0.6" absolute :value="loadingNextTemplate">
                <v-progress-circular color="grey" indeterminate size="64"></v-progress-circular>
            </v-overlay>
            <v-row>
                <v-col cols="12" height="100" class="pt-8" v-if="pagination">
                    <v-col class="text-center">
                        <v-btn color="white" class="mx-4 pa-2" @click="getTemplate('PREV')" :disabled="!hasPrevTemplate"><v-icon>mdi-chevron-left</v-icon></v-btn>
                        <v-btn color="white" class="mx-4 pa-2" @click="getTemplate('NEXT')" :disabled="!hasNextTemplate"><v-icon>mdi-chevron-right</v-icon></v-btn>
                    </v-col>
                </v-col>
                <v-col cols="12" class="px-8">
                    <v-slide-x-reverse-transition hide-on-leave>
                        <component v-if="showTemplate" :is="template" :nano-props="nanoProps" :prev-answer="prevAnswer" @submit="submit" />
                        <component v-else-if="showPreviewTemplate" :is="previewTemplate" />
                    </v-slide-x-reverse-transition>
                </v-col>
            </v-row>
        </v-card>
        </div>

        <tutti-dialog ref="dialogInstruction" maxWidth="1000"
            :actions="[
                { label: 'Close', color: 'green darken-1', text: true }
            ]">
            <template v-slot:body-raw>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn icon text @click="$refs.dialogInstruction.shown=false"><v-icon>mdi-close</v-icon></v-btn>
                </v-card-actions>
                <component :is="instructionTemplate" />
            </template>
        </tutti-dialog>

        <tutti-dialog ref="dialogLogout" title="Are you sure to log out?" maxWidth="500"
            :actions="[
                { label: 'Logout', color: 'indigo darken-1', text: true, onclick: logout },
                { label: 'Cancel', color: 'grey darken-1', text: true }
            ]">
            <template v-slot:body>
                Some of your working history may not be saved.
            </template>
        </tutti-dialog>
                
        <tutti-dialog ref="dialogAdviseReturn" maxWidth="800"
            :actions="[
                { label: 'OK', color: 'grey darken-1', text: true }
            ]">
            <template v-slot:title>
                <v-icon color="warning" class="mr-2">mdi-alert</v-icon> No more task is currently available
            </template>
            <template v-slot:body>
                Thank you for your interest in this HIT! We are sorry but there is no more task available for you on this HIT for now.<br>
                Please return this HIT (nothing else will happen while this page is open).
            </template>
        </tutti-dialog>

        <tutti-dialog ref="dialogUnskippableNode" maxWidth="800"
            :actions="[
                { label: 'OK', color: 'success', dark: true, onclick: _onSubmitWorkSession }
            ]">
            <template v-slot:title>
                <v-icon color="success" class="mr-2">mdi-check-circle</v-icon> You reached the end of this HIT
            </template>
            <template v-slot:body>
                You reached the end of this task now; it might have been earlier than expected, but don't worry, you will still earn the same amount of reward.<br>
                This HIT will be automatically submitted as you close this dialog.
            </template>
        </tutti-dialog>
    </v-app>
</template>

<script>
import { DuctsLoader } from '@/lib/ducts-loader'
import { platformConfig } from './platformConfig'
import Dialog from '@/views/assets/Dialog.vue'

export default {
    components: {
        TuttiDialog: Dialog
    },
    data: () => ({
        projectTitle: "",
        showTemplate: false,
        showPreviewTemplate: false,
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
        prevAnswer: null,
        pagination: false,
        instruction: {
            enabled: false,
            shown: false
        },
        showTitle: false,

        hasPrevTemplate: false,
        hasNextTemplate: false,
    }),
    computed: {
        template() {
            try { return require(`@/projects/${this.projectName}/templates/${this.templateName}/Main.vue`).default }
            catch { return null }
        },
        previewTemplate() {
            try { return require(`@/projects/${this.projectName}/templates/Preview.vue`).default }
            catch { return null }
        },
        showWorkerMenu() {
            return platformConfig && platformConfig.showWorkerMenu;
        },
        instructionTemplate() {
            try { return require(`@/projects/${this.projectName}/templates/Instruction.vue`).default }
            catch { return null }
        }
    },
    props: ["projectName"],
    methods: {
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
            this.platformWorkerId = "";
            window.location.reload();
            //window.location.href = `../private-prod-login?project=${this.projectName}`;
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
        },
        _onSubmitWorkSession() {
            platformConfig.onSubmitWorkSession(this);
        }
    },
    created: function(){
        this.loadClientToken().then(() => {
            console.log("clientToken:", this.clientToken);

            new DuctsLoader().initDuct("guest").then( ({ loader, duct }) => {
                this.duct = duct;

                duct.addOnOpenHandler(() => {
                    this.duct.setTuttiEventHandler(this.duct.EVENT.GET_PROJECT_SCHEME,
                        ({ data }) => {
                            console.log(data);
                            const config = data["Config"];
                            this.pagination = config["Pagination"];
                            this.projectTitle = config["Title"] || "";
                            this.instruction.enabled = config["Instruction"];
                            this.showTitle = config["ShowTitle"];

                            this.platformWorkerId = platformConfig.workerId(this);
                            if(!this.platformWorkerId) {
                                this.showPreviewTemplate = true;
                                this.$refs.dialogInstruction.shown = true;
                                return;
                            } else {
                                this.duct.sendMsg({
                                    tag: this.name,
                                    eid: this.duct.EVENT.CHECK_PLATFORM_WORKER_ID_EXISTENCE_FOR_PROJECT,
                                    data: { ProjectName: this.projectName, Platform: platformConfig.platformName, PlatformWorkerId: this.platformWorkerId }
                                });
                                this._evtSession({
                                    "Command": "Create",
                                    "ProjectName": this.projectName,
                                    "PlatformWorkerId": this.platformWorkerId,
                                    "ClientToken": this.clientToken,
                                    "Platform": platformConfig.platformName
                                });
                            }
                        },
                        ({ reason }) => {
                            alert("Error occured; please kindly report this to us!" + reason);
                        }
                    );
                    this.duct.setTuttiEventHandler(this.duct.EVENT.CHECK_PLATFORM_WORKER_ID_EXISTENCE_FOR_PROJECT,
                        ({ data }) => {
                            if(!data["Exists"]) this.$refs.dialogInstruction.shown=true;
                        },
                        ({ reason }) => {
                            console.error(reason);
                        }
                    );
                    this.duct.setTuttiEventHandler(this.duct.EVENT.SESSION,
                        ({ data }) => {
                            const command = data["Command"];
                            if(command=="Create"){
                                //if(data["Status"]=="Error") { console.error(`failed to create session ID: ${data["Reason"]}`); return; }

                                this.wsid = data["WorkSessionId"];
                                this.workerId = data["WorkerId"];
                                //this.pagination = data["Pagination"];
                                //this.projectTitle = data["Title"] || "";
                                //this.instruction.enabled = data["InstructionEnabled"];
                                this.getTemplate("NEXT");
                            }
                            else if(command=="Get"){
                                //if(data["Status"]=="Error") { console.error(`failed to get from state machine: ${data["Reason"]}`); return; }
                                this.hasPrevTemplate = data["HasPrevTemplate"];
                                this.hasNextTemplate = data["HasNextTemplate"];
                                if(data["Template"]){
                                    this.count += 1;
                                    this.showTemplate = false;
                                    this.$nextTick(() => {
                                        this.showTemplate = true;
                                        this.templateName = data["Template"];
                                        this.nsid = data["NodeSessionId"];
                                        if(data["IsStatic"]) {
                                            console.log("loading static task");
                                            this.$set(this, "nanoProps", null);
                                            this.nanotaskId = null;
                                        }
                                        else {
                                            this.$set(this, "nanoProps", data["Props"]);
                                            this.nanotaskId = data["NanotaskId"];
                                        }
                                        
                                        if("Answers" in data) {
                                            this.$set(this, "prevAnswer", data["Answers"]);
                                        }
                                    });
                                } else if(data["WorkSessionStatus"]=="Terminated") {
                                    if(this.templateName=="")  this.$refs.dialogAdviseReturn.shown = true;
                                    else if(data["TerminateReason"]=="UnskippableNode")  this.$refs.dialogUnskippableNode.shown = true;
                                    else if(data["TerminateReason"]=="SessionEnd")  this._onSubmitWorkSession(this);
                                    else  this._onSubmitWorkSession(this);
                                    //else  this.$refs.unexpectedTermination.shown = true;
                                }
                                this.loadingNextTemplate = false;
                            }
                            else if(command=="SetAnswer"){
                                //if(data["Status"]=="Error") { console.error(`failed to send answer: ${data["Reason"]}`); return; }

                                this.answer = {}
                                this.getTemplate("NEXT");
                            }
                        },
                        ({ reason }) => {
                            console.error(reason);
                        }
                    );
                });

                loader.openDuct().then(() => {
                    this.duct.sendMsg({
                        tag: this.name,
                        eid: this.duct.EVENT.GET_PROJECT_SCHEME,
                        data: { "ProjectName": this.projectName }
                    });
                });
            })

        }).catch(platformConfig.onClientTokenFailure);
    }
}
</script>
