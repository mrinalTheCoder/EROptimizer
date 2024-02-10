import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ClientComponent from './Components/Client/ClientComponent';
import ServerComponent from './Components/Server/ServerComponent';


const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/client" element={<ClientComponent />} />
        <Route path="/server" element={<ServerComponent />} />
      </Routes>
    </Router>
  );
};

export default App;