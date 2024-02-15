import React from 'react'
import { FormProvider } from './context/FormContext'
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from "@mui/material/CssBaseline";
import Form from './Form'
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
        <Form />
      </ThemeProvider>
    </FormProvider>
  )

}

export default App;