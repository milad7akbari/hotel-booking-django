$(document).ready(function () {
    $(document).on('click', '.btnShowMenuMain', function (e) {
        $(this).parents('.header_top_container').next().slideToggle(0)
    });
    $(document).on('click', '.btnShowRooms', function (e) {
        $([document.documentElement, document.body]).animate({
            scrollTop: $(".formReservation").offset().top
        }, 2000);
    });

    function calcPrice(thiss) {
        if (thiss.hasClass('active')) {
            thiss.next().val(0)
            thiss.removeClass('active  icon-checkbox-checked').addClass('icon-checkbox-unchecked')
        } else {
            thiss.next().val(1)
            thiss.addClass('active icon-checkbox-checked').removeClass('icon-checkbox-unchecked')
        }
        const price = parseInt(thiss.attr('data-price'))
        let total = 0
        const basePrice = parseInt(thiss.parents('.hotelPricing').attr('data-price'))
        if (thiss.next().val() == 1) {
            total = basePrice + price
        } else {
            total = basePrice - price
        }
        thiss.parents('.hotelPricing').attr('data-price', total)
        thiss.parents('.hotelPricing').find('._price').html(total.toLocaleString())
    }

    $(document).on('click', '.inp_checkout', function (e) {
        calcPrice($(this))
    });
    $(document).on('click', '.inp_checkin', function (e) {
        calcPrice($(this))
    });

    $(document).on('click', '._extra_person_opt option', function (e) {
        let total = 0
        const basePrice = parseInt($(this).parents('.hotelPricing').attr('data-price'))
        const oldPerson = parseInt($(this).parent().attr('data-person'));
        const person = parseInt($(this).val());
        const price = parseInt($(this).parent().attr('data-price'));
        if (person > oldPerson) {
            total = basePrice + (price * (person - oldPerson))
        } else {
            total = basePrice - ((oldPerson - person) * price)
        }
        $(this).parent().attr('data-person', person);
        $(this).parents('.hotelPricing').attr('data-price', total)
        $(this).parents('.hotelPricing').find('._price').html(total.toLocaleString())

    });


    $(document).on('submit', '#reservationUserInfo', function (e) {
        e.preventDefault();
        if ($('#id_last_name').val().length <= 2) {
            $(this).removeClass('border-red-err text-danger');
            return false
        }
        if ($('#id_first_name').val().length <= 2) {
            $(this).removeClass('border-red-err text-danger');
            return false
        }
        let pattern = /^09\d{9}$/i
        if (!pattern.test($('#id_username').val())) {
            $('#id_username').addClass('border-red-err text-danger');
            return false
        }
        $.ajax({
            url: $(this).attr("action"),
            type: 'POST',
            dataType: "JSON",
            data: $(this).serialize(),
            success: function (data) {
                if (data.err) {
                    let msg = '';
                    for (var error in data.result) {
                        if (error == 'username') {
                            msg = data.result.username
                        }
                        if (error == 'last_name') {
                            msg = data.result.last_name
                        }
                        if (error == 'first_name') {
                            msg = data.result.first_name
                        }
                        $('#id_' + error).prev().append('<sup class="text-danger sup">' + msg + '</sup>');
                        $('#id_' + error).addClass('border-red-err box-shadow-red-err text-danger')
                    }
                } else {
                    $('.errMsgReservationUserInfo').addClass('d-block alert-success').removeClass('d-none alert-danger').html(data.result)
                    $('.btnRegisterLoginPasswd').find('label').html('<a href="/panel">حساب کاربری</a>').removeClass('btnRegisterLoginPasswd')
                }
            },
            error: function (xhr, desc, err) {
                $('.errMsgReservationUserInfo').removeClass('d-none').addClass('d-block').html('خطایی در درخواست شما روی داد لطفا دوباره تلاش کنید')
            }
        });
    });


    $(document).on('submit', '#addToCartDetails', function (e) {
        let flag
        $('.inpReservation_').each(function () {
            if ($(this).hasClass('id_mobile')) {
                let pattern = /^09\d{9}$/i
                if (!pattern.test($(this).val())) {
                    $(this).addClass('border-red-err text-danger');
                    flag = true
                } else {
                    flag = false
                    $(this).removeClass('border-red-err text-danger');
                }
            } else if ($(this).hasClass('id_nationality')) {
                if ($(this).val() == 1 || $(this).val() == 2) {
                    $(this).removeClass('border-red-err text-danger');
                    flag = false
                } else {
                    $(this).addClass('border-red-err text-danger');
                    flag = true
                }
            } else {
                if ($(this).val().length < 3) {
                    $(this).addClass('border-red-err text-danger');
                    flag = true
                } else {
                    flag = false
                    $(this).removeClass('border-red-err text-danger');
                }
            }
        });
        if (flag) {
            return false
        }
        e.preventDefault();
        $.ajax({
            url: $(this).attr("action"),
            type: 'POST',
            dataType: "JSON",
            data: $(this).serialize(),
            success: function (data) {
                if (data.err) {
                    let msg = '';
                    for (var error in data.result) {
                        if (error == 'password') {
                            msg = data.result.password
                        }
                        $('#id_' + error).prev().append('<sup class="text-danger sup">' + msg + '</sup>');
                        $('#id_' + error).addClass('border-red-err box-shadow-red-err text-danger')
                    }
                } else if (data.status == 1) {
                    $('._step_2').toggleClass('pending-tl active-tl')
                    $('._step_3').addClass('pending-tl')
                    $('.errMsg').html('')
                    $('._reservation_form_main').html(data.html)
                }
            },
            error: function (xhr, desc, err) {

                $('.errMsg').removeClass('d-none').addClass('d-block').html('خطایی در درخواست شما روی داد لطفا دوباره تلاش کنید')
            }
        });
    });

})