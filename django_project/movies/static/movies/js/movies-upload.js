$(function () {
  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
    done: function (e, data) {
      if (data.result.is_valid) {
        $("#gallery tbody tr td").prepend(
          "<img  class='thumbnail' style='display: inline-block;' width='370' height='220' src='" + data.result.url + "'>"
        )
      }
    }
  });

});