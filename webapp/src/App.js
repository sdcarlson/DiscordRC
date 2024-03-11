import React, {useEffect} from 'react'
import { FormProvider } from './context/FormContext'
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from "@mui/material/CssBaseline";
import { Routes, Route, useNavigate} from 'react-router-dom';
import HomePage from './pages/HomePage.js'
import LoginPage from './pages/LoginPage.js'
const theme = createTheme({
  palette: {
    background: {
      default: "#7289DA",
      form: "#FFFFFF",
    },
    primary: {
        main: '#7289DA',
        dark: '#424549',
    },
    text: {
      primary: "#ffffff",
      secondary: "#000000", 
    },
  },
  typography: {
    fontFamily: [
      'sans-serif',
      'Roboto',
    ].join(','),
  },
})

const App = () => {

  const navigate = useNavigate();

  useEffect(() => {
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
      navigate('/');
    } else {
      navigate('/login');
    }
  }, [navigate]);

  return (
    <FormProvider>
      <ThemeProvider theme={theme}> 
        <CssBaseline />
          <HomePage />
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage/>} />
          </Routes>
      </ThemeProvider>
    </FormProvider>
  )

}

export default App;