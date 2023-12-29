const express = require('express');
const router = express.Router();

// middleware specific to this router
router.use((req, res, next) => {
  console.log('Time: ', Date.now());
  next();
});

// define the home page route
router.get('/', function(req, res) {
  res.send('User home page');
});

// define the about route
router.get('/about', function(req, res) {
  res.send('About users');
});

module.exports = router;
