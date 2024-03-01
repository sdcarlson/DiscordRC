import React, { useState, useEffect, useRef } from 'react'
import { Box, Container, Stack, Button, ToggleButton, ToggleButtonGroup, Typography } from "@mui/material";
import { useFormContext } from '../context/FormContext';
import EditIcon from '@mui/icons-material/Edit';
import CheckIcon from '@mui/icons-material/Check';
import CloseIcon from '@mui/icons-material/Close';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import { LocalConvenienceStoreOutlined } from '@mui/icons-material';

const ConfigurationPageRolePermissions = (props) => {

    const {
        roleData,
        setRoleData,
    } = useFormContext()
    
    const [role, setRole] = useState({})
    const [values, setValues] = useState({})
    const [roleDataId, setRoleDataId] = useState(-1)

    useEffect(() => {
        for (let i = 0; i < roleData.length; i++) {
            if (roleData[i].id === props.id) {
                setRole(roleData[i])
                setRoleDataId(i)
            }
        }
    }, [props.id, roleData])

    useEffect(() => {
        if (!role || Object.keys(role).length === 0) {
            return;
        }
        let build = {}
        for (let i = 0; i < props.rowNames.length; i++) {
            if (props.rowNames[i] in role.permissions) {
                build[props.rowNames[i]] = role.permissions[props.rowNames[i]]
            } else {
                build[props.rowNames[i]] = 'Inherit'
            }
        }
        setValues(build)
    }, [role])


    const handleToggleButtonChange = (event, newOption) => {
        if (!newOption)
            return
        const r = props.rowNames[event.currentTarget.getAttribute('rownum')]
        let tempRoleData = [...roleData]
        tempRoleData[roleDataId] = {...tempRoleData[roleDataId]}
        tempRoleData[roleDataId].permissions[r] = newOption
        setRoleData(tempRoleData)
        //setRole(tempRoleData[roleDataId])
    };
    
    return (
        <Box sx={{
            width: '65%',
            height: '100%',
            display: 'flex',
            'flex-flow': 'column',
            border: 1,
            borderColor: 'primary.main',
            float: 'right'
        }}>
            <Box sx={{
                width: '100%',
                margin: '5',    
                direction: "column",
                alignItems: "center",
                justifyContent: "center"
            }}>
                <Stack spacing={5} direction="row" alignItems="center" justifyContent="center">
                    <>Role Name: {role.name} <EditIcon/></>
                </Stack>
            </Box>
            
            <Box sx={{
                flex: '1 1 auto',
                overflow: 'auto',
                margin: '5',
            }}>
               {props.rowTypes.map((rowtype, i) => {
                    // FIXME: map rownames to text
                    if (rowtype === 'text') {
                        // return (
                        //     <TextField
                        //         id="filled-search"
                        //         name={props.rownames[i]}
                        //         label={props.headings[i]}
                        //         variant="filled"
                        //         fullWidth
                        //         onChange={handleTextFieldChange}
                        //     />
                        // )
                    } else if (rowtype === 'slider') {
                        // return (
                        //     <FormControlLabel control={<Switch onChange={handleSwitchChange} name={props.rownames[i]} />} label={props.rownames[i]} />
                        // )
                    } else if (rowtype === 'toggleButton') {
                        return (
                        <Stack spacing={2} direction="row" alignItems="center" justifyContent="center">
                            <Typography>{props.rowNames[i]}</Typography>
                            <ToggleButtonGroup 
                                exclusive='true'
                                value={values[props.rowNames[i]]}
                                onChange={handleToggleButtonChange}
                                rownum={i}
                            >
                                <ToggleButton value="True" rownum={i}>
                                    <CheckIcon />
                                </ToggleButton>
                                <ToggleButton value="Inherit" rownum={i}>
                                    <ArrowUpwardIcon />
                                </ToggleButton>
                                <ToggleButton value="False" rownum={i}>
                                    <CloseIcon />
                                </ToggleButton>
                            </ToggleButtonGroup>
                        </Stack>)
                    }
                })}
            </Box>
        </Box>
        
    );
}

export default ConfigurationPageRolePermissions;