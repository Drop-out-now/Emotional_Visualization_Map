const http = require('http');
const fs = require('fs');
let filepath = 'twitterapi_test/array_lola.txt';

const server = http.createServer((req, res) => {
  fs.watchFile(filepath,(curr,prev) =>{
    fs.readFile(filepath, 'utf-8', (err, data) => {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ value: data }));
    });
  });
});
server.listen(3000);