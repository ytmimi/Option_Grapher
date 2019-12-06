// constants and functions
const GREEN = "#329600"
const RED = "rgb(255,0,0)"
const POST_URL = 'http://127.0.0.1:8000/api/options/'

// sets the color for + and - values
function changeColors(){
  if ($(this).text()[0] === "+") {
    $(this).css('color', GREEN)
  }
  else if ($(this).text()[0] === '-') {
    $(this).css('color', RED)
  }
}

//gets all the information from a single row of a table
function getRowData(){
  let data = []
  $(this).parent().siblings().each(function(){
    data.push($(this).text())
  });
  data.push($(this).text())
  data.push(getStockTicker())
  return data
}

// Gets the stock ticker from the top of the page
function getStockTicker(){
  let fullText = $('#Company').text()
  let ticker = fullText.split('(')[1].replace(')', '')
  return ticker
}

//removes "," from number strings
function removeCommas(value){
  return value.replace(',', '')
}

//Get the stock price from the page
function getStockPrice(){
    return $('#stock-price').text()
}

// sets the selector to its initial value
function setExpiratoinDate(){
  let date = $('#expiratoin-selector').attr('value')
  let dateList = $('option')
  let dateText;
  dateList.each(function(){
    if ($(this).val() == date){
      dateText = $(this).text()
      $(this).attr('selected', 'selected')
    }
  })
  return dateText
}

// gets the current date from the selector
function getExpirationDate(){
    let date = $('#expiratoin-selector').val()
    let dateList = $('option')
    let dateText;
    dateList.each(function(){
      if ($(this).val() == date){
        dateText = $(this).text()
        $(this).attr('selected', 'selected')
      }
    })
    return dateText
}

//zeropads date values (months and dates)
function zeroPadValue(month){
  if (month.length < 2) {
    return `0${month}`
  }else {
    return month
  }
}

// converts js Date object into string MM/DD/YYYY
function convertDate(dateString){
  let date = new Date(dateString)
  let month = zeroPadValue((date.getMonth()+1).toString())
  let day = zeroPadValue(date.getDate().toString())
  let year = date.getFullYear().toString()
  return `${month}/${day}/${year}`

}

// gets the option type from its respective table
function getOptionType(){
  let optionType = $(this).parents('table').attr('id')
  return optionType
}

function addOptionToDataBase(){
  let stock_price = getStockPrice()
  let optionType = getOptionType.apply($(this));
  let expirationDate = convertDate(getExpirationDate())
  // optionData is an array [lastTradeDAte, strike, lastPrice, Bid,
  // Ask, change, %change, Volume, openInterest, impliedVolatility, Position, ticker]
  let optionData = getRowData.apply($(this))
  let data = {
    "strike_price": Number(removeCommas(optionData[1])),
    "traded_price":Number(removeCommas(optionData[2])),
    "position":optionData[10],
    "stock_ticker":optionData[11],
    "quantity":1,
    "interest_rate":.025, //might have to remove commas
    "stock_price":Number(removeCommas(stock_price)),
    "option_type":optionType,
    "expiration_date":expirationDate
  }
  $.post(POST_URL, data, function(data, status, xhr){
    console.log(status)
  }, 'json');
}



// workig on the documenet
$(document).ready(function () {
  //set the expiration date
  setExpiratoinDate()
  //changes colors for values that are ment to be highlighted
  $('.Option-data').each(changeColors);
  //update the expiration date when changed
  expirationDate = $('select').change(getExpirationDate)

  // sets event listeners
  $('.Long').click(addOptionToDataBase);

  $('.Short').click(addOptionToDataBase);


});
