$("#filterform").on("submit", function(event) {
  event.preventDefault();
  var query = $(":input", this).filter(function(index, element) {
    return $(element).val() != '';
  }).serialize();
  if (query) {
    query = "?" + query;
  }
  location.replace(location.pathname + query);
});

$("#filterform").on("click", ":reset", function() {
  $(":selected", this.parent).removeAttr("selected");
  $(":text", this.parent).attr("value", "");
});
