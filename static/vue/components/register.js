export const register = Vue.component("register", {
    template: ` 
    <div class="card mx-auto" style="width: 20rem;margin-top:20px;">
          <div class="card-body">  
                <p><input type="text" placeholder="name" name="name" v-model="name"></p>
                <p><input type="text" placeholder="email" name="email" v-model="email"></p>
                <p><input type="text" placeholder="username" name="username" v-model="username"></p>
                <p><input type="password" placeholder="password" name="password" v-model="password"></p>
                <p><input type="text" placeholder="webhook url" name="webhook_url" v-model="webhook_url"></p>
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
            webhook_url:"",
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
            if (!this.webhook_url){
                return this.err="Please enter webhook URL for alert"
            }
            const data = { name: this.name, email: this.email, username: this.username, password: this.password, webhook_url:this.webhook_url };
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

