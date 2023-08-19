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

    /*$('#datepicker12from').datepicker({
        minDate: '0',
        changeMonth: true,
        dateFormat: 'yy-mm-dd',
        changeYear: true,
        showButtonPanel: true,
        onSelect: function (dateText, inst) {
            $('#datepicker12to').parent().show();
            $('#datepicker12to').datepicker('option', 'minDate', new JalaliDate(inst['selectedYear'], inst['selectedMonth'], parseInt(inst['selectedDay']) + 1));
            const date = inst['selectedYear'] + '-' + inst['selectedMonth'] + '-' + inst['selectedDay'];
            const final_date = moment.from(date, 'fa', 'YYYY-M-D').format('YYYY-M-D')
            $('.alt-field-check-in-inp').val(final_date)
            $('.alt-field-check-out-inp').val(final_date)
            $('.countOrderRoomPerson option:first-child').each(function () {
                $(this).prop('selected' , true)
            });
            checkCalcDiff(-1)
        },
    });
    $('#datepicker12to').datepicker({
        changeMonth: true,
        showButtonPanel: true,
        dateFormat: 'yy-mm-dd',
        changeYear: true,
        onSelect: function (dateText, inst) {
            const date = inst['selectedYear'] + '-' + inst['selectedMonth'] + '-' + inst['selectedDay'];
            const final_date = moment.from(date, 'fa', 'YYYY-M-D').format('YYYY-M-D')
            $('.alt-field-check-out-inp').val(final_date)
            const check_in = $('.alt-field-check-in-inp').val().split('-');
            const check_out = $('.alt-field-check-out-inp').val().split('-');
            var a = moment([check_out[0], check_out[1], check_out[2]]);
            var b = moment([check_in[0], check_in[1], check_in[2]]);
            checkCalcDiff(a.diff(b, 'days'))
        },
    });*/

    // $('.check-in-inp').persianDatepicker({
    //     persianDigit: true,
    //     altField: '.alt-field-check-in-inp',
    //     autoClose : true,
    //     position: [25,250],
    //     format: 'YYYY-MM-DD',
    //     minDate: Date.now(),
    //     onSelect: function(unix){
    //         checkCalcDiff(unix)
    //     }
    // });

    function checkCalcDiff(diff) {
        let final = 0
        if (diff > 0) {
            $('.countOrderRoomPerson').each(function () {
                const base_price = $(this).parents('.hotelPricing').attr('data-price')
                final = diff * base_price
                $(this).attr('data-price', final)
                $(this).parents('.hotelPricing').find('._price_per_night').html(Math.round(final).toLocaleString())
                $('.containerMsgDiv').empty();
            });
        } else {
            $('.containerMsgDiv').html('<p class="alert alert-warning fs-13 w-100">' + $('.containerMsgDiv').attr('data-msg-lang') + '</p>')
            $('.countOrderRoomPerson').each(function () {
                const base_price = $(this).parents('.hotelPricing').attr('data-price')
                $(this).parents('.hotelPricing').find('._price_per_night').html(Math.round(base_price).toLocaleString())
            });
        }
    }

    new Vue({
        el: '#_app_start',
        components: {
            datePicker
        }, methods: {
            submit(date) {
                $('#_app_to').show()
                $('.diff_front_').addClass('d-none')
            },
            open() {
                $('#_app_to').hide()
                $('.containerMsgDiv').empty()
                $('.countOrderRoomPerson option:first-child').each(function () {
                    $(this).prop('selected', true)
                });
            },
        }
    })


    new Vue({
        el: '#_app_to',
        components: {
            datePicker
        }, methods: {
            submit(date) {
                const start = $('input[name="check-in"]').val();
                const end = date.toDate().toISOString().split('T')[0];
                const date1 = new Date(start);
                const date2 = new Date(end);
                const diffTime = date2 - date1;
                this.dayCount = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
                $('.diff_front_').removeClass('d-none').html($('.diff_front_').attr('data-lang') + ' ' + this.dayCount + ' شب ')
                if (this.dayCount > 0){
                    checkCalcDiff(this.dayCount)
                }else $('.containerMsgDiv').empty().append('<p class="alert alert-warning fs-13 w-100">'+$('.containerMsgDiv').attr('data-msg-lang')+'</p>')
            },
            open() {
                $('.countOrderRoomPerson option:first-child').each(function () {
                    $(this).prop('selected', true)
                });
            },
        }
    })

})
