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


 	// Functions

	function scroll(toBottom, duration){
        /*
            toBottom: true | false,
            duration: time in ms
        */

        var h = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
        var verticalCoordinate = toBottom ? $(document).height() - h: 0; //(-1 * $(document).height());

		$('body').animate({ scrollTop: verticalCoordinate}, duration, "linear", function(){
			scroll(toBottom ? false : true, duration);
		});
 	}

 	// start Scrolling:
    var speed = 20; // px/s
 	scroll(true, ($(document).height()/speed)*1000);
});