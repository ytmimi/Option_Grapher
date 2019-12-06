const CHART = document.getElementById('option_chart')

//sets up the chart object
var chart = new Chart(CHART, {
    // The type of chart we want to create
    type: 'line',
    // The data for our dataset
    data: setData(),
    // Configuration options go here
    options: getChartOptions()
});

//sets the data values and settings for the chart
function setData(){
	return {
		// Use labels if not using [{x: _ y: _}, ...] object list
        // labels: payoff.x,
        datasets: [{
        	fill: false,
          borderColor: '#262C2C',
          borderWidth:3,
          radius:0,
          // payoff is a variable passed from the html file
          data: [{x:0, y:0},]
        }]
    }
}

//sets the options for the chart
function getChartOptions(){
	return {
		defaultFontFamily: 'Roboto Condensed',
		defaultFontSize: 20,
		title: {
      display: true,
      text: "Position Payoff Chart",
      fontSize: 20,
      fontFamily:"Roboto Condensed",
      fontColor:"#262C2C",
    },
		elements: {
      line: {
        tension: 0, // disables bezier curves
      },
		},
		scales: {
      xAxes: [{
        display: true,
        type:'linear',
        gridLines: {
          display: false,
        },
        position: 'bottom',
        scaleLabel: {
          display: true,
          labelString: 'Stock Price (At expiration)'
        },
        ticks: {
          suggestedMin: 0,
        },
      }],
      yAxes: [{
        scaleLabel: {
          display: true,
          labelString: 'Payoff ($)'
        },
      }],
  	},
    	legend: {
        display: false,
      },
	}
}
