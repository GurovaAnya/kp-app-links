import './App.css';
import Header from "./Header"
import RoutesLocal from "./RoutesLocal";
import MainPage from "./MainPage";
import {useState} from "react";

const App = () => {
    const [showSideMenu, setShowSideMenu] = useState(true);
    console.log("App", showSideMenu);
    return (
        <div className="App">
            <Header toggleSideMenu={() => setShowSideMenu(!showSideMenu)}/>
            <RoutesLocal showSideMenu={showSideMenu}>
                <MainPage showSideMenu={showSideMenu}/>
            </RoutesLocal>

        </div>
    );
}

export default App;
