$(function () {

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-movie").modal("show");
      },
      success: function (data) {
        $("#modal-movie .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#movie-table tbody").html(data.html_movie_read);
          $("#modal-movie").modal("hide");
        }
        else {
          $("#modal-movie .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };




  $(".js-create-movie").click(loadForm);
  $("#modal-movie").on("submit", ".js-movie-create-form", saveForm);

  $("#movie-table").on("click", ".js-update-movie", loadForm);
  $("#modal-movie").on("submit", ".js-movie-update-form", saveForm);

  $("#movie-table").on("click", ".js-delete-movie", loadForm);
  $("#modal-movie").on("submit", ".js-movie-delete-form", saveForm);

});
