<template>
    <v-main>
        <v-container>
        <v-row class="justify-center">
            <v-col cols="10" md="6">
                <v-select max-width="400px" class="mx-auto" :items="childProps[name].projects" v-model="projectName" label="Project name"></v-select>
            </v-col>
        </v-row>
        <v-row class="justify-center">
        <v-col cols="10" md="6"><v-textarea id="task-flow" label="JSON for task flow profile" height="500px" outlined v-model="profileString"></v-textarea></v-col>
        </v-row>
        </v-container>
        <!--<v-container>
            <v-row class="justify-center">
                <v-col cols="10" md="6">
                    <v-select max-width="400px" class="mx-auto" :items="childProps[name].projects" v-model="projectName" label="Project name"></v-select>
                </v-col>
            </v-row>

            <v-row class="justify-center">
                <v-col cols="10" md="6">
                    <v-card class="pa-6">
                        <v-select class="mr-3" :items="childProps[name].templates" label="Choose template..." solo>
                        </v-select>
                        <v-row align="center" class="d-flex px-4">
                            <div class="mr-3">Repeat:</div>
                            <div style="width:70px" class="mx-3"><v-text-field type="number"></v-text-field></div>
                            <div class="mx-3">times</div>
                        </v-row>
                    </v-card>
                </v-col>
            </v-row>
            <v-row class="justify-center my-10">
                <v-tooltip bottom>
                    <template v-slot:activator="{ on }">
                    <v-btn icon v-on="on"><v-icon x-large>mdi-plus</v-icon></v-btn>
                    </template>
                    <span>Add flow</span>
                </v-tooltip>
            </v-row>
        </v-container>-->
    </v-main>
</template>

<script>
import store from '@/store.js'
import { mapGetters } from 'vuex'

export default {
    store,
    data: () => ({
        projectName: null,
        templateName: null,
        profile: ""
    }),
    props: ["childProps","name"],
    computed: {
        ...mapGetters("ductsModule", [
            "duct"
        ]),
        profileString() {
            return JSON.stringify(this.childProps[this.name].profile)   // can't be synchronized with v-model
        }
        //events() { return this.childProps[this.name].events },
        //sentMsg() {
        //    if(!this.duct) return []
        //    var msg = []
        //    for(var i in this.duct.log.sent){
        //        var l = this.duct.log.sent[i]
        //        msg.push(`${l.tag}__${l.rid}__${l.eid}__${l.data}`)
        //    }
        //    return msg
        //},
        //receivedMsg() {
        //    if(!this.duct) return []
        //    var msg = []
        //    for(var i in this.duct.log.received){
        //        var l = this.duct.log.received[i]
        //        msg.push(`${l.rid}__${l.eid}__${JSON.stringify(l.data)}`)
        //    }
        //    return msg
        //},
    },
    watch: {
        projectName() {
            this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.NANOTASK_SESSION_MANAGER, data: `GET_SM_PROFILE ${this.projectName}`})
        },
        childProps: {
            deep: true,
            handler: function(){ console.log(this.childProps) }
        }
    }
}

document.addEventListener('keydown', function (e) {
    var elem, end, start, value;
    if (e.keyCode === 9) {
        if (e.preventDefault) {
            e.preventDefault();
        }
        elem = e.target;
        start = elem.selectionStart;
        end = elem.selectionEnd;
        value = elem.value;
        console.log(elem, start, end, value)
        elem.value = "" + (value.substring(0, start)) + "    " + (value.substring(end));
        elem.selectionStart = elem.selectionEnd = start + 4;
        return false;
    }
});
</script>

<style>
#task-flow {
    font-family: Consolas,Menlo,Monaco,Lucida Console,Liberation Mono,DejaVu Sans Mono,Bitstream Vera Sans Mono,Courier New,monospace,sans-serif;
    font-size: 0.8em;
}
</style>
