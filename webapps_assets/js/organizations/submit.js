function add_data_to_form(form, id) {
  var row = document.getElementById('tr-' + id);

  for(var i = 0; i < row.childNodes.length; i++) {
    var c = row.childNodes[i];
    var input = document.createElement('input');
    input.type = 'text';
    input.name = get_node_name();
    input.value = c.innerHTML;
  }
}

function get_node_name(i) {
  var header_row = document.getElementById('tr-header');
  var nodeName = header_row.childNodes[i].innerHTML.toLowerCase();
  return nodeName;
}

function delete_alert(name) {
  var message = "Are you sure that you wish to delete organization ";
  message += name;
  message += "?"
  
  var input_box = confirm(message);
  return input_box;
}
