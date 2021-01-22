<template>
    <v-dialog v-model="shown" :max-width="maxWidth" :persistent="persistent">
        <v-card>
            <v-card-title class="headline" v-if="title" v-html="title"></v-card-title>
            <v-card-title class="headline" v-else-if="$slots.title">
                <slot name="title"></slot>
            </v-card-title>
            <v-card-text v-if="$slots.body">
                <v-form v-model="valid">
                    <slot name="body"></slot>
                </v-form>
            </v-card-text>
            <div class="px-4 py-2">
                <slot name="body-raw"></slot>
            </div>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn v-for="(action,i) in actions.slice().reverse()" :key="i" :color="action.color" @click="action.onclick ? action.onclick() : null; shown=false;" :dark="action.dark" :text="action.text" :disabled="action.disableByRule && !valid">{{ action.label }}</v-btn>
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
    props: ["title", "actions", "maxWidth", "persistent"]
}
</script>
