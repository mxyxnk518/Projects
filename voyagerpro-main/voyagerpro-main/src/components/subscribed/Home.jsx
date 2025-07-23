import React from "react";
import { useCookies } from "react-cookie";

const Home = () => {
  const [cookies, setCookie, removeCookie] = useCookies(["user"]);

  if (!cookies.name == true || !cookies.logged_in == true) {
    console.log(false);
    return (window.location.href = "/signin");
  }

  function upperCaseFirstLetters(str) {
    return str
      .split(" ")
      .map((word) => word[0].toUpperCase() + word.slice(1))
      .join(" ");
  }

  const logout = () => {
    removeCookie("name");
    removeCookie("logged_in");
    removeCookie("email")
    return (window.location.href = "/signin");
  };

  return (
    <div>
      <h1>{upperCaseFirstLetters(cookies.name)}</h1>

      <button type="button" onClick={logout}>
        Log out
      </button>
    </div>
  );
};

export default Home;
