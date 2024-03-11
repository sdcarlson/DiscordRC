import React from 'react'
import Stack from '@mui/material/Stack';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { useTheme } from '@mui/material/styles';
import { useFormContext } from '../context/FormContext';
import { ConvertJson } from '../utils/ConvertJson';

const EndPage = () => {
    const {
        page,
        setPage,
        roleData,
        channelData,
        serverData
    } = useFormContext()

    const theme = useTheme();

    return  <Container maxWidth="lg" 
                sx={{ 
                    background: '#FFFFFF',
                    marginTop: theme.spacing(10),
                    marginBottom: theme.spacing(5)
            }} >
            <Container sx={{ padding: 5}}>
                <Stack alignItems="center" justifyContent="center">
                    <Typography variant="h2">DiscordRC for {serverData.name} Completed</Typography>
                </Stack>
                <Stack sx={{ m: 2 }} spacing={5} direction="row" alignItems="center" justifyContent="center">
                    <Button variant="contained" onClick={()=>{setPage(page-1);}}>Previous</Button>
                    <Button variant="contained" onClick={(()=>{
                        console.log(ConvertJson(roleData, channelData, serverData))
                    })}> Download </Button>
                </Stack>
            </Container>
        </Container>
}

export default EndPage
