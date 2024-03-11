
import React, { useEffect, useState } from 'react'
import Stack from '@mui/material/Stack';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import { useTheme } from '@mui/material/styles';
import { useFormContext } from '../context/FormContext';
import { FromJson } from '../utils/FromJson';

const ServerSelectPage = () => {
    const {
        page,
        setPage,
        serverData,
        channelData,
        roleData,
        setServerData,
        setChannelData,
        setRoleData,
    } = useFormContext()

    const theme = useTheme();

    const [file, setFile] = useState();
    function handleUpload(event) {
        setFile(event.target.files[0]);
    }

    const [config, setConfig] = useState();

    useEffect(() => {
        console.log(file);
        let reader = new FileReader();
        reader.addEventListener(
            "load",
            () => {
                const config = JSON.parse(reader.result)
                console.log(config);
                setConfig(config);
            },
            false
        );
        if (file) {
            reader.readAsText(file);
        }
    }, [file]);

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
                    <Button
                        variant="contained"
                        component="label"
                        // onClick={()=>{setPage(page+1);}}
                    >Upload Json
                    <input type="file" hidden onChange={handleUpload} />
                    </Button>
                </Stack>
                {
                    file ?
                    <div>
                        <Stack sx={{ m: 2 }} spacing={5} direction="row" alignItems="center" justifyContent="center">
                            <Typography variant="p">Uploaded file: {file.name}</Typography>
                        </Stack>
                        <Stack sx={{ m: 2 }} spacing={5} direction="row" alignItems="center" justifyContent="center">
                            <Button variant="contained" onClick={()=>{
                                FromJson(setServerData, setChannelData, setRoleData, config);
                                setPage(page+1);
                            }}>Edit</Button>
                            <Button variant="contained">Create Server</Button>
                        </Stack>
                    </div>
                    : <></>
                }
            </Container>
        </Container>
}

export default ServerSelectPage
