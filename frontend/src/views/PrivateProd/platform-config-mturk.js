function turkGetSubmitToHost() {
    var defaultHost = "https://www.mturk.com";
    var submitToHost = this.$route.query.turkSubmitTo;// || defaultHost;
    if (submitToHost.startsWith("https://")) return submitToHost;
    if (submitToHost.startsWith("http://")) return submitToHost;
    if (submitToHost.startsWith("//")) return submitToHost;
    return defaultHost;
}

function getAssignmentId(self) {
    return self.$route.query.assignmentId;
}
export const getClientToken = function() {
    return getAssignmentId(this);
};
export const onClientTokenFailure = function(a,b,c) {
    console.log("clienttokenFailure",a,b,c);
};
const onSubmitWorkSession = function() {
    this.$http.post(turkGetSubmitToHost(),
                    {
                        assignmentId: getAssignmentId(this),
                        dummy: "dummy"
                    },
                    //function(data, status, request){
                    //}
    );
};
export default {
    getClientToken,
    onClientTokenFailure,
    onSubmitWorkSession
}
