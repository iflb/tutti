<template>
    <v-app>
        <div class="text-right ma-3">
        <v-menu offset-y>
            <template v-slot:activator="{ on, attrs }">
            <v-btn text color="primary" class="text-none" v-bind="attrs" v-on="on">
                Your worker ID: {{ workerId }}
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
        <v-row>
            {{ count }}
            <v-col class="text-center">
                <v-btn color="white" class="mx-4 pa-2" @click="getTemplate('PREV')" :disabled="!hasPrevTemplate"><v-icon>mdi-chevron-left</v-icon></v-btn>
                <v-btn color="white" class="mx-4 pa-2" @click="getTemplate('NEXT')" :disabled="!hasNextTemplate"><v-icon>mdi-chevron-right</v-icon></v-btn>
            </v-col>
        </v-row>
        <v-row>
            <v-slide-x-reverse-transition hide-on-leave>
                <component :is="template" :nano-data="nanoPropData" :prev-answer="prevAnswer" @submit="submit" />
            </v-slide-x-reverse-transition>
        </v-row>
    </v-app>
</template>

<script>
import store from '@/store.js'
import { mapActions, mapGetters } from 'vuex'

export default {
    store,
    beforeRouteEnter: (to,from,next) => {
        var workerId = localStorage.getItem("workerId");
        next(vm => {
            if(!workerId) next({ path: `/private-prod-login?project=${vm.projectName}` })
            else {
                vm.workerId = workerId;
                next();
            }
        });
    },
    data: () => ({
        templateName: "",
        count: 0,
        wsid: null,
        nanotaskId: null,
        nsid: "",
        answer: {},
        name: "/private-prod/",
        nanoData: null,
        workerId: "",
        dialogLogout: false,
        prevAnswer: null,

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
        nanoPropData() {
            return this.nanoData;
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
                this.duct.sendMsg({
                    tag: this.name, eid: this.duct.EVENT.NANOTASK_SESSION_MANAGER,
                    data: `GET ${direction} ${this.wsid} ${this.nsid}`
                })
            }
        },
        submit($event) {
            Object.assign(this.answer, $event);
            //console.log(this.answer);
            this.duct.sendMsg({
                tag: this.name, eid: this.duct.EVENT.NANOTASK_SESSION_MANAGER,
                data: `ANSWER ${this.wsid} ${this.nsid} ${JSON.stringify(this.answer)}`
            })
        },
        logout() {
            localStorage.removeItem("workerId");
            window.location.href = `../private-prod-login?project=${this.projectName}`;
        },
        


        getClientToken() {
            function someRandomStringGenerator(){
                return Math.random().toString(32).substring(2)
            }
            var token = sessionStorage.getItem("someClientToken");
            if(!token) {
                token = someRandomStringGenerator();
                sessionStorage.setItem("someClientToken", token);
            }
            console.log("token:", token);

            return token;
        },
        onClientTokenFailure() {
            console.log("clienttokenFailure");
        },
        loadClientToken() {
            return new Promise((resolve, reject) => {
                this.clientToken = this.getClientToken();
                if(this.clientToken) resolve();
                else reject();
            });
        }
    },
    created: function(){
        this.loadClientToken().then(() => {

            this.initDuct( window.ducts = window.ducts || {}).then(() => {
                this.duct.setEventHandler(this.duct.EVENT.NANOTASK_SESSION_MANAGER, (rid, eid, data) => {
                    if(data["Command"]=="CREATE_SESSION"){
                        if(data["Status"]=="error") { console.error(`failed to create session ID: ${data["Reason"]}`); return; }

                        console.log(`created work-session: ${data["WorkSessionId"]}`);
                        this.wsid = data["WorkSessionId"];
                        this.getTemplate("NEXT");
                    }
                    else if(data["Command"]=="GET"){
                        if(data["Status"]=="error") { console.error(`failed to get from state machine: ${data["Reason"]}`); return; }

                        this.hasPrevTemplate = data["HasPrevTemplate"];
                        this.hasNextTemplate = data["HasNextTemplate"];
                        if(data["Template"]){
                            this.count += 1;
                            this.templateName = data["Template"];
                            this.nsid = data["NodeSessionId"];
                            if(data["IsStatic"]) {
                                console.log("loading static task");
                                this.nanoData = null;
                                this.nanotaskId = null;
                            }
                            else {
                                this.nanoData = data["Props"];
                                this.nanotaskId = data["NanotaskId"];
                            }
                            
                            if("Answers" in data) {
                                this.$set(this, "prevAnswer", data["Answers"]);
                                console.log(this.prevAnswer);
                            }
                        } else {
                            alert("finished!");
                        }
                    }
                    else if(data["Command"]=="ANSWER"){
                        if(data["Status"]=="error") { console.error(`failed to send answer: ${data["Reason"]}`); return; }

                        console.log(`successfully sent answer: ${data["SentAnswer"]}`);
                        this.answer = {}
                        this.getTemplate("NEXT");
                    }
                })

                this.openDuct().then(() => {
                    this.duct.sendMsg({
                        tag: this.name, eid: this.duct.EVENT.NANOTASK_SESSION_MANAGER,
                        data: `CREATE_SESSION ${this.projectName} ${this.workerId} ${this.clientToken}`
                    })
                })
            })

        }).catch(this.onClientTokenFailure);
    }
}
</script>
