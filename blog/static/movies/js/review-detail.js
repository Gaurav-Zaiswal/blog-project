const iStar = document.querySelector("#imdb-rating-dp");
const mScore = document.querySelector("#met-score-dp");
const rTomato = document.querySelector("#rotten-tomato-dp");

imdb_id
    fetch(`https://imdb-api.com/API/Ratings/k_opxgs2hf/${imdb_id}`)
    .then(
        response => response.json())
    .then( function(data){
        iStar.innerText = data['imDb'];
        mScore.innerText = data['metacritic'];
        rTomato.innerText = data['rottenTomatoes'];

});