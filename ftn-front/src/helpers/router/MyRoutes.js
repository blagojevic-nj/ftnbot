import { Routes, Route } from "react-router-dom";
import Home from "../../pages/home/Home";
import Admin from "../../pages/admin/Admin";
import Chatbot from "../../pages/chatbot/Chatbot";

const MyRoutes = () => {
  return (
    <Routes>
      <Route exact path="" element={<Chatbot />} />
      <Route exact path="/home" element={<Home />} />
      <Route exact path="/admin" element={<Admin />} />
    </Routes>
  );
};

export default MyRoutes;
