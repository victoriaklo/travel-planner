'use strict';

// use AJAX to make get requests to the Google Maps 
// People Nearby Search API for restaurants and attractions


function getRestData() {
  fetch("/api/restaurants")
      .then(response => response.json())
      .then(data => { // take this data and iterate over it and take what's important and add to html
        // name, rating, photos
        let rest_lists = []
        const results = JSON.parse(data)
        for (const result of results.results) {
          rest_lists.push(`<li>${result.name}</li>`)
        }
        console.log(JSON.parse(data))

          document.querySelector('#restaurants-data').innerHTML = `<ul>${rest_lists.join("")}</ul>`;
      })

}
