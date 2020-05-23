const chartNavLinks = document.getElementsByClassName('chart-nav-link');
let mapChartTitle = document.getElementById('geochart-title');

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
      label: 'Casos - MM',
      borderColor: '#014a0f',
      data: detailStateData['new_confirmed_moving_average'],
      fill: false,
      borderDash: [6, 4],
    },
    {
      label: 'Mortes',
      borderColor: '#cf3c48',
      data: detailStateData['new_deaths'],
      fill: false,
      pointStyle: 'null',
    },
    {
      label: 'Mortes - MM',
      borderColor: '#610006',
      data: detailStateData['new_deaths_moving_average'],
      fill: false,
      borderDash: [6, 4],
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

function createChoroplethMapChart(dataForMapChart) {
  // Create map instance
  var chart = am4core.create(dataForMapChart['id'], am4maps.MapChart);
  chart.maxZoomLevel = 1;
  chart.chartContainer.wheelable = false;
  chart.panBehavior = 'none';

  // Enable responsive feature
  chart.responsive.enabled = true;

  // Enabling locale
  chart.language.locale = am4lang_pt_BR;
  chart.language.locale['_decimalSeparator'] = ',';
  chart.language.locale['_thousandSeparator'] = '.';

  // Set map definition
  chart.geodata = am4geodata_brState;

  // Set projection
  chart.projection = new am4maps.projections.Mercator();

  // Create map polygon series
  var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());

  // Define colors
  chart.colors.list = [
    am4core.color('#d66568'),
    am4core.color('#d92127'),
    am4core.color('#03a106'),
    am4core.color('#240900'),
    am4core.color('#FFC75F'),
    am4core.color('#F9F871'),
  ];

  //Set min/max fill color for each area
  polygonSeries.heatRules.push({
    property: 'fill',
    target: polygonSeries.mapPolygons.template,
    min: chart.colors.getIndex(dataForMapChart['colorIndex']).brighten(5),
    max: chart.colors.getIndex(dataForMapChart['colorIndex']).brighten(-0.3),
  });

  // Make map load polygon data (state shapes and names) from GeoJSON
  polygonSeries.useGeodata = true;

  let polygonData = [];
  let minValueMapBr = 0;
  let maxValueMapBr = 0;

  let numberOfEventsForMap = [];

  for (let i = 0; i < dataForMapChart['citiesData'].length; i++) {
    numberOfEventsForMap.push(
      dataForMapChart['citiesData'][i][dataForMapChart['dataToShowOnMapChart']]
    );
    polygonData.push({
      id: dataForMapChart['citiesData'][i]['city_ibge_code'],
      value:
        dataForMapChart['citiesData'][i][
          dataForMapChart['dataToShowOnMapChart']
        ],
    });
  }

  minValueMapBr = Math.min.apply(Math, numberOfEventsForMap);
  maxValueMapBr = Math.max.apply(Math, numberOfEventsForMap);

  // Set heatmap values for each state
  polygonSeries.data = polygonData;

  // Set up heat legend
  let heatLegend = chart.createChild(am4maps.HeatLegend);
  heatLegend.series = polygonSeries;
  heatLegend.align = 'right';
  heatLegend.valign = 'bottom';
  // heatLegend.orientation = 'vertical';
  heatLegend.width = am4core.percent(22);
  heatLegend.marginRight = am4core.percent(10);
  heatLegend.minValue = 0;
  heatLegend.maxValue = 40000000;

  // Set up custom heat map legend labels using axis ranges
  var minRange = heatLegend.valueAxis.axisRanges.create();
  minRange.value = heatLegend.minValue;
  minRange.label.text = `${minValueMapBr}`
    .replace('.', ',')
    .replace(/\B(?=(\d{3})+(?!\d))/g, '.');

  var maxRange = heatLegend.valueAxis.axisRanges.create();
  maxRange.value = heatLegend.maxValue;
  maxRange.label.text = `${maxValueMapBr}`
    .replace('.', ',')
    .replace(/\B(?=(\d{3})+(?!\d))/g, '.');

  // Blank out internal heat legend value axis labels
  heatLegend.valueAxis.renderer.labels.template.adapter.add('text', function (
    labelText
  ) {
    return '';
  });

  // Configure series tooltip
  var polygonTemplate = polygonSeries.mapPolygons.template;
  polygonTemplate.tooltipText = '{name}: {value}';
  polygonTemplate.nonScalingStroke = true;
  polygonTemplate.strokeWidth = 0.5;

  // Create hover state and set alternative fill color
  var hs = polygonTemplate.states.create('hover');
  hs.properties.fill = am4core.color(dataForMapChart['hoverColor']);

  return chart;
}

