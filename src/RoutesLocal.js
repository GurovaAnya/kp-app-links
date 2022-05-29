import React from 'react';
import DocumentInfo from "./DocumentInfo";

import {
    BrowserRouter as Router,
    Routes,
    Route
} from "react-router-dom";
import MainPage from "./MainPage";


const RoutesLocal = ({showSideMenu}) => (
    <Router>
        <Routes>
            <Route path="/document/:id" element={<DocumentInfo/>}/>
            <Route path="/" element={<MainPage showSideMenu={showSideMenu}/>}/>
        </Routes>
    </Router>
);

export default RoutesLocal;