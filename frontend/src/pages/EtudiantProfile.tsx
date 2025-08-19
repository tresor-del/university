import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import styled from "styled-components";
import { FaUserCircle } from "react-icons/fa";
import { toast } from "react-toastify";

const FullPageContainer = styled.div`
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(120deg, #f5f7fa 0%, #e3eaf2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
`;

const ProfileCard = styled.div`
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(44, 62, 80, 0.13);
  padding: 48px 38px 38px 38px;
  min-width: 340px;
  max-width: 420px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

// const ProfilePhoto = styled.img`
//   width: 110px;
//   height: 110px;
//   border-radius: 50%;
//   object-fit: cover;
//   margin-bottom: 22px;
//   border: 4px solid #2d3e50;
//   background: #f5f7fa;
// `;

const IconPhoto = styled(FaUserCircle)`
  width: 110px;
  height: 110px;
  color: #b0bec5;
  margin-bottom: 22px;
  border-radius: 50%;
  background: #f5f7fa;
  border: 4px solid #2d3e50;
  padding: 10px;
`;

const Title = styled.h2`
  color: #2d3e50;
  text-align: center;
  margin-bottom: 24px;
  font-weight: 800;
  letter-spacing: 1px;
  font-size: 2rem;
`;

const InfoList = styled.div`
  width: 100%;
  margin-bottom: 28px;
`;

const Info = styled.div`
  margin-bottom: 18px;
  font-size: 18px;
  color: #223044;
  display: flex;
  justify-content: space-between;
  align-items: center;
  span {
    font-weight: 700;
    color: #2d3e50;
    min-width: 120px;
    display: inline-block;
  }
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 18px;
  margin-top: 10px;
  width: 100%;
  justify-content: center;
`;

const EditButton = styled.button`
  background: #2d3e50;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 12px 28px;
  font-size: 17px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  &:hover {
    background: #223044;
    color: #4fc3f7;
  }
`;

const DeleteButton = styled.button`
  background: #f44336;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 12px 28px;
  font-size: 17px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  &:hover {
    background: #b71c1c;
    color: #fff;
  }
`;


interface Etudiant {
  id: number;
  id_etudiant: number;
  nom: string;
  prenom: string;
  sexe: string;
  date_creation: number;
}

const EtudiantProfile = () => {
  const { id } = useParams();
    const [etudiant, setEtudiant] = useState<Etudiant>({
      id: 0,
      id_etudiant:0,
      nom: "",
      prenom: "",
      sexe: "",
      date_creation: 0,
    });
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/etudiants`)
      .then((res) => res.json())
      .then((data) => {
        const found = data
          .map((item: Etudiant) => ({
            id: item.id_etudiant,
            id_etudiant: item.id_etudiant,
            nom: item.nom,
            prenom: item.prenom,
            sexe: item.sexe,
            date: item.date_creation,
          }))

          .find((et: Etudiant) => String(et.id) === String(id));
        setEtudiant(found);
        console.log(found)
      });
  }, [id]);

  const handleDelete = () => {
    if (
      window.confirm(
        "Êtes-vous sûr de vouloir supprimer cet étudiant ? Cette action est irréversible."
      )
    ) {
      fetch(`http://127.0.0.1:8000/effacer_etudiant/${etudiant.id_etudiant}`, {
        method: "DELETE",
      })
        .then((res) => {
          if (res.ok) {
            toast.success("Étudiant supprimé.");
            navigate("/liste");
          } else {
            toast.error("Erreur lors de la suppression.");
          }
        })
        .catch(() => toast.error("Erreur lors de la suppression."));
    }
  };

  if (!etudiant)
    return (
      <FullPageContainer>
        <ProfileCard>Chargement...</ProfileCard>
      </FullPageContainer>
    );

  return (
    <FullPageContainer>
      <ProfileCard>
          <IconPhoto />
        <Title>Profil Étudiant</Title>
        <InfoList>
          <Info>
            <span>Identifiant :</span> {etudiant.id_etudiant}
          </Info>
          <Info>
            <span>Nom :</span> {etudiant.nom}
          </Info>
          <Info>
            <span>Prénom :</span> {etudiant.prenom}
          </Info>
          <Info>
            <span>Sexe :</span> {etudiant.sexe}
          </Info>
          <Info>
            <span>Date d'inscription :</span> {etudiant.date_creation}
          </Info>
        </InfoList>
        <ButtonGroup>
          <EditButton onClick={() => navigate(`/editer/${etudiant.id}`)}>
            Modifier le profil
          </EditButton>
          <DeleteButton onClick={handleDelete}>Supprimer</DeleteButton>
        </ButtonGroup>
      </ProfileCard>
    </FullPageContainer>
  );
};

export default EtudiantProfile;
