export const cards = Vue.component("cards", {
  template: `
    <div>
      <div class="d-flex justify-content-center" style="margin-top:10px">
        <input type="text" v-model="deck_name" disabled>
        <input type="text" placeholder="Question..." v-model="question">
        <input type="text" placeholder="Answer..." v-model="answer">
        <button @click="create" class="btn btn-primary">Create Card</button>
        <button @click="syncCards" class="btn btn-info">Sync Cards</button>
      </div>
      <div>
      <div class="card-deck">
            <div v-for="card in cards" class="eachdata">
                <eachcard v-bind:c="card"></eachcard>
            </div>
          </div>
      </div>
    </div>`,
  props: [],
  data() {
    return {
      question: "",
      answer: "",
      cards: [],
      err: ""
    }
  },
  computed: {
    deck_name() {
      if (localStorage.deck_name) {
        return localStorage.deck_name;
      }
    }
  },
  methods: {
    async syncCards() {
      const deck_id = localStorage.deck_id;
      let url = "/card/" + deck_id + "?token="
      const token = localStorage.getItem("token")
      url = url + token
      try {
        const response = await fetch(url);
        const result = await response.json();
        if (!response.ok) {
          return alert(result.message)
        }
        console.log(result)
        this.cards = []
        for (let i in result) {
          this.cards.push(result[i])
        }
        localStorage.cards = JSON.stringify(this.cards)
        alert("Card synced")
      } catch (err) { console.log(err) }
    },
    async create() {

      const data = { question: this.question, answer: this.answer };
      const deck_id = localStorage.deck_id;
      let url = "/card/" + deck_id + "?token="
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
          alert("Card created")
          let myDataObject = {
            id: result.id,
            user_id: result.user_id,
            deck_id: result.deck_id,
            question: result.question,
            answer: result.answer,
            score: result.average,
            last_review_time: result.last_review_time
          };
          this.cards.push(myDataObject)
          localStorage.cards = JSON.stringify(this.cards)
        }

      } catch (err) { console.log(err) }
    }
  },
  components: {
    eachcard: {
      props: ['c'],
      template: `
        <div class="card" style="width: 20rem;">
            <div class="card-body">
                <h5 class="card-title">Question: <input type="text" v-model="c.question" class="border-0"></h5>
                <p>Answer:<br> <textarea v-model="c.answer" cols="28" class="border-0"></textarea></p>
                
                <p>Card Score: {{c.score}}</p>
                
                <button class="btn btn-success" @click="update">Update</button>
                <button class="btn btn-danger" @click="remove">Delete</button><br><br>
    
                <div class="card-footer">
                    <small class="text-muted">User ID: {{c.user_id}}</small><br>
                    <small class="text-muted">Card ID: {{c.id}}</small><br>
                    <small class="text-muted">Deck ID: {{c.deck_id}}</small><br>
                    <small class="text-muted">Last Review: {{ Number(c.last_review_time)!=0 ? new Date(Number(c.last_review_time)) : "NA"}}</small>
                </div>
            </div>
            
        </div>`,

      methods: {
        async remove() {
          const con = confirm("Do you really want to delete this card ?")
          if (con == false) {
            return
          }
          for (let i = 0; i < this.$parent.cards.length; i++) {
            if (this.$parent.cards[i].id === this.c.id) {

              const data = { id: this.c.id };
              const deck_id = localStorage.deck_id;
              let url = "/card/" + deck_id + "?token="
              const token = localStorage.getItem("token")
              url = url + token
              try {
                const response = await fetch(url, {
                  method: "DELETE",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify(data)
                });
                if (response.ok) {
                  this.$parent.cards.splice(i, 1);
                  localStorage.cards = JSON.stringify(this.$parent.cards);
                  alert("Card deleted")

                }
              } catch (err) { console.log(err) }

            }
          }


        },
        async update() {
          for (let i = 0; i < this.$parent.cards.length; i++) {
            if (this.$parent.cards[i].id === this.c.id) {
              this.$parent.cards[i].question = this.c.question
              this.$parent.cards[i].answer = this.c.answer

              const data = { id: this.c.id, question: this.c.question, answer: this.c.answer };
              const deck_id = localStorage.deck_id;
              let url = "/card/" + deck_id + "?token="
              const token = localStorage.getItem("token")
              url = url + token
              try {
                const response = await fetch(url, {
                  method: "PUT",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify(data)
                });
                if (response.ok) {
                  alert("Card Updated")
                }
              } catch (err) { console.log(err) }

            }
          }
          localStorage.cards = JSON.stringify(this.$parent.cards)
        }

      }

    }
  },
  mounted() {
    if (!localStorage.token) {
      return window.location.replace("/#/login")
    }
    if (!localStorage.deck_id || !localStorage.deck_name) {
      alert("Sorry No deck selected");
      window.location.replace("/#/decks")
    }
    if (localStorage.cards) {
      this.cards = JSON.parse(localStorage.cards);
    }

  }
});