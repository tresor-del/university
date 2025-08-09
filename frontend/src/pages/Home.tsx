import React from 'react'
import { Navbar } from '../components/Navbar'
import { Outlet } from 'react-router-dom'

export const Home = () => {
  return (
    <div>
        <Navbar />
        <Outlet />
    </div>
  )
}
