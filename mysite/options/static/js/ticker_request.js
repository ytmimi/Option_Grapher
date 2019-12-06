const URL = 'http://127.0.0.1:8000/api/options/';
const BaseColor = $('.ticker-tab').css('color')
const HighlightColor = '#FFFF72'
const allData = allOptionData()
const allCoordinates = {}
let activeTicker = 'GENERIC OPTION'
let contractCheckbox = false

/////////////function that make requests to the server

//GETs all the option data from the server
function allOptionData(){
  let allOptionData = {};
  $.get(URL, function(data, status){
      data.forEach(function(option){
        if (allOptionData[option.stock_ticker]){
          allOptionData[option.stock_ticker].push(option)
        }else{
          allOptionData[option.stock_ticker] = [option]
        }
      });
    })
    return allOptionData
}

//sends a delete request to the server
function deleteOption(ticker, id){
  let slug = ticker.replace(' ', '-')
  let deletURL = URL + slug + `/${id}/`
  $.ajax({
    url: deletURL,
    type: 'DELETE',
    success: function(result) {
        console.log(result)
    }
});
}

/////////////function that effect the ticker tabs

//adds stying
function addHighlight (){
  $(this).css('color', HighlightColor);
}

//removes styling
function removeHighlight (){
  $(this).css('color', BaseColor);
}

//adds stying to a tab and removes it from its siblings
function toggleHighlight(tab){
  addHighlight.apply(tab);
  tab.siblings().each(removeHighlight);
}

//changes the value of the globaal activeTicker varible
function setActiveTicker (ticker){
  activeTicker = ticker
}

//sets the active ticker and adds styling for the active tab
function toggleTab(tab, ticker){
  setActiveTicker(ticker)
  toggleHighlight(tab)
}

//remvos the ticker from the ticker tab if its not a 'GENERIC OPTION'
function removeTicker(ticker){
  if (ticker !== 'GENERIC OPTION'){
    $('.ticker-tab').each(function(){
      if ($(this).text() === ticker) {
        $(this).remove()
      }
    })
  }
}

/////////////function that effect the data table

//removes a single row from the data table
function removeTableRow(row){
  row.remove()
};

//function that should be bound to a remove button
function removeButton(row, ticker){
  let numberOfRows = $('tbody>tr').length
  if (numberOfRows === 1){
    removeTableRow(row)
    //remove ticker from the list as its last row was just removed
    removeTicker(ticker)
    //add the default row to the empty table
    $('table>tbody').append(defaultRow())
  }else{
    removeTableRow(row)
  }
}

//removes all rows from the data table
function removeAllRows(){
  $('tbody>tr').remove()
};

//adds a single data value to a table
function addTableData(value){
  return '<td class="Option-data">'+value+'</td>'
}

//The default row if there isn't any data
function defaultRow(){
  return '<tr><td class="Option-data" colspan="14">'
          +'Use the form above to add options</td></tr>'
}

//adds a single row to the data table
function addTableRow(option){
  let allTd = '';
  let optionData = ['position','option_type','quantity','strike_price','stock_price',
                'traded_price','interest_rate','days_till_exp','iv','delta','gamma',
                'vega','theta','rho']
  for (i in optionData){
    item = optionData[i]
    allTd += addTableData(option[item])
  }
  allTd += addRemoveButtonHTML()
  return '<tr>'+allTd+'</tr>'
}

//adds all rows to the data table
function addAllRows(optionList){
  if (optionList){
    optionList.forEach(function(option){
      $('table>tbody').append(addTableRow(option))
    });
  }else {
    $('table>tbody').append(defaultRow())
  }
};

//adds the html for the remove button to a row of the table
function addRemoveButtonHTML(){
  return '<td class="Option-data">'
          +'<a class="btn btn-danger remove-btn">Remove</a>'
          +'</td>'
};


