$(document).ready(function () {
    $(document).on('click', '.btnShowMenuMain', function (e) {
        $(this).parents('.header_top_container').next().slideToggle(0)
    });
    $(document).on('click', '.btnShowRooms', function (e) {
        $([document.documentElement, document.body]).animate({
            scrollTop: $(".formReservation").offset().top
        }, 2000);
    });

    function en_digit(thiss) {
        const p2e = s => s.replace(/[۰-۹]/g, d => '۰۱۲۳۴۵۶۷۸۹'.indexOf(d))
        const a2e = s => s.replace(/[٠-٩]/g, d => '٠١٢٣٤٥٦٧٨٩'.indexOf(d))
        let final = p2e(thiss.val())
        final = a2e(final)
        thiss.val(final)
    }
    $(document).on('keyup', '.id_mobile', function (e) {
        en_digit($(this))
    });
    $(document).on('keyup', '.id_username', function (e) {
        en_digit($(this))
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


    $(document).on('click', '._extra_person_opt', function () {
        let total = 0
        const basePrice = parseInt($(this).parents('.hotelPricing').attr('data-price'))
        const oldPerson = parseInt($(this).attr('data-person'));
        const person = parseInt($(this).val());
        const price = parseInt($(this).attr('data-price'));
        if (person > oldPerson) {
            total = basePrice + (price * (person - oldPerson))
        } else {
            total = basePrice - ((oldPerson - person) * price)
        }
        $(this).attr('data-person', person);
        $(this).parents('.hotelPricing').attr('data-price', total)
        $(this).parents('.hotelPricing').find('._price').html(total.toLocaleString())

    });




    $(document).on('submit', '#addToCartDetails', function (e) {
        let flag = false
        if ($(this).attr('data-auth') === 1){
            $('.__frm_user_reservation').find('sup').remove();
            $('.__frm_user_reservation').find('input').removeClass('border-red-err box-shadow-red-err text-danger');
            if ($('#id_first_name').val().length <= 2) {
                $('#id_first_name').prev().append('<sup class="text-danger sup">*</sup>');
                $('#id_first_name').addClass('border-red-err box-shadow-red-err text-danger');
                flag = true
            }
            if ($('#id_last_name').val().length <= 2) {
                $('#id_last_name').prev().append('<sup class="text-danger sup">*</sup>');
                $('#id_last_name').addClass('border-red-err box-shadow-red-err text-danger');
                flag = true
            }
            let pattern_user = /^(\+98|0)?9\d{9}$/i
            if (!pattern_user.test($('#id_username').val())) {
                console.log(flag)
                $('#id_username').prev().append('<sup class="text-danger sup">*</sup>');
                $('#id_username').addClass('border-red-err box-shadow-red-err text-danger');
                flag = true
            }
        }

        $('.inpReservation_').removeClass('border-red-err text-danger');
        $('.inpReservation_').each(function () {
            if ($(this).hasClass('id_mobile')) {
                let pattern_guest = /^(\+98|0)?9\d{9}$/i
                if (!pattern_guest.test($(this).val())) {
                    $(this).addClass('border-red-err text-danger');
                    flag = true
                }
            }
            if ($(this).hasClass('id_nationality')) {
                if ($(this).val() > 2 || $(this).val() < 1) {
                    $(this).addClass('border-red-err text-danger');
                    flag = true
                }
            }
            if ($(this).hasClass('id_fullname')) {
                if ($(this).val().length < 3) {
                    $(this).addClass('border-red-err text-danger');
                    flag = true
                }
            }
        });

        if (flag) {
            $([document.documentElement, document.body]).animate({
                scrollTop: $("#addToCartDetails").offset().top
            }, 2000);
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
                        msg = data.result[error]
                        if (data.type === 'User') {
                            $('#id_' + error).prev().find('sup').remove().append('<sup class="text-danger sup">' + msg + '</sup>');
                            $('#id_' + error).prev().append('<sup class="text-danger sup">' + msg + '</sup>');
                            $('#id_' + error).addClass('border-red-err box-shadow-red-err text-danger');
                        }
                        if (data.type === 'Guest' && error !== 'err') {
                            $('.__show_errs').append('<p class="alert-danger alert my-2 fs-12">' + msg + '</p>')
                        }
                    }
                    $([document.documentElement, document.body]).animate({
                        scrollTop: $("#addToCartDetails").offset().top
                    }, 2000);
                } else if (data.status == 1) {
                    $('._step_2').toggleClass('pending-tl active-tl')
                    $('._step_3').addClass('pending-tl')
                    $('.errMsg').html('')
                    $('._reservation_form_main').empty().html(data.html)
                }
            },
            error: function (xhr, desc, err) {

                $('.errMsg').removeClass('d-none').addClass('d-block').html('خطایی در درخواست شما روی داد لطفا دوباره تلاش کنید')
            }
        });
    });





    $(document).on('submit', '#placeOrders', function (e) {
        if (!$('#id_agree_rule').is(':checked')) {
            $('#id_agree_rule').next().addClass('text-danger');
            return false
        }
        e.preventDefault();
        $.ajax({
            url: $(this).attr("action"),
            type: 'POST',
            dataType: "JSON",
            data: $(this).serialize(),
            success: function (data) {
                if (data.status == 1) {
                    window.location.replace(window.location.origin + data.url);
                } else alert('err')
            },
            error: function (xhr, desc, err) {

                $('.errMsg').removeClass('d-none').addClass('d-block').html('خطایی در درخواست شما روی داد لطفا دوباره تلاش کنید')
            }
        });
    });

    $(document).on('submit', '#_tracking_form', function (e) {
        $('.span_loader_').removeClass('d-none').addClass('d-block')
        $('.errMsg').removeClass('alert-success').addClass('d-none alert-danger').html('')
        $('#id_username').removeClass('border-red-err text-danger')
        $('#id_reference').removeClass('border-red-err text-danger')
        let pattern_guest = /^(\+98|0)?9\d{9}$/i
        if (!pattern_guest.test($('#id_username').val())) {
            $('#id_username').addClass('border-red-err text-danger');
            return false
        }
        if ($('#id_reference').val() < 8) {
            $('#id_reference').addClass('border-red-err text-danger');
            return false
        }
        e.preventDefault();
        $.ajax({
            url: $(this).attr("action"),
            type: 'POST',
            dataType: "JSON",
            data: $(this).serialize(),
            success: function (data) {
                $('.span_loader_').addClass('d-none').removeClass('d-block')
                if (!data.err) {
                    $('.errMsg').removeClass('d-none alert-danger').addClass('d-block alert-success').html(data.order)
                } else $('.errMsg').removeClass('d-none').addClass('d-block').html(data.order)
            },
            error: function (xhr, desc, err) {
                $('.span_loader_').addClass('d-none').removeClass('d-block')
                $('.errMsg').removeClass('d-none').addClass('d-block').html('خطایی در درخواست شما روی داد لطفا دوباره تلاش کنید')
            }
        });
    });

})