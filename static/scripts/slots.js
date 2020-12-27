$("#slotscard").on("change", function() {
  let card = $(this);
  let form = card.find('.form');
  let par = card.find('#v-pills-cantrip');
  let action = form.attr('action');
  $.post(action, form.serialize(), function(data) {
    par.empty();
    for (let j in data['cantrip']) {
      if (data['cantrip'][j]) {
        let name = data['cantrip'][j][2];
        let html = "<div class='card'><div class='card-body'>"+name+"</div></div>";
        par.append(html);
      }
    }
  });
});

$("#slotscard").trigger("change");
