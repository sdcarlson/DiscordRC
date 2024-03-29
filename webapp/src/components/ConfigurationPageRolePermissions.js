import React, { useState, useEffect, useRef } from 'react'
import { useFormContext } from '../context/FormContext';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Switch from '@mui/material/Switch';
import Stack from '@mui/material/Stack';
import IconButton from '@mui/material/IconButton';
import Button from '@mui/material/Button';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import EditIcon from '@mui/icons-material/Edit';
import CheckIcon from '@mui/icons-material/Check';
import CloseIcon from '@mui/icons-material/Close';
import HorizontalRuleIcon from '@mui/icons-material/HorizontalRule';
import { roleDisplayedText } from '../constants/DisplayedText';
import { roleRowNames, roleRowTypes } from '../constants/FormRows';

const ConfigurationPageRolePermissions = (props) => {

    const {
        roleData,
    } = useFormContext()
    
    const [role, setRole] = useState({})
    const [values, setValues] = useState({})
    const [roleDataId, setRoleDataId] = useState(-1)

    const [dialogNameValue, setDialogNameValue] = React.useState(null)
    const [openNameDialog, setOpenNameDialog] = React.useState(false);

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
        for (let i = 0; i < roleRowNames.length; i++) {
            if (roleRowNames[i] in role.permissions) {
                build[roleRowNames[i]] = role.permissions[roleRowNames[i]]
            } else {
                build[roleRowNames[i]] = 'Inherit'
            }
        }
        setValues(build)
        setDialogNameValue(role.name)
    }, [role])


    const handleToggleButtonChange = (event, newOption) => {
        if (!newOption)
            return
        const r = roleRowNames[event.currentTarget.getAttribute('rownum')]
        let tempRoleData = [...roleData]
        tempRoleData[roleDataId] = {...tempRoleData[roleDataId]}
        tempRoleData[roleDataId].permissions[r] = newOption
        props.setRoleRows(tempRoleData)
    };

    const handleSwitchChange = (event, newOption) => {
        const r = roleRowNames[event.target.getAttribute('rownum')]
        let tempRoleData = [...roleData]
        tempRoleData[roleDataId] = {...tempRoleData[roleDataId]}
        if (newOption === true)
            tempRoleData[roleDataId].permissions[r] = 'True'
        else
            tempRoleData[roleDataId].permissions[r] = 'False'
        props.setRoleRows(tempRoleData)
    }

    const handleCloseNameDialog = () => {
        setOpenNameDialog(false);
    };
    
    return (
        <>
            <Box sx={{
                width: '100%',
                margin: '5',    
                direction: "column",
                alignItems: "center",
                justifyContent: "center"
            }}>
                <Stack spacing={5} direction="row" alignItems="center" justifyContent="center">
                    <Typography>Role Name: {role.name} </Typography>  
                    <Button onClick={()=>{setOpenNameDialog(true)}} variant="contained">Modify<EditIcon/></Button>
                </Stack>
            </Box>
            
            <Box sx={{
                flex: '1 1 auto',
                overflow: 'auto',
                margin: '5',
            }}>
               {roleRowTypes.map((rowtype, i) => {
                   if (rowtype === 'slider') {
                        return (
                        <Box sx={{
                            display: 'flex',
                            'justify-content': 'space-between',
                            'align-items': 'center',
                            paddingLeft: '20',
                            paddingRight: '20',
                            paddingTop: '20'
                        }}>
                            <Typography>{roleDisplayedText[roleRowNames[i]]}</Typography>
                            <MuiSwitchLarge sx={{marginRight: 5}} checked={values[roleRowNames[i]] === 'True'} onChange={handleSwitchChange} inputProps={{'rownum':i}} />
                        </Box>
                        )
                    } else if (rowtype === 'toggleButton') {
                        return (
                        <Box sx={{
                            display: 'flex',
                            'justify-content': 'space-between',
                            'align-items': 'center',
                            paddingLeft: '20',
                            paddingRight: '20',
                            paddingTop: '20'
                        }}>
                            <Typography>{roleDisplayedText[roleRowNames[i]]}</Typography>
                            <ToggleButtonGroup 
                                exclusive='true'
                                value={values[roleRowNames[i]]}
                                onChange={handleToggleButtonChange}
                                rownum={i}
                            >
                                <ToggleButton value="True" rownum={i}>
                                    <CheckIcon />
                                </ToggleButton>
                                <ToggleButton value="Inherit" rownum={i}>
                                    <HorizontalRuleIcon />
                                </ToggleButton>
                                <ToggleButton value="False" rownum={i}>
                                    <CloseIcon />
                                </ToggleButton>
                            </ToggleButtonGroup>
                        </Box>
                    )}
                })}
            </Box>
            <Dialog
                open={openNameDialog}
                onClose={handleCloseNameDialog}
                fullWidth
                maxWidth="sm"
            >
                <DialogTitle>Change Name</DialogTitle>
                <DialogContent>
                    <TextField
                        autoFocus
                        required
                        margin="dense"
                        label="Name"
                        fullWidth
                        variant="standard"
                        defaultValue={role.name}
                        onChange={(event)=>{setDialogNameValue(event.target.value)}}
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseNameDialog}>Cancel</Button>
                    <Button onClick={()=>{
                        let tempRoleData = [...roleData]
                        tempRoleData[roleDataId] = {...tempRoleData[roleDataId]}
                        tempRoleData[roleDataId].name = dialogNameValue
                        props.setRoleRows(tempRoleData)
                        handleCloseNameDialog()
                    }}>Set Name</Button>
                </DialogActions>
            </Dialog>
        </>
        
    );
}

export const MuiSwitchLarge = styled(Switch)(({ theme }) => ({
    width: 68,
    height: 34,
    padding: 7,
    "& .MuiSwitch-switchBase": {
      margin: 1,
      padding: 0,
      transform: "translateX(6px)",
      "&.Mui-checked": {
        transform: "translateX(30px)",
      },
    },
    "& .MuiSwitch-thumb": {
      width: 32,
      height: 32,
    },
    "& .MuiSwitch-track": {
      borderRadius: 20 / 2,
    },
  }));

export default ConfigurationPageRolePermissions;
