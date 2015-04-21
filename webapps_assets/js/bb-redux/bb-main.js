// BB (7/5/2014)
// this fires a bunch of CSS animations when the sidebar is toggled
function toggle_sidebar() {
       // the "revealing" is a shitty hack.
       // makes the small "s""i""n" circles change from right to left OR left to right
       // (depends on where the sidebar is)
    var revealing = false;
    if ($(".side-bar").hasClass("hide-bar")) {
        revealing = true;
    }
    $(".side-bar, .app-name, #toggle-button, .other-button a, top-bar .sin-letters p")
	.toggleClass("hide-bar");
    $("#toggle-button span").toggleClass("flipY-glyph");
    $(".sin-letter").each(function(index) {
        var letter = $(this);
        var i = 2 - index;
        if (revealing) {
            i = index;
        }
        setTimeout(function() {
            letter.toggleClass("hide-bar");
        },100*(i));
    });
}

// this is used on-load
// flips the fire and then flips it back
function wmd_poi() {
    var fire = $("#toggle-button span");
    fire.toggleClass("flipX-glyph");
    setTimeout(function() {
        fire.toggleClass("flipX-glyph");
    },600);
};

// used on-load
function classify_active_nav() {
    // this needs a patch in case we get linked from one of the old pages

    var paath = location.pathname.split("/");
    var leenk1 = $('.other-button a[href^="/' + paath[1] + '/' + paath[2] + '"]');
    var leenk2 = $('nav a[href^="/' + paath[1] + '/' + paath[2] + '"]');
    //console.log(leenk1); // for testing
    //console.log(leenk2); // for testing
    // leenk1.addClass('disabled'); // I kind of like having that button up there on the home page
    if (leenk2.length > 1) {
	$("#home-link").addClass('active');
	$("#home-link").addClass('disabled');
	return
    }
    leenk2.addClass('active');
    leenk2.addClass('disabled');
    //console.log(leenk1); // for testing
    //console.log(leenk2); // for testing
};