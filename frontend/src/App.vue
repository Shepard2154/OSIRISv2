<template>
  <v-app>
    <Navbar />
    <v-main>
      <router-view/>
    </v-main>
    <Footer />
  </v-app>
</template>

<script>
import Footer from './components/Footer'
import Navbar from './components/Navbar'
import Sidebar from './components/Sidebar'

export default {
  name: 'App',

  components: {
    Sidebar,
    Navbar,
    Footer
  },
};
</script>

<style lang="scss">
@import 'assets/scss/zero.scss'
</style>
