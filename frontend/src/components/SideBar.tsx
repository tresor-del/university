import React from "react";
import styled from "styled-components";
import {
  FaUserPlus,
  FaListUl,
  FaAngleLeft,
  FaAngleRight,
} from "react-icons/fa";
import { Link } from "react-router-dom";

type SidebarProps = {
  collapsed: boolean;
  setCollapsed: React.Dispatch<React.SetStateAction<boolean>>;
};

const SidebarContainer = styled.div<{ collapsed: boolean }>`
  width: ${(props) => (props.collapsed ? "70px" : "250px")};
  height: 100vh;
  background-color: #2d3e50;
  color: #fff;
  position: fixed;
  top: 0;
  left: 0;
  padding: 30px 20px 30px 20px;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.08);
  z-index: 100;
  display: flex;
  flex-direction: column;
  align-items: ${(props) => (props.collapsed ? "center" : "flex-start")};
  transition: width 0.3s;
`;

const ToggleButton = styled.button<{ collapsed: boolean }>`
  background: #223044;
  color: #4fc3f7;
  border: none;
  border-radius: 4px;
  padding: 8px;
  cursor: pointer;
  align-self: ${(props) => (props.collapsed ? "center" : "flex-end")};
  margin-bottom: 30px;
  transition: background 0.2s;
  &:hover {
    background: #1a2533;
  }
`;

const NavList = styled.ul<{ collapsed: boolean }>`
  list-style: none;
  padding: 0;
  margin-top: 10px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: ${(props) => (props.collapsed ? "center" : "flex-start")};
`;

const NavItem = styled.li<{ collapsed: boolean }>`
  width: 100%;
`;

const StyledLink = styled(Link)<{ collapsed: boolean }>`
  display: flex;
  align-items: center;
  gap: ${(props) => (props.collapsed ? "0" : "16px")};
  padding: 14px 0;
  font-size: 18px;
  color: #fff;
  text-decoration: none;
  border-bottom: 1px solid #3c4a5a;
  width: 100%;
  justify-content: ${(props) => (props.collapsed ? "center" : "flex-start")};
  background: none;
  transition: background 0.2s, gap 0.3s, color 0.2s;
  &:hover {
    background: #223044;
    color: #4fc3f7;
  }
  svg {
    font-size: 22px;
    color: #4fc3f7;
  }
  span {
    display: ${(props) => (props.collapsed ? "none" : "inline")};
    transition: display 0.3s;
  }
`;

const Sidebar: React.FC<SidebarProps> = ({ collapsed, setCollapsed }) => {
  const handleToggle = () => setCollapsed((c) => !c);

  return (
    <SidebarContainer collapsed={collapsed}>
      <ToggleButton
        collapsed={collapsed}
        onClick={handleToggle}
        title={collapsed ? "Ouvrir le menu" : "Réduire le menu"}
      >
        {collapsed ? <FaAngleRight /> : <FaAngleLeft />}
      </ToggleButton>
      <NavList collapsed={collapsed}>
        <NavItem collapsed={collapsed}>
          <StyledLink to="/enregistrer" collapsed={collapsed}>
            <FaUserPlus />
            <span>Enrégistrer un Étudiant</span>
          </StyledLink>
        </NavItem>
        <NavItem collapsed={collapsed}>
          <StyledLink to="/liste" collapsed={collapsed}>
            <FaListUl />
            <span>Voir la liste des Étudiants</span>
          </StyledLink>
        </NavItem>
      </NavList>
    </SidebarContainer>
  );
};

export default Sidebar;
