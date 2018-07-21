// hamburger menu handler	
$('.menu-toggle').on('click', e => {
  e.preventDefault();
  $('.menu-toggle').toggleClass('open');
  $('body').toggleClass('is-fixed');
  $('.hamburgermenu-wrapper').toggleClass('expanded');
});