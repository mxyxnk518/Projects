import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import VerticalTimeline from "./VerticalTimeline";

const Viewplan = () => {
  const { id } = useParams();

  const [plan, setPlan] = useState("");

  const getPlan = async () => {
    const response = await axios
      .get(`https://mayank518.pythonanywhere.com/api/get/plan/?id=${id}`)
      .then((res) => {
        console.log(true)
        let text = res.data.plan
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

        setPlan(blah);
      });
  };

  useEffect(() => {
    getPlan();
  }, []);

  return (
    plan !== "" ? <VerticalTimeline data={plan} /> : null
  );
};

export default Viewplan;
