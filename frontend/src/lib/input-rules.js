export default {
    required: value => !!value || "This field is required",
    alphanumeric: value => {
        const pattern = /^[a-zA-Z0-9_-]*$/;
        return pattern.test(value) || 'Alphabets, numbers, "_", or "-" is only allowed';
    }
}
