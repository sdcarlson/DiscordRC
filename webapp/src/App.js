import React from 'react'
import { FormProvider } from './context/FormContext'
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from "@mui/material/CssBaseline";
import Form from './components/Form';
import ConfigurationPage from './pages/ConfigurationPage';
const theme = createTheme({
  palette: {
    background: {
      default: "#FFFFFF",
      form: "#FFFFFF",
    },
    primary: {
        main: '#7289DA',
    },
    secondary: {
      main: '#0000FF',
    }
  },
  typography: {
    fontFamily: [
      'sans-serif',
      'Roboto',
    ].join(','),
  },
})

const App = () => {

  return (
    <FormProvider>
      <ThemeProvider theme={theme}> 
        <CssBaseline />
        <ConfigurationPage />
      </ThemeProvider>
    </FormProvider>
  )

}

export default App;