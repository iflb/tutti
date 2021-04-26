<template>
    <v-app>
        <div class="text-right ma-6" v-if="!prjConfig.Anonymous">
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
            <v-col v-if="prjConfig.ShowTitle" cols="12" class="text-center text-h3 my-3">
                {{ prjConfig.Title }}
            </v-col>
            <v-col cols="12" class="text-center">
                <v-btn v-if="prjConfig.InstructionBtn" @click="$refs.dialogInstruction.shown=true">Show Instruction</v-btn>
            </v-col>
        </v-row>
        <v-card flat>
            <v-overlay color="white" :opacity="0.6" absolute :value="loadingNextTemplate">
                <v-progress-circular color="grey" indeterminate size="64"></v-progress-circular>
            </v-overlay>
            <v-row>
                <v-col cols="12" height="100" class="pt-8" v-if="prjConfig.PageNavigation">
                    <v-col class="text-center">
                        <v-btn color="white" class="mx-4 pa-2" @click="getTemplate('PREV')" :disabled="!hasPrevTemplate"><v-icon>mdi-chevron-left</v-icon></v-btn>
                        <v-btn color="white" class="mx-4 pa-2" @click="getTemplate('NEXT')" :disabled="!hasNextTemplate"><v-icon>mdi-chevron-right</v-icon></v-btn>
                    </v-col>
                </v-col>
                <v-col cols="12" class="px-8">
                    <v-slide-x-reverse-transition hide-on-leave>
                        <component v-if="showTemplate" :is="template" :nano-props="nanoProps" :prev-answer="prevAnswer" @submit="submit" />
                        <div v-if="!showTemplate && showPreviewTemplate">
                            <v-btn v-if="prjConfig.Anonymous" color="indigo" @click="anonymousLogin();">Start Task</v-btn>
                            <component :is="previewTemplate" />
                        </div>
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

        <tutti-dialog ref="dialogSessionError" maxWidth="500"
            :actions="[
                { label: 'OK', color: 'grey darken-1', text: true }
            ]">
            <template v-slot:title>
                <v-icon color="warning" class="mr-2">mdi-alert</v-icon> Please do one HIT at a time
            </template>
            <template v-slot:body>
                Multiple concurrent sessions are not allowed for this HIT. Please finish the other HIT first.<br>
                If you believe this is caused in error, please try again later or contact <a href="mailto:mturk04@pcl.cs.waseda.ac.jp">mturk04@pcl.cs.waseda.ac.jp</a>.
            </template>
        </tutti-dialog>
                
        <tutti-dialog ref="dialogCompleted" maxWidth="500"
            :actions="[
                { label: 'OK', color: 'indigo darken-w', onclick: _onSubmitWorkSession, dark: true }
            ]">
            <template v-slot:title>
                <v-icon color="success" class="mr-2">mdi-check-circle</v-icon> Task Completed!
            </template>
            <template v-slot:body>
                You finished all of our questions. Thank you for your contribution!
            </template>
        </tutti-dialog>

    </v-app>
</template>

<script>
import tutti from '@iflb/tutti'
import { platformConfig } from './platformConfig'

