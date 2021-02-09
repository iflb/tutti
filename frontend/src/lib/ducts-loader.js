export class DuctsLoader {
    initDuct(user) {
        return new Promise((resolve) => {
            window.ducts = {};
            window.ducts.user = user;
            window.ducts.context_url = '/ducts';
            window.ducts.libs_plugin = [window.ducts.context_url + '/libs/tutti-new.js'];

            window.ducts.main = () => {
                window.ducts.app = {}
                window.ducts.app.duct = new window.ducts.tutti.Duct();
                this.duct = window.ducts.app.duct;
                resolve({ loader: this, duct: this.duct });
            };

            var lib_script = document.createElement('script');
            lib_script.src = window.ducts.context_url + "/libs/ducts.js";
            document.body.appendChild(lib_script);
        });
    }
    openDuct() {
        return new Promise((resolve, reject) => {
            this.duct.open(window.ducts.context_url + '/wsd')
                .then(() => { resolve(this.duct) })
                .catch(reject);
        });
    }
    closeDuct() {
        this.duct.close();
    }
    onDuctOpen(f) {
        if(this.duct.state==window.ducts.State.OPEN_CONNECTED) f();
        else this.duct.addOnOpenHandler(f);
    }
}