const dataForFirstMapChart = {
  id: 'chart-map-1',
  colorIndex: 1,
  citiesData: citiesData,
  dataToShowOnMapChart: 'confirmed',
  hoverColor: '#075f85',
  title: 'Casos por município',
};

const dataForSecondMapChart = {
  id: 'chart-map-1',
  colorIndex: 1,
  citiesData: citiesData,
  dataToShowOnMapChart: 'deaths',
  hoverColor: '#075f85',
  title: 'Mortes por município',
};

const dataForThirdMapChart = {
  id: 'chart-map-1',
  colorIndex: 1,
  citiesData: citiesData,
  dataToShowOnMapChart: 'confirmed_per_100k_inhabitants',
  hoverColor: '#075f85',
  title: 'Casos por 100 mil habitantes por município',
};

const dataForFourthMapChart = {
  id: 'chart-map-1',
  colorIndex: 1,
  citiesData: citiesData,
  dataToShowOnMapChart: 'death_per_100k_inhabitants',
  hoverColor: '#075f85',
  title: 'Mortes por 100 mil habitantes por município',
};

am4core.ready(function () {
  // Themes begin
  am4core.useTheme(am4themes_animated);
  // Themes end

  // Try to create the two maps above in bubble form
  createChoroplethMapChart(dataForFirstMapChart);

  for (let i = 0; i < chartNavLinks.length; i++) {
    chartNavLinks[i].addEventListener('click', () => {
      if (chartNavLinks[i].innerHTML === 'Casos') {
        chartNavLinks[i].classList.add('active');
        chartNavLinks[i + 1].classList.remove('active');
        chartNavLinks[i + 2].classList.remove('active');
        chartNavLinks[i + 3].classList.remove('active');
        createChoroplethMapChart(dataForFirstMapChart);
        mapChartTitle.innerHTML = 'Casos por município';
      } else if (chartNavLinks[i].innerHTML === 'Mortes') {
        chartNavLinks[i].classList.add('active');
        chartNavLinks[i - 1].classList.remove('active');
        chartNavLinks[i + 1].classList.remove('active');
        chartNavLinks[i + 2].classList.remove('active');
        createChoroplethMapChart(dataForSecondMapChart);
        mapChartTitle.innerHTML = 'Mortes por município';
      } else if (chartNavLinks[i].innerHTML === 'Taxa de casos') {
        chartNavLinks[i].classList.add('active');
        chartNavLinks[i + 1].classList.remove('active');
        chartNavLinks[i - 1].classList.remove('active');
        chartNavLinks[i - 2].classList.remove('active');
        createChoroplethMapChart(dataForThirdMapChart);
        mapChartTitle.innerHTML = 'Casos por 100 mil habitantes por município';
      } else if (chartNavLinks[i].innerHTML === 'Taxa de mortes') {
        chartNavLinks[i].classList.add('active');
        chartNavLinks[i - 1].classList.remove('active');
        chartNavLinks[i - 2].classList.remove('active');
        chartNavLinks[i - 3].classList.remove('active');
        createChoroplethMapChart(dataForFourthMapChart);
        mapChartTitle.innerHTML = 'Mortes por 100 mil habitantes por município';
      }
    });
  }
});

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
