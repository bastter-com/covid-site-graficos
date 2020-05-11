// var chartOne = {
//   type: 'line',
//   data: {
//     labels: totalsData['data']['dates'],
//     datasets: [
//       {
//         label: 'Casos',
//         borderColor: '#0b2eb8',
//         data: totalsData['data']['new_confirmed'],
//         fill: false,
//       },
//       {
//         label: 'Mortes',
//         borderColor: '#b00003',
//         data: totalsData['data']['new_deaths'],
//         fill: false,
//       },
//       {
//         label: 'Recuperados',
//         borderColor: '#3ad42c',
//         data: totalsData['data']['new_recovered'],
//         fill: false,
//       },
//     ],
//   },
//   options: {
//     responsive: true,
//     elements: {
//       point: {
//         radius: 0,
//         hoverRadius: 5,
//       },
//     },
//     title: {
//       display: true,
//       text: 'Evolução novos casos, mortes e recuperados de Covid-19 no Mundo',
//       fontSize: 24,
//     },
//     tooltips: {
//       mode: 'index',
//       intersect: false,
//     },
//     hover: {
//       mode: 'nearest',
//       intersect: true,
//     },
//     maintainAspectRatio: false,
//     scales: {
//       xAxes: [
//         {
//           display: true,
//           scaleLabel: {
//             display: true,
//             labelString: 'Data',
//           },
//         },
//       ],
//       yAxes: [
//         {
//           display: true,
//           scaleLabel: {
//             display: true,
//             labelString: 'Eventos',
//           },
//         },
//       ],
//     },
//   },
// };

var chartTwo = {
  type: 'line',
  data: {
    labels: totalsData['data']['dates'],
    datasets: [
      {
        label: 'Casos',
        borderColor: '#0b2eb8',
        data: totalsData['data']['confirmed'],
        fill: false,
      },
      {
        label: 'Mortes',
        borderColor: '#b00003',
        data: totalsData['data']['deaths'],
        fill: false,
      },
      {
        label: 'Recuperados',
        borderColor: '#3ad42c',
        data: totalsData['data']['recovered'],
        fill: false,
      },
    ],
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
      text: 'Evolução casos, mortes e recuperados de Covid-19 no Mundo',
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
            labelString: 'Data',
          },
        },
      ],
      yAxes: [
        {
          display: true,
          scaleLabel: {
            display: true,
            labelString: 'Eventos',
          },
        },
      ],
    },
  },
};

// function getQuantityOfDataDays(allCountryData, labelData) {
//   let quantityDays = 0;
//   let dateLabel;
//   for (let i = 0; i < allCountryData.length; i++) {
//     if (allCountryData[i][labelData].length > quantityDays) {
//       quantityDays = allCountryData[i][labelData].length;
//       dateLabel = allCountryData[i]['date_list'];
//     }
//   }
//   return [quantityDays, dateLabel];
// }

// function prepareDataset(dataToGet, quantityDays) {
//   let datasetConfirmedCases = [];

//   let colorsListForCasesMap = [
//     '#eb4034',
//     '#eb9634',
//     '#4d24a6',
//     '#67e314',
//     '#069c0b',
//     '#05f0c1',
//     '#0f5abd',
//     '#d91133',
//     '#ed8154',
//     '#e26050',
//     '#d43d51',
//     '#5f126b',
//     '#6b121e',
//     '#59c27c',
//     '#3d1e15',
//   ];

//   let colorListForDeathsMap = [
//     '#933a16',
//     '#8d021f',
//     '#5e1914',
//     '#b80f0a',
//     '#420d09',
//     '#dff280',
//     '#bf0a30',
//     '#ca3433',
//     '#d21f3c',
//     '#b43757',
//     '#ff0800',
//     '#7e191b',
//     '#ea3c53',
//     '#a45a52',
//     '#800000',
//   ];

//   for (let i = 0; i < country_data.length; i++) {
//     let label = country_data[i]['country'];
//     let borderColor;
//     if (dataToGet === 'confirmed_list') {
//       borderColor = colorsListForCasesMap[i];
//     } else if (dataToGet === 'deaths_list') {
//       borderColor = colorListForDeathsMap[i];
//     }
//     let differenceOfDays = quantityDays - country_data[i][dataToGet].length;
//     for (let j = 0; j < differenceOfDays; j++) {
//       country_data[i][dataToGet].unshift(0);
//     }
//     let data = country_data[i][dataToGet];
//     let fill = false;
//     datasetConfirmedCases.push({
//       label: label,
//       borderColor: borderColor,
//       data: data,
//       fill: fill,
//     });
//   }
//   return datasetConfirmedCases;
// }

// let quantityDays;
// let dateLabel;
// [quantityDays, dateLabel] = getQuantityOfDataDays(
//   country_data,
//   'confirmed_list'
// );

// var chartTwo = {
//   type: 'line',
//   data: {
//     labels: dateLabel,
//     datasets: prepareDataset('confirmed_list', quantityDays),
//   },
//   options: {
//     responsive: true,
//     title: {
//       display: true,
//       text: 'Casos por país',
//       fontSize: 24,
//     },
//     tooltips: {
//       mode: 'index',
//       intersect: false,
//     },
//     hover: {
//       mode: 'nearest',
//       intersect: true,
//     },
//     maintainAspectRatio: false,
//     scales: {
//       xAxes: [
//         {
//           display: true,
//           scaleLabel: {
//             display: true,
//             labelString: 'Dia',
//           },
//         },
//       ],
//       yAxes: [
//         {
//           display: true,
//           scaleLabel: {
//             display: true,
//             labelString: 'Casos',
//           },
//         },
//       ],
//     },
//   },
// };

// var chartThree = {
//   type: 'line',
//   data: {
//     labels: dateLabel,
//     datasets: prepareDataset('deaths_list', quantityDays),
//   },
//   options: {
//     responsive: true,
//     title: {
//       display: true,
//       text: 'Mortes por país',
//       fontSize: 24,
//     },
//     tooltips: {
//       mode: 'index',
//       intersect: false,
//     },
//     hover: {
//       mode: 'nearest',
//       intersect: true,
//     },
//     maintainAspectRatio: false,
//     scales: {
//       xAxes: [
//         {
//           display: true,
//           scaleLabel: {
//             display: true,
//             labelString: 'Dia',
//           },
//         },
//       ],
//       yAxes: [
//         {
//           display: true,
//           scaleLabel: {
//             display: true,
//             labelString: 'Mortes',
//           },
//         },
//       ],
//     },
//   },
// };

window.onload = function () {
  // var ctxOne = document.getElementById('chart').getContext('2d');
  var ctxTwo = document.getElementById('chart-2').getContext('2d');
  // var ctxThree = document.getElementById('chart-3').getContext('2d');
  // window.myLine = new Chart(ctxOne, chartOne);
  window.myLine = new Chart(ctxTwo, chartTwo);
  // window.myLine = new Chart(ctxThree, chartThree);
};
