$("#filterform").on("submit", function(event) {
  event.preventDefault();
  let query = $(":input", this).filter(function(index, element) {
    return $(element).val() != '';
  }).serialize();
  if (query) {
    query = "?" + query;
  }
  location.replace(location.pathname + query);
});

$("#filterform").on("click", ":reset", function() {
  Cookies.remove('collapse');
  location.href = location.pathname;
});

$("#accordion").on("show.bs.collapse", function(event) {
  let card = $(event.target).parent();
  let spell = card.data('spell');
  Cookies.set('collapse', spell);
});

$("#accordion").on("hide.bs.collapse", function(event) {
  let card = $(event.target).parent();
  let spell = card.data('spell');
  if (Cookies.get('collapse') == spell) {
    Cookies.remove('collapse');
  }
});
