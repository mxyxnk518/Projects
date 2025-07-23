import React from 'react';
import { useState, useEffect } from "react";
import axios from "axios"
import { useCookies } from "react-cookie";

const SignIn = () => {
 
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [message, setMessage] = useState("")
  const [cookies, setCookie, removeCookie] = useCookies(['user'])

  const login = async () => {

    if (!email || !password) {
      return setMessage("Please fill the form completely.")
    }


    const response = await axios.get(
      `https://mayank518.pythonanywhere.com/api/login/?email=${email}&password=${password}`
    ).then(
      res => {
        if (res.data.message == "True"){
          setCookie('name', res.data.name)
          setCookie("email", email)
          setCookie('logged_in', true)
          return window.location.href = "/dashboard"
        } else {
          setMessage(res.data.message)
        }

      }
    )
  }

  useEffect(() => {
    if (cookies.logged_in) {
      window.location.href = "/dashboard"
    }
  }, []) 
 
  return (
    <div className='flex justify-center items-center h-screen'>
      <div className="relative">
        
        <div className="absolute inset-0  opacity-50 rounded-lg"></div>
        <div id="form-container" className="p-16 rounded-lg shadow-2xl w-80 relative z-10 transform transition duration-500 ease-in-out border-2">
          <h2 id="form-title" className="text-center text-3xl font-bold mb-10">Login</h2>
          <form className="space-y-5">
            <input className="w-full h-12 border border-gray-800 px-3 rounded-lg" placeholder="Email" id="" name="" type="text" onChange={(e) => setEmail(e.target.value)} />
            <input className="w-full h-12 border border-gray-800 px-3 rounded-lg" placeholder="Password" id="" name="" type="password" onChange={(e) => setPassword(e.target.value)} />
            <h2>
              {message}
            </h2>           
            <button className="w-full h-12 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type='button' onClick={login}>Sign in</button>
            <a className="text-blue-500 hover:text-blue-800 text-sm" href="#">Forgot Password?</a>
            <p className='text-xs text-gray-600'>Don't have an account?<a className="text-blue-500 hover:text-blue-800 ml-2" href='/signup'>Sign Up</a></p>
          </form>
        </div>
      </div>
    </div>
  )
}

export default SignIn;
