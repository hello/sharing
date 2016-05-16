// DOM Ready
$(function() {
  var current_page = $('body').attr('class'),
      is_nav_dark = $('header').hasClass('dark');

  mixpanel.track('Viewed ' + current_page + ' page');

  /**
   * Scrolling header
   */
  var header_height = $('#header').height(),
      current_page = $('body').attr('class'),
      nav_height = $('#header-container .background').height(),
      position = 25;

  if (window.matchMedia('(max-device-width: 48em)').matches) {
    position = 10;
  }

  if (header_height == 0) {
    header_height = $('video').height();
  /*} else if (current_page == 'design') {
    header_height = 200;*/
  } else if (current_page == 'technology') {
    header_height = $('video').height();
  } else if ((current_page == 'home') || (current_page.indexOf('home-test') > -1)) {
    header_height = 100;
  }

  $(document).scroll(function() {
    var scroll = $(document).scrollTop();

    if (scroll >= position) {
      $('#header-container').css({
        'position': 'fixed',
        'padding-top': '0',
      });

      if (scroll >= ((header_height - 60) - nav_height)) {
        $('#header-container .background').css({
          'background': '#fff',
          'border-bottom': '1px solid rgba(0, 0, 0, 0.075)'
        }).addClass('floating');

        if (!is_nav_dark) {
          $('header').addClass('dark');
        }
      } else {
        $('#header-container .background').css({
          'background': 'transparent',
          'border-bottom': '1px solid transparent'
        }).removeClass('floating');

        if (!is_nav_dark) {
          $('header').removeClass('dark');
        }
      }
    } else {
      $('#header-container').css({
        'position': 'absolute',
      });

      $('#header-container').css({
        'padding-top': position + 'px'
      });

      if (scroll < header_height) {
        $('#header-container .background').css({
          'background': 'transparent',
          'border-bottom': '1px solid transparent'
        }).removeClass('floating');

        if (!is_nav_dark) {
          $('header').removeClass('dark');
        }
      }
    }
  });
});
