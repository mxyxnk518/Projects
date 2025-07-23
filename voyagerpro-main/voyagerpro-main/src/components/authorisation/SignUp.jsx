import React from "react";
import { useState } from "react";
import axios from "axios";
import { useCookies } from "react-cookie";

const SignUp = () => {

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [dob, setDob] = useState("");
  const [message, setMessage] = useState("");
  const [cookies, setCookie, removeCookie] = useCookies(["user"]);

  const submit = async () => {

    if (!name || !email || !password || !dob){
      return setMessage("Please fill out all fields.");
    }


    const response = await axios
      .get(
        `https://mayank518.pythonanywhere.com/api/signup/?name=${name}&email=${email}&password=${password}&dob=${dob}`
      )
      .then((res) => {
        setMessage(res.data.message);
        if (res.data.message == "You have signed up successfully.") {
          setCookie("name", name);
          setCookie("email", email);
          setCookie("logged_in", true);
          window.location.href = "/dashboard";
        }
      });
  };

    return (
    <div className='flex justify-center items-center h-screen '>
        <>
            <div className="relative py-3 sm:max-w-xl sm:mx-auto ">
            <div
            className="relative px-4 py-10 bg-slate-900 mx-8 md:mx-0 shadow rounded-3xl sm:p-10 border-2"
            >
            <div className="max-w-md mx-auto">
                <div className="mt-5 grid grid-cols-1 sm:grid-cols-2 gap-5">
                <div>
                    <label
                    className="font-semibold text-sm text-gray-400 pb-1 block"
                    for="fullname"
                    >Full Name</label>
                    <input
                    className="border rounded-lg px-3 py-2 mt-1 mb-5 text-sm w-full bg-black border-gray-800 text-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
                    type="text"
                    id="fullname"
                    onChange={(e) => setName(e.target.value)}
                    />
                </div>
                <div>
                    <label
                    className="font-semibold text-sm text-gray-400 pb-1 block"
                    for="email"
                    >Email</label>
                    <input
                    className="border rounded-lg px-3 py-2 mt-1 mb-5 text-sm w-full bg-black border-gray-800 text-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
                    type="email"
                    id="email"
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>
                <div>
                  <label
                    className="font-semibold text-sm text-gray-400 pb-1 block"
                    for="dob"
                  >
                    Date of Birth
                  </label>
                  <input
                    className="border rounded-lg px-3 py-2 mt-1 mb-5 text-sm w-full bg-black border-gray-800 text-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
                    type="date"
                    id="dob"
                    onChange={(e) => setDob(e.target.value)}
                  />
                </div>
                <div>
                    <label
                    className="font-semibold text-sm text-gray-400 pb-1 block"
                    for="password"
                    >Password</label>
                    <input
                    className="border rounded-lg px-3 py-2 mt-1 mb-5 text-sm w-full bg-black border-gray-800 text-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
                    type="password"
                    id="password"
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                </div>


                <div className="mt-5">
                    <div>{message}</div>
                <button
                    className="py-2 px-4 bg-blue-600 hover:bg-blue-700 focus:ring-blue-500 focus:ring-offset-blue-200 text-gray-300 w-full transition ease-in duration-200 text-center text-base font-semibold shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 rounded-lg"
                    type="button"
                    onClick={submit}
                >
                    Sign up
                </button>
                </div>
                <div className="flex items-center justify-between mt-4">
                <span className="w-1/5 border-b dark:border-gray-600 md:w-1/4"></span>
                <a
                    className="text-xs text-gray-500 uppercase dark:text-gray-400 hover:underline"
                    href="/signin"
                    >have an account? Log in</a>
                <span className="w-1/5 border-b dark:border-gray-600 md:w-1/4"></span>
                </div>
            </div>
            </div>
        </div>
    </>
  </div>
  )
}

export default SignUp
