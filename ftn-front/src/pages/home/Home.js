import React, { useEffect, useState } from "react";
import axios from "axios";
import logo from "../../logo1.png";
import logo2 from "../../logo2.png";
import user from "../../user.png";
import question from "../../question-mark.png";
import { getResponse } from "../../services/HomeService";

const Home = () => {
  const [userMessage, setUserMessage] = useState("");
  const [chatLog, setChatLog] = useState([]);
  const [thinking, setThinking] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [currEntry, setCurrEntry] = useState({
    sender: "",
    message: [],
    contexts: [],
  });

  useEffect(() => {
    setChatLog([
      ...chatLog,
      {
        sender: "FTNBot",
        message:
          "Dobrodošli na FTN AI informator! Tu smo da vam pružimo relevantne informacije o našem fakultetu. Kako vam možemo pomoći danas?",
        contexts: [],
      },
    ]);
  }, []);

  const sendMessage = async () => {
    if (userMessage.trim() === "") return;
    setChatLog([
      { sender: "user", message: userMessage, contexts: [] },
      ...chatLog,
    ]);
    setUserMessage("");
    setThinking(true);

    try {
      const response = await getResponse(userMessage);

      const chatbotResponse = response.data;
      setChatLog([
        {
          sender: "chatbot",
          message: chatbotResponse["answer"],
          contexts: chatbotResponse["contexts"],
        },
        { sender: "user", message: userMessage, contexts: [] },
        ...chatLog,
      ]);
      setThinking(false);
      console.log(chatLog);
    } catch (error) {
      setChatLog([
        {
          sender: "chatbot",
          message: "Greška sa mrežom, pokušaj ponovo!",
          contexts: [],
        },
        { sender: "user", message: userMessage, contexts: [] },
        ...chatLog,
      ]);
      setThinking(false);
    }
  };

  const handleButtonClick = (entry) => {
    setCurrEntry(entry);
    setShowModal(true);
  };

  return (
    <>
      <div className="container">
        <div id="chat-container">
          <div className="logo">
            <img src={logo} height="150px" width="150px" />
          </div>
          <h3 className="mt-2">Fakultet tehničkih nauka u Novom Sadu</h3>
          <p>
            Vaš lični vodič kroz svet tehnologije na Fakultetu tehničkih nauka -
            uvek tu da odgovori na vaša pitanja i olakša vaš akademski put.
          </p>
          <div className="row w-100">
            <div className="input-group mb-3">
              <input
                type="text"
                value={userMessage}
                onChange={(e) => setUserMessage(e.target.value)}
                className="form-control"
                placeholder="Postavi pitanje..."
              />
              <button onClick={sendMessage} className="btn btn-secondary">
                Pitaj
              </button>
            </div>
          </div>
          <hr />
          <div className="messages">
            {thinking && (
              <div class="spinner-border text-success" role="status"></div>
            )}
            {chatLog.map((entry, index) => (
              <>
                {entry.sender === "user" ? (
                  <div
                    key={index}
                    className="d-flex align-items-center justify-content-end user-message"
                  >
                    <div className="message">{entry.message}</div>
                    <span className="user">
                      <img src={user} height="30px" />
                    </span>
                  </div>
                ) : (
                  <div
                    key={index}
                    className="d-flex align-items-center chatbot-message"
                  >
                    <span className="owl-hub">
                      <img src={logo2} height="50px" />
                    </span>
                    <div className="message">{entry.message}</div>
                    {entry.contexts.length > 0 && (
                      <div
                        className="contexts-button"
                        onClick={() => handleButtonClick(entry)}
                      >
                        <img src={question} height="35px" width="18px" />
                      </div>
                    )}
                  </div>
                )}
              </>
            ))}
          </div>
        </div>
      </div>
      {showModal && (
        <div className="modal">
          <div className="modal-content">
            <span className="close" onClick={() => setShowModal(false)}>
              &times;
            </span>
            <h2>Context List</h2>
            <ul>
              {currEntry.contexts.map((context, index) => (
                <li key={index}>{context}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </>
  );
};

export default Home;
