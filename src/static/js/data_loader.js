
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

  updateBarChart(getFilteredData());

  $('#data').on('draw.dt', function () {
    updateBarChart(getFilteredData());
  });
});

function getFilteredData() {
  return getLatestData(getVisibleData());
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
