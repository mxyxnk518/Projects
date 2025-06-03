import React from 'react';
import { NavLink } from 'react-router-dom';
import { routes } from '../AppRouter';

const Navbar = () => {
  return (
    <nav className='mb-4 p-8 bg-slate-300'>
      <ul>
        {
          routes.map((route, index) => {
            return (
              <li className='mt-2 ' key={index}>
                <NavLink className="text-decoration-none text-slate-800 hover:text-lime-500" to={route.path} exact activeClassName="active">
                  {route.name}
                </NavLink>
              </li>
            );
          })
        }
      </ul>
    </nav>
  );
};

export default Navbar;