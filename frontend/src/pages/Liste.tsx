import React, { useState, useEffect } from "react";
import '../Liste.css'

function Liste() {
  const [liste, setListe] = useState([]);
  const url = "http://127.0.0.1:8000/etudiants";

  useEffect(() => {
    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        const formatted = data.map(item => ({
          id: item[0],
          id_etudiant: item[1],
          nom: item[2],
          prenom: item[3],
          date: item[4]
        }));
        setListe(formatted);
        console.log(formatted);
      })
      .catch((err) => console.error("Erreur:", err));
  }, []);

  return (
    <div className="etu-container">
        <table>
          <thead>
            <th>Identifiant</th>
            <th>Nom</th>
            <th>Prénom</th>
            <th>Date d'inscription</th>
          </thead>
        {liste.map((student) => (
          <tr>
            <td>{student.id_etudiant}</td>
            <td>{student.nom}</td>
            <td>{student.prenom}</td>
            <td>{student.date}</td>
          </tr>
        ))}
        </table>
    </div>
  );
}

export default Liste;
