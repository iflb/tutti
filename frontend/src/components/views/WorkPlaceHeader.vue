<template>
    <v-row>
        <v-col
            v-if="showTitle"
            cols="12"
            class="text-center text-h3 my-3">
            {{ title }}
        </v-col>
        <v-col cols="12" class="text-center">
            <v-btn
                v-if="showInstructionBtn"
                @click="$refs.dialogInstruction.show()">
                Show Instruction
            </v-btn>
        </v-col>

        <tutti-dialog ref="dialogInstruction" maxWidth="1000"
            :actions="[
                { label: 'Close', color: 'green darken-1', text: true }
            ]">
            <template v-slot:body-raw>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn icon text @click="$refs.dialogInstruction.shown=false"><v-icon>mdi-close</v-icon></v-btn>
                </v-card-actions>
                <component :is="instructionTemplate" />
            </template>
        </tutti-dialog>
    </v-row>
</template>

<script>
import TuttiDialog from '@/components/ui/TuttiDialog'
export default {
    components: {
        TuttiDialog
    },
    props: ["prjName", "title", "showTitle", "showInstructionBtn"],
    computed: {
        instructionTemplate() {
            try { return require(`@/projects/${this.prjName}/templates/Instruction.vue`).default }
            catch { return null }
        }
    }
}
</script>
