import React from 'react'
import { FormProvider } from './context/FormContext'
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from "@mui/material/CssBaseline";
import ConfigurationPage from './pages/ConfigurationPage';
import PageManager from './pages/PageManager';
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
        <PageManager />
      </ThemeProvider>
    </FormProvider>
  )

}

export default App;