<template>
    <v-main class="mt-10 grey lighten-4">
        <v-row class="justify-center"><v-col cols="11" md="8" lg="6">
            <v-card class="pa-3">
            <v-container>
                <v-row>
                    <v-col align="right">
                        <v-btn text icon @click="refreshFlow()"><v-icon>mdi-refresh</v-icon></v-btn>
                    </v-col>
                </v-row>
                <v-card align="center" class="mx-auto py-2 text-h6" color="grey lighten-2" width="200">Start</v-card>

                <arrow :color="templateColor" depth="1" />

                <div v-if="flow">
                    <!--<recursive-batch
                        v-for="(child, idx) in flow.children"
                        :key="idx"
                        :project="project"
                        :node="child"
                        :is-last="idx==flow.children.length-1"
                        :depth="1"
                        :name="name"
                        :template-color="templateColor" />-->
                    <recursive-batch
                        :project="project"
                        :node="flow"
                        :depth="1"
                        :name="name"
                        :is-last="true"
                        :template-color="templateColor" />
                </div>

                <arrow :color="templateColor" depth="1" />

                <v-card align="center" class="mx-auto py-2 text-h6" color="grey lighten-2" width="200">End</v-card>
            </v-container>
            </v-card>
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

import Arrow from './Arrow.vue'
import RecursiveBatch from './RecursiveBatch.vue'

export default {
    store,
    data: () => ({
        snackbar: {
            visible: false,
            timeout: 3000,
            color: "",
            text: ""
        },
        templateColor: "blue-grey lighten-4"
    }),
    components: {
        Arrow, RecursiveBatch
    },
    props: ["sharedProps","name"],
    computed: {
        ...mapGetters("ductsModule", [ "duct" ]),
        project() { return this.sharedProps.project },
        flow() {
            if(this.project) { return this.sharedProps.project.profile; }
            else { return null; }
        }
    },
    methods: {
        showSnackbar(info){
            Object.assign(this.snackbar, info)
            this.snackbar.visible = true
        },
        refreshFlow(){
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.NANOTASK_SESSION_MANAGER,
                data: `LOAD_FLOW ${this.project.name}`
            })
        }
    },
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
