export const export_csv = Vue.component("export_csv", {
  template: `
  <div>
    <div class="card-deck" style="margin-top:20px;">
         
          <div id="deck-export" class="card" style="width: 20rem;">
          <div class="card-body">
            <h5>Export all Decks as csv</h5>
            <button @click="deckExport" class="btn btn-success">Download Deck</button>
            <a v-show="deck_link" v-bind:href="deck_link">Link</a>
          </div>
          </div>

          <div id="card-export" class="card" style="width: 20rem;">
            <div class="card-body">
              <h5>Export all Cards as csv</h5>
              <button @click="cardExport" class="btn btn-success">Download Card</button>
              <a v-show="card_link" v-bind:href="card_link">Link</a>
            </div>
          </div>
    </div>
    <p v-show="err" class="alert alert-danger">{{err}}</p>
  </div>`,
  data() {
    return {
      err: "",
      deck_link: "",
      card_link: ""
    }
  },
  methods: {
    async deckExport() {
      let url = "/iedeck?token="
      const token = localStorage.getItem("token")
      url = url + token
      try {
        const response = await fetch(url);
        const result = await response.json();
        if (!response.ok) {
          return this.err = result.message
        }
        this.deck_link = result.link
      } catch (err) { console.log(err) }
    },
    async cardExport() {
      let url = "/iecard?token="
      const token = localStorage.getItem("token")
      url = url + token
      try {
        const response = await fetch(url);
        const result = await response.json();
        if (!response.ok) {
          return this.err = result.message
        }
        this.card_link = result.link
      } catch (err) { console.log(err) }
    }
  },
  mounted() {
    if (!localStorage.token) {
      window.location.replace("/#/login")
    }
  }
});