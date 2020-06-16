$(document).ready(function () {
  const chartNavLinks = document.getElementsByClassName('chart-nav-link');
  let cityChartContainer = document.getElementById('city-chart-container');
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

  function updateChart(chart, dataToUpdate) {
    chart.data.labels = dataToUpdate.labels;
    chart.data.datasets = dataToUpdate.datasets;
    chart.options.title.text = dataToUpdate.title;
    chart.options.scales.xAxes[0].scaleLabel.labelString = 'Data';
    chart.options.scales.yAxes[0].scaleLabel.labelString = 'Casos | Mortes';
    chart.update();
  }

  function updateChartLineScaleType(chart, axesType) {
    chart.options.scales.yAxes[0].type = axesType;
    chart.update();
  }

  let dataForChartOne = {
  
  };
  let dataForChartTwo = {
    
  };
  let chartOne = createChart(dataForChartOne);

  let chartTwo = createChart(dataForChartTwo);

  // chart one
  var ctxOne = document.getElementById('chart').getContext('2d');
  var chartOneInline = new Chart(ctxOne, chartOne);
  window.myLine = chartOneInline;
  
  // chart two
  var ctxTwo = document.getElementById('chart-2').getContext('2d');
  var chartTwoInline = new Chart(ctxTwo, chartTwo);
  window.myLine = chartTwoInline;
  
  $('select#select-uf').change(function () {
    let optionStateSelected = $(this).find('option:selected');
    let stateSelected = optionStateSelected.text();

    let dataToAjax = { uf: stateSelected };
    $.ajax({
      url: '/cidades/cidades_detalhe',
      type: 'GET',
      dataType: 'json',
      data: dataToAjax,
      contentType: 'application/json',
      success: function (result) {
        $('#select-city option').remove();
        for (let i = 0; i < result.length; i++) {
          $('#select-city').append(
            '<option class="form-control">' + result[i].name + '</option>'
          );
        }
      },
    });
  });
  $('#search-city-btn').click(function () {
    if ($('select#select-uf').val() === 'Unidade Federativa') {
      alert("Escolha uma cidade para fazer a busca");
    } else {
      let cityFormContainer = document.getElementById('city-form-container');
      cityFormContainer.classList = "row";
      let optionCitySelected = $('select#select-city').find('option:selected');
      let citySelected = optionCitySelected.text();
      let optionStateSelected = $('select#select-uf').find('option:selected');
      let stateSelected = optionStateSelected.text();
      let dataToAjaxCity = { uf: stateSelected, city: citySelected };
      cityChartContainer.style.display = 'flex';
      $.ajax({
        url: '/cidades/cidades_dados',
        type: 'GET',
        dataType: 'json',
        data: dataToAjaxCity,
        contentType: 'application/json',
        success: function (result) {
          let chartResult = result[0];
          let tableResult = result[1];
          let dataForChartOne = {
            labels: chartResult.dates,
            datasets: [
              {
                label: 'Casos',
                borderColor: '#02c20e',
                data: chartResult.new_confirmed,
                fill: false,
              },
              {
                label: 'Casos - MM',
                borderColor: '#014a0f',
                data: chartResult.new_confirmed_moving_average,
                fill: false,
                borderDash: [6, 4],
              },
              {
                label: 'Mortes',
                borderColor: '#cf3c48',
                data: chartResult.new_deaths,
                fill: false,
                pointStyle: 'null',
              },
              {
                label: 'Mortes - MM',
                borderColor: '#610006',
                data: chartResult.new_deaths_moving_average,
                fill: false,
                borderDash: [6, 4],
              },
            ],
            title: `Números novos de casos e mortes por dia - ${citySelected} - ${stateSelected}`,
            labelXAxis: 'Data',
            labelYAxis: 'Casos | Mortes',
          };
          let dataForChartTwo = {
            labels: chartResult.dates,
            datasets: [
              {
                label: 'Casos',
                borderColor: '#256dd9',
                data: chartResult.confirmed,
                fill: false,
              },
              {
                label: 'Mortes',
                borderColor: '#cf3c48',
                data: chartResult.deaths,
                fill: false,
                pointStyle: 'null',
              },
            ],
            title: `Evolução números totais de casos e mortes - ${citySelected} - ${stateSelected}`,
            labelXAxis: 'Data',
            labelYAxis: 'Casos | Mortes',
          };

          $('#city-data-name').text(tableResult.city);
          $('#city-data-name-uf').text(tableResult.uf);
          $('#city-data-confirmed').text(
            `${tableResult.confirmed}`.replace(/\B(?=(\d{3})+(?!\d))/g, '.')
          );
          $('#city-data-confirmed-rate').text(
            `${tableResult.cases_rate_per_inhabitants} %`.replace('.', ',')
          );
          $('#city-data-deaths').text(
            `${tableResult.deaths}`.replace(/\B(?=(\d{3})+(?!\d))/g, '.')
          );
          $('#city-data-deaths-rate').text(
            `${tableResult.deaths_rate_per_inhabitants} %`.replace('.', ',')
          );
          $('#city-data-date').text(tableResult.date);
          $('#city-data-estimated-population').text(
            `${tableResult.estimated_population_2019}`.replace(
              /\B(?=(\d{3})+(?!\d))/g,
              '.'
            )
          );
        
          updateChart(chartOneInline, dataForChartOne);
          updateChart(chartTwoInline, dataForChartTwo);
  
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
                    updateChartLineScaleType(chartOneInline, 'linear');
                    break;
                  case '2':
                    updateChartLineScaleType(chartTwoInline, 'linear');
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
                    updateChartLineScaleType(chartOneInline, 'logarithmic');
                    break;
                  case '2':
                    updateChartLineScaleType(chartTwoInline, 'logarithmic');
                    break;
                }
              }
            });
          }
        },
      });
    }
  });
});