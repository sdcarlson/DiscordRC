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
      default: "#FFFFFF",
      form: "#FFFFFF",
    },
    primary: {
      main: "#7289DA",
      dark: "#424549",
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
  },
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
