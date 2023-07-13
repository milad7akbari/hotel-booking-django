$(document).ready(function () {
    const old_url = window.location.href;
    var url = old_url.replace(/\?.*/, '');
    $(document).on('click' , '.showBtnFilterHotelList' , function () {
        $(this).next().show()
    })
    $(document).on('click' , '.closeBtnFilterHotelList ' , function () {
        $('.filterContainer').hide();
    })
    $(document).on('click' , '.btnDeleteFilters' , function () {
        getData(url , [])
        $('.filter-options').prop('checked', false);
        $(this).hide()
    });
    $(document).on('click' , '.filter-options' , function () {
        $('.filter-options').parents('li').removeClass('bg-primary').find('span').removeClass('text-white')
        let data = {}
        let arr = []
        let i
        if ($(this).is(':checked') && $(this).hasClass('sorting')){
            $(this).parents('li').addClass('bg-primary').find('span').addClass('text-white')
        }
        $('.filter-options').each(function () {
            if ($(this).is(':checked')){
                if ($(this).hasClass('sorting')){
                    $(this).addClass('sorting')
                }
                i+=1
                const key = $(this).attr('data-action');
                const value = $(this).val();
                if (data[key] === undefined){
                    data[key] = [value];
                }else{
                    data[key].push(value)
                }
            }

        });
        let params = '';
        for (i in data){
            const temp = i + '=' +data[i].join(',')
            arr.push(temp)
            params = arr.join('&')
            //history.pushState(state, "", data[i]);
        }
        const finalParams = url + '?' + params
        getData(finalParams , arr)
        $('.btnDeleteFilters').show();
    });
    function getData(finalParams, arr){
        $('.icon-spinner9').show();
        $.ajax({
            type:"get",
            data:{'filter' : true},
            url: finalParams,
            success: function(data){
                $('.icon-spinner9').hide();
                $('#_list_hotel_container').empty().html(data);
                history.pushState(arr, "", finalParams);
            }
        });
    }

    $(document).on('keyup' , '.inpSearchHotelCity' , function () {
        const url = $(this).attr('data-url');
        const title =  $(this).val();
        const thiss = $(this);
        if (title.length > 2){
            $.ajax({
                url: url,
                type:"GET",
                dataType: 'JSON',
                data: {'filter' : true, 'title' :title, },
                success: function(data){
                    var records = data.hotel;
                    var out = '';
                    if (thiss.attr('data-field-id') === 'ih-search'){
                        const url = thiss.attr('data-url_root');
                        for (const i in records) {
                            const record = records[i];
                            const id = 'inp_'+i;
                            out += '<li class=""><label for="'+id+'" class="fs-12"><a href="'+url+'?search='+record.name+'">'+record.name+'</a></label></li>';
                        }
                    }else{
                        for (const i in records) {
                            const record = records[i];
                            const id = 'inp_'+i;
                            out += '<li class=""><label for="'+id+'" class="fs-12"><span>'+record.name+'</span><input id="'+id+'" data-action="search" value="'+record.name+'" class="filter-options" name="search" type="radio"></label></li>';
                        }
                    }

                    $('#findCityByInpContainer').show().empty().html(out);
                }
            });
        }
    });
    $(document).on('click' , '#findCityByInpContainer input' , function () {
        $('.inpSearchHotelCity').val($(this).val());
        $('#findCityByInpContainer').hide();
    });
});