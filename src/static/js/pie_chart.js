
var total = parseFloat(document.querySelector('#data').getAttribute('data-total'));
var data = [...document.querySelectorAll('#data>div')].map(div => {
    return {
        label: div.getAttribute('data-title'),
        value: parseFloat(div.getAttribute('data-value')) * 100 / total
    };
});

var width = 700,
    height = 450,
    radius = Math.min(width, height) / 2;

var svg = d3.select("#donut")
    .append("svg")
    .attr("viewBox", `0 0 ${width} ${height}`)
    .attr("class", "max-w-xl mx-auto")
    .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

svg.append("g")
    .attr("class", "slices");
svg.append("g")
    .attr("class", "labels");
svg.append("g")
    .attr("class", "lines");

var pie = d3.pie()
    .sort(null)
    .value(function(d) {
        return d.value;
    });

var arc = d3.arc()
    .outerRadius(radius * 0.8)
    .innerRadius(radius * 0.4);

var outerArc = d3.arc()
    .innerRadius(radius * 0.9)
    .outerRadius(radius * 0.9);

var color = d3.scaleOrdinal()
    .range(["#6875f5", "#ff5b1f", "#0695a2"]);

var key = function(d){ return d.data.label; };

function midAngle(d){
    return d.startAngle + (d.endAngle - d.startAngle)/2;
}

/* ------- PIE SLICES ------- */
var slice = svg.select(".slices").selectAll("path.slice")
    .data(pie(data), key)
    .enter()
    .insert("path")
    .style("fill", function(d) { return color(d.data.label); })
    .attr("class", "slice")
    .attr("d", arc);

slice.exit().remove();

/* ------- TEXT LABELS ------- */
var text = svg.select(".labels").selectAll("text")
    .data(pie(data), key)
    .enter()
    .append("text")
    .style("text-anchor", function(d){
        return midAngle(d) < Math.PI ? "start":"end";
    });

text.append("tspan")
    .attr("x", "0")
    .attr("dy", "-0.3em")
    .attr("font-weight", "bold")
    .attr("font-size", "120%")
    .text(function(d) {
        return d.data.label;
    });
text.append("tspan")
    .attr("x", "0")
    .attr("dy", "1.2em")
    .text(function(d) {
        return d.data.value.toFixed(2) + " %";
    });

text.attr("transform", function(d) {
    var pos = outerArc.centroid(d);
    pos[0] = radius * 0.95 * (midAngle(d) < Math.PI ? 1 : -1);
    return "translate("+ pos +")";
})

/* ------- SLICE TO TEXT POLYLINES ------- */
var polyline = svg.select(".lines").selectAll("polyline")
    .data(pie(data), key)
    .enter()
    .append("polyline")
    .attr("style", "opacity: .3; stroke: black; stroke-width: 2px; fill: none;")
    .attr("points", function(d){
        var pos = outerArc.centroid(d);
        pos[0] = radius * 0.9 * (midAngle(d) < Math.PI ? 1 : -1);
        return [arc.centroid(d), outerArc.centroid(d), pos];
    });
