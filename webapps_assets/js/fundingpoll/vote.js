function check_form(form) {
  var top_deep_count = 0;
  for(var i = 0;i < form.elements.length;i++) {
    var radio = form.elements[i];
    if(radio.checked) {
      if(radio.value == "top_six" || radio.value == "deep_six") {
	if(top_deep_count === 6) {
	  alert("Error! You can not top six/deep six more than 6 organizations.");
	  return false;
        }
	top_deep_count += 1;
      }
    }
  }
  return true;
}

function jump(anchor) {
  var url = anchor;
  window.location.hash = escape(url);
}
