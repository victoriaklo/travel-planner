'use strict';

const restButton = document.querySelector('#restaurants-btn');

restButton.addEventListener('click', () => {
  const queryString = new URLSearchParams({city_id:city_id}).toString();
  const url = `/api/restaurants?${queryString}`;

  fetch(url)
  .then(result => result.json()) // takes the response from api and converts to JS object,
  // creating another promise (then) to do something else with that data
  .then(data => { // take this data and iterate over it and take what's important and add to html
    // name, rating, photos

    console.log(data)

    // clears anything in the HTML and prevents user from seeing duplicate request data
    document.querySelector('#restaurants-data').innerHTML = "";
    
    for (const result of data.results) {

      if (result.photo_url === undefined) {
        result.photo_url = "/static/img/travel_and_planet.png";
      }
        document.querySelector("#restaurants-data").innerHTML += `
        <div class="card" style="width: 18rem;">
          <img class="card-img-top" src="${result.photo_url}" alt="Card image cap"width="300" 
          height="200">
            <div class="card-body">
              <h5 class="card-title">${result.name}</h5>
              <input type="checkbox" id="${result.name}" name="rest-choice" value="${result.name}">
              <label for="${result.name}">${result.name} (Rating: ${result.rating} stars)</label>
            </div>
        </div>`

    };

    }
  )
});
