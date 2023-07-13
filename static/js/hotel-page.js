$(document).ready(function () {

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
    $(document).on('click', '.countOrderRoomPerson option', function () {
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

    $(document).on('submit', '#registerNewCustomers', function (e) {
        $('.errMsg').removeClass('d-block').addClass('d-none')
        $(this).find('.sup').remove()
        $(this).find('.border-red-err').removeClass('border-red-err box-shadow-red-err text-danger')
        if ($('#id_re_password').val() != $('#id_password').val()){
            $('#id_re_password').addClass('border-red-err text-danger');
            $('#id_password').addClass('border-red-err text-danger');
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
                    for (var error in data.result){
                        if (error == 'username'){
                            msg = data.result.username
                        }
                        if (error == 'email'){
                            msg = data.result.email
                        }
                        if (error == 'mobile'){
                            msg = data.result.mobile
                        }
                        if (error == 'password'){
                            msg = data.result.password
                        }
                        $('#id_'+error).prev().append('<sup class="text-danger sup">'+msg+'</sup>');
                        $('#id_'+error).addClass('border-red-err box-shadow-red-err text-danger')
                    }
                } else {
                    $('.errMsg').addClass('d-block alert-success').removeClass('d-none alert-danger').html(data.result)
                    $('.btnRegisterLoginPasswd').find('label').html('<a href="/panel">حساب کاربری</a>').removeClass('btnRegisterLoginPasswd')
                    setTimeout(function () {
                        $("#registerLoginModal").remove();
                    } , 1000)
                }
            },
            error: function (xhr, desc, err) {
                $('.errMsg').removeClass('d-none').addClass('d-block').html('خطایی در درخواست شما روی داد لطفا دوباره تلاش کنید')
            }
        });
    });
})