'use strict';

const newItinerary = document.querySelector('#new-itinerary');

newItinerary.addEventListener('click', () => {
    document.querySelector('.submit-update').style.display = "none"
    document.querySelector('.submit-new-itinerary').style.display = "block"
    document.getElementById('itinerary-title').setAttribute('required', "");
});

const updateItinerary = document.querySelector('#update-itinerary');

updateItinerary.addEventListener('click', () => {

      document.querySelector('.submit-update').style.display = "block"
      document.querySelector('.submit-new-itinerary').style.display = "none"
      document.getElementById('itinerary-title').removeAttribute('required');

});