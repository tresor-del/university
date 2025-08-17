import '../styles/Navbar.css'
import { Link } from 'react-router-dom'

export  const Navbar  = () => {
  return (
    <>

      <nav>
      <ul>
        {/* <li>
          <Link className='link' to="/liste">Liste des Étudiants</Link>
        </li> */}
        <li>
          {/* <Link className='link enre '>
              <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#000000"><path d="M440-120v-240h80v80h320v80H520v80h-80Zm-320-80v-80h240v80H120Zm160-160v-80H120v-80h160v-80h80v240h-80Zm160-80v-80h400v80H440Zm160-160v-240h80v80h160v80H680v80h-80Zm-480-80v-80h400v80H120Z"/></svg>
              Filtrer la liste 
           </Link> */}
        </li>
        <li>
          <Link className='link enre' to="/enregistrer">
            <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#000000"><path d="M440-440H200v-80h240v-240h80v240h240v80H520v240h-80v-240Z"/></svg> Ajouter un Étudiant
          </Link>
        </li>
      </ul>
    </nav>

    </>
  )
}
