'use strict';

const rest_button = document.querySelector('#restaurants-btn');

rest_button.addEventListener('click', () => {
  const queryString = new URLSearchParams({city_id:city_id}).toString();
  // you could also hard code url to '/status?order=123'
  const url = `/api/restaurants?${queryString}`;

  fetch(url)
  .then(response => response.json()) // takes the response from api and converts to JS object,
  // creating another promise (then) to do something else with that data
  .then(data => { // take this data and iterate over it and take what's important and add to html
    // name, rating, photos
    let rest_lists = []
    const results = JSON.parse(data)
    for (const result of results.results) {
      rest_lists.push(`${result.name}`)
    };

    // clears anything in the HTML and prevents user from duplicate request data
    document.querySelector('#restaurants-data').innerHTML = ""

    // iterate through the list of restaurants and display in an input form
    // for of will return the value, not the index
    for (let rest_item of rest_lists) {

      document.querySelector('#restaurants-data').innerHTML += `<div>
      <input type="checkbox" id="${rest_item}" name="rest-choice" value="${rest_item}">
      <label for="${rest_item}">${rest_item}</label>
      </div>`
    };
  })
});

