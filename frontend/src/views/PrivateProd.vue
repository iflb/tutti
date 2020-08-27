<template>
    <v-app>
        {{ count }}
        <component :is="template" :nano-data="nanoPropData" @submit="submit" />
    </v-app>
</template>

<script>
import store from '@/store.js'
import { mapActions, mapGetters } from 'vuex'

export default {
    store,
    data: () => ({
        templateName: "",
        count: 0,
        sessionId: null,
        nanotaskId: null,
        answer: {},
        name: "/private-prod/",
        nanoData: null
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
