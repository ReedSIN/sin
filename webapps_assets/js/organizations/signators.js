"use strict";

$(document).ready(function() {
    var sig_template = $('#sig_list_template').html();


    var compile_temp = _.template(sig_template);

    var form = $('#sig_list_search'),
        old_url = form.attr('action'),
        sigs,// Signators go in this scope so we can access them from all functions here
        search_obj;


    function compile_signator(sig) {
        var name = sig.name,
            email = sig.email,
            remove_url = sig.remove_url;

        return compile_temp({ name: name,
                              email: email,
                              remove_url: remove_url});
    }

    $.get(old_url).done(function(response) {
        sigs = response.signators;
        search_obj = new Fuse(sigs, { keys: ["name", "email"] });
        print_sigs(sigs);
    });

    function print_sigs(sigs) {
        console.log(sigs);
        if (sigs == undefined)
            $('#sig-table-container').html('');
        else if (sigs.length == 0)
            $('#sig-table-container').html('');
        else
            $('#sig-table-container').html(sigs.map(compile_signator).reduce(sum));
    }
    function sum(a, b) {return a + b;}

    function update_sig_list() {
        var query = $('#sig_list_search_query').val(),
            new_url = old_url + '?s=' + query;

        // Print them all if query is blank

        if (query == '') print_sigs(sigs);
        else print_sigs(search_obj.search(query));

        return false; // Don't submit the form
    }


    var timer,
        delay = 300; // Have 0.3 sec of delay between updates

    $('#sig_list_search_query').bind('input', function() {
        window.clearTimeout(timer); // reset timer
        timer = window.setTimeout(update_sig_list, delay);
    });
});
