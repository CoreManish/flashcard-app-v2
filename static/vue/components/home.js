export const home = Vue.component("home", {
  template: `
    <div class="card-deck">
      <div class="card" style="width:20rem">
        <div class="card-body">
          <p>Hi, This is a flash card application.</p>
          <p>You can create decks and cards.</p>
        </div>
      </div>
    </div>`,
  mounted() {
    if (!localStorage.token) {
      window.location.replace("/#/login")
    }
  }
});