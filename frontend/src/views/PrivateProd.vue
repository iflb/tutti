<template>
    <v-app>
        {{ count }}
        <component :is="template" @submit="submit" />
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
        answer: {},
        name: "/private-prod/"
    }),
    computed: {
        ...mapGetters("ductsModule", [
            "duct"
        ]),
        template() {
            console.log(this.templateName)
            try { return require(`@/projects/${this.projectName}/templates/${this.templateName}/Main.vue`).default }
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
        getNextTemplate() {
            if(this.sessionId) {
                this.duct.sendMsg({
                    tag: this.name, eid: this.duct.EVENT.NANOTASK_SESSION_MANAGER,
                    data: `GET ${this.sessionId}`
                })
            }
        },
        submit($event) {
            Object.assign(this.answer, $event);
            console.log(this.answer);
            this.getNextTemplate();
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
                        this.templateName = data["NextTemplate"].name;
                    } else {
                        alert("finished!");
                    }
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
