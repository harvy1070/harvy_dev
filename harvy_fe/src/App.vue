<template>
    <div id="app">
        <NavBar />
        <router-view></router-view>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';

export default {
    name: 'App',
    components: {
        NavBar,
    },
};
</script>

<style>
@font-face {
    font-family: 'NanumSquare';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_two@1.0/NanumSquareR.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}

#app {
    font-family: 'NanumSquare', sans-serif !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
}
</style>
