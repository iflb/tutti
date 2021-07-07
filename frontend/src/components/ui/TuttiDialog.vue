<template>
    <v-dialog v-model="shown" :max-width="maxWidth" :persistent="persistent">
        <v-card>
            <v-card-title class="headline" v-if="title" v-html="title"></v-card-title>
            <v-card-title class="headline" v-else-if="$slots.title">
                <slot name="title"></slot>
            </v-card-title>
            <v-card-text v-if="$slots.body">
                <v-form v-model="valid" @submit.prevent="allowEnter ? submit(actions[0].onclick) : null;">
                    <slot name="body"></slot>
                </v-form>
            </v-card-text>
            <div class="px-4 py-2" v-if="$slots['body-raw']">
                <slot name="body-raw"></slot>
            </div>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                        v-for="(action,i) in actions.slice().reverse()"
                        :key="i"
                        :color="action.color"
                        @click="submit(action.onclick)"
                        :dark="action.dark"
                        :text="action.text"
                        :disabled="action.disableByRule && !valid"
                    >{{ action.label }}</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>
<script>
export default {
    data: () => ({
        shown: false,
        valid: false,
    }),
    methods: {
        show() {
            this.shown = true;
        },
        hide() {
            this.shown = false;
        },
        submit(onclick) {
            if(onclick) onclick();
            this.hide();
        }
    },
    props: ["title", "actions", "maxWidth", "persistent", "allowEnter"]
}
</script>
