
function updateBarChart(data) {
  d3.select('#barChart').html('');

  const margin = { top: 20, right: 30, bottom: 40, left: 70 },
    width = 1200 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

  const svg = d3.select('#barChart')
    .append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);

  const categories = ['Energy Usage', 'Waste', 'Travel'];
  const parsedData = data.map(d => ({
    name: d.name,
    values: [
      { category: 'Energy Usage', value: d.energy_co2 },
      { category: 'Waste', value: d.waste_co2 },
      { category: 'Travel', value: d.travel_co2 },
    ],
  }));

  parsedData.sort(function (a, b) {
    return d3.ascending(a.name, b.name)
  });

  const x0 = d3.scaleBand()
    .domain(parsedData.map(d => d.name))
    .range([0, width])
    .padding(0.2);

  const x1 = d3.scaleBand() // Sub-bars
    .domain(categories)
    .range([0, x0.bandwidth()])
    .padding(0.1);

  const y = d3.scaleLinear()
    .domain([0, d3.max(parsedData, d => d3.max(d.values, v => v.value))])
    .range([height, 0]);

  const color = d3.scaleOrdinal()
    .domain(categories)
    .range(["#6875f5", "#ff5b1f", "#0695a2"]);

  const groups = svg.selectAll('g.group')
    .data(parsedData)
    .enter()
    .append('g')
    .attr('class', 'group')
    .attr('transform', d => `translate(${x0(d.name)},0)`);

  groups.selectAll('rect')
    .data(d => d.values)
    .enter()
    .append('rect')
    .attr('x', d => x1(d.category))
    .attr('y', d => y(d.value))
    .attr('width', x1.bandwidth())
    .attr('height', d => height - y(d.value))
    .attr('fill', d => color(d.category));

  // X axis Categories
  svg.append('g')
    .attr('transform', `translate(0,${height})`)
    .call(d3.axisBottom(x0))
    .selectAll('text')
    .attr('transform', 'rotate(-15)')
    .style('text-anchor', 'end')
    .style('font-size', '0.8rem');

  // Y axis Values
  svg.append('g')
    .call(d3.axisLeft(y))
    .style('font-size', '0.8rem');

  const legend = svg.append('g')
    .attr('transform', `translate(${width - 100}, 0)`);

  categories.forEach((cat, i) => {
    legend.append('rect')
      .attr('x', 0)
      .attr('y', i * 20)
      .attr('width', 10)
      .attr('height', 10)
      .attr('fill', color(cat));

    legend.append('text')
      .attr('x', 15)
      .attr('y', i * 20 + 6)
      .text(cat)
      .style('font-size', '12px')
      .attr('alignment-baseline', 'middle');
  });
}
