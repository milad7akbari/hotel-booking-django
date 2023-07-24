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
    $('.countOrderRoomPerson option').on('click', function () {
        let final = 0
        const lang = $(this).parent().attr('data-price-lang');
        $('.countOrderRoomPerson option:selected').each(function () {
            const count = $(this).val();
            const price = $(this).parent().attr('data-price');
            final += count * price;
            if (final > 0){
                $('#finalAmount').next().removeClass('d-none');
            }else{
                $('#finalAmount').next().addClass('d-none');
            }
        });
        $('#finalAmount').val(final.toLocaleString() + ' ' + lang);
    })

    $(document).on('click', '.btnShowImages', function () {
        const id = $(this).attr('data-ref');
        const get = $(this).attr('data-get');
        modalImages(id, get)
    })
    $(document).on('click', '.btnHideImages', function () {
        $('#_partial').empty();
    });
    function modalImages(ref, get) {
        $.ajax({
            type: "GET",
            data: {'get': get},
            url: "/hotel-l/images/" + ref,
            success: function (data) {
                $('#_partial').empty().html(data);
            }
        });
    }


    $('.check-in-inp').persianDatepicker({
        persianDigit: true,
        altField: '.alt-field-check-in-inp',
        autoClose : true,
        position: [25,250],
        format: 'YYYY-MM-DD',
        minDate: Date.now()
    });
    $('.check-out-inp').persianDatepicker({
        persianDigit: false,
        altField: '.alt-field-check-out-inp',
        autoClose : true,
        format: 'YYYY-MM-DD',
        position: [25,250],
        minDate: Date.now(),
        onSelect: function(unix){
            if (unix > $('.alt-field-check-in-inp').val()){
                var difference = unix - $('.alt-field-check-in-inp').val();
                var daysDifference = Math.floor(difference/1000/60/60/24);
                const final = daysDifference * $('.countOrderRoomPerson').attr('data-price')
                $('.countOrderRoomPerson').attr('data-price' , final)
                $('._price_per_night').html(final.toLocaleString())
            }else return false
        }
    });





})