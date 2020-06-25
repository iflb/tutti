export default {
    data: function(){
        return { nanoAns: { _optional: {} } };
    },
    watch: {
        "nanoAns._optional": {
            handler: function(){
                this.$store.commit("updateAnswer", this.nanoAns);
            },
            immediate: true
        }
    },
    methods: {
        submit: function(){ this.$store.commit("submitAnswer", this.nanoAns); }
    }
};
