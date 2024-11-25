import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { useState, useEffect} from 'react';
import logo from '../assets/images/logo.png';

const RenderNavbar = () => {
   const [isAuth, setIsAuth] = useState(false);
   const isTokenExpired = (token) => {
       const payload = JSON.parse(atob(token.split('.')[1]));
       return payload.exp < Date.now() / 1000;
   };
   useEffect(() => {
       if (localStorage.getItem('access_token') !== null && !isTokenExpired(localStorage.getItem('access_token'))) {
            setIsAuth(true);
        }
   }, [isAuth]);
   return (
      <>
          <div className={"navbar-component"}>
              <Navbar bg="dark" variant="dark">
                  <ul>
                        <li>
                            <Navbar.Brand href="/">
                                <img
                                    alt=""
                                    src={logo}
                                    height="20px"
                                />
                            </Navbar.Brand>
                        </li>
                      <li>
                          <Nav>
                              {isAuth ? <Nav.Link href="/">Home</Nav.Link> : null}
                          </Nav>
                      </li>
                      <li>
                          <Nav>
                              {isAuth ? <Nav.Link href="/logout">Logout</Nav.Link> :
                                  <Nav.Link href="/login">Login</Nav.Link>}
                          </Nav>
                      </li>
                  </ul>
              </Navbar>
          </div>
      </>
   );
}


export default RenderNavbar;