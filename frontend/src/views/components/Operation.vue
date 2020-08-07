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
                <v-btn color="primary" @click="duct.sendMsg({ tag: name, eid: selectedEventId, data: selectedEventArgs })">Send</v-btn>
                <v-btn color="primary" @click="getDuct()">get duct</v-btn>
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
import store from '@/store.js'
import { mapGetters } from 'vuex'

export default {
    store,
    data: () => ({
        selectedEventId: "",
        selectedEventArgs: "",
    }),
    props: ["childProps","name"],
    computed: {
        ...mapGetters("ductsModule", [
            "duct"
        ]),
        events() { return this.childProps[this.name].events },
        sentMsg() {
            if(!this.duct) return []
            var msg = []
            for(var i in this.duct.log.sent){
                var l = this.duct.log.sent[i]
                msg.push(`${l.tag}__${l.rid}__${l.eid}__${l.data}`)
            }
            return msg
        },
        receivedMsg() {
            if(!this.duct) return []
            var msg = []
            for(var i in this.duct.log.received){
                var l = this.duct.log.received[i]
                msg.push(`${l.rid}__${l.eid}__${JSON.stringify(l.data)}`)
            }
            return msg
        },
    },
    methods: {
        getDuct() {
            console.log(this.duct.log)
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
