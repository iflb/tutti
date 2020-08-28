export default {
    data: () => ({
        nano: {
            data: {},
            ans: {}
        },
    }),
    props: ["nanoData"],
    methods: {
        updateAnswer() {
            this.$emit("updateAnswer", this.nano.ans);
        },
        submit(ans) {
            if(ans) this.$emit("submit", ans);
            else this.$emit("submit", this.nano.ans);
        }
    },
    watch: {
        nanoData() {   // = when a new nanotask is loaded
            this.nano.data = this.nanoData;
            this.nano.ans = {};
        },
        "nano.ans": {
            deep: true,
            handler() {
                this.updateAnswer();
            }
        }
    },
    mounted() {
        if(!this.nanoData) this.nano.data = this.defaultProps;
        else this.nano.data = this.nanoData;
    }
};
