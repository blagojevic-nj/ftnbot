import { Chat } from "./Chat";

export const Chatbot = () => {
  return (
    <>
      <Chat />
      <iframe
        className="frame"
        title="Ftn frame"
        src="http://ftn.uns.ac.rs/691618389/fakultet-tehnickih-nauka"
      ></iframe>
    </>
  );
};

export default Chatbot;
