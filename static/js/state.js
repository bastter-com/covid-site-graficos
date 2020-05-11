const chartNavLinks = document.getElementsByClassName('chart-nav-link');

$('tbody').each(function () {
  var list = $(this).children('tr');
  $(this).html(list.get().reverse());
});

function createChart(data) {
  let chart = {
    type: 'line',
    data: {
      labels: data['labels'],
      datasets: data['datasets'],
    },
    options: {
      responsive: true,
      elements: {
        point: {
          radius: 0,
          hoverRadius: 5,
        },
      },
      title: {
        display: true,
        text: data['title'],
        fontSize: 24,
      },
      tooltips: {
        mode: 'index',
        intersect: false,
      },
      hover: {
        mode: 'nearest',
        intersect: true,
      },
      maintainAspectRatio: false,
      scales: {
        xAxes: [
          {
            display: true,
            scaleLabel: {
              display: true,
              labelString: data['labelXAxis'],
            },
          },
        ],
        yAxes: [
          {
            display: true,
            scaleLabel: {
              display: true,
              labelString: data['labelYAxis'],
            },
          },
        ],
      },
    },
  };
  return chart;
}

const dataForChartOne = {
  labels: detailStateData['dates'],
  datasets: [
    {
      label: 'Casos',
      borderColor: '#02c20e',
      data: detailStateData['new_confirmed'],
      fill: false,
    },
    {
      label: 'Mortes',
      borderColor: '#cf3c48',
      data: detailStateData['new_deaths'],
      fill: false,
      pointStyle: 'null',
    },
  ],
  title: `Números novos de casos e mortes por dia - ${stateName}`,
  labelXAxis: 'Data',
  labelYAxis: 'Casos / Mortes',
};

const dataForChartTwo = {
  labels: detailStateData['dates'],
  datasets: [
    {
      label: 'Casos',
      borderColor: '#256dd9',
      data: detailStateData['confirmed'],
      fill: false,
    },
    {
      label: 'Mortes',
      borderColor: '#cf3c48',
      data: detailStateData['deaths'],
      fill: false,
      pointStyle: 'null',
    },
  ],
  title: `Evolução números totais de casos e mortes - ${stateName}`,
  labelXAxis: 'Data',
  labelYAxis: 'Casos / Mortes',
};

let chartOne = createChart(dataForChartOne);

let chartTwo = createChart(dataForChartTwo);

window.onload = function () {
  // chart one
  var ctxOne = document.getElementById('chart').getContext('2d');
  var chartOneInline = new Chart(ctxOne, chartOne);
  window.myLine = chartOneInline;

  // chart two
  var ctxTwo = document.getElementById('chart-2').getContext('2d');
  var chartTwoInline = new Chart(ctxTwo, chartTwo);
  window.myLine = chartTwoInline;

  function updateChart(chart, axesType) {
    chart.options.scales.yAxes[0].type = axesType;
    chart.update();
  }
  for (let i = 0; i < chartNavLinks.length; i++) {
    chartNavLinks[i].addEventListener('click', () => {
      if (chartNavLinks[i].classList.contains('linear')) {
        let containerParentId =
          chartNavLinks[i].parentNode.parentNode.parentNode.id;
        let idChart = containerParentId.split('-')[
          containerParentId.split('-').length - 1
        ];
        chartNavLinks[i].classList.add('active');
        chartNavLinks[i + 1].classList.remove('active');
        switch (idChart) {
          case '1':
            updateChart(chartOneInline, 'linear');
            break;
          case '2':
            updateChart(chartTwoInline, 'linear');
            break;
        }
      } else if (chartNavLinks[i].classList.contains('logarithm')) {
        let containerParentId =
          chartNavLinks[i].parentNode.parentNode.parentNode.id;
        let idChart = containerParentId.split('-')[
          containerParentId.split('-').length - 1
        ];
        chartNavLinks[i].classList.add('active');
        chartNavLinks[i - 1].classList.remove('active');
        switch (idChart) {
          case '1':
            updateChart(chartOneInline, 'logarithmic');
            break;
          case '2':
            updateChart(chartTwoInline, 'logarithmic');
            break;
        }
      }
    });
  }
};