export default {
    components: {
        TuttiDialog: () => import('@/views/assets/Dialog')
    },
    data: () => ({
        prjConfig: {},

        showTemplate: false,
        showPreviewTemplate: false,
        loadingNextTemplate: false,
        templateName: "",
        wsid: null,
        nsid: "",
        answer: {},
        nanoProps: null,
        workerId: "",
        platformWorkerId: "",
        prevAnswer: null,

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
                this.duct.controllers.resource.getTemplateNode(direction, this.wsid, this.nsid);
            }
        },
        submit($event) {
            Object.assign(this.answer, $event);
            this.duct.controllers.resource.setResponse(this.wsid, this.nsid, this.answer);
        },
        logout() {
            localStorage.removeItem("tuttiPlatformWorkerId");
            this.platformWorkerId = "";
            window.location.reload();
        },
        
        loadClientToken() {
            return new Promise((resolve, reject) => {
                this.clientToken = platformConfig.clientToken(this);
                if(this.clientToken) resolve();
                else reject();
            });
        },
        _onSubmitWorkSession() {
            platformConfig.onSubmitWorkSession(this);
        },
       
        anonymousLogin() {
            localStorage.setItem("tuttiPlatformWorkerId", "__ANONYMOUS__"+this.getDuctSSID());
            window.location.reload();
        },
        getDuctSSID() {
            let splitUrl = this.duct.WSD.websocket_url.split("/");
            return splitUrl[splitUrl.length-1].split(".")[0];
        }
    },
    created: function(){
        this.loadClientToken().then(() => {
            this.duct = new tutti.Duct();
            this.duct.logger = new tutti.DuctEventLogger(this.duct);

            this.duct.addOnOpenHandler(() => {
                this.duct.eventListeners.resource.on("getProjectScheme", {
                    success: (data) => {
                        console.log(data["Config"]);
                        this.prjConfig = data["Config"];

                        this.platformWorkerId = platformConfig.workerId(this);
                        if(this.platformWorkerId) {
                            this.duct.controllers.resource.checkPlatformWorkerIdExistenceForProject(this.projectName, platformConfig.platformName, this.platformWorkerId);
                            this.duct.controllers.resource.createSession(this.projectName, this.platformWorkerId, this.clientToken, platformConfig.platformName);
                        } else if(this.prjConfig.Preview) {
                            this.showPreviewTemplate = true;
                            this.$refs.dialogInstruction.shown = this.prjConfig.PushInstruction;
                        } else {
                            this.anonymousLogin();
                        }
                    },
                    error: (data) => {
                        alert("Error occured; please kindly report this to us!" + data["Reason"]);
                    }
                });
                this.duct.eventListeners.resource.on("checkPlatformWorkerIdExistenceForProject", {
                    success: (data) => {
                        console.log("checkPlatformWorkerIdExistenceForProject");
                        if(!data["Exists"]) this.$refs.dialogInstruction.shown = this.prjConfig.PushInstruction;
                    },
                    error: (data) => {
                        console.error(data["Reason"]);
                    }
                });
                this.duct.eventListeners.resource.on("createSession", {
                    success: (data) => {
                        console.log("createSession");
                        if(data.SessionError){
                            console.log("sessionError");
                            this.$refs.dialogSessionError.shown = true;
                        } else {
                            this.wsid = data["WorkSessionId"];
                            this.workerId = data["WorkerId"];
                            this.getTemplate("NEXT");
                        }
                    },
                    error: (data) => {
                        console.log("createSession error", data);
                    }
                });
                this.duct.eventListeners.resource.on("getTemplateNode", {
                    success: (data) => {
                        console.log("getTemplateNode", data);
                        this.hasPrevTemplate = data["HasPrevTemplate"];
                        this.hasNextTemplate = data["HasNextTemplate"];
                        if(data["Template"]){
                            this.showTemplate = false;
                            this.$nextTick(() => {
                                this.showTemplate = true;
                                this.templateName = data["Template"];
                                this.nsid = data["NodeSessionId"];
                                if(data["IsStatic"]) {
                                    this.$set(this, "nanoProps", null);
                                }
                                else {
                                    this.$set(this, "nanoProps", data["Props"]);
                                }
                                
                                if("Answers" in data) {
                                    this.$set(this, "prevAnswer", data["Answers"]);
                                }
                            });
                        } else if(data["WorkSessionStatus"]=="Terminated") {
                            if(this.templateName=="")  this.$refs.dialogAdviseReturn.shown = true;
                            else if(data["TerminateReason"]=="UnskippableNode")  this.$refs.dialogUnskippableNode.shown = true;
                            else if(data["TerminateReason"]=="SessionEnd") {
                                if(this.prjConfig.CompletionAlert){
                                    console.log("session end..");
                                    this.$refs.dialogCompleted.show();
                                }
                                else  this._onSubmitWorkSession(this);
                            }
                            else  this._onSubmitWorkSession(this);
                        }
                        this.loadingNextTemplate = false;
                    },
                    error: (data) => {
                        console.error(data["Reason"]);
                    }
                });
                this.duct.eventListeners.resource.on("setResponse", {
                    success: () => {
                        this.answer = {}
                        this.getTemplate("NEXT");
                    },
                    error: (data) => {
                        console.error(data["Reason"]);
                    }
                });

                this.duct.controllers.resource.getProjectScheme(this.projectName);
            });

            this.duct.open("/ducts/wsd");

        });
    }
}
</script>
