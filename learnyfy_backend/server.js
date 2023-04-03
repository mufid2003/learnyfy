const express = require('express')
const axios = require('axios')
const app = express()
const port = 3030
const apiKey = 'AIzaSyAc71axiSPsLqn5tXwN-kDpGS7PQq_-K8M'
const baseUrl = 'https://www.googleapis.com/youtube/v3'

//https://www.googleapis.com/youtube/v3/search?key=apiKey&type=video&part=snippet&q=foo
//https://www.googleapis.com/youtube/v3/commentThreads?part=snippet%2Creplies&videoId=_VB39Jo8mAQ&key=AIzaSyAc71axiSPsLqn5tXwN-kDpGS7PQq_-K8M

app.get('/', (req, res) => {
    res.send("Hello from Express")
})
app.get('/search', async (req, res, next) => {
    try {
        const searchQuery = req.query.search_query;
        const url = `${baseUrl}/search?key=${apiKey}&type=video&part=snippet&q=${searchQuery}`;
        const response = await axios.get(url);
        console.log(response.data.items);
        const titles = response.data.items.map((item) => item.snippet.title);
        res.send(response.data.items);
    } catch (err) {
        next(err)
    }

})

app.get('/comment', async (req, res, next) => {
    try {
        const searchQuery = req.query.search_query;
        const url = `${baseUrl}/commentThreads?part=snippet%2Creplies&videoId=_VB39Jo8mAQ&key=${apiKey}`;
        const response = await axios.get(url)
        const titles = response.data.items.map((item) => item.snippet.title);
        res.send(response.data);
    } catch (err) {
        next(err)
    }
})
app.listen(port, () => {
    console.log('server started');
})