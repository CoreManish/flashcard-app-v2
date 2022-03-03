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
    router: router,
    mounted() {
        if (localStorage.loginStatus) {
            //after loading and mounting, take value from localStorage and put in vue data
            this.loginStatus = JSON.parse(localStorage.loginStatus)
        }
    }

});