const CHART = document.getElementById('option_chart')

var something = "dhasdfahasdfhasdfhasdfh "
console.log(something)
console.log(payoff)

var chart = new Chart(CHART, {
    // The type of chart we want to create
    type: 'line',
    // The data for our dataset
    data: get_data(),
    // Configuration options go here
    options: get_options()
});


function get_data(){
	return {
		// Use labels if not using [{x: _ y: _}, ...] object list
        // labels: payoff.x,
        datasets: [{
        	fill: false,
            borderColor: '#262C2C',
            borderWidth:3,
            radius:0,
            // payoff is a variable passed from the html file
            data: payoff,
        }]
    }
}

function get_options(){
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
                            labelString: 'Stock Price'
                },
                ticks: {
                    // can also use min
                    suggestedMin: 0,
                },
            }],
	        yAxes: [{
                scaleLabel: {
                            display: true,
                            labelString: 'Payoff ($)'
                },
	            ticks: {
	                // suggestedMax: maxYAxis,
	                // suggestedMin: maxYAxis*-1,
	                // stepSize: size,
	            }
        	}],

    	},
    	legend: {
            display: false,
        },
	}
}







