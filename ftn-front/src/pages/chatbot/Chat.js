import { useState, useEffect } from "react";
import { getResponse } from "../../services/HomeService";
import logo from "../../logo1.png";
import logo2 from "../../logo2.png";
import user from "../../user.png";
import chatbot from "../../chatbot.png";

export const Chat = () => {
  const [closed, setClosed] = useState(true);
  const [userMessage, setUserMessage] = useState("");
  const [chatLog, setChatLog] = useState([]);
  const [thinking, setThinking] = useState(false);
  const [show, setShow] = useState(false);

  useEffect(() => {
    setChatLog([
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

  const toggleClosed = () => {
    if (closed) {
      setTimeout(() => {
        setShow(true);
      }, 800);
    } else {
      setShow(false);
    }
    setClosed(!closed);
  };

  if (closed) {
    return (
      <div className="chat closed" onClick={toggleClosed}>
        <img
          src={chatbot}
          className="chatbot-img"
          height="50px"
          width="50px"
        ></img>
      </div>
    );
  } else {
    return (
      <div className={show ? "chat open show" : "chat open"}>
        <span className="close-bot" onClick={toggleClosed}>
          x
        </span>
        <div className="messages-container">
          <div className="messages2">
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
                    <div className="message brighter">{entry.message}</div>
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
                  </div>
                )}
              </>
            ))}
          </div>
          <div className="top">
            <div className="small-logo">
              <img src={logo} height="50px" width="50px" />
            </div>
            <h3 className="mt-2">Fakultet tehničkih nauka u Novom Sadu</h3>
          </div>
        </div>
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
              Pošalji
            </button>
          </div>
        </div>
      </div>
    );
  }
};
