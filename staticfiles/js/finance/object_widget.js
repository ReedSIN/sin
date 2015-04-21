function budget_item() {

}

function text_field_widget() {
  var text_field = document.createElement('input');
  text_field.type = 'text';
  text_field.className = 'text_field_widget';
  return text_field;
}

function text_area_widget() {
  var text_area = document.createElement('textarea');
  text_field.className = 'text_area_widget';
  return text_area;
}

function budget(organization_widget, email_widget, description_widget) {
  this.organization = organization_widget;
  this.email = email_widget;
  this.description = description_widget;
  this.budget_items = [];
  
  this.add_budget_item = function(widget, name, description, requested) {
    this.budget_items.push(new budget_item(widget, name, description, requested));
  };
  
  this.remove_budget_item = function(widget) {
    for(var i = 0;i < this.budget_items.length;i++) {
      var budget_item = this.budget_items[i];
      if (budget_item.widget == widget) {
	this.budget_items.splice(i,i+1);
      }
    }
  };
  
  this.update_model = function() {

  };

  this.submit = function() {
    if (null == organization) {
      alert('Can not submit if organization is null');
      return;
    }
    
    if (null == email) {
      alert('Can not submit if email is null');
      return;
    }
    
    if (null == description) {
      alert('Can not submit if description is null');
    }
  };
}

function 

function object_widget() {
  
  this.model = budget();
  
  this.outer_div = document.createElement('div');
  this.outer_div.id = 'ow-outer-div';
  
  this.inner_div_left = document.createElement('div');
  this.inner_div_left.id = 'ow-inner-div-right';
  this.outer_div.appendChild(this.inner_div_left);
  
  this.inner_div_right = document.createElement('div');
  this.inner_div_right.id = 'ow-inner-div-left';
  this.outer_div.appendChild(this.inner_div_right);
  
  this.inner_div_left_top = document.createElement('div');
  this.inner_div_left_top.id = 'ow-inner-div-left-top';
  this.inner_div_left.appendChild(this.inner_div_left_top);
  
  this.inner_div_left_bottom = document.createElement('div');
  this.inner_div_left_bottom.id = 'ow-inner-div-left-bottom';
  this.inner_div_left.appendChild(this.inner_div_left_buttom);
  
  this.inner_div_right_top = 
}
