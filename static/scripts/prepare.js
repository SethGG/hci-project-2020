$('#prepareModal').on('show.bs.modal', function (event) {
  let button = $(event.relatedTarget);
  let action = button.data('action');
  let spell = button.data('spell');
  let level = button.data('level');
  let title = button.data('title');
  let modal = $(this);
  modal.find('.modal-title').text(title);
  modal.find('.form').attr('action', action);
  modal.find('.alert').hide();
  modal.find('#spell').val(spell)
  modal.find('.form-control').prop( "disabled", false );
  if (Cookies.get('character')) {
    modal.find('#character').val(Cookies.get('character'));
  }
  switch(level) {
    case 'cantrip':
      modal.find('#lv10').prop( "disabled", true );
    case 10:
      modal.find('#lv9').prop( "disabled", true );
    case 9:
      modal.find('#lv8').prop( "disabled", true );
    case 8:
      modal.find('#lv7').prop( "disabled", true );
    case 7:
      modal.find('#lv6').prop( "disabled", true );
    case 6:
      modal.find('#lv5').prop( "disabled", true );
    case 5:
      modal.find('#lv4').prop( "disabled", true );
    case 4:
      modal.find('#lv3').prop( "disabled", true );
    case 3:
      modal.find('#lv2').prop( "disabled", true );
    case 2:
      modal.find('#lv1').prop( "disabled", true );
    case 1:
      modal.find('#cantrip').prop( "disabled", true );
  }
  if (level == 'cantrip') {
    modal.find('#cantrip').prop( "disabled", false );
  }
});

$("#prepareModal").on("submit", function(event) {
  event.preventDefault();
  let modal = $(this)
  let form = modal.find('.form');
  let action = form.attr('action');
  $.post(action, form.serialize(), function(data) {
    char = form.find('#character').val();
    Cookies.set('character', char);
    location.reload();
  }).fail(function(data) {
    let alert = modal.find('.alert-danger');
    alert.find('span').text(data.responseText);
    alert.show();
  });
});
