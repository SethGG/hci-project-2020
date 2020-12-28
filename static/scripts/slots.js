$("#charselect").on("change", function(event) {
  let select = $(this);
  let selection = select.find(':selected');
  let options = select.find('option');
  options.removeClass('active');
  selection.tab('show');
  Cookies.set('character', selection.val());
});
