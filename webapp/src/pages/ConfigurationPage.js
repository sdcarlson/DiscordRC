import React, { useState, useEffect, useRef } from 'react'
import { Box, Container, Stack, Button, ButtonGroup, ToggleButton, ToggleButtonGroup } from "@mui/material";
import { useFormContext } from '../context/FormContext';
import { v4 as uuid } from 'uuid';
import DeleteIcon from '@mui/icons-material/Delete';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import ConfigurationPageRolePermissions from './ConfigurationPageRolePermissions';
import ConfigurationPageChannelPermissions from './ConfigurationPageChannelPermissions';
import { VolumeUp, FormatColorText, North, South, ViewList } from '@mui/icons-material';
import IconButton from '@mui/material/IconButton';

const roleRowNames=['display_separately', 'allow_mention', 'roleperm1', 'roleperm2']; 
const roleRowTypes=['slider', 'slider', 'toggleButton', 'toggleButton'];

const channelRowNames=['age_restriction', 'view_channel']; 
const channelRowTypes=['slider', 'toggleButton'];

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
            type: 'text',
            name: 'New Channel',
            permissions: {
                '@everyone': {}
            },
        }], 
        )
        setChannelSelected(id)
        setRoleSelected(null)
        setAddedChannel(addedChannel + 1)
        console.log(channelRows)
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
    
    const handleRoleUp = () => {
        let row = -1
        for (let i = 0; i < roleData.length; i++) {
            if (roleData[i].id === roleSelected) {
                row = i
            }
        }
        if (row !== null && row !== 0) {
            let tempRoleData = [...roleData]
            let tempRole = tempRoleData[row - 1]
            tempRoleData[row - 1] = tempRoleData[row]
            tempRoleData[row] = tempRole
            setRoleRows(tempRoleData);
        }
    }

    const handleRoleDown = () => {
        let row = -1
        for (let i = 0; i < roleData.length; i++) {
            if (roleData[i].id === roleSelected) {
                row = i
            }
        }
        if (row !== null && row !== roleData.length-1) {
            let tempRoleData = [...roleData]
            let tempRole = tempRoleData[row + 1]
            tempRoleData[row + 1] = tempRoleData[row]
            tempRoleData[row] = tempRole
            setRoleRows(tempRoleData);
        }
    }

    const handleChannelUp = () => {
        let row = -1
        for (let i = 0; i < channelData.length; i++) {
            if (channelData[i].id === channelSelected) {
                row = i
            }
        }
        if (row !== null && row !== 0) {
            let tempChannelData = [...channelData]
            let tempChannel = tempChannelData[row - 1]
            tempChannelData[row - 1] = tempChannelData[row]
            tempChannelData[row] = tempChannel
            setChannelRows(tempChannelData);
        }
    }

    const handleChannelDown = () => {
        let row = -1
        for (let i = 0; i < channelData.length; i++) {
            if (channelData[i].id === channelSelected) {
                row = i
            }
        }
        if (row !== null && row !== channelData.length-1) {
            let tempChannelData = [...channelData]
            let tempChannel = tempChannelData[row + 1]
            tempChannelData[row + 1] = tempChannelData[row]
            tempChannelData[row] = tempChannel
            setChannelRows(tempChannelData);
        }
    }

    return (
        <Container disableGutters={true} maxWidth={false} sx={{ display: 'flex', height:'100%', 'flex-wrap': 'wrap' }}>
            <Box sx = {{ display: 'flex', height: '100%', width: '35%', 'flex-direction': 'column'}}>
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
                            <Box>
                                <IconButton onClick={handleRoleUp} size="large">
                                    <North color='primary'/>
                                </IconButton>
                                <IconButton onClick={handleRoleDown} size="large">
                                    <South color='primary' />
                                </IconButton>
                            </Box>
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
                            <Box>
                                <IconButton onClick={handleChannelUp} size="large">
                                    <North color='primary'/>
                                </IconButton>
                                <IconButton onClick={handleChannelDown} size="large">
                                    <South color='primary' />
                                </IconButton>
                            </Box>
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
                                >
                                    
                                    {channelRows.map((channel) => {
                                        let icon = null
                                        if (channel.type === 'category') {
                                            return <ToggleButton value={channel.id} color="secondary" sx={{minWidth: '80%', maxWidth: '80%', border: 0, display:'flex', position: 'relative'}}>
                                            <Box sx={{left: 0, marginLeft: 2.5, position: 'absolute'}}>{channel.name}</Box>
                                            <Box sx={{right: 0, marginRight: 5, position: 'absolute'}}><ViewList /></Box>
                                            <Box sx={{flex: 1, flexDirection: 'row', justifyContent: 'flex-end', fontWeight: 'bold'}}>Category</Box>
                                            </ToggleButton>
                                        }

                                        if (channel.type === 'voice') 
                                            icon = <VolumeUp />
                                        else if (channel.type === 'text')
                                            icon = <FormatColorText />

                                        return <ToggleButton value={channel.id} color="secondary" sx={{minWidth: '80%', maxWidth: '80%', border: 0, display:'flex', position: 'relative'}}>
                                            <Box sx={{left: 0, marginLeft: 5, position: 'absolute'}}>{icon}</Box>
                                            <Box sx={{flex: 1, flexDirection: 'row', justifyContent: 'center'}}>{channel.name}</Box>
                                        </ToggleButton>
                                    })}
                                </ToggleButtonGroup>
                            </Stack>
                        </div>
                    </Box>
                </Box>
            </Box>
            <Box sx={{
                width: '65%',
                height: '100%',
                display: 'flex',
                'flex-flow': 'column',
                border: 1,
                borderColor: 'primary.main',
                float: 'right'
            }}>
                {roleSelected !== null &&
                    <ConfigurationPageRolePermissions id={roleSelected} rowNames={roleRowNames} rowTypes={roleRowTypes} setRoleRows={setRoleRows}/>
                }
                {channelSelected !== null &&
                    <ConfigurationPageChannelPermissions id={channelSelected} rowNames={channelRowNames} rowTypes={channelRowTypes} setChannelRows={setChannelRows}/>
                } 
                {channelSelected === null && roleSelected === null &&
                    <Box sx={{
                        flex: '1 1 auto',
                        overflow: 'auto',
                        margin: '5',
                    }}/>
                }
                <Box sx={{                    
                    borderTop: 2,
                    borderColor: 'primary.main'
                }}>
                    <Stack sx={{
                        marginTop: '10',
                        marginBottom: '15',
                        marginRight: '30',
                        justifyContent: "flex-end",
                    }} spacing={5} direction="row">
                        <Button variant="contained"> Prev </Button> 
                        <Button variant="contained"> Next </Button>
                    </Stack>
                </Box>
            </Box>
        </Container>
    );
}

export default ConfigurationPage;