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

// Chart dimensions.
var margin = {top: 19.5, right: 19.5, bottom: 19.5, left: 39.5},
    width = 900 - margin.right,
    height = 500 - margin.top - margin.bottom;




// Create the SVG container and set the origin.
var svg = chart.append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


// Load the data.
d3.json("/static/data/results_json.json", function(data) {
    var orgs = data.fp_orgs;

    // Various scales. These domains make assumptions of data, naturally.
    var xScale = d3.scale.linear()
            .domain([0,d3.max(orgs.map(disapprove))])
            .range([0, width]),
        yScale = d3.scale.linear()
            .domain([0,d3.max(orgs.map(approve))])
            .range([height, 0]),
        radiusScale = d3.scale.sqrt().domain([0,d3.max(orgs.map(points))]).range([0, 40]),
        colorScale = d3.scale.category10();

    // The x & y axes.
    var xAxis = d3.svg.axis().orient("bottom")
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
    var tip_template = _.template($('#template-org').html());
    var makeTemplate = function (d) {
        return tip_template({name: name(d),
                            points: points(d),
                            approve: approve(d),
                            noopinion: noopinion(d),
                            disapprove: disapprove(d),
                            deepsix: deepsix(d)});
    };
    var tip = d3.tip().attr('class', 'd3-tip').html(makeTemplate);
    svg.call(tip);

    svg.append('g')
        .selectAll('circle')
        .data(orgs)
        .enter()
        .append('circle')
        .attr('cx', function (d) { return xScale(disapprove(d)); })
        .attr('cy', function (d) { return yScale(approve(d)); })
        .attr('r', function (d) { return radiusScale(points(d)); })
        .classed('org-circle', true)
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);
});
