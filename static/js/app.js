// DOM Ready
$(function() {
  var current_page = $('body').attr('class'),
      is_nav_dark = $('header').hasClass('dark');

  mixpanel.track('Viewed ' + current_page + ' page');
});
