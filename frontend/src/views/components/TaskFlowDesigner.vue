<template>
    <v-main class="mt-10 grey lighten-4">
        <v-row class="justify-center"><v-col cols="6">
            <v-container>
                <v-card align="center" class="ma-3 py-2 text-h5">Start</v-card>

                <flow-arrow/>

                <Recursive :node="flow" :is-last="true" :depth="1"></Recursive>

                <flow-arrow/>

                <v-card align="center" class="ma-3 py-2 text-h5">End</v-card>

                <!--<v-row><v-col cols="12" md="6">
                    <v-row><v-col>
                        <v-alert type="error" v-if="error!=null">{{ error }}</v-alert>
                    </v-col></v-row>

                    <v-row><v-col>
                        <v-card class="pa-6">
                        <v-textarea id="task-flow" label="JSON for task flow profile" v-model="profileString" rows="20" auto-grow></v-textarea>
                        </v-card>
                    </v-col></v-row>

                    <v-row><v-col align="right">
                        <v-btn @click="updateProfile()" class="primary">update</v-btn>
                    </v-col></v-row>
                </v-col></v-row>-->
            </v-container>
        </v-col></v-row>


        <v-snackbar v-model="snackbar.visible" :timeout="snackbar.timeout" :color="snackbar.color">
            {{ snackbar.text }}
            <template v-slot:action="{ attrs }">
            <v-btn color="white" text v-bind="attrs" @click="snackbar.visible = false">Close</v-btn>
            </template>
        </v-snackbar>

    </v-main>
</template>

<script>
import store from '@/store.js'
import { mapGetters } from 'vuex'

import FlowArrow from './FlowArrow.vue'
import Recursive from './Recursive.vue'

export default {
    store,
    data: () => ({
        projectName: null,
        templateName: null,
        profileString: "",
        error: null,
        snackbar: {
            visible: false,
            timeout: 3000,
            color: "",
            text: ""
        }
    }),
    components: {
        "flow-arrow": FlowArrow,
        Recursive
    },
    props: ["sharedProps","name"],
    computed: {
        ...mapGetters("ductsModule", [ "duct" ]),
        project() { return this.sharedProps.project },
        flow() { return this.sharedProps.project.profile }
    },
    methods: {
        showSnackbar(info){
            Object.assign(this.snackbar, info)
            this.snackbar.visible = true
        },
        displayProfile() {
            //if(this.project.profile) this.profileString = JSON.stringify(this.project.profile, null, 4)
            console.log(this.project.profile)
            if(this.project.profile) this.profileString = this.project.profile
            else this.profileString = ""
        },
        updateProfile() {
            try {
                JSON.parse(this.profileString)
                this.error = null
            } catch(a) {
                this.error = `${a.name}: ${a.message}`
                this.showSnackbar({ color: "error", text: "JSON parse error" })
                return
            }

            const inlineProfile = this.profileString.replace(/ /g, "").replace(/\n/g, "")
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.NANOTASK_SESSION_MANAGER,
                data: `REGISTER_SM ${this.project.name} ${inlineProfile}`
            })
        }
    },
    mounted() {
        this.displayProfile()
    },
    watch: {
        "project.profile": function(){
            this.displayProfile()
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
        if(value){
            elem.value = "" + (value.substring(0, start)) + "    " + (value.substring(end));
            elem.selectionStart = elem.selectionEnd = start + 4;
        }
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
