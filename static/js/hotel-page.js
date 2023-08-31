$(document).ready(function () {


    $('#id_star_container .star').click(function (e) {
        $('#id_stars').val($(this).attr('data-val'));
        var length = $('.review-container .star').length;
        var selected = $('.review-container .star').index($(this));
        $(".review-container .star").each(function (index) {
            if (index <= selected) {
                $(this).addClass("active");
            } else {
                $(this).removeClass("active");
            }
        });
    });
    $(document).on('change', '.countOrderRoomPerson', function () {
        let final = 0
        const lang = $(this).attr('data-price-lang');
        $('.countOrderRoomPerson option:selected').each(function () {
            const count = $(this).val();
            const price = $(this).parent().attr('data-price');
            final += count * price;
            if (final > 0) {
                $('#finalAmount').next().removeClass('d-none');
            } else {
                $('#finalAmount').next().addClass('d-none');
            }
        });
        $('#finalAmount').val(Math.round(final).toLocaleString() + ' ' + lang);
    })

    $(document).on('click', '.btnShowImages', function () {
        const id = $(this).attr('data-ref');
        const get = $(this).attr('data-get');
        modalImages(id, get)
    })
    $(document).on('click', '.btnHideImages', function () {
        $('#_partial').empty();
    });
    $(document).on('change', '#_filter_rooms_', function () {
        const capacity_selected = $(this).val();
        $('.roomListContainer').addClass('d-none');
        $('.roomListContainer').each(function () {
            const capacity = $(this).attr('data-capacity');
            if (capacity <= capacity_selected && (capacity === 1 || capacity === 2)){
                $(this).removeClass('d-none').addClass('d-block')
            }else if (capacity >= capacity_selected) {
                $(this).removeClass('d-none').addClass('d-block')
            }
        });
    });

    function modalImages(ref, get) {
        $.ajax({
            type: "GET",
            data: {'get': get},
            url: "/get/hotel-l/images/" + ref,
            success: function (data) {
                $('#_partial').empty().html(data);
            }
        });
    }

})
