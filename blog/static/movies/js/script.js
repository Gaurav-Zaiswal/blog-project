const imdbRating = document.getElementsByClassName("imdb-star");
const metaScore = document.getElementsByClassName("meta-score");

let i = 0;

imdb_ids.forEach(element => {
    fetch(`https://imdb-api.com/API/Ratings/k_opxgs2hf/${element['imdb_id']}`)
    .then(
        response => response.json())
    .then( function(data){
        console.log(data);
        imdbRating[i].innerText = data['imDb'];
        // console.log(imdbRating);
        metaScore[i].innerText = data['metacritic'];
    })
});