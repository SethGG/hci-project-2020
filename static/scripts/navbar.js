$('#logout').on('click', function (event) {
  let link = $(this);
  let action = link.data('action');
  $.post(action).fail(function() {
    console.log('we failed bois');
    event.preventDefault();
  });
});
