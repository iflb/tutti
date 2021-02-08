<template>
    <v-snackbar :color="color" v-model="shown" :timeout="timeout">
        {{ text }}
        <template v-slot:action="{ attrs }">
            <v-btn dark color="white" text v-bind="attrs" @click="shown=false">Close</v-btn>
        </template>
    </v-snackbar>
</template>
<script>
export default {
    data: () => ({
        shown: false,
        text: ""
    }),
    props: ["color", "timeout"],
    methods: {
        show(text){
            this.text = text;
            this.shown = true;
        }
    }
}
</script>
