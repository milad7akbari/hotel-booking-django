$(document).ready(function () {


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
    let start = 0
    let end = 0
    new Vue({
        el: '#_app_start',
        components: {
            datePicker
        }, methods: {
            submit(date) {
                start = date;
            },
            open() {
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
                end = date;
                this.dayCount = end.diff(start, 'date')
                if (this.dayCount > 0){
                    $('.diff_front_').removeClass('d-none').html($('.diff_front_').attr('data-lang') + ' ' + this.dayCount + ' روز ')
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
    $(document).on('click' , '.btnAddToCart_' , function () {
        if ($('input[name="check-in"]').val().length < 5 || $('input[name="check-out"]').val().length < 5){
            const start = $('input[name="check-in-"]').val();
            const end = $('input[name="check-out-"]').val();
            $('input[name="check-in"]').val(start);
            $('input[name="check-out"]').val(end);
        }
    })
})
