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
            const data={name:this.name, email:this.email,username:this.username,password:this.password};
            fetch("/register",{
                method:"POST",
                headers:{"Content-Type":"application/json"},
                body:JSON.stringify(data)
            }).then(response=> response.json()).then(data=> { this.err=data.message }).catch((error) => {
                console.error('Error:', error);
            });
        }
    }

});

