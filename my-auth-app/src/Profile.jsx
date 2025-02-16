import React, { useState, useEffect } from "react";
import { getProfile } from "./api";

const Profile = ({ token }) => {
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (token) {
      getProfile(token)
        .then((data) => setProfile(data.user))
        .catch((err) => setError("Error fetching profile"));
    }
  }, [token]);

  return (
    <div>
      <h2>User Profile</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {profile ? (
        <div>
          <p>ID: {profile.user_id}</p>
          <p>Username: {profile.username}</p>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Profile;
