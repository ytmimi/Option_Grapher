/* calculates the payoff of call and put options
*@param {string} optionType - either Call or Put
*@param {string} position - stock option position, either Long or Short
*@param {number} strikePrice - the excersice price on the option
*@param {number} premium - price payed for an option
*@param {number} quantity - the number of option(s) purchased
*@param {number} stockPrice - the stock price used to determin the option payoff
*/
function optionPayoff(optionType, position, strikePrice,
   premium, quantity, stockPrice ){
     if (optionType === 'Call'){
       return callPayoff(position, strikePrice, premium, quantity, stockPrice)
     }else if (optionType === 'Put') {
       return putPayoff(position, strikePrice, premium, quantity, stockPrice)
   }else{
     throw  new Error('optionType must be either Call or Put');
   }
};

/* return the payoff of a call option given a variable stockPrice
*@param {string} position - stock option position, either Long or Short
*@param {number} strikePrice - the excersice price on the option
*@param {number} premium - price payed for an option
*@param {number} quantity - the number of option(s) purchased
*@param {number} stockPrice - the stock price used to determin the option payoff*/
function callPayoff(position, strikePrice,
   premium, quantity, stockPrice){
   let numPosition = convertPosition(position)
   let payoff = (Math.max(stockPrice - strikePrice, 0) - premium ) * numPosition * quantity
   return roundTwoPlaces(payoff)
};

/* return the payoff of a put option given a variable stockPrice
*@param {string} position - stock option position, either Long or Short
*@param {number} strikePrice - the excersice price on the option
*@param {number} premium - price payed for an option
*@param {number} quantity - the number of option(s) purchased
*@param {number} stockPrice - the stock price used to determin the option payoff*/
function putPayoff(position, strikePrice,
   premium, quantity, stockPrice){
   let numPosition = convertPosition(position)
   let payoff = (Math.max(strikePrice - stockPrice, 0) - premium ) * numPosition * quantity
   return roundTwoPlaces(payoff)
};

/*returns 1 if Long and -1 if Short.
*@param {string} position - stock option position, either Long or Short*/
function convertPosition(position){
  if (position === 'Long'){
    return 1
  }else if (position === 'Short'){
    return -1
  }else{
    throw new Error('position must be either Long or Short')
  }
};

//js has a really weird way of rounding
function roundTwoPlaces(value){
  return Math.round(value * 100) / 100
}


const OPTIONPAYOFF = {
  'optionPayoff': optionPayoff,
}

//module.exports = {optionPayoff, callPayoff, putPayoff, convertPosition}
