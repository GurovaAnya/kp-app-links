import React from 'react';
import DocumentInfo from "./DocumentInfo";

import {
    BrowserRouter as Router,
    Routes,
    Route
} from "react-router-dom";


const RoutesLocal = () => (
  <Router>
    <Routes>
      <Route path="/document/:id" element={<DocumentInfo/>} />
    </Routes>
  </Router>
);

export default RoutesLocal;