$("#charselect").on("change", function(event) {
  let select = $(this);
  let selection = select.find(':selected');
  let options = select.find('option');
  options.removeClass('active');
  selection.tab('show');
});

$("#slotscard").on("shown.bs.tab", function(event) {
  let card = $(this);
  let char_select = card.find("#charselect");
  let lvl_select = card.find("#v-pills-tab-"+char_select.val()+" .active");
  Cookies.set('character', char_select.val());
  Cookies.set('level', lvl_select.data('value'));
});

$("#slotscard").on("click", ".spell-link", function(event) {
  let spell = $(event.target).data('link');
  Cookies.set('collapse', spell);
});

$("#slotscard").on("click", ".close", function(event) {
  let action = $(event.target).data('action');
  $.ajax({
    method: "DELETE",
    url: action,
    success: function(result){
      location.reload();
    }
  });
});

$("#slotscard").on("click", "#charpagebtn", function(event) {
  let select = $('#charselect');
  let selection = select.find(':selected');
  let link = selection.data('link');
  location.href = link;
});
