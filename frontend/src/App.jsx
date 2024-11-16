import { BrowserRouter, Routes, Route } from 'react-router-dom'
import RenderHome from './components/Home'
import RenderNavbar from './components/Navbar';
import RenderLogIn from './components/LogIn';
import RenderLogOut from './components/LogOut';
import RenderChat from './components/Chat';
import './App.css'
import '@fortawesome/fontawesome-free/css/all.min.css';

function App() {

  return (
      <>
          <RenderNavbar />
          <BrowserRouter>
              <Routes>
                  <Route path='/' element={<RenderHome />} />
                  <Route path='/login' element={<RenderLogIn />} />
                  <Route path="/logout" element={<RenderLogOut/>}/>
                  <Route path='/home/:id' element={<RenderChat />} />
              </Routes>
          </BrowserRouter>
      </>
  )
}

export default App
