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
  let card = link.parents('.slotcard');
  if (link.hasClass('active')) {
    let tab = $(this.hash);
    tab.removeClass('show active');
    link.removeClass('active');
    card.removeClass('border-secondary');
  }
  else {
    let prep = $(event.delegateTarget);
    let pref_link = prep.find('.spell-link.active');
    if (pref_link.length > 0) {
      let pref_tab = $(pref_link[0].hash);
      let pref_card = pref_link.parents('.slotcard');
      pref_tab.removeClass('show active');
      pref_link.removeClass('active');
      pref_card.removeClass('border-secondary');
    }
    link.tab("show");
    card.addClass('border-secondary');
  }
});

$("#prepspells").on("click", ".delspell", function(event) {
  let action = $(event.target).data('action');
  $.ajax({
    method: "DELETE",
    url: action,
    success: function(result){
      location.reload();
    }
  });
});

$("#prepspells").on("click", ".addspell", function(event) {
  let action = $(event.target).data('action');
  let char = $(event.target).data('char');
  let lvl = $(event.target).data('lvl');
  Cookies.set('character', char);
  Cookies.set('level', lvl);
  Cookies.remove('collapse');
  location.href = action;
});

$("#prepspells").on("click", ".togglespell", function(event) {
  let action = $(event.target).data('action');
  $.ajax({
    method: "PUT",
    url: action,
    success: function(result) {
      location.reload();
    }
  });
});

$("#prepspells").on("click", "#regainall", function(event) {
  let prep = $(event.delegateTarget);
  let used = prep.find('.regainspell');
  used.each(function(index, element) {
    let action = $(element).data('action');
    $.ajax({
      method: "PUT",
      url: action,
      success: function(result) {
        if (index === used.length - 1) {
          location.reload();
        }
      }
    });
  });
});
