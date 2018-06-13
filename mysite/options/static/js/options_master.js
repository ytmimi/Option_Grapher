const CHART = document.getElementById('option_chart')

var something = "dhasdfahasdfhasdfhasdfh "
console.log(something)

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
            text: "Payoff Chart",
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
	        yAxes: [{
	            ticks: {
	                // suggestedMax: maxYAxis,
	                // suggestedMin: maxYAxis*-1,
	                // stepSize: size,
	            }
        	}],
        	xAxes: [{
      			gridLines: {
         			display: false
      			},
      			display:true,
      		}]	
    	},
    	legend: {
            display: false
        },
	}
}







