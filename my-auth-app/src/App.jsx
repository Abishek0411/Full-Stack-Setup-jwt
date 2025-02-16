import React, { useState } from "react";
import Register from "./Register";
import Login from "./Login";
import Profile from "./Profile";

const App = () => {
  const [token, setToken] = useState("");

  return (
    <div>
      <h1>FastAPI + React Authentication</h1>
      {!token ? (
        <>
          <Register />
          <Login setToken={setToken} />
        </>
      ) : (
        <Profile token={token} />
      )}
    </div>
  );
};

export default App;
