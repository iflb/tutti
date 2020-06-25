<template>
    <div id="nano">
        <input type="text" v-model="nanoAns.text1" />
        <input type="text" v-model="nanoAns.hoge" />
        <input type="text" v-model="nanoAns._optional.text2" />
        <select v-model="nanoAns._optional.select1">
            <option value="1">hoge1</option>
            <option value="2">hoge2</option>
            <option value="3">hoge3</option>
            <option value="4">hoge4</option>
            <option value="5">hoge5</option>
            <option value="6">hoge6</option>
            <option value="6">hoge6</option>
            <option value="6">hoge6</option>
            <option value="6">hoge6</option>
            <option value="6">hoge6</option>
            <option value="6">hoge6</option>
        </select>
        <button @click="submit">button</button>
    </div>
</template>

<script src="../../base.js"></script>

<style scoped>
#nano {
    width: 100%;
    padding: 30px;
    box-sizing: border-box;
}
</style>
