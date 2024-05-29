import axios from "axios";

const BACKEND_PATH = "http://localhost:5000/get-response";

export const getResponse = (userMessage) => {
  return axios.post(BACKEND_PATH, {
    user_message: userMessage,
  });
};
