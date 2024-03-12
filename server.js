// fileName : server.js
// Example using the http module
import { createServer } from "http";
import { Express } from "express";

// Create an HTTP server
const app = new Express();
app.get("/", (req, res) => {
  res.send("Hello World");
});

const port = process.env.PORT || 3000;

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
