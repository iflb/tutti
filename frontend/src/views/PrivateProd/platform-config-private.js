function generateRandomString(){
    return Math.random().toString(32).substring(2)
}

export default {
    beforeRouteEnter: (to,from,next) => {
        var workerId = localStorage.getItem("workerId");
        next(vm => {
            if(!workerId) next({ path: `/private-prod-login?project=${vm.projectName}` })
            else {
                vm.workerId = workerId;
                next();
            }
        });
    },

    getClientToken: function() {
        var token = sessionStorage.getItem("someClientToken");
        if(!token) {
            token = generateRandomString();
            sessionStorage.setItem("someClientToken", token);
        }
        return token;
    },

    onClientTokenFailure: function() {
        console.log("clienttokenFailure");
    },

    onSubmitWorkSession: function() {}
}
