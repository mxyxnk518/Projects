import React from "react";
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";

const Message = () => {
  const { id } = useParams();

  const [message, setMessage] = useState("");

  const getMessage = async () => {
    const response = await axios
      .get(`https://mayank518.pythonanywhere.com/api/contact/view/?id=${id}`)
      .then((res) => setMessage(res.data.message));
  };

  const edit = async (id) => {
    const response = await axios
      .get(`https://mayank518.pythonanywhere.com/api/contact/edit/?id=${id}`)
      .then((res) => {
        getMessage();
      });
  };

  useEffect(() => {
    getMessage();
  }, []);

  return (
    <center>
      <div>
        <h1 className="text-3xl">{message.message}</h1>
        <br />
        <br />
        {typeof message == "string" ? (
          ""
        ) : (
          <button
            onClick={() => edit(id)}
            className="bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-md"
          >
            Mark as {message.solved ? "unread" : "read"}
          </button>
        )}
      </div>
    </center>
  );
};

export default Message;
