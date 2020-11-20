export default {
    data: () => ({
        nano: {
            props: {},
            ans: {}
        },
        requiredAnsKeys: []
    }),
    props: ["nanoProps", "prevAnswer"],
    directives: {
        nano: {
            bind: (el, binding, vnode) => {
                const required = binding.modifiers.required || false;
                if(required){
                    const self = vnode.context;
                    var key = self.getKeyAndValue(binding, vnode)[0];
                    self.requiredAnsKeys.push(key);
                }
            },
            update: (el, binding, vnode) => {
                const self = vnode.context;
                var key;
                key = self.getKeyAndValue(binding, vnode)[0];
                self.$set(self.nano.ans, key, self[key]);
            }
        }
    },
    computed: {
        canSubmit() {
            for(const i in this.requiredAnsKeys){
                const key = this.requiredAnsKeys[i];
                const val = this.nano.ans[key];
                if(!val || Object.keys(val).length==0) return false;
            }
            return true;
        }
    },
    methods: {
        updateAnswer() {
            this.$emit("updateAnswer", this.nano.ans);
        },
        submit(ans) {
            if(ans) this.$emit("submit", ans);
            else this.$emit("submit", this.nano.ans);
        },
        getKeyAndValue(binding, vnode) {
            var key, val;
            key = binding.arg;
            try {   // normal v-model
                key = key || vnode.data.directives.find(e=>e.name=="model").expression;
                val = vnode.data.domProps.value;
            } catch {   // vuetify v-model
                key = key || vnode.data.model.expression;
                val = vnode.data.model.value;
            }
            return [key, val];
        }
    },
    watch: {
        nanoProps() {   // = when a new nanotask is loaded
            this.nano.props = this.nanoProps;
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
        if(this.prevAnswer) {
            for(const [key,val] of Object.entries(this.prevAnswer)){ this[key] = val; }
            this.nano.ans = this.prevAnswer;
        }

        if(!this.nanoProps) this.nano.props = this.defaultNanoProps;
        else this.nano.props = this.nanoProps;
    }
};
