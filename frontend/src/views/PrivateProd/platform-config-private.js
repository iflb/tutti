function generateRandomString(){
    return Math.random().toString(32).substring(2)
}

export default {
    workerId: function() {
        return localStorage.getItem("workerId");
    },

    clientToken: function() {
        var token = sessionStorage.getItem("someClientToken");
        if(!token) {
            token = generateRandomString();
            sessionStorage.setItem("someClientToken", token);
        }
        return token;
    },

    onWorkerIdNotFound: function(next, pn) {
        next({ path: `/private-prod-login?project=${pn}` })
        return false;
    },

    onClientTokenFailure: function() {
        console.log("clienttokenFailure");
    },

    onSubmitWorkSession: function() {}
}
