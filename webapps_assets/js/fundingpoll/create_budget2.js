String.prototype.trim = function() {
  return this.replace(/^\s+|\s+$/g,"");
}

counter = 0;
budgetitem_dict = {};

function con_budgetitem(fieldset,args) {
  var new_widget = document.createElement('fieldset');
  this.widget = new_widget;
  
  function add_textfield(label,contents) {
    var new_div = document.createElement('div');
    new_div.className = 'object-div';
    
    var new_div_title = document.createElement('div');
    new_div_title.className = 'object-div-small-gap-title';
    new_div.appendChild(new_div_title);
    
    var new_div_content = document.createElement('div');
    new_div_content.className = 'object-div-content';
    new_div.appendChild(new_div_content);
    
    var new_label = document.createElement('label');
    new_label.innerHTML = label;
    new_div_title.appendChild(new_label);
    
    var input = document.createElement('input');
    input.type = 'text';
    input.className = 'form-control';
    input.value = contents;
    new_div_content.appendChild(input);
    
    new_widget.appendChild(new_div);
    
    return input;
  }
  
  function add_textarea(label,contents) {
    var new_div = document.createElement('div');
    new_div.className = 'object-div';
    
    var new_div_title = document.createElement('div');
    new_div_title.className = 'object-div-textarea-small-gap-title';
    new_div.appendChild(new_div_title);
    
    var new_div_content = document.createElement('div');
    new_div_content.className = 'object-div-textarea-content';
    new_div.appendChild(new_div_content);

    var new_label = document.createElement('label');
    new_label.innerHTML = label;
    new_div_title.appendChild(new_label);
    
    var input = document.createElement('textarea');
    input.className = 'budgetitem-textarea';
    input.innerHTML = contents;
    
    new_div_content.appendChild(input);
    
    var hr = document.createElement('hr');
      hr.className = 'featurette-divider';
    new_widget.appendChild(new_div);

      if (label === 'Requested: ') {
	  new_widget.appendChild(hr);
      }
    
    return input;
  }
  
  function add_constant(label, contents) {
    var new_div = document.createElement('div');
    new_div.className = 'object-div';
    
    var new_div_title = document.createElement('div');
    new_div_title.className = 'object-div-small-gap-title';
    new_div.appendChild(new_div_title);
    
    var new_div_content = document.createElement('div');
    new_div_content.className = 'object-div-content';
    new_div.appendChild(new_div_content);
    
    var new_label = document.createElement('label');
    new_label.innerHTML = label;
    new_div_title.appendChild(new_label);
    

    var input = document.createElement('input');
    input.type = 'text';
    input.value = contents;
    input.readOnly = true;
    new_div_content.appendChild(input);
    
    new_widget.appendChild(new_div);

    var hr = document.createElement('hr');
    hr.className = 'featurette-divider';

    
    return input;
  }
  
  
  function create_new_delete_button(count) {
    var new_delete_link = document.createElement('input');
    new_delete_link.type = 'submit';
    new_delete_link.className = 'btn btn-priamry';
    new_delete_link.value = 'Delete Budget Item';
    new_delete_link.onclick = function() {
      var answer = confirm("Are you sure you wish to delete this budget item?");
      
      if (answer) {
        new_widget.parentNode.removeChild(new_widget);
        delete budgetitem_dict[count];
      }
      
      return false;
    }
    
      var hr = document.createElement('hr');
      hr.className = 'featurette-divider';
      
    
    new_widget.appendChild(new_delete_link);
      new_widget.appendChild(hr);
    return new_delete_link;
  }
  
  if ('name' in args)
    this.name = add_constant('Name: ',args['name']);
  else
    this.name = add_constant('Name: ','');
  
  if ('description' in args)
    this.description = add_textarea('Description: ',args['description']);
  else 
    this.description = add_textarea('Description: ','');
  
  if ('requested' in args)
    this.requested = add_textfield('Requested: ',args['requested']);
  else
    this.requested = add_textfield('Requested: ','');
  /*create_new_delete_button(counter);*/
  fieldset.insertBefore(new_widget, document.getElementById('add-new-budgetitem-link'));
}


function budgetitem(args) {
  var fieldset = document.getElementById('budget-item-fieldset');
  var i = new con_budgetitem(fieldset,args);
  budgetitem_dict[counter] = i;
  counter++;
  return i;
}


function submit_form(form, url) {
  var new_form = document.createElement('form');
  new_form.method = 'post';
  //new_form.action = '/webapps/fundingpoll/budgets/save/' + budgetID;
  new_form.action = url;
  new_form.style.visibility = 'hidden';
  document.getElementById('create-budget-fieldset').appendChild(new_form);

  var csrf_token = document.getElementById('token');
  new_form.appendChild(csrf_token);

  var query = {};
  var org_select = document.getElementById('organization_select');
  query['organization'] = org_select.options[org_select.selectedIndex].value;
  query['description'] = document.getElementById('description-textarea').value;
  
  query['budget_items'] = new Array();
  for(var f in budgetitem_dict) {
    var query_item = {};
    var model = budgetitem_dict[f];
    query_item['name'] = model.name.value;
    query_item['description'] = model.description.value;
    query_item['requested'] = model.requested.value;
    query['budget_items'].push(query_item);
  }
  var query_string = JSON.stringify(query);
  var new_input = document.createElement('input');
  new_input.type = 'text';
  new_input.name = 'query_string';
  new_input.value = query_string;
  new_input.style.visibility = 'hidden';
  new_form.appendChild(new_input);
  new_form.submit();
}
