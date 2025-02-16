import axios from "axios";

const API_URL = "http://127.0.0.1:8000";  // FastAPI backend URL

// Function to register a user
export const registerUser = async (username, email, password) => {
    try {
      const response = await axios.post(`${API_URL}/register`, {
        username,
        email,
        password
      });
      console.log("User registered:", response.data);
      return response.data;
    } catch (error) {
      console.error("Error registering user:", error.response || error.message);
      throw error;
    }
  };
// Function to login a user
export const loginUser = async (username, password) => {
    try {
      const response = await axios.post(
        `${API_URL}/login`,
        new URLSearchParams({
          username,
          password
        }),
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
      );
      return response.data;
    } catch (error) {
      console.error("Error logging in:", error.response ? error.response.data.detail : error.message);
      throw error;
    }
  };
  

// Function to fetch user profile (protected route)
export const getProfile = async (token) => {
  try {
    const response = await axios.get(`${API_URL}/profile`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching profile:", error);
    throw error;
  }
};
