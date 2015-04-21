function reset_table(table) {
  var tableLength = table.rows.length;
  for(var i = 1;i < tableLength;i++) {
    table.deleteRow(1);
  }
}

function get_table() {
  return document.getElementById('user-table');
}

function update_table(user_list, textStatus) {
  table = get_table();
  reset_table(table);
  add_rows(table, user_list);
}

function send_ajax(form) {
  var map = {};
  
  for(var i = 0; i < form.length;i++) {
    var input = form.elements[i];
    map[input.name] = input.value;
  }
  
  $.getJSON('/webapps/users/lookup/',map,update_table);
}

function add_row(table, user) {
  var id = user['id'];
  var username = user['username'];
  var first = user['first_name'];
  var last = user['last_name'];
  var email = user['email'];
  
  
  var row = create_table_row(id, username, first, last, email);
  table.appendChild(row);
}


function add_rows(table, user_list) {
  for(var j = 0; j < user_list.length; j++) {
    add_row(table, user_list[j]);
  }
}

//function init_header_row(row) {
//  for(var i = 0;i < factor_list.length;i++) {
//    var f = factor_list[i];
//    var td_p = document.createElement('td');
//    td_p.className = 'user-table-subcol-permissions';
//    td_p.innerHTML = decamelcase(f);
//    row.appendChild(td_p);
//  }
//}

function create_table_row(id, username, first_name, last_name, email) {
  var tr = document.createElement('tr');
  tr.className = 'user-table-row';
  
  var td_id = document.createElement('td');
  td_id.className = 'user-table-col-id';
  td_id.innerHTML = id;
  tr.appendChild(td_id);
  
  var td_username = document.createElement('td');
  td_username.className = 'user-table-col-username';
  td_username.innerHTML = username;
  tr.appendChild(td_username);

  var td_first = document.createElement('td');
  td_first.className = 'user-table-col-first';
  td_first.innerHTML = first_name;
  tr.appendChild(td_first);
  
  var td_last = document.createElement('td');
  td_last.className = 'user-table-col-last';
  td_last.innerHTML = last_name;
  tr.appendChild(td_last);
  
  var td_email = document.createElement('td');
  td_email.className = 'user-table-col-email';
  td_email.innerHTML = email;
  tr.appendChild(td_email);
  
  var td_p = document.createElement('td');
  td_p.className = 'user-table-col-permissions';
  var button = document.createElement('input');
  button.type = 'button';
  var closure_id = id;
  button.onclick = function() {
    location.href = '/webapps/users/edit/' + closure_id;
  };
  button.value = 'edit';
  td_p.appendChild(button);
  tr.appendChild(td_p);
  
  return tr;
}
