<template>
    <v-main class="mt-10 grey lighten-4">
        <v-container>
        <v-row class="justify-center"><v-col cols="10" md="6">
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
        </v-col></v-row>
        </v-container>


        <v-snackbar v-model="snackbar.visible" :timeout="snackbar.timeout" :color="snackbar.color">
            {{ snackbar.text }}
            <template v-slot:action="{ attrs }">
            <v-btn color="white" text v-bind="attrs" @click="snackbar.visible = false">Close</v-btn>
            </template>
        </v-snackbar>


        <!--<v-container>
            <v-row class="justify-center">
                <v-col cols="10" md="6">
                    <v-select max-width="400px" class="mx-auto" :items="sharedProps[name].projects" v-model="projectName" label="Project name"></v-select>
                </v-col>
            </v-row>

            <v-row class="justify-center">
                <v-col cols="10" md="6">
                    <v-card class="pa-6">
                        <v-select class="mr-3" :items="sharedProps[name].templates" label="Choose template..." solo>
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
        profileString: "",
        error: null,
        snackbar: {
            visible: false,
            timeout: 3000,
            color: "",
            text: ""
        }
    }),
    props: ["sharedProps","name"],
    computed: {
        ...mapGetters("ductsModule", [ "duct" ]),
        project() { return this.sharedProps.project },
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
