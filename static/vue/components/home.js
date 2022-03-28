export const home = Vue.component("home", {
  template: `
    
      <div class="card" style="width:20rem;margin-top:20px;">
        <div class="card-body">
          <p>Hi, This is a flash card application.</p>
          <p>You can create decks and cards.</p>
        </div>
      </div>
    `,
  mounted() {
    if (!localStorage.token) {
      window.location.replace("/#/login")
    }
  }
});