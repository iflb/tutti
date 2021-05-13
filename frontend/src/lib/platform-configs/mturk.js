function turkGetSubmitToHost(self) {
    var defaultHost = "https://www.mturk.com";
    var submitToHost = self.$route.query.turkSubmitTo;// || defaultHost;
    if (submitToHost.startsWith("https://")) return submitToHost;
    if (submitToHost.startsWith("http://")) return submitToHost;
    if (submitToHost.startsWith("//")) return submitToHost;
    return defaultHost;
}

function getAssignmentId(self) {
    const assignmentId = self.$route.query.assignmentId;
    return assignmentId;
}

function generateSubmitForm(self, data) {
    const action = turkGetSubmitToHost(self) + "/mturk/externalSubmit";
    
    var form = '<form name="myform" action="' + action + '" method="post" hidden="true">';
    for(const [key, val] of Object.entries(data)){
        form += '<input type="text" name="' + key + '" value="'+ val + '" />';
    }
    form += '</form>';

    return form;
}

export default {
    platformName: "MTurk",

    workerId: function(vm) {
        return vm.$route.query.workerId;
    },

    clientToken: function(self) {
        return getAssignmentId(self);
    },

    showWorkerMenu: false,

    onClientTokenFailure: function(a,b,c) {
        console.log("clienttokenFailure",a,b,c);
    },

    onWorkerIdNotFound: function(next, pn) {
        next({ path: `/workplace/${pn}/preview` });
        return false;
    },

    onSubmitWorkSession: function(self) {
        var data = {
            assignmentId: getAssignmentId(self),
            dummy: "dummy"
        };
        const form = generateSubmitForm(self, data);
        document.body.innerHTML += form;
        document.forms.myform.submit();
    }
}
