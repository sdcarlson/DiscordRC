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

const ConfigurationPageRolePermissions = (props) => {

    const displayedText = {
        'add_reactions': "User can add reactions to messages.",
        'administrator': "User is an administrator. This overrides all other permissions,.",
        'attach_files': "User can send files in their messages.",
        'ban_members': "User can ban users from the guild.",
        'change_nickname': "User can change their nickname in the guild.",
        'connect': "User can connect to a voice channel.",
        'create_expressions': "User can create emojis, stickers, and soundboard sounds.",
        'create_instant_invite': "User can create instant invites.",
        'create_private_threads': "User can create private threads.",
        'create_public_threads': "User can create public threads.",
        'deafen_members': "User can deafen other users.",
        'embed_links': "User’s messages will automatically be embedded by Discord.",
        'external_emojis': "User can use emojis from other guilds.",
        'external_stickers': "User can use stickers from other guilds.",
        'kick_members': "User can kick users from the guild.",
        'manage_channels': "User can edit, delete, or create channels in the guild.",
        'manage_events': "User can manage guild events.",
        'manage_expressions': "User can edit or delete emojis, stickers, and soundboard sounds.",
        'manage_guild': "User can edit guild properties.",
        'manage_messages': "User can delete or pin messages in a text channel.",
        'manage_nicknames': "User can change other user’s nickname in the guild.",
        'manage_roles': "User can create or edit roles less than their role’s position.",
        'manage_threads': "User can manage threads.",
        'manage_webhooks': "User can create, edit, or delete webhooks.",
        'mention_everyone': "User’s @everyone or @here will mention everyone in the text channel.",
        'moderate_members': "User can time out other members.",
        'move_members': "User can move users between other voice.",
        'mute_members': "User can mute other users.",
        'priority_speaker': "User’s @everyone or @here will mention everyone in the text channel.",
        'read_message_history': "User can read a text channel’s previous messages.",
        'read_messages': "User can read messages from all or specific text channels.",
        'request_to_speak': "User can request to speak in a stage channel.",
        'send_messages': "User can send messages from all or specific text channels.",
        'send_messages_in_threads': "User can send messages in threads.",
        'send_tts_messages': "User can send TTS messages from all or specific text channels.",
        'send_voice_messages': "User can send voice messages.",
        'speak': "User can speak in a voice channel.",
        'stream': "User can stream in a voice channel.",
        'use_application_commands': "User can use slash commands.",
        'use_embedded_activities': "User can launch an embedded application in a Voice channel.",
        'use_external_emojis': "User can use emojis from other guilds.",
        'use_external_sounds': "User can use sounds from other guilds.",
        'use_soundboard': "User can use the soundboard.",
        'use_voice_activation': "User can use voice activation in voice channels.",
        'view_audit_log': "user can view the guild’s audit log.",
        'view_guild_insights': "User can view the guild’s insights."
    }

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
        for (let i = 0; i < props.rowNames.length; i++) {
            if (props.rowNames[i] in role.permissions) {
                build[props.rowNames[i]] = role.permissions[props.rowNames[i]]
            } else {
                build[props.rowNames[i]] = 'Inherit'
            }
        }
        setValues(build)
        setDialogNameValue(role.name)
    }, [role])


    const handleToggleButtonChange = (event, newOption) => {
        if (!newOption)
            return
        const r = props.rowNames[event.currentTarget.getAttribute('rownum')]
        let tempRoleData = [...roleData]
        tempRoleData[roleDataId] = {...tempRoleData[roleDataId]}
        tempRoleData[roleDataId].permissions[r] = newOption
        props.setRoleRows(tempRoleData)
    };

    const handleSwitchChange = (event, newOption) => {
        const r = props.rowNames[event.target.getAttribute('rownum')]
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
               {props.rowTypes.map((rowtype, i) => {
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
                            <Typography>{displayedText[props.rowNames[i]]}</Typography>
                            <MuiSwitchLarge sx={{marginRight: 5}} checked={values[props.rowNames[i]] === 'True'} onChange={handleSwitchChange} inputProps={{'rownum':i}} />
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
                            <Typography>{displayedText[props.rowNames[i]]}</Typography>
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
