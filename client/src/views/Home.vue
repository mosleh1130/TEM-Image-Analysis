<template>
  <div class="home">
    <img alt="Gigalogy logo" src="../assets/logo.png" width="250">
    <HelloWorld msg="Welcome to TEM Image analysis application"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue';

export default {
  name: 'home',
  components: {
    HelloWorld,
  },
};
</script>
