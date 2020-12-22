const clientTokenKey = "someClientToken";

function generateRandomString(){
    return Math.random().toString(32).substring(2)
}

export default {
    platformName: "Private",

    workerId: function() {
        return localStorage.getItem("workerId");
    },

    clientToken: function() {
        var token = sessionStorage.getItem(clientTokenKey);
        if(!token) {
            token = generateRandomString();
            sessionStorage.setItem(clientTokenKey, token);
        }
        return token;
    },

    showWorkerMenu: true,

    onWorkerIdNotFound: function(next, pn) {
        next({ path: `/private-prod-login?project=${pn}` })
        return false;
    },

    onClientTokenFailure: function() {
        console.log("clienttokenFailure");
    },

    onSubmitWorkSession: function() {
        sessionStorage.removeItem(clientTokenKey);
        window.location.reload();
    }
}
