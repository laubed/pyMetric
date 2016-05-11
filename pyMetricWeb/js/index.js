var lineCharts = [];
var doughnutCharts = [];

$(document).ready(function(){
  
  	// Chart Data
    
    lineCharts[0] = new Chartist.Line('#lineChart1', {
                        series: [
                            {
                                name: "cpu_usage",
                                data: []
                            },
                            {
                                name: "timeframe",
                                data: [{x:0},{x:0}]
                            }
                        ]
                    }, {
                    series: {
                    "timeframe":{
                        showLine: false,
                        showPoint: false
                    },
                    "cpu_usage":{
                        showLine: true,
                        showPoint: false
                    }
                    },
          axisX: {
            type: Chartist.FixedScaleAxis,
            divisor: 10,
            labelInterpolationFnc: function(value) {
              return moment(value*1000).fromNow();
            }
          },
          axisY: {
            low: 0,
            high: 100
          },
          height: 400
        });
    /*

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
    */
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

    function getCPU(chart, origin, timeframe){
        $.getJSON('http://localhost:5000/api/v1.0/metrics/get?origin=' + origin + '&key=cpu_usage&fromtime=' + parseInt(((Date.now()/1000) - timeframe)) + "&totime=" + parseInt(((Date.now()/1000))) + "&desc=False&order=time&_t=" + Date.now(), function(data){
                window.setTimeout(function(){ getCPU(chart, origin, timeframe); }, 1000);
                console.log(chart);
                ndata = [];

                chart.data.series[1].data = [];
                $.each(data.results, function(){
                    ndata.push( { y: parseFloat(this.Value), x: this.Time });
                });
                chart.data.series[0].data = ndata;
                chart.data.series[1].data = [{x:parseInt(((Date.now()/1000) - timeframe)),y:0},{x:parseInt(((Date.now()/1000))), y:0}];
                chart.update();


        });
    }


    function checkObjectValue(x, object){
        for(var i in object){
            if(x == this[i]) return true;
        }

        return false;
    };
    
    // Activate Functions

    getCPU(lineCharts[0], 'laptop', 60);

    setTimeout(scroll, 2000); // fix issue with website not populated with data


});