
field_types = {
  0 : 'textfield',
  1 : 'textarea',
  2 : 'radiobutton'
};

counter = 0;
field_dict = {};

function field(widget, title, type, core, admin_only) {
  var f = {};
  
  f.widget = widget;
  f.title = title;
  f.type = type;
  f.core = core;
  f.admin_only = admin_only;
  
  return f;
}

function submit_form(form,suffix) {
  var new_form = document.createElement('form');
  new_form.method = 'post';
  new_form.action = '/webapps/forms/my_forms/edit/' + suffix;
  new_form.style.visibility = 'hidden';
  document.getElementById('hidden_div').appendChild(new_form);
  
  var query = {};
  
  query['title'] = document.getElementById('form-title-field').value;
  
  var org_select = document.getElementById('select-organization');
  query['org_id'] = org_select.options[org_select.selectedIndex].value;
  
  query['description'] = document.getElementById('description-textarea').value;
  
  var radio_list = document.getElementsByName('radio-email');
  for(var i = 0;i < radio_list.length;i++) {
    var radio = radio_list[i];
    if (radio.checked) {
      query['email_signator'] = radio.value;
      break;
    }
  }
  
  query['field_list'] = [];
  for(var f in field_dict) {
    var query_field = {};
    var model = field_dict[f];
    query_field['title'] = model.title.value;
    query_field['type'] = model.type.options[model.type.selectedIndex].value;
    query_field['core'] = model.core.checked;
    query_field['admin_only'] = model.admin_only.checked;
    query['field_list'].push(query_field);
  }
  
  var query_string = JSON.stringify(query);
  
  var new_input = document.createElement('input');
  new_input.type = 'text';
  new_input.name = 'query_string';
  new_input.value = query_string;
  new_input.style.visiblity = 'hidden';
  new_form.appendChild(new_input);
  
  new_form.submit();
}

function create_new_title(fieldset) {
  var new_field_title_label = document.createElement('label');
  new_field_title_label.innerHTML = 'Title: ';
  
  var new_field_title = document.createElement('input');
  new_field_title.type = 'text';
  
  fieldset.appendChild(new_field_title_label);
  fieldset.appendChild(new_field_title);
  
  return new_field_title;
}

function create_new_br(fieldset) {
  var br = document.createElement('br');
  fieldset.appendChild(br);
}

function create_hidden_radio_button_panel() {
  var widget = new PeekWidget();
  
  return widget;
}

function create_new_type(fieldset) {
  var new_field_type_label = document.createElement('label');
  new_field_type_label.innerHTML = 'Type: ';
  
  var new_field_type = document.createElement('select');
  
  var option = null;
  for(var o in field_types) {
    option = document.createElement('option');
    option.value = o;
    option.innerHTML = field_types[o];
    new_field_type.appendChild(option);
  }
  
  
  //var hidden_radio_button_panel = create_hidden_radio_button_panel();
  //
  //new_field_type.onChange = function() {
  //  if (this.options[this.selectedIndex].value == 2) {
  //    hidden_radio_button_panel.show();
  //  } else {
  //    hidden_radio_button_panel.hide();
  //  }
  //}
  
  fieldset.appendChild(new_field_type_label);
  fieldset.appendChild(new_field_type);
  //fieldset.appendChild(hidden_radio_button_panel)
  
  return new_field_type;
}

function create_new_core_field(fieldset) {
  var new_field_core_label = document.createElement('label');
  new_field_core_label.innerHTML = 'Core Field: ';
  
  var new_field_core = document.createElement('input');
  new_field_core.type = 'checkbox';
  
  fieldset.appendChild(new_field_core_label);
  fieldset.appendChild(new_field_core);
  return new_field_core;
}

function create_new_admin_only_field(fieldset) {
  var new_field_admin_label = document.createElement('label');
  new_field_admin_label.innerHTML = 'Admin Only: ';
  
  var new_field_admin = document.createElement('input');
  new_field_admin.type = 'checkbox';
  
  fieldset.appendChild(new_field_admin_label);
  fieldset.appendChild(new_field_admin);
  
  return new_field_admin;
}

function remove_fieldset_from_dict(counter) {
  var fieldset = field_dict[counter];
  var widget = fieldset.widget;
  widget.parentNode.removeChild(widget);
  delete field_dict[counter];
}

function create_new_delete_button(fieldset,counter) {
  var delete_item_widget = document.createElement('input');
  delete_item_widget.type = 'button';
  delete_item_widget.value = 'Delete Field';
  delete_item_widget.onclick = function() {
    var answer = confirm("Are you sure you wish to delete this form field?");
    
    if (answer) {
      remove_fieldset_from_dict(counter);
    }
    return false;
  };
  
  fieldset.appendChild(delete_item_widget);
  return delete_item_widget;
}

function create_new_field() {
  var outer_fieldset = document.getElementById('fields_list');
  var new_fieldset = document.createElement('fieldset');
  
  var new_title = create_new_title(new_fieldset);
  create_new_br(new_fieldset);
  
  var new_type = create_new_type(new_fieldset);
  create_new_br(new_fieldset);

  var new_core = create_new_core_field(new_fieldset);
  create_new_br(new_fieldset);

  var new_admin = create_new_admin_only_field(new_fieldset);
  create_new_br(new_fieldset);

  var cur_count = counter + 0;
  create_new_delete_button(new_fieldset, cur_count);
  
  var f = new field(new_fieldset, new_title, new_type, new_core, new_admin);
  field_dict[cur_count] = f;
  counter++;
  
  outer_fieldset.appendChild(new_fieldset);
}


function create_and_init_new_field(input) {
  var form = document.getElementById('fields_list');
  var new_fieldset = document.createElement('fieldset');
  
  var new_title = create_new_title(new_fieldset);
  new_title.value = input['title'];
  create_new_br(new_fieldset);
  
  var new_type = create_new_type(new_fieldset);
  new_type.selectedIndex = input['type'];
  create_new_br(new_fieldset);
  
  var new_core = create_new_core_field(new_fieldset);
  new_core.checked = input['core'];
  create_new_br(new_fieldset);
  
  var new_admin = create_new_admin_only_field(new_fieldset);
  new_admin.checked = input['admin'];
  create_new_br(new_fieldset);
  
  var cur_count = counter + 0;
  create_new_delete_button(new_fieldset, cur_count);
  
  var f = new field(new_fieldset, new_title, new_type, new_core, new_admin);
  field_dict[cur_count] = f;
  counter++;
  
  form.appendChild(new_fieldset);
}
