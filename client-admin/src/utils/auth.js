function getToken() {
  const token = `Bearer ${localStorage.getItem('token')}`;
  return token;
}

function setToken(token) {
  localStorage.setItem('token', token);
}

const GetAuthHeader = () => {
  return {
    'Authorization': getToken(),
  };
}

export { getToken, setToken };

export default GetAuthHeader;
