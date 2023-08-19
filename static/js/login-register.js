$(document).ready(function () {
    function modalRegisterForm(url) {
        $.ajax({
            type:"GET",
            url: "/get/login/get-modal?modalName=" + url,
            success: function(data){
                $('#_partial').empty().html(data);
            }
        });
    }
$(document).on('submit', '#registerNewCustomers', function (e) {
         e.preventDefault();
        $('.errMsg').removeClass('d-block').addClass('d-none')
        $(this).find('.sup').remove()
        $(this).find('.border-red-err').removeClass('border-red-err box-shadow-red-err text-danger')
        if ($('#id_re_password').val() != $('#id_password').val()){
            $('#id_re_password').addClass('border-red-err text-danger');
            $('#id_password').addClass('border-red-err text-danger');
            return false
        }
        let pattern = /^9\d{9}$/i
        if(!pattern.test($('#registerNewCustomers #id_username').val())) {
            $('#registerNewCustomers #id_username').addClass('border-red-err text-danger');
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
                    for (var error in data.result){
                        if (error === 'username'){
                            msg = data.result.username
                        }
                        if (error === 'email'){
                            msg = data.result.email
                        }
                        if (error === 'mobile'){
                            msg = data.result.mobile
                        }
                        if (error === 'password'){
                            msg = data.result.password
                        }
                        $('#registerNewCustomers #id_'+error).prev().append('<sup class="text-danger sup">'+msg+'</sup>');
                        $('#registerNewCustomers #id_'+error).addClass('border-red-err box-shadow-red-err text-danger')
                    }
                } else {
                    $('.errMsg').addClass('d-block alert-success').removeClass('d-none alert-danger').html(data.result)
                    $('.btnRegisterLoginPasswd').find('label').html('<a href="/panel">حساب کاربری</a>').removeClass('btnRegisterLoginPasswd')
                    $("._reservation_user_form_container").remove();
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

        $('#formLoginUser .errMsg').removeClass('d-block').addClass('d-none').html('');
        if ($('#formLoginUser #id_password').val().length < 1){
            $('#formLoginUser .errMsg').removeClass('d-none').addClass('d-block').html('پسورد را به درستی وارد کنید')
            $('#id_password').addClass('border-red-err text-danger');
            return false
        }
        if ($('#formLoginUser #id_username').val().length >= 1){
            if($('#formLoginUser #id_username').val().indexOf('@') != -1){
                let pattern = /[a-z0-9]+@[a-z]+\.[a-z]{2,3}/i
                if(!pattern.test($('#formLoginUser #id_username').val())) {
                    $('#formLoginUser .errMsg').removeClass('d-none').addClass('d-block').html('ایمیل را به درستی وارد کنید');
                    return false
                }
            }else {
                let pattern = /^09\d{9}$/i
                if(!pattern.test($('#formLoginUser #id_username').val())) {
                    $('#formLoginUser .errMsg').removeClass('d-none').addClass('d-block').html('موبایل را به درستی وارد کنید');
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
                    $("._reservation_user_form_container").remove();
                } else if (data.status == 0 ||data.status == -1) {
                    $('#formLoginUser .errMsg').removeClass('d-none').addClass('d-block').html('کاربری با این مشخصات پیدا نشد')
                }
            },
            error: function (xhr, desc, err) {
                $('#formLoginUser .errMsg').removeClass('d-none').addClass('d-block').html('خطایی در درخواست شما روی داد لطفا دوباره تلاش کنید')
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
                    window.location.replace("https://hoteltik.com");
                    $('#forgotPassConfirm').attr('action' , '');
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
