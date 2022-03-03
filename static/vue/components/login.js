export const login = Vue.component("login", {
    template: ` 
      <div class="card mx-auto" style="width: 20rem;">
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
            const f =await fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });
            if (f.status==200){
                window.location.replace("/");
                localStorage.setItem("loginStatus",true)
            }else{
                const j=await f.json();
                this.err=j.message;
                
            }
        }
    }

});

