var lineCharts = [];
var doughnutCharts = [];

$(document).ready(function(){
  
  	// Chart Data
    
    lineCharts[0] = new CanvasJS.Chart("lineChart1", {
        animationEnabled: false,
        data: [{
            type: "spline",
            dataPoints: [
                { x: 10, y: 10 },
                { x: 20, y: 12 },
                { x: 30, y: 8 },
                { x: 40, y: 14 },
                { x: 50, y: 6 },
                { x: 60, y: 24 },
                { x: 70, y: 4 },
                { x: 80, y: 10 }
            ]
        }]
    });

    lineCharts[0].render();

    doughnutCharts[0] = new CanvasJS.Chart("doughnutChart1", {
        animationEnabled: false,
        toolTip: {
            enabled: true,
        },
        data: [{
            type: "doughnut",
            dataPoints: [
                {  y: 53.37 },
                {  y: 35.0 },
                {  y: 7 },
                {  y: 2 },
                {  y: 5 }
            ]
        }]
    });

   doughnutCharts[0].render();

    // Functions

    function addChartData(chart, data){
        var length = chart.options.data[0].dataPoints.length;

        chart.options.data[0].dataPoints[length] = data;

        chart.render();
    }

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

    function getCPU(chart, origin, count){
        $.getJSON('http://localhost:5000/api/v1.0/metrics/get?origin=' + origin + '&key=cpu_usage&count=' + count + "&desc=False&order=time&_t=" + Date.now(), function(data){
                chart.options.data[0].dataPoints = [];
                $.each(data.results, function(){

                    addChartData(chart, { y: parseFloat(this.Value), x: this.Time });

                });
                
                window.setTimeout(function(){ getCPU(chart, origin, count); }, 1000);
        });
    }


    function checkObjectValue(x, object){
        for(var i in object){
            if(x == this[i]) return true;
        }

        return false;
    };
    
    // Activate Functions

    getCPU(lineCharts[0], 'laptop', '60');

    setTimeout(scroll, 2000); // fix issue with website not populated with data


});