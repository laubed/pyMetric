var lineCharts = [];
var doughnutCharts = [];

$(document).ready(function(){
  
  	// Chart Data
    
    function MessageViewModel() {
        var self = this;
        self.messages = ko.observableArray();

        function updateMessages() {
            $.getJSON(API_ENDPOINT + "api/v1.0/messages/get?count=20&_t=" + parseInt(((Date.now()/1000))) , function (data) {
                self.messages.removeAll();
                $.each(data.results, function() {
                    self.messages.push({
                        Time: ko.observable(moment.unix(this.Time).format("HH:mm:ss")),
                        Origin: ko.observable(this.Origin),
                        Message: ko.observable(this.Message),
                        Type: ko.observable(this.Type, 10)
                    });
                });
                setTimeout(updateMessages, 2000);
            });
        }

        updateMessages();

    }
    ko.applyBindings(new MessageViewModel(), $('#message_table')[0]);
    
    // Init Functions

    setTimeout(scroll, 2000); // fix issue with website not populated with data

    loadConfig();

});

// Functions

function addLineChart(chartDOMElementID, chartID, origin, timeframe, yMax, yMin, chartHeight, seriesName1, seriesName2){

    // TODO: create DOM automatical and sort by side. Instead of chartDOMElementID, the side as attribut.

    // SeriesName1 == yAxis && SeriesName2 == xAxis

    // Chart Config

    var obj1 = {
        series: [
            {
                // name: "cpu_usage",
                name: seriesName1,
                data: []
            },
            {
                // name: "timeframe",
                name: seriesName2,
                data: [{x:0},{x:0}]
            }
        ]
    };

    var obj2 = {

        axisX: {
            type: Chartist.FixedScaleAxis,
            divisor: 10,
            labelInterpolationFnc: function(value) {
                return moment(value*1000).fromNow();
            }
        },

        axisY: {
            low: yMin,
            high: yMax
        },

        height: chartHeight,

        series: {

        }

    }

    // e.g. obj2.series.cpu_usage: ...

    obj2.series[seriesName1] = {
        showLine: true,
        showPoint: false,
        lineSmooth: Chartist.Interpolation.none()
    }

    obj2.series[seriesName2] = {
        showLine: false,
        showPoint: false,
        showArea: true,
        lineSmooth: Chartist.Interpolation.none()
    }
            
    // Chart Config End;

    lineCharts[chartID] = new Chartist.Line('#' + chartDOMElementID, obj1, obj2);

    getCPU(lineCharts[chartID], origin, timeframe); // e.g. getCPU(lineCharts[0], 'laptop', 60*60);

}

var toBottom = true;

function scroll(){
    var speed = 30; // px/s

    var h = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
    var verticalCoordinate = toBottom ? $(document).height() - h: 0;
    var duration = Math.abs((($(document).height() - h)/speed)*1000);
    console.log(duration);

    toBottom = !toBottom;

    $('body').animate({ scrollTop: verticalCoordinate}, duration, "linear", function(){
        if(toBottom){ location.reload(); }
	setTimeout(scroll, 3000);
    });
}

function getCPU(chart, origin, timeframe){
    $.getJSON(API_ENDPOINT + 'api/v1.0/metrics/get?origin=' + origin + '&key=cpu_usage&fromtime=' + parseInt(((Date.now()/1000) - timeframe)) + "&totime=" + parseInt(((Date.now()/1000))) + "&desc=False&order=time&_t=" + Date.now(), function(data){
            window.setTimeout(function(){ getCPU(chart, origin, timeframe); }, 1000);
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
