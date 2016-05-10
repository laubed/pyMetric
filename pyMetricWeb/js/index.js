var lineCharts = [];
var doughnutCharts = [];

$(document).ready(function(){
  
  	// Chart Data
  
    var lineChartData = [];
    
    lineChartData[0] = {
        labels: [""],
        datasets: [
          {
            label: "CPU-Auslastung",
            fillColor: "rgba(220,220,220,0.2)",
            strokeColor: "rgba(220,220,220,1)",
            pointColor: "rgba(220,220,220,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,1)",
            data: [0]
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
    
    lineCharts[0] = new Chart($('#lChart1').get(0).getContext('2d'), {
        type: 'line',
        data: lineChartData[0],
        options: {
            title: {
                display: true,
                position: "top",
                text: "CPU-Auslastung"
            }
        }
    });
  
    doughnutCharts[0] = new Chart($('#dChart' + (0 + 1) ).get(0).getContext("2d"),{ type: 'doughnut', data: dChartData[0] });
    doughnutCharts[1] = new Chart($('#dChart' + (1 + 1) ).get(0).getContext("2d"),{ type: 'doughnut', data: dChartData[1] });


 	// Functions

    var toBottom = true;
	function scroll(){
        var speed = 200; // px/s
        var duration = ($(document).height()/speed)*1000
        var h = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
        var verticalCoordinate = toBottom ? $(document).height() - h: 0; //(-1 * $(document).height());

        toBottom = !toBottom;

		$('body').animate({ scrollTop: verticalCoordinate}, duration, "linear", function(){
			setTimeout(scroll, 2000);
		});
 	}

    function getCPU(origin, count){
        $.getJSON('http://localhost:5000/metrics/api/v1.0/get?origin=' + origin + '&key=cpu_usage&count=' + count, function(response){
                var data = JSON.parse(response);
                var currentData = lineCharts[0].getChartData();

                $.each(data.results, function(){
                    if(checkObjectValue(this.Id, currentData.labels)){
                        lineCharts[0].addChartData(0, { label: this.Id, value: parseInt(this.Value) });
                    }
                });
                
                window.setTimeout(function(){ getCPU(origin, count); }, 1000);
        });
    }


    function checkObjectValue(x, object)
        for(var i in object){
            if(x == this[i]) return true;
        }

        return false;
    };
    

    // Activate Functions

    getCPU('laptop', '20');

    setTimeout(scroll, 2000); // fix issue with website not populated with data


});