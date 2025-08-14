import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import '../Liste.css'

export const Enr = () => {

  const [name, setname] = useState("")
  const [prenom, setprenom] = useState("")
  const [id, setid] = useState("")
  const navigate = useNavigate();


  const url = "http://127.0.0.1:8000/enregistrer_etudiant/";

  console.log(name, prenom, id)

  function enregistrer() {
    fetch(url, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'Autorization': 'Bearer'
      },
      body: JSON.stringify({nom: name, prenom: prenom, id_etudiant: id})
    })
    .then(res => res.json())
    .then((data) => {
      console.log(data.result.success)
      if (data.result.success) {
        const result = confirm("Etudiant Enrégistré. Voire ?")
        if (result) {
          navigate("/liste")
        }
        
      }
    })
    .catch(error => console.log(error))
  }

  return (
    <div>
      <form className="form-container" action="">
        <div className="champ">
          <input onChange={ (e) => setname(e.target.value)} type="text" placeholder="Nom de l'étudiant" />
        </div>

        <div className="champ">
          <input onChange={(e) => setprenom(e.target.value)} type="text" placeholder="Prénom de l'étudiant"/>
        </div>

        <div className="champ">
          <input onChange={(e) => setid(e.target.value)} type="number" placeholder="Identifiant de l'étudiant"/>
        </div>
        <input className="btn" type="button" onClick={enregistrer} value="Valider" />
      </form>
    </div>
  );
};
