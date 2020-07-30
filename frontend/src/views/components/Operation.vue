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
                <v-btn color="primary" @click="sendDuctEvent()">実行</v-btn>
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
        receivedMsg: [],
        sentMsg: [],
        componentName: "Operation"
    }),
    props: ["duct"],
    mounted: function(){
        if(this.duct) {
            this.duct.setState(this.componentName)
            this.onDuctOpen()
        }
    },
    methods: {
        sendDuctEvent: function() {
            const eid = this.selectedEventId
            const data = this.selectedEventArgs
            this.duct.send(this.duct.next_rid(), eid, data)
            this.appendSentMessage(eid, data)
        },
        appendSentMessage: function(eid, data){
            this.sentMsg.push(eid+'_'+data);
        },
        appendReceivedMessage: function(rid, eid, data) {
            this.receivedMsg.push(rid+'_'+eid+'_'+data);
        },
        onDuctOpen(){
            for(var key in this.duct.EVENT) {
                var id = this.duct.EVENT[key]
                if(id>=1000){
                    this.duct.setChildEventHandler("Operation", id, this.appendReceivedMessage)
                    this.events.push({id: id, key: key, label: `${id}:: ${key}`})
                }
            }

        },
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
