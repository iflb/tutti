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
        shown: false
    }),
    props: ["text", "color", "timeout"],
    watch: {
        text() {
            this.shown = true;
        }
    }
}
</script>
