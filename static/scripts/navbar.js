$('#logout').on('click', function (event) {
  let link = $(this);
  let action = link.data('action');
  $.post(action).fail(function() {
    event.preventDefault();
  });
});

$('#loginModal').on('show.bs.modal', function (event) {
  let button = $(event.relatedTarget);
  let action = button.data('action');
  let title = button.data('title');
  let modal = $(this);
  modal.find('.modal-title').text(title);
  modal.find('.form').attr('action', action);
  modal.find('.alert').hide();
});

$("#loginModal").on("submit", function(event) {
  event.preventDefault();
  let modal = $(this)
  let form = modal.find('.form');
  let action = form.attr('action');
  $.post(action, form.serialize(), function() {
    location.reload();
  }).fail(function(data) {
    let alert = modal.find('.alert');
    alert.find('span').text(data.responseText);
    alert.show();
  });
});
