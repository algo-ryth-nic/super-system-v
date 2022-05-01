import React from 'react'
import ReactDOM from 'react-dom/client'
import Homepage from './components/homepage'
import TopAppBar from './components/appbar'


ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <TopAppBar />
    <Homepage />
  </React.StrictMode>
)
