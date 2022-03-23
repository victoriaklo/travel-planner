'use strict';

const attractionBtn = document.querySelector('#attractions-btn');

attractionBtn.addEventListener('click', () => {
  const queryString = new URLSearchParams({city_id:city_id}).toString();
  const url = `/api/attractions?${queryString}`;

  fetch(url)
  .then(response => response.json()) // takes the response from api and converts to JS object,
  // creating another promise (then) to do something else with that data
  .then(data => { // take this data and iterate over it and take what's important and add to html
    // name, rating, photos
    let attrList = []
    const results = JSON.parse(data)
    for (const result of results.results) {
      attrList.push(`${result.name}`)
    };

    // clears anything in the HTML and prevents user from seeing duplicate request data
    document.querySelector('#attractions-data').innerHTML = ""

    // iterate through the list of restaurants and display in an input form
    // for of will return the value, not the index
    for (let attrItem of attrList) {

      document.querySelector('#attractions-data').innerHTML += `<div>
      <input type="checkbox" id="${attrItem}" name="attr-choice" value="${attrItem}">
      <label for="${attrItem}">${attrItem}</label>
      </div>`
    };
  })
});