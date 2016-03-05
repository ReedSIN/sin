"use strict";

$(document).ready(function() {
    var org_template = $('#org_list_template').html();

    var compile_temp = _.template(org_template);

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

    $.get('/search_orgs').done(print_orgs);

    function print_orgs(response) {
        var orgs = response.orgs;
        if (orgs.length == 0)
            $('#org-table-container').html('');
        else
            $('#org-table-container').html(orgs.map(compile_org).reduce(sum));
    }
    function sum(a, b) {return a + b;}

    function update_org_list() {
        var form = $('#org_list_search'),
            old_url = form.attr('action'),
            query = $('#org_list_search_query').val(),
            new_url = old_url + '?s=' + query;

        $.get(new_url).done(print_orgs);

        return false;
    }

    $('#org_list_search').submit(update_org_list);
});
