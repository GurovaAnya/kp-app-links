import React from "react";
import {Graph} from "./Graph";

const MainPage = ({showSideMenu}) => {
    console.log("MainPage", showSideMenu);
    return (
        <>
            <Graph showSideMenu={showSideMenu}/>
        </>
    );
}

export default MainPage;