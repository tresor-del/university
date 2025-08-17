import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
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

export const Enr = () => {
  const [name, setname] = useState("");
  const [prenom, setprenom] = useState("");
  const [id, setid] = useState("");
  const [sexe, setSexe] = useState("")
  const navigate = useNavigate();

  const url = "http://127.0.0.1:8000/enregistrer_etudiant/";

  function enregistrer() {
    fetch(url, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        Autorization: "Bearer",
      },
      body: JSON.stringify({id_etudiant: id, nom: name, prenom: prenom,  sexe: sexe }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          toast.success("Etudiant Enrégistré avec succes");
          setTimeout(() => {
            navigate(`/etudiant/${id}`);
          }, 1200);
        } else {
          toast.error("Une erreur s'est produite. Veuillez réessayer")
        }
      })
      .catch((error) => console.log(error));
  }

  return (
    <FormContainer>
      <Title>Enregistrer un Étudiant</Title>
      <StyledForm action="">
        <StyledInput
          onChange={(e) => setname(e.target.value)}
          type="text"
          placeholder="Nom de l'étudiant"
        />
        <StyledInput
          onChange={(e) => setprenom(e.target.value)}
          type="text"
          placeholder="Prénom de l'étudiant"
        />
        <StyledInput
          onChange={(e) => setid(e.target.value)}
          type="number"
          placeholder="Identifiant de l'étudiant"
        />
        <StyledInput
          onChange={(e) => setSexe(e.target.value)}
          type="text"
          placeholder="Sexe"
        />
        <SubmitButton type="button" onClick={enregistrer} value="Valider" />
      </StyledForm>
    </FormContainer>
  );
};
