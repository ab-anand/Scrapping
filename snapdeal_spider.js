var express = require('express');
var request = require('request')
var cheerio = require('cheerio');
var fs = require('fs');
var app = express();
var port = 8000;
var jsonfile=require('jsonfile');

var url="https://www.snapdeal.com/product/selfcare-maroon-nonwired/1202350508";
var file='snapdeal.json'
request(url,function(err,resp,body){
  
 var $=cheerio.load(body);
 var product=$('.pdp-e-i-head').text().toString().trim();
 var price =$('.payBlkBig').text();
 var emi=$('.emi-price').text();
 if(emi=='')
 	emi="Not available";
 var obj={
 	'Product':product,
 	'Price':'Rs. '+price,
 	'Emi':emi
 }
 //console.log(obj);
 jsonfile.writeFile(file, obj, {spaces: 2}, function(err) {
      if(err){
      	 console.error(err);
      }  
      else
        console.log('Scraping successful!');
      })
})