var days = new Array("Sat", "Sun", "Mon", "Tues", "Weds", "Thurs", "Fri", "Sat", "Sun");
var verboseDays = new Array("Saturday, Jan 16", "Sunday, Jan 17", "Monday, Jan 18", "Tuesday, Jan 19", "Wednesday, Jan 20", "Thursday, Jan 21", "Friday, Jan 22", "Saturday, Jan 23", "Sunday, Jan 24");
var dates = new Array(16, 17, 18, 19, 20, 21, 22, 23, 24);
var BEGIN_DATE = 16;
var END_DATE = 25;
var BEGIN_HOUR = 1;
var END_HOUR = 24;

var currentDay = -1;

function fillOverview() {
  $.get("/webapps/paideia/count", function(counts) {
    counts = counts.split(",");
    for (i = 0; i < counts.length; i++) {
      if (counts[i] == 0) continue;

      var day = i % days.length + BEGIN_DATE;
      var hour = Math.floor(i / days.length) + BEGIN_HOUR;
      var dots = "";
      for (j = 0; j < counts[i]; j++) {
        dots += "&bull;";
      }
      $("#jan-" + day + "-" + hour).append(dots);
    }
  });
}

function examineDay(index) {
  if (index == currentDay) return;

  $("#listingWrapper").slideUp();

  $.post("/webapps/paideia/listing", {day:"" + index}, function(classes) {
    $("#listingWrapper").empty();
    $("#listingWrapper").append(classes);
    $(".listingDescription").hide();
    $("#listingWrapper").slideDown();
    document.location = "#classes";
  });

  currentDay = index;
}

function moreInfo(class_id) {
  if ($("#d-" + class_id).css('display') == "none") {  
    $.post("/webapps/paideia/description", {cid:"" + class_id}, function(desc) {
      var info = desc.split("|"); 
      $("#d-" + info[0]).empty();
      $("#d-" + info[0]).append(info[1]);
      $("#d-" + info[0]).slideDown();
    });
  } else {
    $("#d-" + class_id).slideUp();
  }
}

function editClass(class_id) {
  if($("#efd-" + class_id).html() == "") {
    $(".editFormDiv").slideUp();
    $(".editFormDiv").empty();
    $.post("/webapps/paideia/ajax_form", {cid:"" + class_id}, function(info) {
      info = info.split("|");
      $("#efd-" + info[0]).hide();
      $("#efd-" + info[0]).empty();
      $("#efd-" + info[0]).append(info[1]);

      $("#name").val(info[2]);

      $("#fbevent").val(info[3]);
      $("#description").val(info[4]);

      $("#efd-" + info[0]).slideDown();
    });
  }
}

function deleteClass(class_id, class_name) {
  if (!confirm("Are you sure you want to delete \"" + class_name + "\"?")) {
    return;
  }
  
  $("#listing-" + class_id).slideUp();
  $.post("/webapps/paideia/delete", {cid:"" + class_id});
}


function validate_registration(form) {
  if (form.name.value.length == 0) { 
    alert("Your class needs a title!");
    form.name.focus();
    return false;
  }

  if (parseInt(form.length.value) == 0 || isNaN(parseInt(form.length.value))) {
    alert("Please enter the length of the class, in hours.");
    form.length.focus();
    return false;
  }

  if (form.location.value.length == 0) {
    alert("Please enter a location for your class.");
    form.location.focus();
    return false;
  }

  if (form.description.value.length == 0) {
    alert("Please fill out the class description.");
    form.description.focus();
    return false;
  }

  return true;
}

function validate_edit(form) {
  if (form.name.value.length == 0) { 
    alert("Your class needs a title!");
    form.name.focus();
    return false;
  }

  if (form.description.value.length == 0) {
    alert("Please fill out the class description.");
    form.description.focus();
    return false;
  }

  return true;
}

function pause(millis) {
  var start = new Date();
  var now = null;

  do {
    now = new Date();
  } while (now-start < millis);
}
