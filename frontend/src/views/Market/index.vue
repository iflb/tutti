<template>
    <div>
        <iframe
            src="/workplace/handson-image"
            frameborder="0"
            :style="style"
            ref="iframe"
            />
    </div>
</template>
<script>
export default {
    data: () => ({
        style: {
            width: '100%',
            height: '100vh'
        }
    }),
    mounted() {
        setTimeout(() => {
            let iframe = document.querySelector('iframe').contentWindow;
            console.log(iframe);
            iframe.postMessage({
                action: 'SyncMessage',
                message: 'Hello'
            }, '*');
        }, 2000);
    }
}
</script>
