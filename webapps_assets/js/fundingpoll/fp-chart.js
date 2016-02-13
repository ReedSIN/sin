var fp_results_chart = (function() {
    /* Initialize Chart */
    var chart = d3.select('#top-chart');

    // Accessor functions
    function name(d) { return d.name; }
    function signator(d) { return d.signator; }
    function points(d) { return d.points; }
    function topsix(d) { return d.topsix; }
    function approve(d) { return d.approve; }
    function noopinion(d) { return d.noopinion; }
    function disapprove(d) { return d.disapprove; }
    function deepsix(d) { return d.deepsix; }
    function dis_deep(d) { return disapprove(d) + deepsix(d); }
    function app_top(d) { return approve(d) + topsix(d); }

    // Chart dimensions.
    var margin = {top: 19.5, right: 19.5, bottom: 19.5, left: 39.5},
        width = 700 - margin.right,
        height = 500 - margin.top - margin.bottom;

    // Create the SVG container and set the origin.
    var svg = chart.append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    d3.json("/static/data/results_json.json", init_chart);

    // We need these variables in this scope.
    var orgs, xScale, yScale, radiusScale, colorScale, xAxis, yAxis;

    /* Functions! */

    /**
     * @function update_top_deep updates chart to show top sixes versus deep sixes
     */
    var update_app_dis = update_general(disapprove, approve, "disapprovals", "approvals"),
        update_top_deep = update_general(deepsix, topsix, "deep sixes", "top sixes"),
        update_hybrid = update_general(dis_deep, app_top, "disapprovals + deep sixes",
                                      "approvals + top sixes");

    function init_chart(data) {
        orgs = data.fp_orgs;

        // Various scales. These domains make assumptions of data, naturally.
        xScale = d3.scale.linear()
            .domain([0,d3.max(orgs.map(disapprove))])
            .range([0, width]),
        yScale = d3.scale.linear()
            .domain([0,d3.max(orgs.map(approve))])
            .range([height, 0]),
        radiusScale = d3.scale.sqrt().domain(d3.extent(orgs.map(points))).range([1, 15]),

        // The x & y axes.
        xAxis = d3.svg.axis().orient("bottom")
            .scale(xScale).ticks(6, d3.format(",d"))
            .tickSize(-height,0)
            .tickPadding(10),
        yAxis = d3.svg.axis().scale(yScale).orient("left")
            .ticks(6)
            .tickSize(-width)
            .tickPadding(10,0);


        // Add the x-axis.
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        // Add the y-axis.
        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis);

        // Add an x-axis label.
        svg.append("text")
            .attr("class", "x label")
            .attr("text-anchor", "end")
            .attr("x", width)
            .attr("y", height - 6)
            .text("disapprovals");

        // Add a y-axis label.
        svg.append("text")
            .attr("class", "y label")
            .attr("text-anchor", "end")
            .attr("y", 6)
            .attr("dy", ".75em")
            .attr("transform", "rotate(-90)")
            .text("approvals");

        // Tooltips
        var tip_template = _.template($('#template-org-tooltip').html());
        var makeTemplate = function (d) {
            return tip_template({name: name(d),
                                 points: points(d),
                                 topsix: topsix(d),
                                 approve: approve(d),
                                 noopinion: noopinion(d),
                                 disapprove: disapprove(d),
                                 deepsix: deepsix(d)});
        };
        var tip = d3.tip()
                .direction('e')
                .attr('class', 'd3-tip')
                .html(makeTemplate);
        svg.call(tip);

        svg.append('g')
            .classed('circles', true)
            .selectAll('circle')
            .data(orgs)
            .enter()
            .append('circle')
            .classed('org-circle', true)
            .on('mouseover', tip.show)
            .on('mouseout', tip.hide)
            .on('click', select_org)
            .attr('cx', sequence(disapprove, xScale))
            .attr('cy', sequence(approve, yScale))
            .attr('r', sequence(points, radiusScale));


    }

    function update_general(x_access, y_access, x_label, y_label) {
        return function() {
            // Update scales
            xScale = d3.scale.linear()
                .domain([0,d3.max(orgs.map(x_access))])
                .range([0, width]);
            yScale = d3.scale.linear()
                .domain([0,d3.max(orgs.map(y_access))])
                .range([height, 0]);

            // Update Axes
            xAxis = xAxis.scale(xScale);
            yAxis = yAxis.scale(yScale);
            svg.select(".y.axis").transition()
                .call(yAxis);
            svg.select(".x.axis").transition()
                .call(xAxis);

            // Update Axes Labels
            svg.select(".x.label")
                .text(x_label);
            svg.select(".y.label")
                .text(y_label);

            // Update points
            svg.selectAll('circle')
                .transition()
                .attr('cx', sequence(x_access, xScale))
                .attr('cy', sequence(y_access, yScale));
        };
    }
    // Org panel
    var info_template = _.template($('#template-org-panel').html());
    function make_info(d) {
        return info_template({name: name(d),
                             points: points(d),
                             topsix: topsix(d),
                             approve: approve(d),
                             noopinion: noopinion(d),
                             disapprove: disapprove(d),
                             deepsix: deepsix(d)});
    }
    function select_org(d) {
        // deselect other elements
        svg.select('circles').classed('selected', false);
        // select element
        d3.select(this).classed('selected', true);
        // render org info panel
        $('#org-info-panel').html(make_info(d));
    }

    return { update_app_dis: update_app_dis,
             update_top_deep: update_top_deep,
             update_hybrid: update_hybrid };
})();


// Add event handlers
(function() {
    var buttons = $('#plot-choices').children();

    $('#app_dis').click(select_new_plot('app_dis', fp_results_chart.update_app_dis));
    $('#top_deep').click(select_new_plot('top_deep', fp_results_chart.update_top_deep));
    $('#hybrid').click(select_new_plot('hybrid', fp_results_chart.update_hybrid));

    function select_new_plot(name, update_function) {
        return function() {
            buttons.removeClass('active');
            $('#' + name).addClass('active');
            update_function();
            return false;
        };
    }
})();


/**
 * @function sequence takes any number of functions and returns their left-to-right composition
 */
function sequence() {
    var fns = arguments;
    return function (result) {
        for (var i = 0; i < fns.length; i++) {
            result = fns[i].call(this, result);
        }
        return result;
    };
};
