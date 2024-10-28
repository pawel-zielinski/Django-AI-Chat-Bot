import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { useState, useEffect} from 'react';

const RenderNavbar = () => {
   const [isAuth, setIsAuth] = useState(false);
   useEffect(() => {
       if (localStorage.getItem('access_token') !== null) {
           setIsAuth(true);
       }
   }, [isAuth]);
   return (
      <>
        <Navbar bg="dark" variant="dark">
          <Nav className="me-auto">
          {isAuth ? <Nav.Link href="/">Home</Nav.Link> : null}
          </Nav>
          <Nav>
          {isAuth ? <Nav.Link href="/logout">Logout</Nav.Link> :
                    <Nav.Link href="/login">Login</Nav.Link>}
          </Nav>
        </Navbar>
       </>
   );
}


export default RenderNavbar;