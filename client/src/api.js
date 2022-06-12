import axios from 'axios';

export default axios.create({
  baseURL: `https://legislation-links-app-server.herokuapp.com/`
});