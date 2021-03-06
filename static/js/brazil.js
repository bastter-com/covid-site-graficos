let dataToShowOnCharts = statesDailyData.slice(0, 6);
let dataToShowOnChartsDayZero = dayZeroData.slice(0, 6);
const quantityOfDays = datesList.length;
const chartNavLinks = document.getElementsByClassName('chart-nav-link');
let mapChartTitle = document.getElementById('geochart-title');

const colorsListForCasesMap = [
  '#5899da',
  '#e8743b',
  '#19a979',
  '#ed4a7b',
  '#945ecf',
  '#b90c0d',
  '#525df4',
  '#bf399e',
  '#6c8893',
  '#ee6868',
  '#2f6497',
  '#eb0510',
  '#B7A755',
  '#D6A65A',
  '#ABEBC6',
  '#F5CBA7',
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

function getSelectedStatesToSeeData() {
  let states = Array.from(document.getElementsByClassName('state-data-option'));
  let selectedStates = [];
  for (let i = 0; i < states.length; i++) {
    if (states[i].checked) {
      selectedStates.push(states[i].value);
    }
  }
  return selectedStates;
}

function prepareStatesDataset(dataToGet) {
  let datasetDataToChart = [];
  for (let i = 0; i < dataToShowOnCharts.length; i++) {
    let label = dataToShowOnCharts[i]['state'];
    let borderColor = colorsListForCasesMap[i];
    let data = dataToShowOnCharts[i][dataToGet];
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
  for (let i = 0; i < dataToShowOnChartsDayZero.length; i++) {
    let label = dataToShowOnChartsDayZero[i]['state'];
    let borderColor = colorsListForCasesMap[i];
    let data = dataToShowOnChartsDayZero[i][dataToGet];
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
    data: doughtnutChartData,
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

function updateChart(chart, axesType) {
  chart.options.scales.yAxes[0].type = axesType;
  chart.update();
}

function updateChartLineDatasets(chart, dataset) {
  chart.data.datasets = chart.update();
}

function updateDoughnutChart(chart, dataToUpdateDoughnutChart, title) {
  chart.options.title.text = title;
  chart.data = dataToUpdateDoughnutChart;
  chart.update();
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
      label: 'Casos - MM',
      borderColor: '#014a0f',
      data: brazilTotalData['data']['new_confirmed_moving_average'],
      fill: false,
      borderDash: [6, 4],
    },
    {
      label: 'Mortes',
      borderColor: '#cf3c48',
      data: brazilTotalData['data']['new_deaths'],
      fill: false,
      pointStyle: 'null',
    },
    {
      label: 'Mortes - MM',
      borderColor: '#610006',
      data: brazilTotalData['data']['new_deaths_moving_average'],
      fill: false,
      borderDash: [6, 4],
    },
  ],
  title: 'N??meros novos de casos e mortes por dia no Brasil',
  labelXAxis: 'Data',
  labelYAxis: 'Casos | Mortes',
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
  title: 'Evolu????o n??meros totais de casos e mortes no Brasil',
  labelXAxis: 'Data',
  labelYAxis: 'Casos | Mortes',
};

let dataForChartThree = () => {
  return {
    labels: datesList,
    datasets: prepareStatesDataset('new_confirmed', quantityOfDays),
    title: 'Novos casos por estado do Brasil',
    labelXAxis: 'Data',
    labelYAxis: 'Novos casos',
  };
};

let dataForChartFour = () => {
  return {
    labels: datesList,
    datasets: prepareStatesDataset(
      'new_confirmed_moving_average',
      quantityOfDays
    ),
    title: 'M??dia m??vel de 7 dias - novos casos',
    labelXAxis: 'Data',
    labelYAxis: 'M??dia m??vel novos casos',
  };
};

let dataForChartFive = () => {
  return {
    labels: datesList,
    datasets: prepareStatesDataset('new_deaths', quantityOfDays),
    title: 'Novas mortes por estado do Brasil',
    labelXAxis: 'Data',
    labelYAxis: 'Novas mortes',
  };
};

let dataForChartSix = () => {
  return {
    labels: datesList,
    datasets: prepareStatesDataset('new_deaths_moving_average', quantityOfDays),
    title: 'M??dia m??vel de 7 dias - novas mortes',
    labelXAxis: 'Data',
    labelYAxis: 'M??dia m??vel novas mortes',
  };
};

let dataForChartSeven = () => {
  return {
    labels: datesList,
    datasets: prepareStatesDataset('confirmed', quantityOfDays),
    title: 'Casos por estado do Brasil',
    labelXAxis: 'Data',
    labelYAxis: 'Casos',
  };
};

let dataForChartEight = () => {
  return {
    labels: datesList,
    datasets: prepareStatesDataset('deaths', quantityOfDays),
    title: 'Mortes por estado do Brasil',
    labelXAxis: 'Data',
    labelYAxis: 'Mortes',
  };
};

let dataForChartNine = () => {
  return {
    labels: baseDayZeroDays,
    datasets: prepareStatesDayZeroDatasets('confirmed_day_0'),
    title: 'Casos por estado no Brasil a partir do caso n?? 1000',
    labelXAxis: 'Dia a partir do caso n?? 1000',
    labelYAxis: 'Casos',
  };
};

let dataForChartTen = () => {
  return {
    labels: baseDayZeroDays,
    datasets: prepareStatesDayZeroDatasets('deaths_day_0'),
    title: 'Mortes por estado no Brasil a partir do caso n?? 1000',
    labelXAxis: 'Dia a partir do caso n?? 1000',
    labelYAxis: 'Mortes',
  };
};

let dataForChartEleven = () => {
  return {
    labels: datesList,
    datasets: prepareStatesDataset('cases_rate_per_100k_pop'),
    title: 'Taxa de casos por 100 mil habitantes',
    labelXAxis: 'Data',
    labelYAxis: 'Casos / 100 mil habitantes',
  };
};

let dataForChartTwelve = () => {
  return {
    labels: datesList,
    datasets: prepareStatesDataset('deaths_rate_per_100k_pop'),
    title: 'Taxa de mortes por 100 mil habitantes',
    labelXAxis: 'Data',
    labelYAxis: 'Mortes / 100 mil habitantes',
  };
};

let dataForChartThirteen = () => {
  return {
    labels: baseDayZeroDays,
    datasets: prepareStatesDayZeroDatasets('confirmed_rate_by_100k_pop'),
    title: 'Taxa de casos por 100 mil habitantes a partir do caso n?? 1000',
    labelXAxis: 'Data',
    labelYAxis: 'Casos / 100 mil habitantes',
  };
};

let dataForChartFourteen = () => {
  return {
    labels: baseDayZeroDays,
    datasets: prepareStatesDayZeroDatasets('deaths_rate_by_100k_pop'),
    title: 'Taxa de mortes por 100 mil habitantes a partir do caso n?? 1000',
    labelXAxis: 'Data',
    labelYAxis: 'Mortes / 100 mil habitantes',
  };
};

const dataForChartFifteen = {
  datasets: [
    {
      data: [
        regionCases['Norte'],
        regionCases['Nordeste'],
        regionCases['Sudeste'],
        regionCases['Centro-Oeste'],
        regionCases['Sul'],
      ],
      backgroundColor: ['#856c8b', '#90bd88', '#a4c5c6', '#ffeb99', '#bb3b0e'],
    },
  ],
  labels: ['Norte', 'Nordeste', 'Sudeste', 'Centro-Oeste', 'Sul'],
};

const dataForChartSixteen = {
  datasets: [
    {
      data: [
        regionDeaths['Norte'],
        regionDeaths['Nordeste'],
        regionDeaths['Sudeste'],
        regionDeaths['Centro-Oeste'],
        regionDeaths['Sul'],
      ],
      backgroundColor: ['#856c8b', '#90bd88', '#a4c5c6', '#ffeb99', '#bb3b0e'],
    },
  ],
  labels: ['Norte', 'Nordeste', 'Sudeste', 'Centro-Oeste', 'Sul'],
};

const dataForChartSeventeen = {
  datasets: [
    {
      data: [
        regionCases100kPop['Norte'],
        regionCases100kPop['Nordeste'],
        regionCases100kPop['Sudeste'],
        regionCases100kPop['Centro-Oeste'],
        regionCases100kPop['Sul'],
      ],
      backgroundColor: ['#856c8b', '#90bd88', '#a4c5c6', '#ffeb99', '#bb3b0e'],
    },
  ],
  labels: ['Norte', 'Nordeste', 'Sudeste', 'Centro-Oeste', 'Sul'],
};

const dataForChartEighteen = {
  datasets: [
    {
      data: [
        regionDeaths100kPop['Norte'],
        regionDeaths100kPop['Nordeste'],
        regionDeaths100kPop['Sudeste'],
        regionDeaths100kPop['Centro-Oeste'],
        regionDeaths100kPop['Sul'],
      ],
      backgroundColor: ['#856c8b', '#90bd88', '#a4c5c6', '#ffeb99', '#bb3b0e'],
    },
  ],
  labels: ['Norte', 'Nordeste', 'Sudeste', 'Centro-Oeste', 'Sul'],
};

let chartOne = createChart(dataForChartOne);

let chartTwo = createChart(dataForChartTwo);

let chartThree = createChart(dataForChartThree());

let chartFour = createChart(dataForChartFour());

let chartFive = createChart(dataForChartFive());

let chartSix = createChart(dataForChartSix());

let chartSeven = createChart(dataForChartSeven());

let chartEight = createChart(dataForChartEight());

let chartNine = createChart(dataForChartNine());

let chartTen = createChart(dataForChartTen());

let chartEleven = createChart(dataForChartEleven());

let chartTwelve = createChart(dataForChartTwelve());

let chartThirteen = createChart(dataForChartThirteen());

let chartFourteen = createChart(dataForChartFourteen());

let chartFifteen = createDoughnutChart(dataForChartFifteen, 'Casos por Regi??o');

let chartSixteen = createDoughnutChart(
  dataForChartSixteen,
  'Mortes por Regi??o'
);

let chartSeventeen = createDoughnutChart(
  dataForChartSeventeen,
  'Taxa de Casos por 100 mil habitantes por Regi??o'
);

let chartEighteen = createDoughnutChart(
  dataForChartEighteen,
  'Taxa de Mortes por 100 mil habitantes por Regi??o'
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
  colorIndex: 1,
  statesDailyData: statesDailyData,
  dataToShowOnMapChart: 'total_cases',
  hoverColor: '#075f85',
};

const dataForSecondMapChart = {
  id: 'chart-map-1',
  colorIndex: 1,
  statesDailyData: statesDailyData,
  dataToShowOnMapChart: 'total_deaths',
  hoverColor: '#075f85',
};

const dataForThirdMapChart = {
  id: 'chart-map-1',
  colorIndex: 1,
  statesDailyData: statesDailyData,
  dataToShowOnMapChart: 'cases_per_100k_pop',
  hoverColor: '#075f85',
};

const dataForFourthMapChart = {
  id: 'chart-map-1',
  colorIndex: 1,
  statesDailyData: statesDailyData,
  dataToShowOnMapChart: 'deaths_per_100k_pop',
  hoverColor: '#075f85',
};

am4core.ready(function () {
  // Themes begin
  am4core.useTheme(am4themes_animated);
  // Themes end

  // Try to create the two maps above in bubble form
  createChoroplethMapChart(dataForFirstMapChart);
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
  var chartThirteenInline = new Chart(ctxThirteen, chartThirteen);
  window.myLine = chartThirteenInline;

  // chart fourteen
  var ctxFourteen = document.getElementById('chart-14').getContext('2d');
  var chartFourteenInline = new Chart(ctxFourteen, chartFourteen);
  window.myLine = chartFourteenInline;

  // chart fifteen
  var ctxFifteen = document.getElementById('chart-15').getContext('2d');
  var chartFifteenInline = new Chart(ctxFifteen, chartFifteen);
  window.myLine = chartFifteenInline;

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
          case '13':
            updateChart(chartThirteenInline, 'linear');
            break;
          case '14':
            updateChart(chartFourteenInline, 'linear');
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
          case '13':
            updateChart(chartThirteenInline, 'logarithmic');
            break;
          case '14':
            updateChart(chartFourteenInline, 'logarithmic');
            break;
        }
      }
    });
  }
  for (let i = 0; i < chartNavLinks.length; i++) {
    chartNavLinks[i].addEventListener('click', () => {
      if (chartNavLinks[i].innerHTML === 'Casos') {
        chartNavLinks[i].classList.add('active');
        chartNavLinks[i + 1].classList.remove('active');
        chartNavLinks[i + 2].classList.remove('active');
        chartNavLinks[i + 3].classList.remove('active');
        if (chartNavLinks[i].classList.contains('cases-map')) {
          createChoroplethMapChart(dataForFirstMapChart);
          mapChartTitle.innerHTML = 'Casos por Unidade Federativa';
        } else if (chartNavLinks[i].classList.contains('cases-doughnut')) {
          updateDoughnutChart(
            chartFifteenInline,
            dataForChartFifteen,
            'Casos por Regi??o'
          );
        }
      } else if (chartNavLinks[i].innerHTML === 'Mortes') {
        chartNavLinks[i].classList.add('active');
        chartNavLinks[i - 1].classList.remove('active');
        chartNavLinks[i + 1].classList.remove('active');
        chartNavLinks[i + 2].classList.remove('active');
        if (chartNavLinks[i].classList.contains('deaths-map')) {
          createChoroplethMapChart(dataForSecondMapChart);
          mapChartTitle.innerHTML = 'Mortes por Unidade Federativa';
        } else if (chartNavLinks[i].classList.contains('deaths-doughnut')) {
          updateDoughnutChart(
            chartFifteenInline,
            dataForChartSixteen,
            'Mortes por Regi??o'
          );
        }
      } else if (chartNavLinks[i].innerHTML === 'Taxa de casos') {
        chartNavLinks[i].classList.add('active');
        chartNavLinks[i + 1].classList.remove('active');
        chartNavLinks[i - 1].classList.remove('active');
        chartNavLinks[i - 2].classList.remove('active');
        if (chartNavLinks[i].classList.contains('cases100k-map')) {
          createChoroplethMapChart(dataForThirdMapChart);
          mapChartTitle.innerHTML =
            'Casos por 100 mil habitantes por Unidade Federativa';
        } else if (chartNavLinks[i].classList.contains('cases100k-doughnut')) {
          updateDoughnutChart(
            chartFifteenInline,
            dataForChartSeventeen,
            'Taxa de Casos por 100 mil habitantes por Regi??o'
          );
        }
      } else if (chartNavLinks[i].innerHTML === 'Taxa de mortes') {
        chartNavLinks[i].classList.add('active');
        chartNavLinks[i - 1].classList.remove('active');
        chartNavLinks[i - 2].classList.remove('active');
        chartNavLinks[i - 3].classList.remove('active');
        if (chartNavLinks[i].classList.contains('deaths100k-map')) {
          createChoroplethMapChart(dataForFourthMapChart);
          mapChartTitle.innerHTML =
            'Mortes por 100 mil habitantes por Unidade Federativa';
        } else if (chartNavLinks[i].classList.contains('deaths100k-doughnut')) {
          updateDoughnutChart(
            chartFifteenInline,
            dataForChartEighteen,
            'Taxa de Mortes por 100 mil habitantes por Regi??o'
          );
        }
      }
    });
  }
  $('#confirm-states-selected').click(() => {
    let selectedStates = getSelectedStatesToSeeData();
    let selectedStatesData = statesDailyData.filter((elem) => {
      if (selectedStates.includes(elem.state)) {
        return elem.state;
      }
    });
    let selectedStatesDataDayZero = dayZeroData.filter((elem) => {
      if (selectedStates.includes(elem.state)) {
        return elem.state;
      }
    });
    dataToShowOnCharts = selectedStatesData;
    dataToShowOnChartsDayZero = selectedStatesDataDayZero;

    chartThreeInline.data.labels = dataForChartThree().labels;
    chartThreeInline.data.datasets = dataForChartThree().datasets;
    chartThreeInline.update();

    chartFourInline.data.labels = dataForChartFour().labels;
    chartFourInline.data.datasets = dataForChartFour().datasets;
    chartFourInline.update();

    chartFiveInline.data.labels = dataForChartFive().labels;
    chartFiveInline.data.datasets = dataForChartFive().datasets;
    chartFiveInline.update();

    chartSixInline.data.labels = dataForChartSix().labels;
    chartSixInline.data.datasets = dataForChartSix().datasets;
    chartSixInline.update();

    chartSevenInline.data.labels = dataForChartSeven().labels;
    chartSevenInline.data.datasets = dataForChartSeven().datasets;
    chartSevenInline.update();

    chartEightInline.data.labels = dataForChartEight().labels;
    chartEightInline.data.datasets = dataForChartEight().datasets;
    chartEightInline.update();

    chartNineInline.data.labels = dataForChartNine().labels;
    chartNineInline.data.datasets = dataForChartNine().datasets;
    chartNineInline.update();

    chartTenInline.data.labels = dataForChartTen().labels;
    chartTenInline.data.datasets = dataForChartTen().datasets;
    chartTenInline.update();

    chartElevenInline.data.labels = dataForChartEleven().labels;
    chartElevenInline.data.datasets = dataForChartEleven().datasets;
    chartElevenInline.update();

    chartTwelveInline.data.labels = dataForChartTwelve().labels;
    chartTwelveInline.data.datasets = dataForChartTwelve().datasets;
    chartTwelveInline.update();

    chartThirteenInline.data.labels = dataForChartThirteen().labels;
    chartThirteenInline.data.datasets = dataForChartThirteen().datasets;
    chartThirteenInline.update();

    chartFourteenInline.data.labels = dataForChartFourteen().labels;
    chartFourteenInline.data.datasets = dataForChartFourteen().datasets;
    chartFourteenInline.update();
  });
};
