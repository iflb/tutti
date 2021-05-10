<template>
    <v-snackbar v-model="shown" :color="color" :timeout="timeout">
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
        text: "",
        timeout: 3000,
        color: ""
    }),
    methods: {
        show(color, text, timeout=3000){
            this.shown = false;
            this.$nextTick(() => {
                this.text = text;
                this.color = color;
                this.timeout = timeout;
                this.shown = true;
            });
        }
    }
}
</script>
