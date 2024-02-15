
import React from 'react'
import CustomTable from './components/CustomTable';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import { useTheme } from '@mui/material/styles';

const Form = () => {

    const theme = useTheme();

    return (
        <Container maxWidth="lg" 
            sx={{ 
                background: '#FFFFFF',
                marginTop: theme.spacing(10),
                marginBottom: theme.spacing(5)
            }} >
            <Container sx={{ padding: 5 }}>
                <CustomTable 
                    headings={['Role Name','Display Separately','Allow Mentions','Permission1', 'Permission2']} 
                    rownames={['name', 'display_separately', 'allow_mention', 'roleperm1', 'roleperm2']} 
                    rowtypes={['text', 'slider', 'slider', 'slider', 'slider']}/>
                <Button variant="contained">Next</Button>
            </Container>
        </Container>
    );
  }
  
  export default Form;