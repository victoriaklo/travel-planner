'use strict';

const attractionBtn = document.querySelector('#attractions-btn');

attractionBtn.addEventListener('click', () => {
  const queryString = new URLSearchParams({city_id:city_id}).toString();
  const url = `/api/attractions?${queryString}`;

  fetch(url)
  .then(result => result.json())
    // response.json()) // takes the response from api and converts to JS object,
  // creating another promise (then) to do something else with that data
  .then(data => { // take this data and iterate over it and take what's important and add to html
    // name, rating, photos
    console.log(data)

    // clears anything in the HTML and prevents user from seeing duplicate request data
    document.querySelector('#attractions-data').innerHTML = ""

    // iterate through the list of restaurants and display in an input form
    // for of will return the value, not the index
    for (const result of data.results) {


        document.querySelector('#attractions-data').innerHTML += `

          <div class="card" style="width: 18rem;">
            <img class="card-img-top" src="${result.photo_url}" alt="Card image cap" width="300" 
            height="200">
              <div class="card-body">
                <h5 class="card-title">${result.name}</h5>
                <input type="checkbox" id="${result.name}" name="attr-choice" value="${result.name}">
                <label for="${result.name}">${result.name} (${result.rating} rating)</label>
                <p class="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer. ${result.rating} rating </p>
              </div>
            </div>`
          

    };

  })
});