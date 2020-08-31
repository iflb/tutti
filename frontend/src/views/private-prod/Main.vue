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
        <v-slide-x-reverse-transition hide-on-leave>
            <component :is="template" :nano-data="nanoPropData" @submit="submit" />
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
        const cookieKey = "workerId";
        var workerId = null;
        document.cookie.split("; ").some((q) => {
            const [key,val] = q.split("=");
            if(key==cookieKey) { workerId = val; return true; }
        });
        if(!workerId) next({ path: "/private-prod-login" })
        else next(vm => {
            vm.workerId = workerId;
        });
    },
    data: () => ({
        templateName: "",
        count: 0,
        sessionId: null,
        nanotaskId: null,
        answer: {},
        name: "/private-prod/",
        nanoData: null,
        workerId: "",
        dialogLogout: false
    }),
    computed: {
        ...mapGetters("ductsModule", [
            "duct"
        ]),
        template() {
            console.log(this.templateName)
            try { return require(`@/projects/${this.projectName}/templates/${this.templateName}/Main.vue`).default }
            catch { return null }
        },
        nanoPropData() {
            console.log("nanoPropData", this.nanoData);
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
        getNextTemplate() {
            if(this.sessionId) {
                this.duct.sendMsg({
                    tag: this.name, eid: this.duct.EVENT.NANOTASK_SESSION_MANAGER,
                    data: `GET ${this.projectName} ${this.sessionId}`
                })
            }
        },
        submit($event) {
            Object.assign(this.answer, $event);
            console.log(this.answer);
            this.duct.sendMsg({
                tag: this.name, eid: this.duct.EVENT.NANOTASK_SESSION_MANAGER,
                data: `ANSWER ${this.sessionId} ${this.projectName} ${this.templateName} ${this.nanotaskId} ${JSON.stringify(this.answer)}`
            })
        },
        logout() {
            document.cookie = "workerId=; max-age=0; Path=/";
            window.location.href = `../private-prod-login?project=${this.projectName}`;
        }
    },
    created: function(){
        this.initDuct( window.ducts = window.ducts || {}).then(() => {
            this.duct.setEventHandler(this.duct.EVENT.NANOTASK_SESSION_MANAGER, (rid, eid, data) => {
                if(data["Command"]=="CREATE_SESSION"){
                    if(data["Status"]=="error") { console.error(`failed to create session ID: ${data["Reason"]}`); return; }

                    console.log(`created session: ${data["SessionId"]}`);
                    this.sessionId = data["SessionId"];
                    this.getNextTemplate();
                }
                else if(data["Command"]=="GET"){
                    if(data["Status"]=="error") { console.error(`failed to get from state machine: ${data["Reason"]}`); return; }

                    if(data["NextTemplate"]){
                        this.count += 1;
                        this.templateName = data["NextTemplate"];
                        this.nanoData = data["Props"];
                        this.nanotaskId = data["NanotaskId"];
                        console.log(this.templateName, this.nanoData, this.nanotaskId);
                    } else {
                        alert("finished!");
                    }
                }
                else if(data["Command"]=="ANSWER"){
                    if(data["Status"]=="error") { console.error(`failed to send answer: ${data["Reason"]}`); return; }

                    console.log(`successfully sent answer: ${data["SentAnswer"]}`);
                    this.answer = {}
                    this.getNextTemplate();
                }
            })

            this.openDuct().then(() => {
                this.duct.sendMsg({
                    tag: this.name, eid: this.duct.EVENT.NANOTASK_SESSION_MANAGER,
                    data: `CREATE_SESSION ${this.projectName}`
                })
            })
        })
    }
}
</script>
