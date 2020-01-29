const express   = require("express");
const port      = process.env.PORT || 8080;
const app       = express();
const dist_path = __dirname + "/dist/";

app.use(express.static(dist_path));
app.get(
    /.*/, 
    function(request, response) {
        response.sendFile(dist_path + "index.html");
    }
);
app.listen(port);

console.log("DEBUG: Server started.");