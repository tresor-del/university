import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import styled from "styled-components";
import { toast } from "react-toastify";

const FormContainer = styled.div`
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(44, 62, 80, 0.08);
  padding: 32px 28px;
  margin: 40px auto;
  max-width: 420px;
`;

const StyledForm = styled.form`
  display: flex;
  flex-direction: column;
  gap: 22px;
`;

const StyledInput = styled.input`
  padding: 12px 14px;
  border: 1px solid #b0bec5;
  border-radius: 6px;
  font-size: 16px;
  background: #f8fafc;
  color: #223044;
  outline: none;
  transition: border 0.2s;
  &:focus {
    border: 1.5px solid #4fc3f7;
    background: #f0f7fa;
  }
`;

const SubmitButton = styled.input`
  background: #2d3e50;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 12px 0;
  font-size: 17px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 10px;
  transition: background 0.2s;
  &:hover {
    background: #223044;
    color: #4fc3f7;
  }
`;

const Title = styled.h2`
  color: #2d3e50;
  text-align: center;
  margin-bottom: 18px;
  font-weight: 700;
  letter-spacing: 1px;
`;

interface Etudiant {
  id: number;
  id_etudiant: number;
  nom: string;
  prenom: string;
  sexe: string;
  date_creation: number;
}

const EditEtudiant = () => {
  const { id } = useParams();
  const [etudiant, setEtudiant] = useState<Etudiant | null>(null);
  const [nom, setNom] = useState("");
  const [prenom, setPrenom] = useState("");
  const [sexe, setSexe] = useState("");
  const navigate = useNavigate();

    useEffect(() => {
      fetch(`http://127.0.0.1:8000/etudiant/${id}`)
        .then((res) => {
        if (!res.ok) throw new Error("Erreur réseau");
        return res.json();
        })
        .then((data) => {

          if (data) {

            setEtudiant({
              id: data.id,
              id_etudiant: data.id_etudiant,
              nom: data.nom,
              prenom: data.prenom,
              sexe: data.sexe,
              date_creation: data.date_creation,
            });

          } else {
            toast.error("Etudiant non trouvé");
          }
        })
        .catch(() => {
        toast.error("Erreur lors de la récupération des données.");
        });
    }, [id]);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    fetch(`http://127.0.0.1:8000/modifier_etudiant/${id}`, {
      method: "PUT",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        nom: nom,
        prenom: prenom,
        sexe: sexe
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
            toast.success(`Etudiant ${id} enrégistré avec succes`);
            setTimeout(() => {
                navigate(`/etudiant/${id}`);
            }, 1200);
            
        } else {
            toast.error("Une erreur s'est produite. Veuillez recommencer");
        }
        
      });
  }

  if (!etudiant) return <FormContainer>Chargement...</FormContainer>;

  return (
    <FormContainer>
      <Title>Modifier l'Étudiant</Title>
      <StyledForm onSubmit={handleSubmit}>
        <StyledInput
          value={etudiant.id_etudiant}
          disabled
        />
        <StyledInput
          value={etudiant.nom}
          onChange={(e) => setNom(e.target.value)}
          type="text"
          placeholder="Nom"
        />
        <StyledInput
          value={etudiant.prenom}
          onChange={(e) => setPrenom(e.target.value)}
          type="text"
          placeholder="Prénom"
        />
        <StyledInput
          value={etudiant.sexe}
          onChange={(e) => setSexe(e.target.value)}
          type="text"
          placeholder="Sexe"
        />
        <SubmitButton type="submit" value="Enregistrer" />
      </StyledForm>
    </FormContainer>
  );
};

export default EditEtudiant;