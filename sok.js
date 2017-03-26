//Problem 1

function filldataandconsoleit() {
//To grab the data 
    var product_category = document.getElementsByClassName('product')[0].childNodes[1].innerText.trim();
    var product_name = document.getElementsByClassName('pb-product-title')[0].childNodes[0].nodeValue.trim();
    var product_price = document.getElementsByClassName('price')[0].childNodes[2].nodeValue.trim();

    var data = {
        product_category:"Home->" + product_category,
        product_name: product_name,
        product_price: product_price
    }
    console.log(data);
}

function task1() {
//To print in console whenever button is clicked
    document.getElementById("add_to_bag").onclick = filldataandconsoleit;

}




document.addEventListener("DOMContentLoaded", function(event) {
    task1();
});

//Problem 2


function fillcartinfoandconsoleit() {

    var taskdata = {};
    var total = document.querySelectorAll(".pb-cart-item-price .price")[3].innerText.trim();

    taskdata['total_price'] = total;

    var cartitems = [];

    var noofitemsincart = document.getElementsByClassName('pb-product-lginfo').length;
    for (i = 0; i < noofitemsincart; i++) {

        var eachproduct = document.getElementsByClassName('pb-product-lginfo')[i];


        var productname = eachproduct.childNodes[1].innerText;
        var price = eachproduct.querySelectorAll('.price')[0].lastChild.nodeValue.trim()
        var quantity = document.getElementsByClassName('discoun')[i].childNodes[1].innerText;


        var peiceprice = document.querySelectorAll('.media-body span.cart-price .price-discount')[(2 * i) + 1].innerText.trim();

        var obj = {
            product_name: productname,
            product_qty: quantity,
            unit_price: price,
            line_item_total: peiceprice
        }
        cartitems.push(obj);
    }
    taskdata['items'] = cartitems;

    console.log(taskdata);
}

function task2() {

    fillcartinfoandconsoleit();

    // whenever cart updates data is printed again
    document.addEventListener("DOMNodeRemoved", function() {
        fillcartinfoandconsoleit();
    });

}

document.addEventListener("DOMContentLoaded", function(event) {
    task2();
});