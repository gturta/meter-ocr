var express = require('express')
var trainer = require('./routes/trainer')

var app = express()

app.set('view engine', 'pug')
app.get("/", trainer.get)

app.use(express.static('static'))

var server = app.listen(5000,function(){
    console.log("Server listening on "+server.address().address+":"+server.address().port)
})

