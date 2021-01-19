<template>
    <v-dialog v-model="show" max-width="1400">
      <v-card>
        <v-card-title class="headline">
            <v-icon class="mr-2" color="indigo">mdi-database-check</v-icon>
            Imported Nanotasks for '{{ template }}'
            <v-spacer/>
            <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details />
        </v-card-title>
        <v-card-text class="text-end">
            <v-btn color="error" :disabled="selectedNanotaskIds.length==0" @click="deleteNanotasks()">Delete</v-btn>
        </v-card-text>
        <v-data-table
            v-model="selectedNanotasks"
            :loading="loading"
            dense
            :headers="headers"
            :items="nanotasksFlat"
            item-key="NanotaskId"
            :search="search"
            :footer-props="{
              showFirstLastPage: true,
              firstIcon: 'mdi-chevron-double-left',
              lastIcon: 'mdi-chevron-double-right',
              prevIcon: 'mdi-chevron-left',
              nextIcon: 'mdi-chevron-right',
              itemsPerPageOptions: [10,30,50,100,-1]
            }"
            show-select
            sort-by="NanotaskId"
            >
            <template v-slot:item.GroundTruths="{ item }">
                <v-simple-table dense>
                    <template v-slot:default>
                        <tbody>
                            <tr v-for="(value, key) in item.GroundTruths" :key="key">
                                <td style="width:100px"><b>{{ key }}</b></td>
                                <td style="word-break:break-all">{{ value }}</td>
                            </tr>
                        </tbody>
                    </template>
                </v-simple-table>
            </template>
            <template v-slot:item.Props="{ item }">
                <v-simple-table dense>
                    <template v-slot:default>
                        <tbody>
                            <tr v-for="(value, key) in item.Props" :key="key">
                                <td style="width:100px"><b>{{ key }}</b></td>
                                <td style="word-break:break-all">{{ value }}</td>
                            </tr>
                        </tbody>
                    </template>
                </v-simple-table>
            </template>
            <template v-slot:item.Timestamp="{ item }">
                {{ unixTimeToDatetimeString(item.Timestamp) }}
            </template>
        </v-data-table>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog" >Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
</template>

<script>
export default {
    data: () => ({
        show: false,
        search: "",
        selectedNanotasks: [],

        loading: true
    }),
    props: ["duct", "project", "template", "nanotasks"],
    computed: {
        headers() {
            return [
                { text: "NanotaskId",    value: "NanotaskId",    width: "10%" },
                { text: "Tag",           value: "Tag",           width: "10%" },
                { text: "NumAssignable", value: "NumAssignable", width: "1%" },
                { text: "Priority",      value: "Priority",      width: "1%" },
                { text: "GroundTruths",  value: "GroundTruths",  width: "20%" },
                { text: "Props",         value: "Props",         width: "40%" },
                { text: "Timestamp",     value: "Timestamp",     width: "15%" }
            ];
        },
        nanotasksFlat() {
            return this.nanotasks.map((x) => {
                const { props, ...rest } = x;
                return Object.assign(rest, props);
            });
        },
        selectedNanotaskIds() {
            return this.selectedNanotasks.map((x) => (x.NanotaskId));
        }
    },
    methods: {
        closeDialog() {
            this.show = false;
        },
        unixTimeToDatetimeString(d) {
            d = new Date(d*1000);
            var years = d.getFullYear();
            var month = ("0"+(d.getMonth() + 1)).slice(-2);
            var day =  ("0"+d.getDate()).slice(-2);
            var hours = ("0"+d.getHours()).slice(-2);
            var minutes = ("0"+d.getMinutes()).slice(-2);
            var seconds = ("0"+d.getSeconds()).slice(-2);
            return `${years}-${month}-${day} ${hours}:${minutes}:${seconds}`;
        },
        deleteNanotasks() {
            this.duct.sendMsg({
                tag: "recursive",
                eid: this.duct.EVENT.NANOTASK,
                data: {
                    "Command": "Delete",
                    "ProjectName": this.project.name,
                    "TemplateName": this.template,
                    "NanotaskIds": this.selectedNanotaskIds
                }
            });
        }
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
