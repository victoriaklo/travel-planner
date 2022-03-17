'use strict';

// const button = document.querySelector('#update-status');

// button.addEventListener('click', () => {
//   const queryString = new URLSearchParams({order: 123}).toString();
//   // you could also hard code url to '/status?order=123'
//   const url = `/status?${queryString}`;

//   fetch(url)
//     .then(response => response.text())
//     .then(status => {
//       document.querySelector('#order-status').innerHTML = status;
//     });
// });

function getAttrData() {
  fetch("/api/attractions")
      .then(response => response.json())
      .then(data => { // take this data and iterate over it and take what's important and add to html
        // name, rating, photos
        let attr_lists = []
        const results = JSON.parse(data)
        for (const result of results.results) {
          attr_lists.push(`<li>${result.name}</li>`)
        }
        console.log(JSON.parse(data))

          document.querySelector('#attractions-data').innerHTML = `<ul>${attr_lists.join("")}</ul>`;
      })

}