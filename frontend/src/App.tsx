import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Liste from "./pages/Liste";
import { Enr } from './pages/Enr';
import { Home } from './pages/Home';


function App() {

  return (
    <>
      <Router>
      <Routes>
        <Route path='/' element={<Home />}>
          <Route path="/liste" element={<Liste />} />
          <Route path='/enregistrer' element={<Enr />} ></Route>
        </Route>
        
      </Routes>
    </Router>
    </>
  )
}

export default App;
