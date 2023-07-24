$(document).ready(function () {
    $(document).on('click', '.btnShowMenuBlog', function (e) {
        $(this).next().slideToggle(0)
    });
})