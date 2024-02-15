import Express from 'express'
import React from 'react'
import ReactDOMServer from 'react-dom/server'

const app = Express()

app.use(Express.static('public'))

app.get('/', (req, res) => {
  res.send(ReactDOMServer.renderToString(
    <div>
      <div id="app"/>
      <script src="client.js"/>
    </div>
  ))
})

app.listen(8000, () => {
  console.log('listening on port 8000')
})