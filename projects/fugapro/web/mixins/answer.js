export default {
    props: {
        anskey: String
    },
    methods: {
        updateAnswer: function(val){
            this.$store.dispatch("updateAnswer", [this.anskey, val])
        },
        updateAnswerForTag: function(tag, val){
            this.$store.dispatch("updateAnswerForTag", [this.anskey, tag, val])
        }
    }
}
