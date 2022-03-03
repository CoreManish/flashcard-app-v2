//component import starts
import { home } from "./components/home.js";
import { decks } from "./components/decks.js";
import { login } from "./components/login.js";
import { register } from "./components/register.js";
import { review } from "./components/review.js";

// routing code starts
const routes = [
    { path: "/", component: home },
    { path: "/decks", component: decks },
    { path: "/review", component: review },
    { path: "/login", component:login},
    { path : "/register", component:register}
];
const router = new VueRouter({
    routes: routes
});

// vue instance starts
const app=new Vue({
    el: "#vue-app",
    data:{
        loginStatus:false
    },
    watch:{
        // If clicked on logout loginStatus will become false and
        // after login, loginStatus will become true 
        loginStatus(){
            localStorage.setItem("loginStatus",this.loginStatus)
            if(this.loginStatus==false){
                window.location.replace("/#/login")
            }
        }
    },
    router: router,
    mounted() {
         //after loading and mounting, take value from localStorage and put in vue data
        if (localStorage.loginStatus) {
            this.loginStatus = JSON.parse(localStorage.loginStatus)
        }
        if(this.loginStatus==false){
            window.location.replace("/#/login")
        }
    }

});