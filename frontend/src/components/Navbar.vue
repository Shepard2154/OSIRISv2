<template>
  <div class="mb-6">
    <v-toolbar dark>
      <v-tabs fixed-tabs>
        <v-tab :to="{ name: 'home' }"> Персоны </v-tab>
        <v-tab :to="{ name: 'search' }"> Поиск ЦА </v-tab>
        <v-tab :to="{ name: 'negative' }"> Выявление ДИВ </v-tab>
        <v-tab :to="{ name: 'geofencing' }"> Геофенсинг </v-tab>
        <v-tab :to="{ name: 'reasons' }"> Инфоповоды </v-tab>
        <router-link 
        style="margin: auto"
        :to="{ name: 'login' }">
          <v-icon v-if="this.$store.state.token">mdi-account</v-icon>
          <v-icon v-else>mdi-account-cancel</v-icon>
        </router-link>
      </v-tabs>
    </v-toolbar>
  </div>
</template>


<script>
export default {
  name: "Navbar",
};
</script>


<style scoped lang="scss">
.color-row {
  height: 100px;
  width: 100%;
  position: absolute;
}
</style>