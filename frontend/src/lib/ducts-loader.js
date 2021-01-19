export class DuctsLoader {
    initDuct(user) {
        return new Promise((resolve) => {
            window.ducts = {};
            window.ducts.user = user;
            window.ducts.context_url = '/ducts';
            window.ducts.libs_plugin = [window.ducts.context_url + '/libs/tutti.js'];

            window.ducts.main = () => {
                window.ducts.app = {}
                window.ducts.app.duct = new window.ducts.tutti.Duct();
                resolve(this);
            };

            var lib_script = document.createElement('script');
            lib_script.src = window.ducts.context_url + "/libs/ducts.js";
            document.body.appendChild(lib_script);
        });
    }
    openDuct() {
        return new Promise(function(resolve) {
            window.ducts.app.duct.open(window.ducts.context_url + '/wsd').then(function() {
                resolve(window.ducts.app.duct)
            });
        });
    }
}
