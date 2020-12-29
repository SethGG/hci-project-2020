$('#logout').on('click', function (event) {
  let link = $(this);
  let action = link.data('action');
  $.post(action, function() {
    location.reload();
  });
});
