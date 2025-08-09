import React from "react";
import '../Liste.css'

export const Enr = () => {
  return (
    <div>
      <form className="form-container" action="">
        <h1>Enrégistrer un étudiant</h1>
        <div className="champ">
          <input type="text" placeholder="Nom de l'étudiant" />
        </div>

        <div className="champ">
          <input type="text" placeholder="Prénom de l'étudiant"/>
        </div>

        <div className="champ">
          <input type="text" placeholder="Identifiant de l'étudiant"/>
        </div>
        <input className="btn" type="button" value="Valider" />
      </form>
    </div>
  );
};
