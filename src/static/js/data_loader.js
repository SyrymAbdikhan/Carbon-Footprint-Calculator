
let dataTable;
$(document).ready(function () {
  dataTable = $('#data').DataTable({
    ajax: '/api/data',
    columns: [
      { data: 'id' },
      { data: 'name' },
      { data: 'energy_co2', searchable: false },
      { data: 'waste_co2', searchable: false },
      { data: 'travel_co2', searchable: false },
      { data: 'total_co2', searchable: false },
      { data: 'created_at', searchable: false }
    ],
  });

  updateData(getData());

  $('#data').on('draw.dt', function () {
    updateData(getData());
  });
});

function getData() {
  let data = getLatestData(getVisibleData());
  data = {
    energy_co2: data.map(d => ({ name: d.name, value: d.energy_co2 })),
    waste_co2: data.map(d => ({ name: d.name, value: d.waste_co2 })),
    travel_co2: data.map(d => ({ name: d.name, value: d.travel_co2 })),
    total: data.map(d => ({ name: d.name, value: d.energy_co2 + d.waste_co2 + d.travel_co2 }))
  };
  return data;
}

function updateData(data) {
  if (data.total.length > 0) {
    updateBarCharts(data);
    updateBoxPlots(data);
  }
}

function getVisibleData() {
  let visibleData = [];
  dataTable.rows({ page: 'current' }).every(function (i) {
    visibleData.push(this.data());
  });
  return visibleData;
}

function getLatestData(data) {
  let latestData = new Map();
  for (const d of data) {
    let existing = latestData.get(d.name);
    if (!existing || new Date(d.created_at) > new Date(existing.created_at)) {
      latestData.set(d.name, d);
    }
  }
  return Array.from(latestData.values());
}
