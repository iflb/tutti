<!-- Your HTML code here -->
<template>   
    <div class="card">
        <div class="block">
            <input type="text" v-nano.required v-model="feeling" placeholder="How're you feeling?" />
        </div>
        <div class="next-btn-wrapper">
            <button :disabled="!canSubmit" @click="canSubmit ? submit() : false">SEND</button>
        </div>
    </div>
</template>

<!-- Your JavaScript code here -->
<script>   
import nanoMixIn from "@/mixins/nano";
export default {
    mixins: [nanoMixIn],
    data: () => ({
        feeling: ""
    })
};
</script>

<!-- Your CSS here -->
<style scoped>   
.card {
    width: 600px;
    margin: 100px auto;
    border: 1px solid black;
    padding: 20px;
    box-sizing: border-box;
}
div.block {
    padding: 15px 0;
}
input[type=text] {
    width: 100%;
    border: 1px solid grey;
    font-size: 1.2em;
    padding: 3px 10px;
    border-radius: 3px;
    box-sizing: border-box;
}
div.next-btn-wrapper {
    padding: 10px 0;
    text-align: right;
}
div.next-btn-wrapper>button {
    width: 100px;
    padding: 10px;
    background-color: #eee;
    border-radius: 5px;
}
div.next-btn-wrapper>button:disabled {
    color: grey;
}
</style>
