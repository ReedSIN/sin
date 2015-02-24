
function czarEdit(class_id) {
  if($("#efd-" + class_id).html() == "") {
    $(".editFormDiv").slideUp();
    $(".editFormDiv").empty();
    $.post("/webapps/paideia/ajax_form", {cid:"" + class_id}, function(info) {
      info = info.split("|");
      $("#efd-" + info[0]).hide();
      $("#efd-" + info[0]).empty();
      $("#efd-" + info[0]).append(info[1]);

      $("#name").val(info[2]);
      var hour = parseInt(info[5]) - BEGIN_HOUR;
      var day = parseInt(info[6]) - BEGIN_DATE;
      $("#hour option").removeAttr("selected");
      $("#hour option:eq("+hour+")").attr("selected","selected");
      $("#day option").removeAttr("selected");
      $("#day option:eq("+day+")").attr("selected", "selected");

      $("#length").val(info[7]);
      $("#location").val(info[8]);
      $("#fbevent").val(info[3]);
      $("#description").val(info[4]);
      $("#teacher").val(info[9]);
      $("#notes").val(info[10]);
      
      $("#ajaxForm").ajaxForm({success: showResponse});

      $("#efd-" + info[0]).slideDown();
    });
  }
}

function showResponse(responseText, statusText) {
  info = responseText.split("|");

  $("#listing-" + info[0]).slideUp();
  $("#listing-" + info[0]).empty();
  $("#listing-" + info[0]).append(info[1]);
  $("#listing-" + info[0]).slideDown();

}
