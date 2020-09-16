<template>
    <v-dialog v-model="show" max-width="1200">
      <v-card>
        <v-card-title class="headline">
            <v-icon class="mr-2" color="indigo">mdi-database-check</v-icon>
            Imported Nanotasks for '{{ template }}'
        </v-card-title>
        <v-data-table :loading="loading" dense :headers="headers" :items="nanotasks" :search="search"></v-data-table>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog" >Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
</template>

<script>
import store from '@/store.js'
import { mapGetters } from 'vuex'

export default {
    store,
    data: () => ({
        show: false,
        search: "",

        loading: true
    }),
    props: ["project", "template", "nanotasks"],
    computed: {
        ...mapGetters("ductsModule", [ "duct" ]),
        headers() {
            const keys = Object.keys(this.nanotasks.reduce(function(result, obj) {
                  return Object.assign(result, obj);
            }, {}))
            var headers = [];
            for(const i in keys){
                headers.push({ text: keys[i], value: keys[i] });
            }
            return headers;
        }
    },
    methods: {
        closeDialog() {
            this.show = false;
        },
    },
    watch: {
        show() {
            if(this.show) {
                this.duct.sendMsg({
                    tag: "recursive", eid: this.duct.EVENT.GET_NANOTASKS,
                    data: `NANOTASKS ${this.project.name} ${this.template}`
                });
            }
        },
        nanotasks() {
            this.loading = false;
        }
    }
}
</script>
