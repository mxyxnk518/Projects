import React from "react";
import { useState } from "react";
import { useCookies } from "react-cookie";

const AdminLogin = () => {

    const adminpassword = "blacksheep"

    const [password, setPassword] = useState("")
    const [cookies, setCookie, removeCookie] = useCookies(["user"]);

    const login = () => {
        if (password == adminpassword) {
            setCookie("admin", true)
            window.location.href = "/admin"
        } else {
            alert("Incorrect Password")
        }
    }

    return (
    <div>
      <label>Password: </label>
      <input type="password" onChange={(e) => setPassword(e.target.value)} />

      <br /><br />

      <button onClick={() => login()} type="button" className="bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-md">Login</button>
    </div>
  );
};

export default AdminLogin;
