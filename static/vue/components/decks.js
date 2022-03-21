export const decks = Vue.component("decks", {
  template: `
  <div>
    <div class="d-flex justify-content-center" style="margin-top:10px">
      <input type="text" placeholder="Create new deck" v-model="name" required>
      <button @click="create" class="btn btn-primary">Create Deck</button>
      <button @click="syncDecks" class="btn btn-info">Sync Decks</button>
    </div>
    <div>
    <div class="card-deck">
          <div v-for="deck in decks" class="eachdata">
              <eachdeck v-bind:d="deck"></eachdeck>
          </div>
        </div>
    </div>
  </div>`,
  props: [],
  data() {
    return {
      name: "",
      decks: [],
      err: ""
    }
  },

  methods: {
    async syncDecks() {
      let url = "/deck?token="
      const token = localStorage.getItem("token")
      url = url + token
      try {
        const response = await fetch(url);
        const result = await response.json();
        if (!response.ok) {
          return alert(result.message)
        }
        console.log(result)
        this.decks = []
        for (let i in result) {
          this.decks.push(result[i])
        }
        localStorage.decks = JSON.stringify(this.decks)
        alert("synced")
      } catch (err) { console.log(err) }
    },

    async create() {

      const data = { name: this.name };
      let url = "/deck?token="
      const token = localStorage.getItem("token")
      url = url + token
      try {
        const response = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        });
        const result = await response.json();

        if (!response.ok) {
          //this.err = result.message;
          return alert(result.message)
        }
        if (response.status == 201) {
          alert("Deck created")
          let myDataObject = {
            id: result.id,
            name: result.name,
            average_score: result.average_score,
            user_id: result.user_id,
            last_review_time: result.last_review_time
          };
          this.decks.push(myDataObject)
          localStorage.decks = JSON.stringify(this.decks)
        }

      } catch (err) { console.log(err) }
    }
  },
  components: {
    eachdeck: {
      props: ['d'],
      template: `
      <div class="card" style="width: 20rem;">
          <div class="card-body">
              <p class="card-title">Deck Name: <input type="text" v-model="d.name" class="border-0"></p>
              <p>Average Deck Score: {{d.average_score}}</p>
             
              <button class="btn btn-success" @click="update">Update</button>
              <button class="btn btn-danger" @click="remove">Delete</button><br><br>
              <button class="btn btn-info" @click="review">Review</button>
              <button class="btn btn-info" @click="cards">Cards</button>
              <br><br>
              <div class="card-footer">
                  <small class="text-muted">User ID: {{d.user_id}}</small><br>
                  <small class="text-muted">Deck ID: {{d.id}}</small><br>
                  <small class="text-muted">Last Review: {{Number(d.last_review_time)!=0 ? new Date(Number(d.last_review_time)) : "NA"}}</small>
              </div>
          </div>
          
      </div>`,

      methods: {
        async remove() {
          //alert(this.d.id)
          //console.log(this.$parent.decks[0].name)
          const con = confirm("This will delete all cards present in this deck")
          if (con == false) {
            return
          }
          for (let i = 0; i < this.$parent.decks.length; i++) {
            if (this.$parent.decks[i].id === this.d.id) {
              const data = { id: this.d.id };
              let url = "/deck?token="
              const token = localStorage.getItem("token")
              url = url + token
              try {
                const response = await fetch(url, {
                  method: "DELETE",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify(data)
                });
                if (response.ok) {
                  this.$parent.decks.splice(i, 1);
                  localStorage.decks = JSON.stringify(this.$parent.decks);
                  alert("Deck deleted")
                }
              } catch (err) { console.log(err) }

            }
          }


        },
        async update() {
          for (let i = 0; i < this.$parent.decks.length; i++) {
            if (this.$parent.decks[i].id === this.d.id) {
              this.$parent.decks[i].name = this.d.name

              const data = { id: this.d.id, name: this.d.name };
              let url = "/deck?token="
              const token = localStorage.getItem("token")
              url = url + token
              try {
                const response = await fetch(url, {
                  method: "PUT",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify(data)
                });
                if (response.ok) {
                  alert("Deck Updated")
                }
              } catch (err) { console.log(err) }

            }
          }
          localStorage.decks = JSON.stringify(this.$parent.decks)
        },
        review() {
          localStorage.deck_id = this.d.id;
          localStorage.deck_name = this.d.name;
          window.location.replace("/#/review")
        },
        cards() {
          localStorage.deck_id = this.d.id;
          localStorage.deck_name = this.d.name;
          if (localStorage.cards) {
            localStorage.removeItem("cards")
          }
          window.location.replace("/#/cards")
        }

      }

    }
  },
  mounted() {
    if (localStorage.decks) {
      this.decks = JSON.parse(localStorage.decks);
    }
    if (!localStorage.token) {
      window.location.replace("/#/login")
    }
  }
});