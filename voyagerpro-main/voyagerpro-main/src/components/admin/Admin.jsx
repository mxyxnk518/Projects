import React, { useState, useEffect } from "react";
import { useCookies } from "react-cookie";
import axios from "axios";

const Admin = () => {
  const [cookies, setCookie, removeCookie] = useCookies(["user"]);
  const [temp, setTemp] = useState("");
  const [messages, setMessages] = useState("");

  const getMessages = async () => {
    const response = await axios
      .get(`https://mayank518.pythonanywhere.com/api/contact/fetch/`)
      .then((res) => {
        setTemp(res.data.messages);
        setMessages(res.data.messages);
      });
  };

  useEffect(() => {
    if (!cookies.admin) {
      window.location.href = "/admin/login";
    }
    getMessages();
  }, []);

  const deleteMessage = async (id) => {
    let temp = messages.filter((element) => element.id !== id);
    setMessages(temp.length == 0 ? "" : temp);
    const response = await axios
      .get(`https://mayank518.pythonanywhere.com/api/contact/delete/?id=${id}`)
      .then((res) => {
        getMessages();
      });
  };

  const handleLogout = () => {
    removeCookie("admin");
    window.location.href = "/admin/login";
  };

  const filterSolved = () => {
    setMessages(temp.filter((element) => element.solved === true))
  }

  const filterUnsolved = () => {
    setMessages(temp.filter((element) => element.solved === false))
  }

  return (
    <div className="dashboard h-screen">
      <header className=" text-yellow-400 py-4 px-6 flex justify-between items-center">
        <div className="text-xl font-bold">Admin Dashboard</div>
        <button
          onClick={handleLogout}
          className="bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-md"
        >
          Logout
        </button>
      </header>

      {typeof messages == "string" ? (
        <>
          <center>
            <h1>No Messages Yet!</h1>
          </center>
        </>
      ) : (
        <main className="p-6">
          <>
            <h1 className="text-3xl font-bold mb-6">Messages from Users</h1>
            <h3>Filter</h3>
            <button className="bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-md mr-7" onClick={filterSolved}>
              Solved
            </button>
            <button className="bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-md" onClick={filterUnsolved}>
              Unsolved
            </button>
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-black">
                <tr>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    S.no
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Email
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Message
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Delete
                  </th>
                </tr>
              </thead>
              <tbody className="bg-black divide-y divide-gray-200">
                {messages.map((element, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {element.id}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {element.name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {element.email}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {element.date}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <a
                        href={`/admin/view/message/${element.id}`}
                        target="_blank"
                      >
                        Click here to view
                      </a>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <button
                        className="bg-red-600 hover:bg-red-700 text-white py-1 px-3 rounded-md"
                        onClick={() => deleteMessage(element.id)}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        </main>
      )}
    </div>
  );
};

export default Admin;
