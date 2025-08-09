import '../styles/Navbar.css'
import { Link } from 'react-router-dom'

export  const Navbar  = () => {
  return (
    <>

      <nav>
      <ul>
        <li>
          <Link className='link' to="/liste">Liste des Étudiants</Link>
        </li>
        <li>
          <Link className='link' to="/enregistrer">Enrégistrer un Étudiant</Link>
        </li>
      </ul>
    </nav>

    </>
  )
}
