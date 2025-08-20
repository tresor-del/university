import { useState } from "react";
import Sidebar from "../components/SideBar";
import { Outlet } from "react-router-dom";
import styled from "styled-components";

const SIDEBAR_WIDTH = 250;
const SIDEBAR_COLLAPSED_WIDTH = 70;

const Layout = styled.div`
  display: flex;
  min-height: 100vh;
`;

const Content = styled.main<{ sidebarWidth: number }>`
  flex: 1;
  margin-left: ${({ sidebarWidth }) => sidebarWidth}px;
  padding: 32px;
  background: #f5f7fa;
  min-height: 100vh;
  transition: margin-left 0.3s;
`;

export const Home = () => {
  const [collapsed, setCollapsed] = useState(false);

  // On passe collapsed et setCollapsed au Sidebar pour synchroniser l'état du sidebar
  return (
    <Layout>
      <Sidebar collapsed={collapsed} setCollapsed={setCollapsed} />
      <Content sidebarWidth={collapsed ? SIDEBAR_COLLAPSED_WIDTH : SIDEBAR_WIDTH}>
        <Outlet />
      </Content>
    </Layout>
  );
};