'use strict';

const attr_button = document.querySelector('#attractions-btn');

attr_button.addEventListener('click', () => {

  fetch("/api/attractions")
  .then(response => response.json())
  .then(data => { // take this data and iterate over it and take what's important and add to html
    // name, rating, photos
    let attr_list = []
    const results = JSON.parse(data)
    for (const result of results.results) {
      attr_list.push(`${result.name}`)
    }

    for (let attr_item of attr_list) {

      document.querySelector('#attractions-data').innerHTML += `<div>
      <input type="checkbox" id="${attr_item}" name="rest-choice" value="${attr_item}">
      <label for="${attr_item}">${attr_item}</label>
      </div>`
    };
  })
});
