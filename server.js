var express = require('express');
var app = express();
var childProcess = require('child_process');
var bodyParser = require('body-parser');
var fs = require("fs");

app.set('port', (process.env.PORT || 5000));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(express.static(__dirname + '/public'));

// views is directory for all template files
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');

app.post('/search', function(request, response){
	console.log(request.body);
	py1 = childProcess.spawn('python',['yelp.py',request.body.numberOfBeds,request.body.maxPrice, request.body.city]);
	response.setHeader('Content-Type', 'application/text');

	py1.stdout.on('data', function(data) {

	});
	py1.stdout.on('close', function (data) {
		console.log("Data Recieved!");
		var result = fs.readFileSync("data.json");
		response.send(result);
		console.log(result.length);
	});
});

app.get('/', function(request, response) {
  response.render('pages/test');
});

app.listen(app.get('port'), function() {
  console.log('Node app is running on port', app.get('port'));
});


