let request = require('request-promise');
let cheerio = require('cheerio');
let URL = require('url-parse');
let fs = require('fs');

let MongoClient = require('mongodb').MongoClient;
let assert = require('assert');
let ObjectId = require('mongodb').ObjectID;
let dataUrl = 'mongodb://localhost:27017/meetupDatesDB';


let count = 0;
let userGroupNames = [];
let getGroupTimes = [];
let $ = cheerio;
let tempData = {};


function rss(url, method){
	method = method.toLowerCase();

	let options = {
		url: url,
		headers: {
			'User-Agent': 'request'
		}
	};

	return new Promise(function(resolve, reject){
		request[method](options, function (err, response, body){
			if (err){
				reject(err)
			}

			if (body){

				let $ = cheerio.load(body);
				let times = $('*').toString();

				regStr = times.match(/<p>(Wed(nesday)?|Thur(sday)?|Fri(day)?|Sat(day)?|Sun(day)?|Monday|Tue(day)?).*?<\/p>/ig);
				
					if(regStr === null){
						regStr = [];
					}

			    //Regex was returning duplicates******This returns one of each date
			    regStr = regStr.filter(function(item, index, inputArray){
			    return inputArray.indexOf(item) == index;
			    });
	     			
	    		   	tempData = {"groupName": options.url, "dates: ":regStr};
			    	resolve(tempData);

			}
		});
	});
}

function rssHelper(element){
	return rss(element, 'GET');
}

let data = fs.readFileSync('usergroups.json');
let words = JSON.parse(data);

while(count < words.length){
	userGroupNames.push('https://www.meetup.com/' + words[count].nameInMeetupURL + '/events/rss/');
	count += 1;
}

getGroupTimes = userGroupNames.map(rssHelper);

Promise.all(getGroupTimes)
	.then(function(values){
		
        	let insertDocument = function(db, callback) {
               db.collection('DatesCollection').insert(values
               , function(err, result) {
                 assert.equal(err, null);
                 console.log("Inserted dates and times for Techlahoma meetups in DatesCollection collection.");
                 callback();
                });
              };
            MongoClient.connect(dataUrl, function(err, db) {
 			 assert.equal(null, err);
	   	     insertDocument(db, function() {
               db.close();
              });
            });
	})
	.catch(function(error){
	console.log(error);
	});