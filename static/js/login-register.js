$(document).ready(function () {
    function modalRegisterForm(url) {
        $.ajax({
            type:"GET",
            url: "/login/get-modal?modalName=" + url,
            success: function(data){
                $('#_partial').empty().html(data);
            }
        });
    }

    $(document).on('click' , '.btnRegisterLoginPasswd' , function () {
        modalRegisterForm('login-pass')
    })
    $(document).on('click' , '.btnForgotPasswd' , function () {
        modalRegisterForm('forgot-passwd')
    })
    $(document).on('click' , '.btnRegisterNewUser' , function () {
        modalRegisterForm('register-new')
    })
    $(document).on('click' , '.btnCloseModal' , function () {
        $("#registerLoginModal").remove();
    })
    $(document).on('submit', '#reviewsSubmit', function (e) {
        $('.errMsg').removeClass('d-block').addClass('d-none')
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
                        if (error == 'title'){
                            msg = data.result.title
                        }
                        if (error == 'stars'){
                            msg = data.result.stars
                        }
                        if (error == 'short_desc'){
                            msg = data.result.short_desc
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
    $(document).on('submit', '#reqForgotPassCustomers', function (e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr("action"),
            type: 'POST',
            dataType: "JSON",
            data: $(this).serialize(),
            success: function (data) {
                if (data.status == 0 || data.status == -1) {
                    $('.errMsg').removeClass('d-block').addClass('d-none').html(data.msg);
                } else {
                    $('.errMsg').addClass('d-block alert-success').removeClass('d-none alert-danger').html(data.msg)
                    setTimeout(function () {
                         window.location.href = "";
                    } , 1000)
                }
            },
            error: function (xhr, desc, err) {
                $('.errMsg').removeClass('d-none').addClass('d-block').html('خطایی در درخواست شما روی داد لطفا دوباره تلاش کنید')
            }
        });
    });
    $(document).on('submit', '#formLoginUser', function (e) {
        $('.errMsg').removeClass('d-block').addClass('d-none').html('');
        if ($('#id_password').val().length < 1){
            $('.errMsg').removeClass('d-none').addClass('d-block').html('پسورد را به درستی وارد کنید')
            $('#id_password').addClass('border-red-err text-danger');
            return false
        }
        if ($('#id_username').val().length >= 1){
            if($('#id_username').val().indexOf('@') != -1){
                let pattern = /^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b$/i
                if(!pattern.test($('#id_username').val())) {
                    $('.errMsg').removeClass('d-none').addClass('d-block').html($('#id_username').val());
                    return false
                }
            }else {
                let pattern = /^09\d{9}$/i
                if(!pattern.test($('#id_username').val())) {
                    $('.errMsg').removeClass('d-none').addClass('d-block').html('موبایل را به درستی وارد کنید');
                    return false
                }
            }
        }
        e.preventDefault();
        $.ajax({
            url: $(this).attr("action"),
            type: 'POST',
            dataType: "JSON",
            data: $(this).serialize(),
            success: function (data) {
                if (data.status == 1) {
                    $('.btnRegisterLoginPasswd').find('label').empty().append('<a href="/panel">حساب کاربری</a>').removeClass('btnRegisterLoginPasswd')
                    $("#registerLoginModal").remove();
                } else if (data.status == 0 ||data.status == -1) {
                    $('.errMsg').removeClass('d-none').addClass('d-block').html('کاربری با این مشخصات پیدا نشد')
                }
            },
            error: function (xhr, desc, err) {
                $('.errMsg').removeClass('d-none').addClass('d-block').html('خطایی در درخواست شما روی داد لطفا دوباره تلاش کنید')
            }
        });
    });
    $(document).on('submit', '#forgotPassConfirm', function (e) {
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
                if (data.status == 1) {
                    $('.errMsg').addClass('d-block alert-success').removeClass('d-none alert-danger').html(data.msg)
                }
            },
            error: function (xhr, desc, err) {
                $('.errMsg').removeClass('d-none').addClass('d-block').html('خطایی در درخواست شما روی داد لطفا دوباره تلاش کنید')
            }
        });
    });
    $(document).on('click' , '#registerLoginModal' , function (event) {
        if ($(event.target).is("#registerLoginModal")) {
        }else {
            if ($('.inpPhoneNumberOtp').is(':focus')){
                $('.inpPhoneNumberOtp').prev().addClass('isActiveTransition');
            }else{
                /*if ($('.inpPhoneNumberOtp').val().length < 1){
                    $('.inpPhoneNumberOtp').prev().removeClass('isActiveTransition');
                }*/
            }
        }
    })
});
