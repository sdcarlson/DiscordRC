
import React from 'react'
import Stack from '@mui/material/Stack';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import { useTheme } from '@mui/material/styles';
import { useFormContext } from '../context/FormContext';

const ServerSelectPage = () => {
    const {
        page,
        setPage,
        serverData,
        setServerData
    } = useFormContext()

    const theme = useTheme();

    return  <Container maxWidth="lg" 
            sx={{ 
                background: '#FFFFFF',
                marginTop: theme.spacing(10),
                marginBottom: theme.spacing(5)
            }} >
            <Container sx={{ padding: 5}}>
                <Stack spacing={3} alignItems="center" justifyContent="center">
                    <Typography variant="h2">DiscordRC Server Configuration</Typography>
                    <TextField
                        label="Server Name"
                        defaultValue={serverData.name}
                        helperText="Enter new server name and hit configure, or upload from JSON"
                        variant="standard"
                        onChange={(event) => {
                            let tempServerData = {...serverData}
                            tempServerData.name = event.target.value
                            setServerData(tempServerData);
                        }}
                    />
                </Stack>
                <Stack sx={{ m: 2 }} spacing={5} direction="row" alignItems="center" justifyContent="center">
                    <Button variant="contained" onClick={()=>{setPage(page+1);}}>Configure New</Button>
                    <Button variant="contained" onClick={()=>{setPage(page+1);}}>Upload Json</Button>
                </Stack>
            </Container>
        </Container>
}

export default ServerSelectPage
