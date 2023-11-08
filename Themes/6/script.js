// Sliders

var slider = document.getElementById('song-progress');

noUiSlider.create(slider, {
  start: [20],
  range: {
    min: [0],
    max: [100]
  }
});

var slider = document.getElementById('song-volume');

noUiSlider.create(slider, {
  start: [90],
  range: {
    min: [0],
    max: [100]
  }
});

// Tooltips

$(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

// Viewport Heights

$(window).on('resize load', function () {
  const totalHeight = $(window).height();

  const headerHeight = $('.header').outerHeight();
  const footerHeight = $('.current-track').outerHeight();
  const playlistHeight = $('.playlist').outerHeight();
  const nowPlaying = $('.playing').outerHeight();

  const navHeight = totalHeight - (headerHeight + footerHeight + playlistHeight + nowPlaying);
  const artistHeight = totalHeight - (headerHeight + footerHeight);

  console.log(totalHeight);

  $('.navigation').css('height', navHeight);
  $('.artist').css('height', artistHeight);
  $('.social').css('height', artistHeight);
});

// Collapse Toggles

$('.navigation__list__header').on('click', function () {
  $(this).toggleClass('active');
});

// Media Queries

$(window).on('resize load', function () {
  if ($(window).width() <= 768) {
    $('.collapse').removeClass('in');

    $('.navigation').css('height', 'auto');

    $('.artist').css('height', 'auto');
  }
});

$(window).on('resize load', function () {
  if ($(window).width() > 768) {
    $('.collapse').addClass('in');
  }
});
