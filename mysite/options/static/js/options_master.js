const CHART = document.getElementById('option_chart')

var maxYAxis = max_val(payoff.y)
var size = axisStepSize(maxYAxis)
console.log(size)


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
        labels: payoff.x,
        datasets: [{
        	fill: false,
            borderColor: '#262C2C',
            borderWidth:3,
            radius:0,
            // payoff is a variable passed from the html file
            data: payoff.y,
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
	                suggestedMax: maxYAxis,
	                suggestedMin: maxYAxis*-1,
	                stepSize: size,
	            }
        	}],
        	xAxes: [{
      			gridLines: {
         			display: false
      			},
      			display:false,
      		}]	
    	},
    	legend: {
            display: false
        },
	}
}





function max_val(arr){
	// finds the max of an array
	abs_array = []
	if(arr.length > 0){
		for(i=0; i < arr.length; i++){
			abs_array.push(Math.abs(arr[i]))
		}
		return Math.max.apply(Math, abs_array)
	}else{
		return 50
	}
}

function axisStepSize(num){
	if (num > 500){
		return 50
	}
	else if (250< num <= 500){
		return 25
	}
	else if (100< num <= 250){
		return 15
	}
	else if (45 < num <=100){
		return 10
	}
	else
		return 5
}












