export default {
    required: value => !!value || "This field is required",
    alphanumeric: value => {
        const pattern = /^[a-zA-Z0-9_-]*$/;
        return pattern.test(value) || 'Alphabets, numbers, "_", or "-" is only allowed';
    },
    numbers: value => {  // only for comboboxes. involves side effects.
        const pattern = /^[0-9]*$/;
        var ret = true;
        for(const i in value) {
            if(!pattern.test(value[i])) {
                ret = false; value.splice(i,1); break;
            }
        }
        return ret || '';
    }
}
