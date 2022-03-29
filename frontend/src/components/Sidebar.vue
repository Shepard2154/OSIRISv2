<template>
    <div>
        <v-navigation-drawer
            v-model="drawer"
            absolute
            bottom
            temporary
        >
            <v-list
            nav
            dense
            >
            <v-list-item-group
                v-model="group"
                active-class="deep-purple--text text--accent-4"
            >
                <v-list-item>
                <v-list-item-title>Twitter</v-list-item-title>
                </v-list-item>
    
                <v-list-item>
                <v-list-item-title>Instagram</v-list-item-title>
                </v-list-item>
    
                <v-list-item>
                <v-list-item-title>Telegram</v-list-item-title>
                </v-list-item>
    
                <v-list-item>
                <v-list-item-title>VK</v-list-item-title>
                </v-list-item>
            </v-list-item-group>
            </v-list>
        </v-navigation-drawer>
        <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      </div>
</template>

<script>
export default {
    name: 'Sidebar',

    data() {
        return {
            drawer: false,
            group: null,
        }
    },
    

    watch: {
        group() {
            this.drawer = false
        },
    },
}
</script>