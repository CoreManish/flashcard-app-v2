export const review = Vue.component("review", {
  template: `
      <div>
        <div class="card" style="width: 50rem;">
        <div v-if="cardFound">
          <div class="card-body">
            <h4>Deck: {{deck_name}}</h4>
            <p>Question: {{question}}</p>
            <p>How much difficult it was to recall</p>
            <p>
              <input type="radio" id="easy" value="10" v-model="newScore">
              <label for="easy">Easy</label>
              <br>
              <input type="radio" id="medium" value="5" v-model="newScore">
              <label for="medium">Medium</label>
              <br>
              <input type="radio" id="hard" value="2" v-model="newScore">
              <label for="hard">Hard</label>
            </p>
            <button class="btn btn-info" @click="showAnswer=true">Show Answer</button>
            <br><br>
            <p v-bind:class="[showAnswer ? 'd-block' : 'd-none']">Answer: {{answer}}</p>
          </div>
          <div class="card-footer">
              <small class="text-muted">Card ID: {{id}}</small><br>
              <small class="text-muted">Last Reviewed: {{last_review_date}}</small><br>
              <small class="text-muted">Last Score: {{score}}</small>
          </div>
          <p v-show="err" class="alert alert-danger">{{err}}</p>
          </div>
          <button class="btn btn-success" v-on:click="nextCard">Next Card</button>
         
        </div>
      </div>`,
  props: [],
  data() {
    return {
      id: "",
      question: "",
      answer: "",
      last_review_time: "",
      last_review_date: "",
      score: "",
      newScore: "",
      cardFound: false,
      showAnswer: false,
      err: ""
    }
  },
  computed: {
    deck_name() {
      if (localStorage.deck_name) {
        return localStorage.deck_name;
      }
    },
  },
  watch: {
    last_review_time() {
      let date = new Date(Number(this.last_review_time));
      this.last_review_date = date
    }
  },
  methods: {
    async nextCard() {

      //update current card
      if (this.id) {
        if (!this.newScore) {
          return this.err = "Select Difficulty"
        }
        const d = new Date();
        const last_review_time = d.getTime()
        let next_review_time = last_review_time;
        if (this.newScore == 10) {
          next_review_time = last_review_time + 600000
        } else if (this.newScore == 5) {
          next_review_time = last_review_time + 300000
        } else if (this.newScore == 2) {
          next_review_time = last_review_time + 120000
        }
        const data = { id: this.id, question: this.question, answer: this.answer, score: this.newScore, last_review_time: last_review_time, next_review_time: next_review_time };
        //const data = { id: this.id, question: this.question, answer: this.answer, score: this.difficulty };
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
            //console.log(response)
            this.newScore=0
            this.err=""
          }
        } catch (err) { console.log(err) }
      }
      //fetch another card
      this.showAnswer = false
      const deck_id = localStorage.deck_id;
      let url = "/onecard/" + deck_id + "?token="
      const token = localStorage.getItem("token")
      url = url + token
      try {
        const response = await fetch(url);
        const result = await response.json();
        if (!response.ok) {
          return alert(result.message)
        }
        this.id = result.id
        this.question = result.question
        this.answer = result.answer
        this.last_review_time = result.last_review_time
        this.score = result.score
        this.cardFound = true

        //console.log(result.question)
      } catch (err) { console.log(err) }
    },
  },
  mounted() {
    if (!localStorage.token) {
      return window.location.replace("/#/login")
    }
    if (!localStorage.deck_id || !localStorage.deck_name) {
      alert("Sorry No deck selected");
      window.location.replace("/#/decks")
    }

  }
});