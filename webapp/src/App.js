import React from "react";
import { FormProvider } from "./context/FormContext";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import ConfigurationPage from "./pages/ConfigurationPage";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage.js";
import ServerSelectPage from "./pages/ServerSelectPage.js";
import EndPage from "./pages/EndPage.js";
const theme = createTheme({
  palette: {
    background: {
      default: "#A8AABC",
      form: "#A8AABC",
    },
    primary: {
      main: "#7289DA",
      dark: "#444655",
    },
    text: {
      primary: "#000000",
      secondary: "#000000",
    },
    secondary: {
      main: "#0000FF",
    },
  },
  typography: {
    fontFamily: ["sans-serif", "Roboto"].join(","),
    h2: {
      fontSize: '2rem',
      fontWeight: 500,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 4, 
          padding: '8px 15px',
          boxShadow: '0px 3px 1px -2px rgba(0,0,0,0.2), 0px 2px 2px 0px rgba(0,0,0,0.14), 0px 1px 5px 0px rgba(0,0,0,0.12)', // Subtle shadow
          '&:hover': {
            boxShadow: '0px 4px 5px -2px rgba(0,0,0,0.2), 0px 7px 10px 1px rgba(0,0,0,0.14), 0px 2px 16px 1px rgba(0,0,0,0.12)',
          },
        },
      },
    },
}
});
const App = () => {
  return (
    <FormProvider>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<LoginPage />} />
            <Route path="/home" element={<ServerSelectPage />} />
            <Route path="/config" element={<ConfigurationPage />} />
            <Route path="/end" element={<EndPage />} />
          </Routes>
        </BrowserRouter>
      </ThemeProvider>
    </FormProvider>
  );
};

export default App;
