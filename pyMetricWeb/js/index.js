$(document).ready(function(){
  
  // Chart Data
  
  var lineChartData = [];
  
  lineChartData[0] = {
      labels: ["", "", "", "", "", ""],
      datasets: [
        {
          label: "CPU-Auslastung",
          fillColor: "rgba(220,220,220,0.2)",
          strokeColor: "rgba(220,220,220,1)",
          pointColor: "rgba(220,220,220,1)",
          pointStrokeColor: "#fff",
          pointHighlightFill: "#fff",
          pointHighlightStroke: "rgba(220,220,220,1)",
          data: [13, 53, 32, 34, 123, 10]
        },
        
        {
          label: "CPU-Auslastung",
          fillColor: "rgba(220,220,220,0.2)",
          strokeColor: "rgba(220,220,220,1)",
          pointColor: "rgba(220,220,220,1)",
          pointStrokeColor: "#fff",
          pointHighlightFill: "#fff",
          pointHighlightStroke: "rgba(220,220,220,1)",
          data: [76, 12, 87, 17, 42, 55]
        }
      ]
  };
  
  var dChartData = [];
  
  dChartData[0] = {
      labels: [
          "Red",
          "Green",
          "Yellow"
      ],
      datasets: [
          {
              data: [300, 50, 100],
              backgroundColor: [
                  "#FF6384",
                  "#36A2EB",
                  "#FFCE56"
              ],
              hoverBackgroundColor: [
                  "#FF6384",
                  "#36A2EB",
                  "#FFCE56"
              ]
          }]
  };

  dChartData[1] = {
      labels: [""],
      datasets: [
          {
              data: [300, 50, 100],
              backgroundColor: [
                  "#FF6384",
                  "#36A2EB",
                  "#FFCE56"
              ],
              hoverBackgroundColor: [
                  "#FF6384",
                  "#36A2EB",
                  "#FFCE56"
              ]
          }]
  };

  // Genereate Charts
  
  var lineCharts = [];
  
  lineCharts[0] = new Chart($('#lChart1').get(0).getContext('2d'), {
      type: 'line',
      data: lineChartData[0]
  });

  var doughnutCharts = [];
  
  doughnutCharts[0] = new Chart($('#dChart' + (0 + 1) ).get(0).getContext("2d"),{ type: 'doughnut', data: dChartData[0] });
  doughnutCharts[1] = new Chart($('#dChart' + (1 + 1) ).get(0).getContext("2d"),{ type: 'doughnut', data: dChartData[1] });

});

function addLog(){
  $('#message_table').append('<tr class="danger"><td>10:22:13</td><td>Client 2</td><td>Connection Lost</td><td>Error</td></tr>');
}