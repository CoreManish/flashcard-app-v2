export const import_csv = Vue.component("import_csv", {
    template: `
    <div>
      <div class="card-deck mx-auto" style="margin-top:20px;">
            <div id="deck-import" class="card" style="width: 20rem;">
              <div class="card-body">
                <h5>Import Deck from csv</h5>
                <input type="file" name="csvfile" id=""><br><br>
                <button class="btn btn-info">Upload</button>
              </div> 
            </div>
  
            <div id="card-import" class="card" style="width: 20rem;">
              <div class="card-body">
                <h5>Import Card from csv</h5>
                <input type="file" name="csvfile" id=""><br><br>
                <button class="btn btn-info">Upload</button>
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
      async deckImport() {
        
      },
      async cardImport() {
      }
    },
    mounted() {
      if (!localStorage.token) {
        window.location.replace("/#/login")
      }
    }
  });