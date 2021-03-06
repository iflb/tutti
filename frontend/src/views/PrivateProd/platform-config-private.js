const clientTokenKey = "someClientToken";

function generateRandomString(){
    return Math.random().toString(32).substring(2)
}

export default {
    platformName: "Private",

    workerId: function() {
        return localStorage.getItem("tuttiPlatformWorkerId");
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

    onClientTokenFailure: function(a,b,c) {
        console.log(a,b,c);
        console.log("clienttokenFailure");
    },

    onSubmitWorkSession: function() {
        sessionStorage.removeItem(clientTokenKey);
        if(localStorage.getItem("tuttiPlatformWorkerId").startsWith("__ANONYMOUS__")){
            localStorage.removeItem("tuttiPlatformWorkerId");
        }
        window.location.reload();
    }
}
