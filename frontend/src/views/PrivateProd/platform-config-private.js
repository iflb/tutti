export const getClientToken = function() {
    function someRandomStringGenerator(){
        return Math.random().toString(32).substring(2)
    }
    var token = sessionStorage.getItem("someClientToken");
    if(!token) {
        token = someRandomStringGenerator();
        sessionStorage.setItem("someClientToken", token);
    }
    return token;
};
export const onClientTokenFailure = function() {
    console.log("clienttokenFailure");
};
const onSubmitWorkSession = function() {

};

export default {
    getClientToken,
    onClientTokenFailure,
    onSubmitWorkSession
}
