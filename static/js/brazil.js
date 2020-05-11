const dataOfFirstTenStates = statesDailyData.slice(0, 12);
const dataOfFirstTenStatesDayZero = dayZeroData.slice(0, 12);
const quantityOfDays = datesList.length;
const chartNavLinks = document.getElementsByClassName('chart-nav-link');

const colorsListForCasesMap = [
  '#856c8b',
  '#90bd88',
  '#a4c5c6',
  '#ffeb99',
  '#bb3b0e',
  '#dd7631',
  '#708160',
  '#d8c593',
  '#0779e4',
  '#4cbbb9',
  '#77d8d8',
  '#eb0510',
  '#B7A755',
  '#D6A65A',
  '#ABEBC6',
  '#F5CBA7',
];

const colorsListForDeathsMap = [
  '#003f5c',
  '#2f4b7c',
  '#665191',
  '#a05195',
  '#d45087',
  '#f95d6a',
  '#ff7c43',
  '#ffa600',
  '#488f31',
  '#8ba43c',
  '#c7b854',
  '#ffcb77',
  '#f69e5d',
  '#e97051',
  '#00FFFF',
  '#FF0000',
];

function prepareStatesDataset(dataToGet) {
  let datasetDataToChart = [];
  for (let i = 0; i < dataOfFirstTenStates.length; i++) {
    let label = dataOfFirstTenStates[i]['state'];
    let borderColor;
    if (
      (dataToGet == 'confirmed') |
      (dataToGet == 'cases_rate_per_100k_pop') |
      (dataToGet == 'new_confirmed')
    ) {
      borderColor = colorsListForCasesMap[i];
    } else if (
      (dataToGet == 'deaths') |
      (dataToGet == 'deaths_rate_per_100k_pop') |
      (dataToGet == 'new_deaths')
    ) {
      borderColor = colorsListForDeathsMap[i];
    }
    let data = dataOfFirstTenStates[i][dataToGet];
    let fill = false;
    datasetDataToChart.push({
      label: label,
      borderColor: borderColor,
      data: data,
      fill: fill,
    });
  }
  return datasetDataToChart;
}

function prepareStatesDayZeroDatasets(dataToGet) {
  let datasetDataToChartDayZero = [];
  for (let i = 0; i < dataOfFirstTenStatesDayZero.length; i++) {
    let label = dataOfFirstTenStatesDayZero[i]['state'];
    let borderColor;
    if (
      (dataToGet == 'confirmed_day_0') |
      (dataToGet == 'cases_rate_per_100k_pop') |
      (dataToGet == 'confirmed_rate_by_100k_pop')
    ) {
      borderColor = colorsListForCasesMap[i];
    } else if (
      (dataToGet == 'deaths_day_0') |
      (dataToGet == 'deaths_rate_per_100k_pop') |
      (dataToGet == 'deaths_rate_by_100k_pop')
    ) {
      borderColor = colorsListForDeathsMap[i];
    }
    let data = dataOfFirstTenStatesDayZero[i][dataToGet];
    let fill = false;
    datasetDataToChartDayZero.push({
      label: label,
      borderColor: borderColor,
      data: data,
      fill: fill,
    });
  }
  return datasetDataToChartDayZero;
}

function createChart(chartData) {
  let chart = {
    type: 'line',
    data: {
      labels: chartData['labels'],
      datasets: chartData['datasets'],
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
        text: chartData['title'],
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
              labelString: chartData['labelXAxis'],
            },
          },
        ],
        yAxes: [
          {
            display: true,
            scaleLabel: {
              display: true,
              labelString: chartData['labelYAxis'],
            },
          },
        ],
      },
    },
  };
  return chart;
}

