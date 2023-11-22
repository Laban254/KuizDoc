import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';  
import logo from './logo.svg';
import Auth from './Components/Auth/Auth';
import Home from './Components/Home/Home';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Auth/>} />
        <Route path="/home" element={<Home/>} />
      </Routes>
    </Router>
  );
}

export default App;
