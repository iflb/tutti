<template>
    <div>
    </div>
</template>
<script>
import { DuctsLoader } from '@/lib/ducts-loader.js'

export default {
    created() {
        new DuctsLoader().initDuct("guest").then( loader => {
            loader.openDuct().then( duct => {
                console.log(duct);
            });
        });
    }
};
</script>
