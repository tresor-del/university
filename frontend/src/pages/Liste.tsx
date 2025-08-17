import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { FaEdit, FaTrash } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import {toast} from 'react-toastify'

const TableContainer = styled.div`
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(44, 62, 80, 0.08);
  padding: 24px;
  margin: 0 auto;
  max-width: 900px;
`;

const StyledTable = styled.table`
  width: 100%;
  border-collapse: collapse;
  background: #fff;
`;

const Th = styled.th`
  background: #2d3e50;
  color: #fff;
  padding: 12px 8px;
  font-weight: 600;
  text-align: left;
`;

const Tr = styled.tr`
  &:nth-child(even) {
    background: #f5f7fa;
  }
  position: relative;
  cursor: pointer;
  transition: background 0.2s;
  &:hover {
    background: #e3eaf2;
  }
`;

const Td = styled.td`
  padding: 10px 8px;
  color: #223044;
  position: relative;
`;

const FilterRow = styled.tr`
  background: #e3eaf2;
`;

const FilterInput = styled.input`
  width: 90%;
  padding: 6px 8px;
  border: 1px solid #b0bec5;
  border-radius: 4px;
  font-size: 15px;
  background: #f8fafc;
  color: #223044;
`;

const ActionButtons = styled.div`
  display: flex;
  gap: 10px;
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s;
  z-index: 2;
  ${Tr}:hover & {
    opacity: 1;
    pointer-events: auto;
  }
`;

const ActionButton = styled.button`
  background: #2d3e50;
  color: #4fc3f7;
  border: none;
  border-radius: 4px;
  padding: 6px 8px;
  cursor: pointer;
  font-size: 16px;
  transition: background 0.2s, color 0.2s;
  display: flex;
  align-items: center;
  &:hover {
    background: #4fc3f7;
    color: #2d3e50;
  }
`;

function Liste() {
  const [liste, setListe] = useState([]);
  const [filters, setFilters] = useState({
    id_etudiant: "",
    nom: "",
    prenom: "",
    date: "",
  });
  const [hoveredRow, setHoveredRow] = useState<number | null>(null);
  const navigate = useNavigate();
  const url = "http://127.0.0.1:8000/etudiants";

  useEffect(() => {
    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        const formatted = data.map((item) => ({
          id: item.id_etudiant,
          id_etudiant: item.id_etudiant,
          nom: item.nom,
          prenom: item.prenom
        }));
        console.log(data)
        setListe(formatted);
      })
      .catch((err) => console.error("Erreur:", err));
  }, []);

  const handleFilterChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  const filteredListe = liste.filter((student) =>
    Object.entries(filters).every(([key, value]) =>
      String(student[key] ?? "")
        .toLowerCase()
        .includes(value.toLowerCase())
    )
  );

  const handleEdit = (e: React.MouseEvent, id: number) => {
    e.stopPropagation();
    // Naviguer vers la page d'édition (à adapter selon votre routing)
    navigate(`/editer/${id}`);
  };

  const handleDelete = (e: React.MouseEvent, id_etudiant: number) => {
    e.stopPropagation();
    if (window.confirm("Voulez-vous supprimer cet étudiant ?")) {
     
            fetch(`http://127.0.0.1:8000/effacer_etudiant/${id_etudiant}`, {
              method: "DELETE",
            })
              .then((res) => {
                if (res.ok) {
                  toast.warning("Vous avez supprimé un étudiant.");
                  setListe((prev) => prev.filter((etudiant) => etudiant.id_etudiant !== id_etudiant))
                } else {
                  toast.error("Erreur lors de la suppression.");
                }
              })
              .catch(() => toast.error("Erreur lors de la suppression."));
          
    }
  };

  const handleRowClick = (id: number) => {
    // Naviguer vers la page de profil de l'étudiant
    navigate(`/etudiant/${id}`);
  };

  return (
    <TableContainer>
      <StyledTable>
        <thead>
          <Tr>
            <Th>Identifiant</Th>
            <Th>Nom</Th>
            <Th>Prénom</Th>
          </Tr>
          <FilterRow>
            <Td>
              <FilterInput
                name="id_etudiant"
                placeholder="Filtrer..."
                value={filters.id_etudiant}
                onChange={handleFilterChange}
              />
            </Td>
            <Td>
              <FilterInput
                name="nom"
                placeholder="Filtrer..."
                value={filters.nom}
                onChange={handleFilterChange}
              />
            </Td>
            <Td>
              <FilterInput
                name="prenom"
                placeholder="Filtrer..."
                value={filters.prenom}
                onChange={handleFilterChange}
              />
            </Td>
          </FilterRow>
        </thead>
        <tbody>
          {filteredListe.map((student) => (
            <Tr
              key={student.id}
              onMouseEnter={() => setHoveredRow(student.id)}
              onMouseLeave={() => setHoveredRow(null)}
              onClick={() => handleRowClick(student.id)}
              style={{ position: "relative" }}
            >
              <Td>{student.id_etudiant}</Td>
              <Td>{student.nom}</Td>
              <Td>{student.prenom}</Td>
                {hoveredRow === student.id && (
                  <ActionButtons>
                    <ActionButton
                      title="Éditer"
                      onClick={(e) => handleEdit(e, student.id)}
                    >
                      <FaEdit />
                    </ActionButton>
                    <ActionButton
                      title="Supprimer"
                      onClick={(e) => handleDelete(e, student.id_etudiant)}
                    >
                      <FaTrash />
                    </ActionButton>
                  </ActionButtons>
                )}
            </Tr>
          ))}
        </tbody>
      </StyledTable>
    </TableContainer>
  );
}

export default Liste;
