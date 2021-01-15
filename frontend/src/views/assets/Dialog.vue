<template>
    <v-dialog v-model="shown" :max-width="maxWidth" :persistent="persistent">
        <v-card>
            <v-card-title class="headline" v-if="title" v-html="title"></v-card-title>
            <v-card-title class="headline" v-else>
                <slot name="title"></slot>
            </v-card-title>
            <v-card-text>
                <slot name="body"></slot>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn v-for="(action,i) in actions.slice().reverse()" :key="i" :color="action.color" @click="action.onclick ? action.onclick() : null; shown=false;" :dark="action.dark" :text="action.text">{{ action.label }}</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>
<script>
export default {
    data: () => ({
        shown: false
    }),
    props: ["title", "actions", "maxWidth", "persistent"]
}
</script>
