function show_error(message) {
    $('#error').text(message);
    $('#error').fadeIn('slow');
    setTimeout("$('#error').fadeOut('slow');$('#error').text('');", 3000);
}

function show_shortened_url(short_url_id) {
    $('#short_url').html('<a href="/u/' + short_url_id + ' ">/u/' + short_url_id + '</a>');
}



	
function save_long_url(url) {
    var actionurl = '/api/url/submit';
    var url = $('#urlfield').prop('value');

    if (url == '' || url == undefined) {
        $('#urlfield').focus();  
        show_error('No URL');
        return false;  
    }
    var post_data = JSON.stringify({ url: url });
    $('#submitbutton').button('loading');
    $.ajax({
        type: 'POST',
        url: actionurl,
        dataType : 'json',
        data: post_data,
        success: function(json){
            if (json.success == true) {
                setTimeout(function(){
                    show_shortened_url(json.short_url_id);
                    $('#submitbutton').button('reset');
                },1000);
            }
            else {
                show_error('Shortening failed');
                $('#submitbutton').button('reset');
            }
        }
    });
}