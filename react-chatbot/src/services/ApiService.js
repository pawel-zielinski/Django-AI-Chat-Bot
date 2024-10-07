import axios from "axios";

export function getSessionList() {
  return axios.get("http://localhost:8000/home")
      .then(function(response) {
        return response.data;
      })
      .catch(error => {
        return [];
      });
}
