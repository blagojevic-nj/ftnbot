import axios from "axios";

const ADMIN_PATH = "http://localhost:5000/admin/context";

export const queryDatabase = (query) => {
  return axios.get(ADMIN_PATH + "?query=" + query);
};

export const addContext = (query) => {
  return axios.post(ADMIN_PATH, { query });
};

export const updateContext = (context) => {
  return axios.put(ADMIN_PATH, context);
};

export const deleteContext = (id) => {
  return axios.delete(ADMIN_PATH + "?id=" + id);
};
