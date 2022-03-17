// use AJAX to make get requests to the Google Maps 
// People Nearby Search API for restaurants and attractions

const button = document.querySelector('#update-status');

button.addEventListener('click', () => {
  const queryString = new URLSearchParams({order: 123}).toString();
  // you could also hard code url to '/status?order=123'
  const url = `/status?${queryString}`;

  fetch(url)
    .then(response => response.text())
    .then(status => {
      document.querySelector('#order-status').innerHTML = status;
    });
});

function getRestData() {
    fetch("/api/restaurants")
        .then(response => response.json())
        .then(data => {
            document.querySelector('#restaurants-data').innerHTML = data;
        })

}

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
