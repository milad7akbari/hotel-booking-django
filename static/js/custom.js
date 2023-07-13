$(document).ready(function () {
    $(document).on('click', '.btnShowMenuMain', function (e) {
        $(this).parents('.header_top_container').next().slideToggle(0)
    });
    $(document).on('click', '.btnShowRooms', function (e) {
        $([document.documentElement, document.body]).animate({
            scrollTop: $(".formReservation").offset().top
        }, 2000);
    });
})