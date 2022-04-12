const imdbRating = document.getElementsByClassName("imdb-star");
const metaScore = document.getElementsByClassName("meta-score");
const releaseYear = document.getElementById()
// console.log(imdb_ids)
let i = 0;

imdb_ids.forEach(element => {
    fetch(`https://imdb-api.com/API/Ratings/k_opxgs2hf/${element['imdb_id']}`)
    .then(
        response => response.json())
    .then( function(data){
        // console.log(`imdb value is ${data['imDb']}`);
        // console.log(`metacritic is ${data['metacritic']}`);
        imdbRating[i].innerText = data['imDb'];
        metaScore[i].innerText = data['metacritic'];
        i++;
    })
});