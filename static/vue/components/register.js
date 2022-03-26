export const register = Vue.component("register", {
    template: ` 
      <div class="card mx-auto" style="width: 20rem;">
          <div class="card-body">  
                <p><input type="text" placeholder="name" name="name" v-model="name"></p>
                <p><input type="text" placeholder="email" name="email" v-model="email"></p>
                <p><input type="text" placeholder="username" name="username" v-model="username"></p>
                <p><input type="password" placeholder="password" name="password" v-model="password"></p>
                <button class="btn btn-success" @click="signup">Signup</button>
                <a href="/#/login">Login</a><br><br>
                <p v-show="err" class="alert alert-danger">{{err}}</p>
          </div>           
      </div>`,
    data() {
        return {
            name: "",
            email: "",
            username: "",
            password: "",
            err: ""
        }
    },
    methods: {
        async signup() {
            if (!this.name){
                return this.err="Please enter your name"
            }
            if (!this.email){
                return this.err="Please enter your email"
            }
            if (!this.username){
                return this.err="Please enter your username"
            }
            if (!this.password){
                return this.err="Please enter strong password"
            }
            const data = { name: this.name, email: this.email, username: this.username, password: this.password };
            try {
                const response = await fetch("/register", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                this.err = result.message


            } catch (err) { console.log(err) }
        }
    }

});

