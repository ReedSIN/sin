// the functions that should be placed in the on-load for the homepage
function say_hello(){
    $(".greeting").removeClass("hide-o");
};

function hide_info_sections(n){
    $(".home-info-section").hide(n);
    $(".greeting .btn-group button").each(function(i,v){
	var dis_btn = $(v);
	if (dis_btn.data("appName") !== "elect" && dis_btn.hasClass("disabled")) {
	    dis_btn.removeClass("disabled");
	    console.log("Seriously did this actually work seriously?"); // test
	} 
    });
};

function set_btn_events(){
    $(".greeting .btn-group button").click(function(e){
	hide_info_sections(400);
	$(this).addClass("disabled");
	$("h1.hello, h2.iam, .greeting p.caudex").hide(700);
	var app_name = $(this).data("appName");
	// console.log(app_name); // test
	var app_obj = $('#' + app_name);
	// console.log(app_obj); // test
	app_obj.show(1500);
    });
};

