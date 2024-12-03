function updateSingleBoxPlot(_id, data, color) {
  d3.select(_id).html('');

  const margin = { top: 20, right: 30, bottom: 40, left: 70 },
    width = 270 - margin.left - margin.right,
    height = 350 - margin.top - margin.bottom;

  const svg = d3.select(_id)
    .append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);

  const parsedData = data.map(d => d.value).sort(d3.ascending);
  var q1 = d3.quantile(parsedData, .25);
  var median = d3.quantile(parsedData, .5);
  var q3 = d3.quantile(parsedData, .75);
  var interQuantileRange = q3 - q1;
  const min = Math.max(d3.min(parsedData), q1 - 1.5 * interQuantileRange);
  const max = Math.min(d3.max(parsedData), q3 + 1.5 * interQuantileRange);

  var y = d3.scaleLinear()
    .domain([0, d3.max([max, 1])])
    .range([height, 0]);

  svg.call(d3.axisLeft(y).ticks(5))
    .style('font-size', '0.8rem');

  const center = width / 2;
  const boxWidth = 100;

  svg.append('line')
    .attr('x1', center)
    .attr('x2', center)
    .attr('y1', y(min))
    .attr('y2', y(max))
    .attr('stroke', 'black');

  svg.append('rect')
    .attr('x', center - boxWidth / 2)
    .attr('y', y(q3))
    .attr('height', y(q1) - y(q3))
    .attr('width', boxWidth)
    .attr('stroke', 'black')
    .style('fill', color);

  [min, median, max].forEach(value => {
    svg.append('line')
      .attr('x1', center - boxWidth / 2)
      .attr('x2', center + boxWidth / 2)
      .attr('y1', y(value))
      .attr('y2', y(value))
      .attr('stroke', 'black');
  });
}

function updateBoxPlots(data) {
  updateSingleBoxPlot('#box-plot-energy', data.energy_co2, '#6875f5');
  updateSingleBoxPlot('#box-plot-waste', data.waste_co2, '#ff5b1f');
  updateSingleBoxPlot('#box-plot-travel', data.travel_co2, '#0695a2');
  updateSingleBoxPlot('#box-plot-total', data.total, '#6c757d');
}
