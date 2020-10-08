function turkGetSubmitToHost(self) {
    var defaultHost = "https://www.mturk.com";
    var submitToHost = self.$route.query.turkSubmitTo;// || defaultHost;
    if (submitToHost.startsWith("https://")) return submitToHost;
    if (submitToHost.startsWith("http://")) return submitToHost;
    if (submitToHost.startsWith("//")) return submitToHost;
    return defaultHost;
}

function getAssignmentId(self) {
    return self.$route.query.assignmentId;
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
    beforeRouteEnter: (to, from, next) => {
        next(vm => {
            var workerId = vm.$route.query.workerId;
            if(!workerId) alert("workerId was not found!");
            else {
                vm.workerId = workerId;
                next();
            }
        });
    },

    getClientToken: function(self) {
        return getAssignmentId(self);
    },

    onClientTokenFailure: function(a,b,c) {
        console.log("clienttokenFailure",a,b,c);
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
