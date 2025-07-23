import React, { useState, useRef } from "react";
import { GoogleGenerativeAI } from "@google/generative-ai";
import "./generator.css";
import VerticalTimeline from "./VerticalTimeline";
import { useCookies } from "react-cookie";
import axios from "axios";

const Generator = () => {
  const [destination, setDestination] = useState("");
  const [budget, setBudget] = useState("");
  const [currency, setCurrency] = useState("");
  const [data, setData] = useState("");
  const [loader, setLoader] = useState("");
  const [preference,setPreference] = useState("");
  const [departure, setDeparture] = useState("");
  const [cookies, setCookie, removeCookie] = useCookies(["user"]);
  const [current, setCurrent] = useState("");
  const [length,setLength] = useState("");
  const contentRef = useRef(null);

  const types = ['Relaxing', 'Adventurous', 'Dangerous', 'Informative', 'Beach vacation', 'City break', 'Cultural immersion', 'Family vacation', 'Food and wine tour', 'Hiking and nature', 'Luxury getaway', 'Romantic escape', 'Skiing and snowboarding', 'Solo travel', 'Spa and wellness retreat', 'Wildlife safari', 'Yoga and meditation retreat', 'Volunteer and service trip']

  let depDisplay = !cookies.email ? "none" : "block";

  const genAI = new GoogleGenerativeAI(
    "AIzaSyAzsqBT9wCN03wqE3T3FtbfI11Pe1W71H0"
  );

  async function run(sentence) {
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

    const result = await model.generateContent(sentence);
    const response = await result.response;
    let text = await response.text();
    text = text.replaceAll("`", "");
    text = text.replaceAll("#", "");
    text = text.replace("html", "");

    let raw = text.split("</div>")

    let blah = []

    for (let i = 0; i < raw.length; i ++) {
      let temp = raw[i]
      temp = raw[i].replaceAll("\n", "")
      if (temp.trim() == "") {
        continue
      } else {
        blah.push(temp)
      }
    }

    setData(blah);
    setLoader("");

    if (depDisplay == "block") {
      if (!departure || !current) {
        return alert("Please fill all fields");
      }
      const title = `${current} to ${destination} with budget of ${budget} ${currency}`;
      const date = new Date();
      const response = await axios
        .post(
          `https://mayank518.pythonanywhere.com/api/save/plan/`,
          {
            email: cookies.email,
            plan: text,
            title: title,
            date: `${date.getDate()}-${date.getMonth()}-${date.getFullYear()}`,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        )
        .then((res) => {
          console.log(res.data.saved);
        })
        .catch((err) => console.log(err));
    }

  }

    const generate = () => {
    if (!destination || !budget || !currency) {
      alert("Please fill all fields");
      return;
    }

    const sentence = !cookies.email
    ? `Generate a day wise iterinary for a trip to ${destination} with a budget of ${budget} ${currency} in the form of html code within a div element without using id attribute for any of the elements with a budget summary and use iframe with google maps api for showing location of some of the places mentioned in the plan without output and also add a exciting tagline to each day and make sure to generate maps with respect to each day and also keep your response pattern the same for every propmt never change the pattern also generate your response according to the preference ${preference} and make the itinerary for this ${length} time and give the plans for each day in different single div elements with className="box" react attribute and dont use bootstrap`
    : `Generate a day wise itinerary for a trip to ${destination} with a budget of ${budget} ${currency} in the form of html code without using id attribute for any of the elements with a budget summary and use iframe with google maps api for showing location of some of the places mentioned in the plan without output and also add a exciting tagline to each day and make sure to generate maps with respect to each day and also keep your response pattern the same for every propmt never change the pattern also generate your response according to the preference ${preference} and make the itinerary for this ${length} time generate a list of planes departing on ${departure} from ${current} to ${destination} in the form of a proper html table with deparute time in GST and flight number with links to the main page of websites of the airlines in the table and also give a list of hotels in the location in an html table with links to their websites in the table without output and give the plans for each day in different div elements react attribute and also give the flights and hotels in different div elements and dont use bootstrap`

    setLoader(
      <div className="p-3 animate-spin drop-shadow-2xl bg-gradient-to-bl from-yellow-400 via-orange-400 to-red-600 md:w-48 md:h-48 h-32 w-32 aspect-square rounded-full">
        <div className="rounded-full h-full w-full bg-slate-100 dark:bg-zinc-900 background-blur-md "></div>
      </div>
    );

    setData("");

    run(sentence);
  };

  return (
    <div className="">
      <div className="bg-gradient-to-l from-yellow-600 to-black text-slate-300 border border-slate-300 grid grid-col-2 mt-10 justify-center gap-4 rounded-3xl shadow-md sm:w-[600px] mx-auto lg:w-[1000px]">
        <div className="flex p-10">
          <strong className="text-3xl m-5 ">Enter Country: </strong>
          <input
            className="input input-ghost w-full max-w-xs m-5"
            type="text"
            placeholder="Country name"
            onChange={(e) => setDestination(e.target.value)}
          />
        </div>
        <div className="flex p-10">
          <strong className="text-3xl m-5">Enter Your Budget: </strong>
          <input
            type="text"
            placeholder="Type here"
            className="input input-ghost w-full max-w-xs m-5"
            onChange={(e) => setBudget(e.target.value)}
          />
        </div>
        <div className="flex p-10">
          <strong className="text-3xl m-5">Enter Currency: </strong>
          <input
            type="text"
            placeholder="Type here"
            className="input input-ghost w-full max-w-xs m-5"
            onChange={(e) => setCurrency(e.target.value)}
          />
        </div>
        <div className="flex p-10" style={{ display: depDisplay }}>
          <strong className="text-3xl m-5">Enter Date of Departure: </strong>
          <input
            type="date"
            placeholder="Enter date of departure"
            className="input input-ghost w-full max-w-xs m-5"
            onChange={(e) => setDeparture(e.target.value)}
          />
        </div>
        <div className="flex p-10" style={{ display: depDisplay }}>
          <strong className="text-3xl m-5">Enter Current Location: </strong>
          <input
            type="text"
            placeholder="Enter current location"
            className="input input-ghost w-full max-w-xs m-5"
            onChange={(e) => setCurrent(e.target.value)}
          />
        </div>
        <div className="flex p-10">
          <strong className="text-3xl m-5">Describe what kind of trip you want: </strong>
          <input
            list="types"
            placeholder="Type here"
            className="input input-ghost w-full max-w-xs m-5"
            onChange={(e) => setPreference(e.target.value)}
          />
          <datalist id="types">
            {types.map((element, index) => {
              return <option value={element} key={index}>{element}</option>
            })}
          </datalist>
        </div>
        <div className="flex p-10">
          <strong className="text-3xl m-5">Enter length of trip: </strong>
          <input
            type="text"
            placeholder="Type here"
            className="input input-ghost w-full max-w-xs m-5"
            onChange={(e) => setLength(e.target.value)}
          />
        </div>


        <div className="flex justify-center">
          <button type="button" onClick={generate}>
            <div className="w-full h-40 flex items-center justify-center cursor-pointer ">
              <div
                className="relative inline-flex items-center justify-start py-3 pl-4 pr-12 overflow-hidden font-semibold shadow text-amber-400 transition-all duration-150 ease-in-out rounded hover:pl-10 hover:pr-6 bg-gray-50 dark:bg-gray-700 dark:text-white dark:hover:text-gray-200 dark:shadow-none group"
              >
                <span className="absolute bottom-0 left-0 w-full h-1 transition-all duration-150 ease-in-out bg-yellow-600 group-hover:h-full"></span>
                <span className="absolute right-0 pr-4 duration-200 ease-out group-hover:translate-x-12">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    fill="none"
                    className="w-5 h-5 text-yellow-400"
                  >
                    <path
                      d="M14 5l7 7m0 0l-7 7m7-7H3"
                      strokeWidth="2"
                      strokeLinejoin="round"
                      strokeLinecap="round"
                    ></path>
                  </svg>
                </span>
                <span className="absolute left-0 pl-2.5 -translate-x-12 group-hover:translate-x-0 ease-out duration-200">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    fill="none"
                    className="w-5 h-5 text-yellow-400"
                  >
                    <path
                      d="M14 5l7 7m0 0l-7 7m7-7H3"
                      strokeWidth="2"
                      strokeLinejoin="round"
                      strokeLinecap="round"
                    ></path>
                  </svg>
                </span>
                <span className="relative w-full text-left transition-colors duration-200 ease-in-out group-hover:text-white dark:group-hover:text-gray-200">
                  Generate
                </span>
              </div>
            </div>

          </button>
          <div className=" lg:mt-[-50px] lg:ml-10 sm:ml-20">
            {loader}
          </div>
        </div>
      </div>
      {
        data !== "" ? <VerticalTimeline data={data} />
        : null
      }
    </div>
  );
};

export default Generator;
