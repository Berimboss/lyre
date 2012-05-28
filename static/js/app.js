function hideTitle() {
    $('.hideonclick').css('display', "none").end();
}
$("#fileupload").on("click", hideTitle);
$(document).bind('drop dragover', function (e) {
    $('.hideonclick').css('display', "none").end();
});
$(function () {
    $('#fileupload').fileupload({
        dropZone: $('body'),
        dataType: 'json',
        done: function (e, data) {
            if (data.result.error != '') {
                $('#error').text(data.result.error);
                $('#upload-helper').text("ERROR");
                $('#hint').text("WHOOPS ----->");
            }
            if (data.result.artist != null) {
                $('#error').text("");
                $('#upload-helper').text("FINISHED");
                $('#hint').text("TRY AGAIN ----->");
                $('.finish').css('opacity', "0.5").end()
                $('#song').text(data.result.name);
                $('#artist').text("- " + data.result.artist);
                $('#url').text(data.result.url);
                $('#songpage').attr('href', data.result.url)
                $('.show').css('display', 'inline-block').end()
                $('#tweet').attr('href', "https://twitter.com/intent/tweet?via=lyre.me&status=" + data.result.name + " by " + data.result.artist + " - " + data.result.url)
                $('#tweet').text('Share on Twitter')

            }
        }
    });
});
$('#fileupload').bind('fileuploadprogress', function (e, data) {
    $('.finish').css('opacity', "1").end()
    $('.show').css('display', 'none').end()
    $('#song').text("");
    $('#artist').text("");
    $('#url').text("");
    $('#tweet').text("");
    $('#upload-helper').text("UPLOADING");
    $('#hint').text("HOLD ON ----->");
    $('.finish-line').css('display', 'inline-block').end()
    $('#progress-bar').css('width', parseInt(data.loaded / data.total * 100, 10) + '%').end()
    if ((parseInt(data.loaded / data.total * 100, 10)) == 100) {
        $('#upload-helper').text("DOIN MAGIC");
    };
});
$(function() {
    $('span#timer').countdown(expirationDate, function(event) {
        $this = $(this);
        switch(event.type) {
          case "seconds":
          case "minutes":
          case "hours":
            $this.find('span#'+event.type).html(event.value);
            break;
          case "finished":
            $this.fadeTo('slow', .5);
            break;
        }
      });
    });