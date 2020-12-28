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
