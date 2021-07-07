function generateSubmitForm(self, data) {
    const action = "http://localhost:8888";
    
    var form = '<form name="myform" action="' + action + '" method="post" hidden="true">';
    for(const [key, val] of Object.entries(data)){
        form += '<input type="text" name="' + key + '" value="'+ val + '" />';
    }
    form += '</form>';

    return form;
}

export default {
    platformName: "TuttiMarket",

    workerId: function(vm) {
        return vm.$route.query.workerId;
    },

    clientToken: function() {
        return 'hoge';
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
            dummy: "dummy"
        };
        const form = generateSubmitForm(self, data);
        document.body.innerHTML += form;
        document.forms.myform.submit();
    }
}
