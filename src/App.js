import './App.css';
import Header from "./Header"
import RoutesLocal from "./RoutesLocal";
import MainPage from "./MainPage";

function App() {
  return (
    <div className="App">
        <Header/>
        <RoutesLocal>
           <MainPage/>
        </RoutesLocal>

    </div>
  );
}

export default App;
