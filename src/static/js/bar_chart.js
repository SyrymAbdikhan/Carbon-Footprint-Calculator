
function updateSingleBarChart(_id, data, color) {
  d3.select(_id).html('');

  const margin = { top: 20, right: 30, bottom: 40, left: 70 },
    width = 1200 - margin.left - margin.right,
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
  }));

  parsedData.sort(function (a, b) {
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
    .attr('x', d => x(d.name) + x.bandwidth()*0.1)
    .attr('y', d => y(d.value))
    .attr('width', x.bandwidth()*0.8)
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

function updateBarChart(data) {
  const parsedData = {
    energy_co2: data.map(d => ({ name: d.name, value: d.energy_co2 })),
    waste_co2: data.map(d => ({ name: d.name, value: d.waste_co2 })),
    travel_co2: data.map(d => ({ name: d.name, value: d.travel_co2 })),
    total: data.map(d => ({ name: d.name, value: d.energy_co2 + d.waste_co2 + d.travel_co2 }))
  };
  updateSingleBarChart('#bar-chart-total', parsedData.total, '#6c757d')
  updateSingleBarChart('#bar-chart-energy', parsedData.energy_co2, '#6875f5');
  updateSingleBarChart('#bar-chart-waste', parsedData.waste_co2, '#ff5b1f');
  updateSingleBarChart('#bar-chart-travel', parsedData.travel_co2, '#0695a2');
}
