import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import styled from "styled-components";
import {  FaUser } from "react-icons/fa";
import { toast } from "react-toastify";

const FullPageContainer = styled.div`
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(120deg, #f5f7fa 0%, #e3eaf2 100%);
  display: flex;
  justify-content: center;
`;

const ProfileCard = styled.div`
  border-radius: 18px;
  padding: 48px 38px 38px 38px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 2rem
`;

const IconPhoto = styled(FaUser)`
  width: 200px;
  height: 200px;
  color: #b0bec5;
  // background: #f5f7fa;
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
`;

const Info = styled.div`
  margin-bottom: 18px;
  font-size: 18px;
  color: #223044;
  display: flex;
  // justify-content: space-between;
  gap: 1rem;
  align-items: center;
  span {
    font-weight: 700;
    color: #2d3e50;
    min-width: 120px;
    display: inline-block;
  }
`;

const FlexDiv = styled.div`
  display: flex;
  align-items: start;
  justify-content: center;  
  gap: 5rem;
  width: 100%;
`

const ButtonGroup = styled.div`
  display: flex;
  gap: 18px;
  width: 100%;
  justify-content: center;
`;

const EditButton = styled.button`
  background: #2d3e50;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 12px;
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



const EtudiantProfile = () => {

  interface Etudiant {
  id: number;
  id_etudiant: number;
  nom: string;
  prenom: string;
  sexe: string;
  date_creation: string;
}

  const { id } = useParams();
  const [etudiant, setEtudiant] = useState<Etudiant | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/etudiant/${id}`)
      .then((res) => {
      if (!res.ok) throw new Error("Erreur réseau");
      return res.json();
      })
      .then((data: Etudiant) => {
        console.log(data)
      setEtudiant({
        id: data.id,
        id_etudiant: data.id_etudiant,
        nom: data.nom,
        prenom: data.prenom,
        sexe: data.sexe,
        date_creation: data.date_creation,
      });
      })
      .catch(() => {
      toast.error("Erreur lors de la récupération des données.");
      });
  }, [id]);

  const handleDelete = () => {
    if (
      window.confirm(
        "Êtes-vous sûr de vouloir supprimer cet étudiant ? Cette action est irréversible."
      )
    ) {
      fetch(`http://127.0.0.1:8000/effacer_etudiant/${id}`, {
        method: "DELETE",
      })
        .then((res) => {
          if (res.ok) {
            toast.warning("Étudiant supprimé.");
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
      <Title>Profil Etudiant</Title>
        <FlexDiv>
          <IconPhoto />
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
              <span>Date d'inscription :</span>{" "}
              {etudiant.date_creation
                ? new Date(etudiant.date_creation).toLocaleString("fr-FR", {
                    year: "numeric",
                    month: "long",
                    day: "numeric",
                  })
                : "Non renseignée"}
            </Info>
          </InfoList>
        </FlexDiv>
        <ButtonGroup>
          <EditButton onClick={() => navigate(`/editer/${etudiant.id_etudiant}`)}>
            Modifier le profil
          </EditButton>
          <DeleteButton onClick={handleDelete}>Supprimer</DeleteButton>
        </ButtonGroup>
      </ProfileCard>
    </FullPageContainer>
  );
};

export default EtudiantProfile;
