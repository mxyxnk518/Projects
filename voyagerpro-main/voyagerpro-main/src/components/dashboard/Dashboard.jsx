import React from "react";
import { useCookies } from "react-cookie";
import axios from "axios";
import { useState, useEffect } from "react";

const Dashboard = () => {
  const [cookies, setCookie, removeCookie] = useCookies(["user"]);
  const [plans, setPlans] = useState("");

  const getPlans = async () => {
    const response = await axios
      .get(`https://mayank518.pythonanywhere.com/api/get/plans/?email=${cookies.email}`)
      .then((res) => {
        setPlans(res.data.plans);
      });
  };

  useEffect(() => {
    getPlans();
  }, []);

  if (!cookies.name == true || !cookies.logged_in == true) {
    console.log(false);
    return (window.location.href = "/signin");
  }

  const handleLogout = () => {
    removeCookie("name");
    removeCookie("logged_in");
    removeCookie("email");
    return (window.location.href = "/signin");
  };

  const deletePlan = async (id) => {
    const response = await axios.get(
      `https://mayank518.pythonanywhere.com/api/delete/plan/?id=${id}`
    ).then(
      res => {
        if (res.data.deleted == "yes") {
          getPlans()
        } else {
          alert("An error has occurred. Please try again later.")
        }
      }
    )
  }

  return (
    <div className="dashboard h-screen">
      <header className=" text-yellow-400 py-4 px-6 flex justify-between items-center">
        <div className="text-xl font-bold">Travel Itinerary Dashboard</div>
        <button
          onClick={handleLogout}
          className="bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-md"
        >
          Logout
        </button>
      </header>

      <main className="p-6">
        {typeof(plans) == 'string' ? (
          <>
            <center>
              <h1>No Plans Yet!</h1>
              <h2>
                <a href="/generator">Click here to generate some plans.</a>
              </h2>
            </center>
          </>
        ) : (
          <>
            <h1 className="text-3xl font-bold mb-6">Your Travel Itineraries</h1>
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-black">
                <tr>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    S.no
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Title
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-black divide-y divide-gray-200">
                {plans.map((item, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4 whitespace-nowrap">{index + 1}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <a href={`/dashboard/view/${item.id}`} target="_blank" style={{ textDecoration: 'underline' }}>{item.title}</a>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">{item.date}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <button className="bg-red-600 hover:bg-red-700 text-white py-1 px-3 rounded-md" onClick={() => deletePlan(item.id)}>
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        )}
      </main>
    </div>
  );
};

export default Dashboard;
