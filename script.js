//This code was made by Euri

const app = new Vue({
  el: "#app",
  data: {
    loaded: false,
    books: {},
    borrowers: {},
  },
  mounted() {
    // Fetch the JSON data
    fetch("data.json")
      .then((response) => response.json())
      .then((data) => {
        this.books = data.Books;
        this.borrowers = data.Borrowers;
        this.loaded = true;
      })
      .catch((error) => console.error("Error fetching JSON:", error));
  },
});
