const express = require('express');
const axios = require('axios');

const app = express();

app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  next();
});

app.get('/api/*', async (req, res) => {
  try {
    const response = await axios.get(`https://api.sportmonks.com/v3/football${req.url}`, {
      headers: {
        'Authorization': `Bearer 4yW4jorJiaeP38MGImkZaMrAGhNI6pu8Gidn0zxueDvDHtOg0B78ojT5uOXN`,
        'Content-Type': 'application/json'
      }
    });
    res.json(response.data);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error fetching data' });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Proxy server listening on port ${PORT}`);
});