import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Liste from "./pages/Liste";
import { Enr } from './pages/Enr';
import { Home } from './pages/Home';
import EtudiantProfile from './pages/EtudiantProfile';
import EditEtudiant from './pages/EditEtudiant';
import { ToastContainer } from 'react-toastify';
import "react-toastify/dist/ReactToastify.css"


function App() {

  return (
    <>
      <Router>
      <Routes>
        <Route path='/' element={<Home />}>
          <Route path="/liste" element={<Liste />} />
          <Route path='/enregistrer' element={<Enr />} ></Route>
          <Route path="/etudiant/:id" element={<EtudiantProfile />} />
          <Route path="/editer/:id" element={<EditEtudiant />} />
        </Route>
      </Routes>
    </Router>
    <ToastContainer position='top-right' autoClose={5000}></ToastContainer>
    </>
  )
}

export default App;
