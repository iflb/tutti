<template>
    <component :is="previewTemplate" />
</template>

<script>
export default {
    computed: {
        previewTemplate() {
            try { return require(`@/projects/${this.$route.params.projectName}/templates/Preview.vue`).default }
            catch { return null }
        }
    }
}
</script>
