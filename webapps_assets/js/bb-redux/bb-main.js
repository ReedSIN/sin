function classify_active_nav() {
    // Used on-load.
    // TODO: This needs a patch in case we get linked from one of the old pages

    var paath = location.pathname.split("/");
    var leenk1 = $('.other-button a[href^="/' + paath[1] + '/' + paath[2] + '"]');
    var leenk2 = $('nav a[href^="/' + paath[1] + '/' + paath[2] + '"]');

    if (leenk2.length > 1) {
	$("#home-link").addClass('active');
	$("#home-link").addClass('disabled');
	return;
    }

    leenk2.addClass('active');
    leenk2.addClass('disabled');
}
