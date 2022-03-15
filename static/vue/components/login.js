export const login = Vue.component("login", {
    template: ` 
      <div class="card mx-auto" style="width: 20rem;margin-top:20px;">
          <div class="card-body">  
                <p><input type="text" placeholder="username" name="username" v-model="username"></p>
                <p><input type="password" placeholder="password" name="password" v-model="password"></p>
                <button class="btn btn-success" @click="signin">Login</button>
                <a href="/#/register">Register</a><br><br>
                <p v-show="err" class="alert alert-danger">{{err}}</p>
          </div>           
      </div>`,
    data() {
        return {
            username: "",
            password: "",
            err: ""
        }
    },
    methods: {
        async signin() {
            const data = { username: this.username, password: this.password };
            try {
                const response = await fetch("/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                if (!response.ok) {
                    this.err = result.message
                }
                if (response.status == 200) {
                    localStorage.setItem("loginStatus", true)
                    localStorage.setItem("token", result.token)
                    this.err=""
                    this.$root.loginStatus = true
                    window.location.replace("/#/");

                }

            } catch (err) {
                console.log(err);
            }
        }

    }

});

