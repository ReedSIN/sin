//1;2c1;2c
String.prototype.trim = function() {
  return this.replace(/^\s+|\s+$/g,"");
};

function add_row(form) {
  var select = document.getElementById('org-name-select');

  if(select.options.length === 0) {
    return;
  }

  var selected_option = select.options[select.selectedIndex];
  var org_id = selected_option.value;
  var org_name = selected_option.text;
  
  var other_signators = document.getElementById('other_signators');
  var other_sig_value = other_signators.value;
  other_signators.value = "";

  var comments = document.getElementById('comment-text-area');
  var comments_value = comments.value;
  comments.value = "";
  
  var tr = document.createElement('tr');

  var td_org_id = document.createElement('td');
  td_org_id.innerHTML = org_id;
  td_org_id.id = 'organization-id-' + org_id;
  tr.appendChild(td_org_id);

  var td_org_name = document.createElement('td');
  td_org_name.innerHTML = org_name;
  td_org_name.id = 'organization-name-' + org_id;
  tr.appendChild(td_org_name);

  var td_org_o_sig = document.createElement('td');
  td_org_o_sig.innerHTML = other_sig_value;
  td_org_o_sig.id = 'organization-o-sig-' + org_id;
  tr.appendChild(td_org_o_sig);

  var td_org_com = document.createElement('td');
  td_org_com.innerHTML = comments_value;
  td_org_com.id = 'organization-comment-' + org_id;
  tr.appendChild(td_org_com);

  var button_form = document.createElement('form');
  button_form.onsubmit = function() {
    return false;
  };

  var edit_glyph = '<span class="glyphicon glyphicon-pencil"></span>&nbsp;'
  var edit_button = document.createElement('button');
  edit_button.type = 'submit';
  edit_button.innerHTML = edit_glyph + 'Edit';
  edit_button.id = 'edit-' + org_id;
  edit_button.className = 'btn btn-default btn-block';
  edit_button.onclick = function() {
    edit_row(edit_button);
  };
  button_form.appendChild(edit_button);

  var delete_glyph = '<span class="glyphicon glyphicon-remove"></span>&nbsp;'
  var delete_button = document.createElement('button');
  delete_button.type = 'submit';
  delete_button.innerHTML = delete_glyph + 'Delete';
  delete_button.id = 'delete-' + org_id;
  delete_button.className = 'btn btn-default btn-block';
  delete_button.onclick = function() {
    remove_row(delete_button);
  };
  button_form.appendChild(delete_button);

  var td_buttons = document.createElement('td');
  td_buttons.appendChild(button_form);
  tr.appendChild(td_buttons);
  
  var table = document.getElementById('org-table-body');
  table.appendChild(tr);
  select.removeChild(selected_option);
}

function remove_row(submit) {
  var form = submit.parentNode;
  var td = form.parentNode;
  var tr = td.parentNode;
  var table = tr.parentNode;
  
  var select = document.getElementById('org-name-select');
  var option = document.createElement('option');
  
  var org_id = tr.cells[0].innerHTML;
  var org_name = tr.cells[1].innerHTML;
  
  option.value = org_id;
  option.innerHTML = org_name;
  select.appendChild(option);
  select.selectedIndex = select.options.length - 1;
  table.removeChild(tr); 
}

function edit_row(submit) {
  var form = submit.parentNode;
  var td = form.parentNode;
  var tr = td.parentNode;
  var table = tr.parentNode;
  
  var select = document.getElementById('org-name-select');
  var o_sig_box = document.getElementById('other_signators');
  var comment_box = document.getElementById('comment-text-area');
  var option = document.createElement('option');
  
  var id = submit.id.substring(5);
  
  var org_id = document.getElementById('organization-id-' + id).innerHTML.trim();
  var org_name = document.getElementById('organization-name-' + id).innerHTML.trim();
  var org_o_sig = document.getElementById('organization-o-sig-' + id).innerHTML.trim();
  var org_com = document.getElementById('organization-comment-' + id).innerHTML.trim();
  
  option.value = org_id;
  option.text = org_name;
  
  select.appendChild(option);
  select.selectedIndex = select.options.length - 1;
  if(org_o_sig === ""|| org_o_sig === null) {
    o_sig_box.value = "";
  } else {
    o_sig_box.value = org_o_sig;
  }
  comment_box.value = org_com;
  
  
  table.removeChild(tr);
  
  c_len = table.childNodes.length;
  
  for(var i = 0;i < c_len; i++) {
    var c = table.childNodes[i];
    if(c.nodeType == 3) {
      table.removeChild(c);
      c_len--;
      i--;
    }
  }  
}

function add_to_form(form) {
  var table = document.getElementById('org-table-body');
  var query = [];
  // start counter at 2 to ignore first two rows of table
  for(var i = 2;i < table.rows.length;i++) {
    var tr = table.rows[i];
    query.push(get_tr_list(tr));
  }
  var query_input = document.createElement('input');
  query_input.style.visibility = 'hidden';
  query_input.name = 'query_string';
  var q_string = JSON.stringify(query);
  query_input.value = q_string;
  form.appendChild(query_input);
}

// NOt sure if a timeout is the best way to go... 
// esp. since this is a POST thingy
function more_convenient_save(form) {
    add_row(form);
    setTimeout( function() {
	add_to_form(form);
    }, 5000)
}

function get_tr_list(tr) {
  var obj = {};
  
  obj['id'] = tr.cells[0].innerHTML;
  obj['name'] = tr.cells[1].innerHTML;
  obj['other_signators'] = tr.cells[2].innerHTML;
  obj['comments'] = tr.cells[3].innerHTML;
  
  return obj;
}
