import React, { useState, useEffect } from "react";
import { Container, TextField, Button, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const accessToken = localStorage.getItem("access_token");
    if (accessToken) {
      navigate("/home");
    }
  }, []);

  const handleLoginSubmit = async (event) => {
    event.preventDefault();
    const form_data = new FormData();
    form_data.append("username", username);
    form_data.append("password", password);
    const response = await fetch("http://localhost:8000/auth/login", {
      method: "POST",
      body: form_data,
    });

    if (response.ok) {
      const data = await response.json();
      const { access_token } = data;
      localStorage.setItem("access_token", access_token);
      console.log("Login successful:", data);
      navigate("/home");
    } else {
      console.error("Login failed");
    }
  };

  const handleRegisterSubmit = async (event) => {
    event.preventDefault();
    const form_data = new FormData();
    form_data.append("username", username);
    form_data.append("password", password);
    const response = await fetch("http://localhost:8000/auth/signup", {
      method: "POST",
      body: form_data,
    });
    if (response.ok) {
      const data = await response.json();
      const { access_token } = data;
      localStorage.setItem("access_token", access_token);
      console.log("Registration successful:", data);
      navigate("/home");
    } else {
      console.error("Registration failed");
    }
  };

  return (
    <>
      <Typography
          component="h1"
          variant="h1"
          sx={{ mb: 4, textAlign: "center", fontFamily: 'Fredericka the Great' }}
        >
          DiscordRC
        </Typography>
      <Container component="main" maxWidth="xs" sx={{ mt: 8 }}>
        
        <Typography component="h1" variant="h5">
          Login:
        </Typography>
        <form onSubmit={handleLoginSubmit}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="username"
            label="Username"
            name="username"
            autoComplete="username"
            autoFocus
            value={username}
            // sx={{ backgroundColor: "primary.light", color: "text.primary" }}
            onChange={(e) => setUsername(e.target.value)}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
            value={password}
            // sx={{ backgroundColor: "primary.light", color: "text.primary" }}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{
              mt: 3,
              mb: 2,
              // backgroundColor: "primary.dark",
              // color: "text.primary",
            }}
          >
            Sign In
          </Button>
          <Button
            fullWidth
            variant="contained"
            sx={{
              mt: 3,
              mb: 2,
              // backgroundColor: "primary.dark",
              // color: "text.primary",
            }}
            onClick={handleRegisterSubmit}
            type="button"
          >
            Register
          </Button>
        </form>
      </Container>
    </>
  );
};

export default LoginPage;
