$(document).ready(function() {
    $('.header-burger').click(function(event) {
        $('.b-1, .b-2, .b-3, .header-menu').toggleClass('active');
        $('.i-body').toggleClass('lock');
    });
    /* $('.b-1, .b-2, .b-3').mouseover(function(event) {
        $('.b-1, .b-2, .b-3').toggleClass('hover');
    });
    $('.b-1, .b-2, .b-3').mouseout(function(event) {
        $('.b-1, .b-2, .b-3').remove('hover');
    });*/
});