//removes the option from allData,
//and sends a delete request to the server
function removeOption(index, ticker){
  option = allData[ticker].splice(index, 1)[0]
  deleteOption(option.stock_ticker, option.id)
}

/////////////function that effect the option chart
//chart defined in option_master.js
//(until I figure out how to import the chart variable, this is my work around)
//optionPayoff defined in option_payoff.js

function getCharData(){
  optionList = allData[activeTicker]
  if (optionList) {
    let coordinateData = [{'x':0, 'y':0}]
    //gets all the x values
    for(let i=0; i < optionList.length; i++){
      coordinateData.push({'x':optionList[i].strike_price, 'y':0})
      coordinateData.push({'x':optionList[i].strike_price * 2, 'y':0})
    }
    //set the payoff data
    for (let i = 0; i < optionList.length; i++){
      let option = optionList[i]
      for (let j=0; j < coordinateData.length; j++){
        let stockPrice = coordinateData[j]['x']
        let payoff = optionPayoff(option.option_type, option.position,
        option.strike_price, option.traded_price, option.quantity, stockPrice)
          if (contractCheckbox){
            coordinateData[j]['y'] += payoff * 100
          }
          else{
            coordinateData[j]['y'] += payoff
          }
      }
    }
    return coordinateData.sort(function(coordinateOne,coordinateTwo){
      return coordinateOne['x'] - coordinateTwo['x']
    })
  }
  return null

}

function setChartTitle(){
  console.log(allData[activeTicker])
  if (allData[activeTicker] && allData[activeTicker].length > 0){
    let title = activeTicker + ' Position Payoff Chart';
    chart.options.title.text = title;
  }else{
    chart.options.title.text = 'Position Payoff Chart';
  }
}

function updateChart(){
  let data = getCharData()
  if (data !== null){
    chart.data.datasets[0].data = data
  }else{
    chart.data.datasets[0].data = [{'x':0, 'y':0}]
  }
  setChartTitle()
  chart.update();
}

function toggleContractCheckbox(){
  if (contractCheckbox){
    contractCheckbox = false
  }else{
    contractCheckbox = true
  }
}

function multipyGraphBy100(){
  for (let i =0; i < chart.data.datasets[0].data.length; i++){
    let data = chart.data.datasets[0].data[i]
    let newData = {'x':data.x, 'y':data.y*100}
    chart.data.datasets[0].data[i] = newData
  }
  chart.update();
}


function divideGraphBy100(){
  for (let i=0; i < chart.data.datasets[0].data.length; i++){
    let data = chart.data.datasets[0].data[i]
    let newData = {'x':data.x, 'y':data.y/100}
    chart.data.datasets[0].data[i] = newData
  }
  chart.update();
}








//function that sets all the event listeners
$(document).ready(function (){
  //adds a click function to the remove btn when the page is loaded
  $('.remove-btn').click(function(){
    let row = $(this).parents('tr')
    let index = $('#greeks tr').index($(this).closest('tr')) - 1;
    let ticker = activeTicker
    removeButton(row, ticker)
    removeOption(index, ticker)
    updateChart()
  })
  //adds click functionality to ticker tabs
  $('.ticker-tab').click(function(){
    let tab = $(this)
    let ticker =  $(this).text()
    //toggleTab sets the active ticker
    toggleTab(tab, ticker)
    removeAllRows()
    addAllRows(allData[ticker])
    updateChart()
    //applies the click function for the newly added buttons created with addAllRows
    $('.remove-btn').click(function(){
      let row = $(this).parents('tr')
      let index = $('#greeks tr').index($(this).closest('tr')) - 1;
      let ticker = activeTicker
      removeButton(row, ticker)
      removeOption(index, ticker)
      updateChart()
    })
  });
  $('#contractCheckbox').click(function(){
    toggleContractCheckbox()
    if (contractCheckbox){
      multipyGraphBy100()
    }else{
      divideGraphBy100()
    }
  })


})
