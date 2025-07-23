import React, { useEffect } from "react";
import "./VerticalTimeline.css";

const VerticalTimeline = (props) => {
  useEffect(() => {
    const boxes = document.querySelectorAll(".box");

    const displayContent = () => {
      const triggerBottom = (window.innerHeight / 5) * 4;

      boxes.forEach((box) => {
        const topBox = box.getBoundingClientRect().top;

        if (topBox < triggerBottom) {
          box.classList.add("show");
        } else {
          box.classList.remove("show");
        }
      });
    };

    window.addEventListener("scroll", displayContent);
    displayContent();

    return () => {
      window.removeEventListener("scroll", displayContent);
    };
  }, []);

  const data = props.data;

  return (
    <section id="timeline" className="text-white">
      <h2 className="heading">Your Iterinary</h2>
      <ul>
        {data.map((element) => {
          return (
            <li className="li">
              <i className="fab fa-html5"></i>
              <div className="box">
                <p dangerouslySetInnerHTML={{ __html: element }}>
                </p>
              </div>
            </li>
          );
        })}
      </ul>
    </section>
  );
};

export default VerticalTimeline;
