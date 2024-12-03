
function updateSingleBarChart(_id, data, color) {
  d3.select(_id).html('');

  const margin = { top: 20, right: 30, bottom: 40, left: 70 },
    width = 970 - margin.left - margin.right,
    height = 350 - margin.top - margin.bottom;

  const svg = d3.select(_id)
    .append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);

  const parsedData = data.map(d => ({
    name: d.name,
    value: d.value
  }))
    .sort((a, b) => {
      return d3.ascending(a.value, b.value);
    });

  const x = d3.scaleBand()
    .domain(parsedData.map(d => d.name))
    .range([0, width])
    .padding(0.2);

  const y = d3.scaleLinear()
    .domain([0, d3.max(parsedData, d => d.value)])
    .range([height, 0]);

  svg.selectAll('rect')
    .data(parsedData)
    .enter()
    .append('rect')
    .attr('x', d => x(d.name) + x.bandwidth() * 0.1)
    .attr('y', d => y(d.value))
    .attr('width', x.bandwidth() * 0.8)
    .attr('height', d => height - y(d.value))
    .attr('fill', color);

  svg.append('g')
    .attr('transform', `translate(0,${height})`)
    .call(d3.axisBottom(x))
    .selectAll('text')
    .attr('transform', 'rotate(-15)')
    .style('text-anchor', 'end')
    .style('font-size', '0.8rem');

  svg.append('g')
    .call(d3.axisLeft(y))
    .style('font-size', '0.8rem');
}

function updateBarCharts(data) {
  updateSingleBarChart('#bar-chart-total', data.total, '#6c757d')
  updateSingleBarChart('#bar-chart-energy', data.energy_co2, '#6875f5');
  updateSingleBarChart('#bar-chart-waste', data.waste_co2, '#ff5b1f');
  updateSingleBarChart('#bar-chart-travel', data.travel_co2, '#0695a2');
}
