<template>
    <v-main>
        <v-container justify="center">
            <v-row class="d-flex justify-center">
                <v-col>
                <v-select :items="events" item-text="label" item-value="id" label="Event" v-model="selectedEventId"></v-select>
                </v-col>
                <v-col>
                <v-text-field id="input-args" type="text" v-model="selectedEventArgs" placeholder="Args separated by spaces"></v-text-field>
                </v-col>
                <v-col>
                <v-btn color="primary" @click="emitWebSocketEvent()">実行</v-btn>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <v-simple-table>
                        <template v-slot:default>
                            <thead><tr><th class="text-left">Sent Messages</th></tr></thead>
                            <tbody><tr v-for="m in sentMsg" :key="m"><td>{{ m }}</td></tr></tbody>
                        </template>
                    </v-simple-table>
                </v-col>
                <v-col>
                    <v-simple-table>
                        <template v-slot:default>
                            <thead><tr><th class="text-left">Received Messages</th></tr></thead>
                            <tbody><tr v-for="m in receivedMsg" :key="m"><td>{{ m }}</td></tr></tbody>
                        </template>
                    </v-simple-table>
                </v-col>
            </v-row>
        </v-container>
    </v-main>
</template>

<script>
export default {
    data: () => ({
        events: [],
        selectedEventId: "",
        selectedEventArgs: "",
        sentMsg: [],
        receivedMsg: [],
    }),
    mounted: function(){
        this.initOnMount()
    },
    computed: {
        ws() { return this.$store.getters.ws },
        wsd() { return this.$store.getters.wsd },
        isWSOpened() { return this.$store.getters.isWSOpened },
        isTemplateSelectDisabled() { return this.templates.length==0 }
    },
    methods: {
        emitWebSocketEvent: function() {
            const eid = this.selectedEventId
            const data = this.selectedEventArgs
            this.$store.dispatch("sendWSMessage", [eid, data.split(" ")])
            this.appendSentMessage(eid, data)
        },
        appendSentMessage: function(eid, data){
            this.sentMsg.push(eid+'_'+data);
        },
        appendReceivedMessage: function(rid, eid, data) {
            this.receivedMsg.push(rid+'_'+eid+'_'+data);
        },
        initOnMount(){
            if(!this.ws || !this.wsd){ return }

            this.$store.dispatch("removeAllOnMessageHandlers")
            this.$store.dispatch("setOnMessageDefaultHandler", this.appendReceivedMessage)

            if(this.isWSOpened){
                var _events = []
                for(let [key,id] of Object.entries(this.wsd.EVENT)){
                    _events.push({id: id, key: key, label: `${id}:: ${key}`})
                }
                this.events = _events;
            }
        },
    },
    watch: {
        isWSOpened(){
            this.initOnMount()
        }
    }
}
</script>

<style>
#operation {
    width: 90%;
    margin: 50px auto;
} 
#operation>ul {
    display: flex;
    list-style: none;
    padding: 0;
}
#msg-wrapper>* {
    width: 50%;
    height: 50%;
}
#select-event {
    width: initial;
    min-width: 200px;
}
#input-args {
    width: 400px;
}
</style>