function createDoughnutChart(doughtnutChartData, title) {
  let doughnutChart = {
    type: 'doughnut',
    data: {
      datasets: [
        {
          data: doughtnutChartData,
          backgroundColor: [
            '#856c8b',
            '#90bd88',
            '#a4c5c6',
            '#ffeb99',
            '#bb3b0e',
          ],
        },
      ],
      labels: ['Norte', 'Nordeste', 'Sudeste', 'Centro-Oeste', 'Sul'],
    },
    options: {
      responsive: true,
      title: {
        display: true,
        text: title,
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
      tooltips: {
        callbacks: {
          label: function (tooltipItem, data) {
            var dataset = data.datasets[tooltipItem.datasetIndex];
            var total = dataset.data.reduce(function (
              previousValue,
              currentValue
            ) {
              return previousValue + currentValue;
            });
            var currentValue = dataset.data[tooltipItem.index];
            var percentage = Math.floor((currentValue / total) * 100 + 0.5);
            return `${data.labels[tooltipItem.index]}: ${percentage}%`;
          },
        },
      },
    },
  };
  return doughnutChart;
}

const dataForChartOne = {
  labels: brazilTotalData['data']['dates_brazil'],
  datasets: [
    {
      label: 'Casos',
      borderColor: '#02c20e',
      data: brazilTotalData['data']['new_confirmed'],
      fill: false,
    },
    {
      label: 'Mortes',
      borderColor: '#cf3c48',
      data: brazilTotalData['data']['new_deaths'],
      fill: false,
      pointStyle: 'null',
    },
  ],
  title: 'Números novos de casos e mortes por dia no Brasil',
  labelXAxis: 'Data',
  labelYAxis: 'Casos / Mortes',
};

const dataForChartTwo = {
  labels: brazilTotalData['data']['dates_brazil'],
  datasets: [
    {
      label: 'Casos',
      borderColor: '#256dd9',
      data: brazilTotalData['data']['confirmed_brazil'],
      fill: false,
    },
    {
      label: 'Mortes',
      borderColor: '#cf3c48',
      data: brazilTotalData['data']['deaths_brazil'],
      fill: false,
      pointStyle: 'null',
    },
  ],
  title: 'Evolução números totais de casos e mortes no Brasil',
  labelXAxis: 'Data',
  labelYAxis: 'Casos / Mortes',
};

const dataForChartThree = {
  labels: datesList,
  datasets: prepareStatesDataset('new_confirmed', quantityOfDays),
  title: 'Novos casos por estado do Brasil',
  labelXAxis: 'Data',
  labelYAxis: 'Novos casos',
};

const dataForChartFour = {
  labels: datesList,
  datasets: prepareStatesDataset('new_deaths', quantityOfDays),
  title: 'Novas mortes por estado do Brasil',
  labelXAxis: 'Data',
  labelYAxis: 'Novas mortes',
};

const dataForChartFive = {
  labels: datesList,
  datasets: prepareStatesDataset('confirmed', quantityOfDays),
  title: 'Casos por estado do Brasil',
  labelXAxis: 'Data',
  labelYAxis: 'Casos',
};

const dataForChartSix = {
  labels: datesList,
  datasets: prepareStatesDataset('deaths', quantityOfDays),
  title: 'Mortes por estado do Brasil',
  labelXAxis: 'Data',
  labelYAxis: 'Mortes',
};

const dataForChartSeven = {
  labels: baseDayZeroDays,
  datasets: prepareStatesDayZeroDatasets('confirmed_day_0'),
  title: 'Casos por estado no Brasil a partir do caso nº 1000',
  labelXAxis: 'Dia a partir do caso nº 1000',
  labelYAxis: 'Casos',
};

const dataForChartEight = {
  labels: baseDayZeroDays,
  datasets: prepareStatesDayZeroDatasets('deaths_day_0'),
  title: 'Mortes por estado no Brasil a partir do caso nº 1000',
  labelXAxis: 'Dia a partir do caso nº 1000',
  labelYAxis: 'Mortes',
};

const dataForChartNine = {
  labels: datesList,
  datasets: prepareStatesDataset('cases_rate_per_100k_pop'),
  title: 'Taxa de casos por 100 mil habitantes',
  labelXAxis: 'Data',
  labelYAxis: 'Casos / 100 mil habitantes',
};

const dataForChartTen = {
  labels: datesList,
  datasets: prepareStatesDataset('deaths_rate_per_100k_pop'),
  title: 'Taxa de mortes por 100 mil habitantes',
  labelXAxis: 'Data',
  labelYAxis: 'Mortes / 100 mil habitantes',
};

const dataForChartEleven = {
  labels: baseDayZeroDays,
  datasets: prepareStatesDayZeroDatasets('confirmed_rate_by_100k_pop'),
  title: 'Taxa de casos por 100 mil habitantes a partir do caso nº 1000',
  labelXAxis: 'Data',
  labelYAxis: 'Casos / 100 mil habitantes',
};

const dataForChartTwelve = {
  labels: baseDayZeroDays,
  datasets: prepareStatesDayZeroDatasets('deaths_rate_by_100k_pop'),
  title: 'Taxa de mortes por 100 mil habitantes a partir do caso nº 1000',
  labelXAxis: 'Data',
  labelYAxis: 'Mortes / 100 mil habitantes',
};

const dataForChartThirteen = [
  regionCases['Norte'],
  regionCases['Nordeste'],
  regionCases['Sudeste'],
  regionCases['Centro-Oeste'],
  regionCases['Sul'],
];

const dataForChartFourteen = [
  regionDeaths['Norte'],
  regionDeaths['Nordeste'],
  regionDeaths['Sudeste'],
  regionDeaths['Centro-Oeste'],
  regionDeaths['Sul'],
];

const dataForChartFifteen = [
  regionCases100kPop['Norte'],
  regionCases100kPop['Nordeste'],
  regionCases100kPop['Sudeste'],
  regionCases100kPop['Centro-Oeste'],
  regionCases100kPop['Sul'],
];

const dataForChartSixteen = [
  regionDeaths100kPop['Norte'],
  regionDeaths100kPop['Nordeste'],
  regionDeaths100kPop['Sudeste'],
  regionDeaths100kPop['Centro-Oeste'],
  regionDeaths100kPop['Sul'],
];

let chartOne = createChart(dataForChartOne);

let chartTwo = createChart(dataForChartTwo);

let chartThree = createChart(dataForChartThree);

let chartFour = createChart(dataForChartFour);

let chartFive = createChart(dataForChartFive);

let chartSix = createChart(dataForChartSix);

let chartSeven = createChart(dataForChartSeven);

let chartEight = createChart(dataForChartEight);

let chartNine = createChart(dataForChartNine);

let chartTen = createChart(dataForChartTen);

let chartEleven = createChart(dataForChartEleven);

let chartTwelve = createChart(dataForChartTwelve);

let chartThirteen = createDoughnutChart(
  dataForChartThirteen,
  'Casos por Região'
);

let chartFourteen = createDoughnutChart(
  dataForChartFourteen,
  'Mortes por Região'
);

let chartFifteen = createDoughnutChart(
  dataForChartFifteen,
  'Taxa de Casos por 100 mil habitantes por Região'
);

let chartSixteen = createDoughnutChart(
  dataForChartSixteen,
  'Taxa de Mortes por 100 mil habitantes por Região'
);

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
  chart.geodata = am4geodata_brazilLow;

  // Set projection
  chart.projection = new am4maps.projections.Mercator();

  // Create map polygon series
  var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());

  // Define colors
  chart.colors.list = [
    am4core.color('#0650bf'),
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

  for (let i = 0; i < dataForMapChart['statesDailyData'].length; i++) {
    numberOfEventsForMap.push(
      dataForMapChart['statesDailyData'][i][
        dataForMapChart['dataToShowOnMapChart']
      ]
    );
    polygonData.push({
      id: `BR-${dataForMapChart['statesDailyData'][i]['state']}`,
      value:
        dataForMapChart['statesDailyData'][i][
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
  colorIndex: 2,
  statesDailyData: statesDailyData,
  dataToShowOnMapChart: 'total_cases',
  hoverColor: '#075f85',
};

const dataForSecondMapChart = {
  id: 'chart-map-2',
  colorIndex: 3,
  statesDailyData: statesDailyData,
  dataToShowOnMapChart: 'total_deaths',
  hoverColor: '#7695a3',
};

const dataForThirdMapChart = {
  id: 'chart-map-3',
  colorIndex: 0,
  statesDailyData: statesDailyData,
  dataToShowOnMapChart: 'cases_per_100k_pop',
  hoverColor: '#0c7876',
};

const dataForFourthMapChart = {
  id: 'chart-map-4',
  colorIndex: 1,
  statesDailyData: statesDailyData,
  dataToShowOnMapChart: 'deaths_per_100k_pop',
  hoverColor: '#cf4a08',
};

am4core.ready(function () {
  // Themes begin
  am4core.useTheme(am4themes_animated);
  // Themes end

  createChoroplethMapChart(dataForFirstMapChart);

  createChoroplethMapChart(dataForSecondMapChart);

  createChoroplethMapChart(dataForThirdMapChart);

  createChoroplethMapChart(dataForFourthMapChart);
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

  // chart three
  var ctxThree = document.getElementById('chart-3').getContext('2d');
  var chartThreeInline = new Chart(ctxThree, chartThree);
  window.myLine = chartThreeInline;

  // chart four
  var ctxFour = document.getElementById('chart-4').getContext('2d');
  var chartFourInline = new Chart(ctxFour, chartFour);
  window.myLine = chartFourInline;

  // chart five
  var ctxFive = document.getElementById('chart-5').getContext('2d');
  var chartFiveInline = new Chart(ctxFive, chartFive);
  window.myLine = chartFiveInline;

  // chart six
  var ctxSix = document.getElementById('chart-6').getContext('2d');
  var chartSixInline = new Chart(ctxSix, chartSix);
  window.myLine = chartSixInline;

  // chart seven
  var ctxSeven = document.getElementById('chart-7').getContext('2d');
  var chartSevenInline = new Chart(ctxSeven, chartSeven);
  window.myLine = chartSevenInline;

  // chart eight
  var ctxEight = document.getElementById('chart-8').getContext('2d');
  var chartEightInline = new Chart(ctxEight, chartEight);
  window.myLine = chartEightInline;

  // chart nine
  var ctxNine = document.getElementById('chart-9').getContext('2d');
  var chartNineInline = new Chart(ctxNine, chartNine);
  window.myLine = chartNineInline;

  // chart ten
  var ctxTen = document.getElementById('chart-10').getContext('2d');
  var chartTenInline = new Chart(ctxTen, chartTen);
  window.myLine = chartTenInline;

  // chart eleven
  var ctxEleven = document.getElementById('chart-11').getContext('2d');
  var chartElevenInline = new Chart(ctxEleven, chartEleven);
  window.myLine = chartElevenInline;

  // chart twelve
  var ctxTwelve = document.getElementById('chart-12').getContext('2d');
  var chartTwelveInline = new Chart(ctxTwelve, chartTwelve);
  window.myLine = chartTwelveInline;

  // chart thirteen
  var ctxThirteen = document.getElementById('chart-13').getContext('2d');
  window.myLine = new Chart(ctxThirteen, chartThirteen);

  // chart fourteen
  var ctxFourteen = document.getElementById('chart-14').getContext('2d');
  window.myLine = new Chart(ctxFourteen, chartFourteen);

  // chart fifteen
  var ctxFifteen = document.getElementById('chart-15').getContext('2d');
  window.myLine = new Chart(ctxFifteen, chartFifteen);

  // chart sixteen
  var ctxSixteen = document.getElementById('chart-16').getContext('2d');
  window.myLine = new Chart(ctxSixteen, chartSixteen);

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
          case '3':
            updateChart(chartThreeInline, 'linear');
            break;
          case '4':
            updateChart(chartFourInline, 'linear');
            break;
          case '5':
            updateChart(chartFiveInline, 'linear');
            break;
          case '6':
            updateChart(chartSixInline, 'linear');
            break;
          case '7':
            updateChart(chartSevenInline, 'linear');
            break;
          case '8':
            updateChart(chartEightInline, 'linear');
            break;
          case '9':
            updateChart(chartNineInline, 'linear');
            break;
          case '10':
            updateChart(chartTenInline, 'linear');
            break;
          case '11':
            updateChart(chartElevenInline, 'linear');
            break;
          case '12':
            updateChart(chartTwelveInline, 'linear');
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
          case '3':
            updateChart(chartThreeInline, 'logarithmic');
            break;
          case '4':
            updateChart(chartFourInline, 'logarithmic');
            break;
          case '5':
            updateChart(chartFiveInline, 'logarithmic');
            break;
          case '6':
            updateChart(chartSixInline, 'logarithmic');
            break;
          case '7':
            updateChart(chartSevenInline, 'logarithmic');
            break;
          case '8':
            updateChart(chartEightInline, 'logarithmic');
            break;
          case '9':
            updateChart(chartNineInline, 'logarithmic');
            break;
          case '10':
            updateChart(chartTenInline, 'logarithmic');
            break;
          case '11':
            updateChart(chartElevenInline, 'logarithmic');
            break;
          case '12':
            updateChart(chartTwelveInline, 'logarithmic');
            break;
        }
      }
    });
  }
};
