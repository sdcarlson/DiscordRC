
// import React, { useState } from 'react'
// import Stack from '@mui/material/Stack';
// import Container from '@mui/material/Container';
// import Button from '@mui/material/Button';
// import { useTheme } from '@mui/material/styles';
// import CircleIcon from '@mui/icons-material/Circle';
// import CircleOutlinedIcon from '@mui/icons-material/CircleOutlined';
// import RolePage from '../pages/RolePage';
// import TempPage from '../pages/TempPage';
// import TempPage2 from '../pages/TempPage2';

// const Form = () => {

//     const theme = useTheme();

//     const [page, setPage] = useState(0);
//     const totalPages = 3;

//     return (
//         <Container maxWidth="lg" 
//             sx={{ 
//                 background: '#FFFFFF',
//                 marginTop: theme.spacing(10),
//                 marginBottom: theme.spacing(5)
//             }} >
//             <Container sx={{ padding: 5 }}>
//                 {(() => {
//                     switch(page) {
//                         case 0:
//                             return <RolePage />
//                         case 1:
//                             return <TempPage />
//                         case 2:
//                             return <TempPage2 />
//                         default:
//                     }
//                 })()}

//                 <Stack spacing={1} direction="row" alignItems="center" justifyContent="center">
//                     {[...Array(totalPages).keys()].map((i) => {
//                         if (i == page)
//                             return (<CircleIcon color="primary" fontSize="medium" />);
//                         else
//                             return (<CircleOutlinedIcon color="primary" fontSize="small" onClick={()=>{setPage(i);}} />);
//                     })}
//                 </Stack>
//                 <Stack sx={{ m: 2 }} spacing={5} direction="row" alignItems="center" justifyContent="center">
//                     {(() => {
//                         if (page != 0)
//                             return (<Button variant="contained" onClick={()=>{setPage(page-1);}}>Prev</Button>);
//                         else
//                             return (<Button variant="contained" disabled>Prev</Button>)
//                     })()}
//                     {(() => {
//                         if (page != totalPages-1)
//                             return (<Button variant="contained" onClick={()=>{setPage(page+1);}}>Next</Button>);
//                         else
//                             return (<Button variant="contained" disabled>Next</Button>)
//                     })()}
//                 </Stack>
//             </Container>
//         </Container>
//     );
//   }
  
//   export default Form;