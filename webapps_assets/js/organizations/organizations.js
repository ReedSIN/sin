"use strict";

$(document).ready(function() {
    var org_template = $('#org_list_template').html();

    var compile_temp = _.template(org_template);

    var form = $('#org_list_search'),
        old_url = form.attr('action'),
        orgs,// Orgs go in this scope so we can access them from all functions here
        search_obj;


    function compile_org(org) {
        var name = org.name,
            signator = org.signator,
            email = org.email,
            id = org.id,
            url = org.url;

        return compile_temp({ name: name,
                              signator: signator,
                              email: email,
                              id: id,
                              url: url});
    }

    $.get(old_url).done(function(response) {
        orgs = response.orgs;
        search_obj = new Fuse(orgs, { keys: ["name", "signator", "email"] });
        print_orgs(orgs);
    });

    function print_orgs(orgs) {
        console.log(orgs);
        if (orgs == undefined)
            $('#org-table-container').html('');
        else if (orgs.length == 0)
            $('#org-table-container').html('');
        else
            $('#org-table-container').html(orgs.map(compile_org).reduce(sum));
    }
    function sum(a, b) {return a + b;}

    function update_org_list() {
        var query = $('#org_list_search_query').val(),
            new_url = old_url + '?s=' + query;

        var options = { extract: function(d) { return d.name; } };

        // Print them all if query is blank

        if (query == '') print_orgs(orgs);
        else print_orgs(search_obj.search(query));

        return false; // Don't submit the form
    }


    var timer,
        delay = 300; // Have 0.3 sec of delay between updates

    $('#org_list_search_query').bind('input', function() {
        window.clearTimeout(timer); // reset timer
        timer = window.setTimeout(update_org_list, delay);
    });

        //submit(update_org_list);
});
