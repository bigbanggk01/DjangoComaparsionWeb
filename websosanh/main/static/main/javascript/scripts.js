let prices = [];
let top5;
$(document).ready(function () {
   $('#login-button').mouseup(function (e) { 
        e.preventDefault();
        $(this).parent().find(".login-field").toggle();
        $(".login-modal").toggle();
   });
   let all;

   all = $(".card").toArray();
   all.forEach(getprice);
   prices.sort(function(a, b){return a-b});
   top5 = prices[5];
   $(".card").each(addLowCostAttribute);
});

function getprice(element){
   let price = element.innerText.split(/\r?\n/)[1].split(" ")[0].replace(/,/g,"");
   prices.push(parseInt(price));
}

function addLowCostAttribute(){
   let price = $(this).find('#product-price').text();
      price = price.trim().split(" ")[0].split("-")[0].replace(/,/g,"");
      console.log(price);
      price = parseInt(price);
      if(price<top5){
         $(this).css("border","5px solid #f4511e");
   }
}