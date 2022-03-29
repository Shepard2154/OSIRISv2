<template>
    <div>
        <h1>Login page</h1>
        <v-btn @click="authorize">Login hard</v-btn>
    </div>
</template>

<script>
export default {
    name: 'Login',

    data() {
        return {
            login: 'oleg',
            password: '12345678'
        }
    },

    methods: {
        authorize() {
            try {
                axios.post(`http://127.0.0.1:8000/twitter/login/`, 
                    {
                        'Content-Type': 'application/json',
                        'username': this.login,
                        'password': this.password
                    }
                ).then(response => {
                    console.log(response.data.token)
                    this.$store.commit('setToken', response.data.token)  
                })
            } catch(Error) {
                this.isFalseLogin = true
            }
        }   
    }
}
</script>
