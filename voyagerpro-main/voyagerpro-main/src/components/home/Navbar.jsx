import React, { useState } from 'react';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div>
      <div className="navbar relative z-10"> 
        <div className="">
          <button className="btn btn-square btn-ghost mr-5" onClick={toggleMenu}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" className="inline-block w-5 h-5 stroke-current">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path>
            </svg>
          </button>
        </div>
        {isOpen && (
          <div className="flex flex-col absolute top-10 left-0 w-40 z-10 ml-[-15px]"> 
            <a href='/'><button className="bg-yellow-700 text-yellow-200 border border-yellow-200 border-b-4 font-medium overflow-hidden relative px-9 py-2 mb-2 mt-10 rounded-md hover:brightness-150 hover:border-t-4 hover:border-b active:opacity-75 outline-none duration-300 group">
              Home
            </button></a>
            <a href='/generator'><button className="bg-yellow-700 text-yellow-200 border border-yellow-200 border-b-4 font-medium overflow-hidden relative px-6 py-2 mb-2 rounded-md hover:brightness-150 hover:border-t-4 hover:border-b active:opacity-75 outline-none duration-300 group">
              Generate
            </button></a>
            <a href='/dashboard'><button className="bg-yellow-700 text-yellow-200 border border-yellow-200 border-b-4 font-medium overflow-hidden relative px-5 py-2 rounded-md hover:brightness-150 hover:border-t-4 hover:border-b active:opacity-75 outline-none duration-300 group">
              Dashboard
            </button></a>
          </div>
        )}
        <button className="bg-yellow-900 text-yellow-400 border border-yellow-400 border-b-4 font-medium overflow-hidden relative px-4 py-2 rounded-md hover:brightness-150 hover:border-t-4 hover:border-b active:opacity-75 outline-none duration-300 group">
          Voyager
        </button>
      </div>
    </div>
  );
};

export default Navbar;
