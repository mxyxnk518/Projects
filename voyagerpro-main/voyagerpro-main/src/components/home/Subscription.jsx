import React from 'react';
import { useCookies } from "react-cookie";

const Subscription = () => {
  const [cookies, setCookie, removeCookie] = useCookies(["user"]);  
  return (
    <div className='flex justify-center items-center' id='subscription'>
      <div className="group before:hover:scale-95 before:hover:h-72 before:hover:w-screen before:hover:rounded-b-2xl before:transition-all before:duration-500 before:content-[''] before:w-screen before:h-24 before:rounded-t-2xl before:bg-gradient-to-bl from-yellow-800 via-cyan-700 to-yellow-600 before:absolute before:top-0 h-72 relative bg-black flex flex-col items-center justify-center gap-2 text-center rounded-2xl overflow-hidden w-screen">
        <div className="w-28 h-28 bg-yellow-600 mt-8 rounded-full border-4 border-gray-400 z-10 group-hover:scale-150 group-hover:-translate-x-24 group-hover:-translate-y-20 transition-all duration-500"></div>
        <div className="z-10 group-hover:-translate-y-10 transition-all duration-500">
          <span className="text-2xl font-semibold text-gray-200">Voyager Pro</span>
          <p className="text-gray-200">Travel Smarter, Not Harder: Your Ultimate Itinerary Planner App!</p>
        </div>
               {!cookies.email ? (
          <a
            className="bg-yellow-900 px-4 py-1 text-white rounded-md z-10 hover:scale-125 transition-all duration-500 hover:bg-yellow-700"
            href="/signin"
          >
            Subscribe
          </a>
        ) : (
          <a
            className="bg-yellow-900 px-4 py-1 text-white rounded-md z-10 hover:scale-125 transition-all duration-500 hover:bg-yellow-700"
            href="/dashboard"
          >
            Dashboard
          </a>
        )}
      </div>
    </div>
  );
}

export default Subscription;
