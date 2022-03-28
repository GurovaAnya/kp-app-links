import './App.css';
import Header from "./Header"
import RoutesLocal from "./RoutesLocal";
import MainPage from "./MainPage";

const App = () => (
    <div className="App">
        <Header/>
        <RoutesLocal>
           <MainPage/>
        </RoutesLocal>

    </div>
)

export default App;
