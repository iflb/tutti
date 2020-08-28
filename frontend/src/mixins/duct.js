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

            this.nano.ans = {};
        }
    },
    watch: {
        nanoData() {
            this.nano.data = this.nanoData;
        },
        "nano.ans": {
            deep: true,
            handler() {
                this.updateAnswer();
            }
        }
    }
};
