$("#statsform").on("submit", function(event) {
  event.preventDefault();
  let form = $(this);
  let action = form.attr('action');
  $.post(action, form.serialize(), function() {
    location.reload();
  });
});

$("#prepspells").on("click", ".spell-link", function(event) {
  event.preventDefault();
  let link = $(this);
  if (link.hasClass('active')) {
    let tab = $(this.hash);
    tab.removeClass('show active');
    link.removeClass('active');
  }
  else {
    let prep = $(event.delegateTarget);
    let links = prep.find('.spell-link');
    links.removeClass('active');
    link.tab("show");
  }
});

$(".tab-pane").on("click", ".close", function(event) {
  let tab = $(event.delegateTarget);
  let links = $("#prepspells").find('.spell-link');
  links.removeClass('active');
  tab.removeClass('show active');
});
