import { useState } from 'react'
import Topbar from './components/Topbar.jsx'
import Home from './components/home/Home.jsx'
import Browse from './components/browse/Browse.jsx'

export default function App() {
  const [page, setPage] = useState('home')

  return (
    <>
      <Topbar page={page} setPage={setPage} />
      {page === 'home' ? <Home setPage={setPage} /> : <Browse />}
    </>
  )
}
