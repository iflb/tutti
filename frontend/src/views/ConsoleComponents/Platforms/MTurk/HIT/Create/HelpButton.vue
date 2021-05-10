<template>
    <v-btn icon @click="openNewHelpWindow(name);">
        <v-icon>mdi-help-circle-outline</v-icon>
    </v-btn>
</template>

<script>
export default {
    props: ["name"],
    methods: {
        openNewHelpWindow(name) {
            const urls = {
                QualificationRequirements: "https://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html#ApiReference_QualificationType-IDs",
                HITType: "https://docs.aws.amazon.com/AWSMechTurk/latest/AWSMechanicalTurkRequester/Concepts_HITTypesArticle.html",
                CreateHITType: "https://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_CreateHITTypeOperation.html",
                CreateHITWithHITType: "https://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_CreateHITWithHITTypeOperation.html"
            };
            window.open(urls[name], "_blank");
        }
    }
}
</script>
