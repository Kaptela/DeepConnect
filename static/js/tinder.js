
$(window).on('load', async function () {
  async function populateCards() {
    try {
      // Fetch cards data from the API
      let response = await fetch('api/get-cards/');
      
      // Check if the response is successful
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      // Parse the JSON response
      let data = await response.json()
      data = JSON.parse(data.card)

      console.log(data)

      // Loop through each card in the response and append it
      data.forEach(card => {
        $('.tinder--cards').append(`
          <div class="tinder--card" user-id="${card.pk}">
              <img src="/media/${card.fields.picture}" class="w-50" alt="Profile Picture">
              <h3>${card.fields.name} ${card.fields.lastname}</h3>
              <p>Date of Birth: ${card.fields.date_of_birth}</p>
              <p>${card.fields.description}</p>
              <p>Sex: ${card.fields.sex}</p>
              <p>Orientation: ${card.fields.social_orientation}</p>
          </div>
        `);
      });
    } catch (error) {
      console.error("Error fetching or displaying cards:", error);
      // Optionally show an error message to the user
      $('.tinder--cards').append('<p>Failed to load cards. Please try again later.</p>');
    }
  }

  // Call the populateCards function
  await populateCards();





'use strict';

var tinderContainer = document.querySelector('.tinder');
var allCards = document.querySelectorAll('.tinder--card');
var nope = document.getElementById('nope');
var love = document.getElementById('love');




function initCards(card, index) {
  var newCards = document.querySelectorAll('.tinder--card:not(.removed)');

  newCards.forEach(function (card, index) {
    card.style.zIndex = allCards.length - index;
    card.style.transform = 'scale(' + (20 - index) / 20 + ') translateY(-' + 30 * index + 'px)';
    card.style.opacity = (10 - index) / 10;
  });
  
  tinderContainer.classList.add('loaded');
}

initCards();

allCards.forEach(function (el) {
  var hammertime = new Hammer(el);

  hammertime.on('pan', function (event) {
    el.classList.add('moving');
  });

  hammertime.on('pan', function (event) {
    if (event.deltaX === 0) return;
    if (event.center.x === 0 && event.center.y === 0) return;

    tinderContainer.classList.toggle('tinder_love', event.deltaX > 0);
    tinderContainer.classList.toggle('tinder_nope', event.deltaX < 0);

    var xMulti = event.deltaX * 0.03;
    var yMulti = event.deltaY / 80;
    var rotate = xMulti * yMulti;

    event.target.style.transform = 'translate(' + event.deltaX + 'px, ' + event.deltaY + 'px) rotate(' + rotate + 'deg)';
  });

  hammertime.on('panend', function (event) {
    el.classList.remove('moving');
    tinderContainer.classList.remove('tinder_love');
    tinderContainer.classList.remove('tinder_nope');

    var moveOutWidth = document.body.clientWidth;
    var keep = Math.abs(event.deltaX) < 80 || Math.abs(event.velocityX) < 0.5;

    event.target.classList.toggle('removed', !keep);

    if (keep) {
      event.target.style.transform = '';
    } else {
      var endX = Math.max(Math.abs(event.velocityX) * moveOutWidth, moveOutWidth);
      var toX = event.deltaX > 0 ? endX : -endX;
      var endY = Math.abs(event.velocityY) * moveOutWidth;
      var toY = event.deltaY > 0 ? endY : -endY;
      var xMulti = event.deltaX * 0.03;
      var yMulti = event.deltaY / 80;
      var rotate = xMulti * yMulti;

      event.target.style.transform = 'translate(' + toX + 'px, ' + (toY + event.deltaY) + 'px) rotate(' + rotate + 'deg)';
      initCards();
    }
  });
});

function createButtonListener(love) {
  return async function (event) {
    var cards = document.querySelectorAll('.tinder--card:not(.removed)');
    var moveOutWidth = document.body.clientWidth * 1.5;

    if (!cards.length) return false;

    var card = cards[0];

    card.classList.add('removed');

    if (love) {
      try {
        $.ajax({
          url: `/api/like-card/${card.getAttribute('user-id')}/`,
          method: 'POST',
          contentType: 'application/json', // Specify content type
          dataType: 'json', // Expect JSON response
          data: JSON.stringify({
          }),
          success: function (data) {
          console.log(data)
          },
          error: function (xhr, status, error) {
            console.log(xhr);
            console.log(error);
          }
        });
        
        card.style.transform = 'translate(' + moveOutWidth + 'px, -100px) rotate(-30deg)';
      } catch (error) {
        console.log(error)
      }

    } else {
      try {
        $.ajax({
          url: `/api/dislike-card/${card.getAttribute('user-id')}/`,
          method: 'POST',
          contentType: 'application/json', // Specify content type
          dataType: 'json', // Expect JSON response
          data: JSON.stringify({
          }),
          success: function (data) {
          console.log(data)
          },
          error: function (xhr, status, error) {
            console.log(xhr);
            console.log(error);
          }
        });
        
        card.style.transform = 'translate(' + moveOutWidth + 'px, -100px) rotate(-30deg)';
      } catch (error) {
        console.log(error)
      }
      card.style.transform = 'translate(-' + moveOutWidth + 'px, -100px) rotate(30deg)';
    }

    initCards();

    event.preventDefault();
  };
}

var nopeListener = createButtonListener(false);
var loveListener = createButtonListener(true);

nope.addEventListener('click', nopeListener);
love.addEventListener('click', loveListener);

});