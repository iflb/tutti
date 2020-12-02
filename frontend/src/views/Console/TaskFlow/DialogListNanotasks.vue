<template>
    <v-dialog v-model="show" max-width="1200">
      <v-card>
        <v-card-title class="headline">
            <v-icon class="mr-2" color="indigo">mdi-database-check</v-icon>
            Imported Nanotasks for '{{ template }}'
            <v-spacer/>
            <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details />
        </v-card-title>
        <v-data-table
            :loading="loading"
            dense
            :headers="headers"
            :items="nanotasksFlat"
            :search="search"
            :footer-props="{
              showFirstLastPage: true,
              firstIcon: 'mdi-chevron-double-left',
              lastIcon: 'mdi-chevron-double-right',
              prevIcon: 'mdi-chevron-left',
              nextIcon: 'mdi-chevron-right'
            }"
            />
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
            const keys = Object.keys(this.nanotasksFlat.reduce((result, obj) => Object.assign(result, obj), {}));
            return keys.map((x) => ({ text: x, value: x }));
        },
        nanotasksFlat() {
            return this.nanotasks.map((x) => {
                const { props, ...rest } = x;
                return Object.assign(rest, props);
            });
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
                    tag: "recursive",
                    eid: this.duct.EVENT.NANOTASK,
                    data: {
                        "Command": "Get",
                        "ProjectName": this.project.name,
                        "TemplateName": this.template
                    }
                });
            }
        },
        nanotasks() {
            this.loading = false;
        }
    }
}
</script>
