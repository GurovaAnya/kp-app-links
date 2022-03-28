import React from 'react';
import DocumentInfo from "./DocumentInfo";

import {
    BrowserRouter as Router,
    Routes,
    Route
} from "react-router-dom";
import MainPage from "./MainPage";


const RoutesLocal = () => (
    <Router>
        <Routes>
            <Route path="/document/:id" element={<DocumentInfo/>}/>
            <Route path="/main" element={<MainPage/>}/>
        </Routes>
    </Router>
);

export default RoutesLocal;