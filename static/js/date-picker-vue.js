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

    new Vue({
        el: '#_app_start',
        components: {
            datePicker
        }, methods: {
            submit(date) {
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
                const start = $('input[name="check-in-"]').val();
                $('input[name="check-in"]').val(start);
                const end = date.toDate().toISOString().split('T')[0];
                $('input[name="check-out"]').val(end);
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
            close() {
                $('#getCapacityRoom').submit();
            },
        }
    })
    $('.pdp-group .pdp-pointer').remove()


})
