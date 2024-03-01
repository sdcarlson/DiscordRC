import React, { useState, useEffect, useRef } from 'react'
import { Box, Container, Stack, Button, ToggleButton, ToggleButtonGroup } from "@mui/material";
import { useFormContext } from '../context/FormContext';
import { v4 as uuid } from 'uuid';
import DeleteIcon from '@mui/icons-material/Delete';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import ConfigurationPageRolePermissions from './ConfigurationPageRolePermissions';

const roleRowNames=['display_separately', 'allow_mention', 'roleperm1', 'roleperm2']; 
const roleRowTypes=['toggleButton', 'toggleButton', 'toggleButton', 'toggleButton'];

const ConfigurationPage = () => {

    const {
        roleData,
        setRoleData,
        channelData,
        setChannelData
    } = useFormContext()
    
    const [addedRole, setAddedRole] = useState(0);
    const [addedChannel, setAddedChannel] = useState(0);
    const [roleRows, setRoleRows] = useState([]);
    const [roleSelected, setRoleSelected] = useState(null);
    const [channelRows, setChannelRows] = useState([]);
    const [channelSelected, setChannelSelected] = useState(null);

    const roleBox = useRef(null);
    const channelBox = useRef(null);
    
    useEffect(() => {
        setRoleRows(roleData)
        setChannelRows(channelData)
    }, [])
    
    useEffect(() => {
        setRoleData(roleRows);
    }, [roleRows])
    
    useEffect(() => {
        setChannelData(channelRows);
    }, [channelRows])

    useEffect(() => {
        roleBox.current.scrollIntoView({ behavior: "smooth", block: "end" })
    }, [addedRole])

    useEffect(() => {
        channelBox.current.scrollIntoView({ behavior: "smooth", block: "end" })
    }, [addedChannel])

    const handleRoleToggleButtonSelection = (event, nextRole) => {
        setRoleSelected(nextRole)
        setChannelSelected(null)
    }

    const handleChannelToggleButtonSelection = (event, nextChannel) => {
        setChannelSelected(nextChannel)
        setRoleSelected(null)
    }

    const handleAddRole = () => {
        const id = uuid()
        setRoleRows([...roleRows, {
            id: id,
            name: 'New Role',
            permissions: {},
        }], 
        )
        setRoleSelected(id)
        setChannelSelected(null)
        setAddedRole(addedRole + 1)
    }

    const handleAddChannel = () => {
        const id = uuid()
        setChannelRows([...channelRows, {
            id: id,
            name: 'New Channel',
            permissions: {},
        }], 
        )
        setChannelSelected(id)
        setRoleSelected(null)
        setAddedChannel(addedChannel + 1)
    }

    const handleDeleteRole = () => {
        if (roleSelected !== null) {
            const currRows = [...roleRows];
            let index = -1;
            for (let i = 0; i < currRows.length; i++) {
                if (currRows[i].id === roleSelected) {
                    index = i;
                }
            }
            if (index !== -1) {
                currRows.splice(index, 1);
                setRoleSelected(null);
                setRoleRows(currRows);
            }
        }
    }

    const handleDeleteChannel = () => {
        if (channelSelected !== null) {
            const currRows = [...channelRows];
            let index = -1;
            for (let i = 0; i < currRows.length; i++) {
                if (currRows[i].id === channelSelected) {
                    index = i;
                }
            }
            if (index !== -1) {
                currRows.splice(index, 1);
                setChannelSelected(null);
                setChannelRows(currRows);
            }
        }
    }

    return (
        <Container disableGutters={true} maxWidth={false} sx={{ display: 'flex', height:'100%', 'flex-wrap': 'wrap' }}>
            <Box sx = {{ dispaly: 'flex', height: '100%', width: '35%', 'flex-direction': 'column'}}>
                <Box sx={{
                    width: '100%',
                    height: '50%',
                    display: 'flex',
                    'flex-flow': 'column',
                    border: 1,
                    borderColor: 'primary.main'
                }}>
                    <Box sx={{
                        width: '100%',
                        margin: '5',    
                        direction: "column",
                        alignItems: "center",
                        justifyContent: "center",
                    }}>
                        <Stack spacing={5} direction="row" justifyContent="center">
                            <Button variant="contained" style={{maxWidth: '175px', maxHeight: '40px', minWidth: '175px', minHeight: '40px'}} 
                            onClick={handleAddRole}><b>Add Role&nbsp;&nbsp;</b><AddCircleIcon/></Button>
                            <Button variant="contained" style={{maxWidth: '175px', maxHeight: '40px', minWidth: '175px', minHeight: '40px'}} 
                            onClick={handleDeleteRole}><b>Delete&nbsp;</b><DeleteIcon/></Button>
                        </Stack>

                    </Box>
                    
                    <Box sx={{
                        overflow: 'auto',
                    }}>
                        <div ref={roleBox} sx={{
                            flex: '1 1 auto',
                            overflow: 'auto',
                            margin: '5',
                        }}>
                            <Stack spacing={2} direction="column">
                                <ToggleButtonGroup
                                    sx={{
                                        width:'100%',
                                        display: "flex", 
                                        flexDirection: "column",
                                        alignItems: "center",
                                        justifyContent: "center",
                                        gridTemplateRows: "auto auto auto auto",
                                        gridGap: "10px",
                                    }}
                                    orientation="vertical"
                                    value={roleSelected}
                                    exclusive
                                    onChange={handleRoleToggleButtonSelection}
                                    fullWidth
                                    alignItems="center" 
                                    justifyContent="center"
                                >
                                    {roleRows.map((role) => {
                                        return <ToggleButton value={role.id} color="secondary" sx={{minWidth: '80%', maxWidth: '80%', border: 0}}>{role.name}</ToggleButton>
                                    })}
                                </ToggleButtonGroup>
                            </Stack>
                        </div>
                    </Box>
                </Box>
                <Box sx={{
                    width: '100%',
                    height: '50%',
                    display: 'flex',
                    'flex-flow': 'column',
                    border: 1,
                    borderColor: 'primary.main'
                }}>
                    <Box sx={{
                        width: '100%',
                        margin: '5',    
                        direction: "column",
                        alignItems: "center",
                        justifyContent: "center",
                    }}>
                        <Stack spacing={5} direction="row" justifyContent="center">
                            <Button variant="contained" style={{maxWidth: '175px', maxHeight: '40px', minWidth: '175px', minHeight: '40px'}} 
                            onClick={handleAddChannel}><b>Add Channel&nbsp;&nbsp;</b><AddCircleIcon/></Button>
                            <Button variant="contained" style={{maxWidth: '175px', maxHeight: '40px', minWidth: '175px', minHeight: '40px'}} 
                            onClick={handleDeleteChannel}><b>Delete&nbsp;</b><DeleteIcon/></Button>
                        </Stack>

                    </Box>
                    
                    <Box sx={{
                        overflow: 'auto',
                    }}>
                        <div ref={channelBox} sx={{
                            flex: '1 1 auto',
                            overflow: 'auto',
                            margin: '5',
                        }}>
                            <Stack spacing={2} direction="column">
                                <ToggleButtonGroup
                                    sx={{
                                        width:'100%',
                                        display: "flex", 
                                        flexDirection: "column",
                                        alignItems: "center",
                                        justifyContent: "center",
                                        gridTemplateRows: "auto auto auto auto",
                                        gridGap: "10px",
                                    }}
                                    orientation="vertical"
                                    value={channelSelected}
                                    exclusive
                                    onChange={handleChannelToggleButtonSelection}
                                    fullWidth
                                    alignItems="center" justifyContent="center" 
                                >
                                    
                                    {channelRows.map((channel) => {
                                        // TODO: add symbols e.g. voice text has similar to on discord, announce is a speaker etc.
                                        return <ToggleButton value={channel.id} color="secondary" sx={{minWidth: '80%', maxWidth: '80%', border: 0}}>{channel.name}</ToggleButton>
                                    })}
                                </ToggleButtonGroup>
                            </Stack>
                        </div>
                    </Box>
                </Box>
            </Box>
            {roleSelected !== null &&
                <ConfigurationPageRolePermissions id={roleSelected} rowNames={roleRowNames} rowTypes={roleRowTypes}/>
            }
            {channelSelected !== null &&
                <></>
            }
            
        </Container>
    );
}

export default ConfigurationPage;