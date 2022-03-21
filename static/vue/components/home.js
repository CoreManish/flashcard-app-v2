export const home = Vue.component("home", {
  template: `
    <div>
      <div class="card-deck">
        <div v-for="deck in decks" class="eachdata">
          <eachdata v-bind:c="city"></eachdata>
        </div>
      </div>
    </div>`,
  mounted() {
    if (!localStorage.token) {
      window.location.replace("/#/login")
    }
  }
});