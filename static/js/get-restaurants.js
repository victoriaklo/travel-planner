'use strict';

const restButton = document.querySelector('#restaurants-btn');

restButton.addEventListener('click', () => {
  const queryString = new URLSearchParams({city_id:city_id}).toString();
  const url = `/api/restaurants?${queryString}`;

  fetch(url)
  .then(response => response.json()) // takes the response from api and converts to JS object,
  // creating another promise (then) to do something else with that data
  .then(data => { // take this data and iterate over it and take what's important and add to html
    // name, rating, photos

    const restObj = JSON.parse(data);
    console.log(restObj);

    // clears anything in the HTML and prevents user from seeing duplicate request data
    document.querySelector('#restaurants-data').innerHTML = "";
    
    for (const result of restObj.results) {

      if (result.business_status === "OPERATIONAL") {
        // result.photos = a list of objects. need to parse the data to get photo

        document.querySelector("#restaurants-data").innerHTML += `
        <div class="card mb-3">
          <!-- <p>${result.photos}</p> -->
          <!-- <img class="card-img-top" src="${result.photos}" alt="Card image cap"> -->
            <div class="card-body">
              <h5 class="card-title">${result.name}</h5>
              <input type="checkbox" id="${result.name}" name="rest-choice" value="${result.name}">
              <label for="${result.name}">${result.name} (Rating: ${result.rating} stars)</label>
              <p class="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer. ${result.rating} rating </p>
            </div>
        </div>`
      }
    };

    }
  )
});



