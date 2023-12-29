const express = require('express');
const app = express();
const userRouter = require('./users/userRoutes'); // the path to your router file

app.use('/users', userRouter);


// Catch 404 and forward to error handler
app.use((req, res, next) => {
    res.status(404).send("Sorry can't find that!")
  });
  
  // Error handler
  app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Something broke!');
  });
  