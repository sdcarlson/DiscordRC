import React, { useState, useEffect, useRef } from 'react'
import { useFormContext } from '../context/FormContext';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Switch from '@mui/material/Switch';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import Typography from '@mui/material/Typography';
import CheckIcon from '@mui/icons-material/Check';
import CloseIcon from '@mui/icons-material/Close';
import HorizontalRuleIcon from '@mui/icons-material/HorizontalRule';
import { textDisplayedText, categoryDisplayedText, voiceDisplayedText } from '../constants/DisplayedText';
import { categoryChannelRowTypes, categoryChannelRowNames, textChannelRowNames, textChannelRowTypes, voiceChannelRowNames, voiceChannelRowTypes } from '../constants/FormRows';


const ConfigurationChannelRoleSpecificPermissions = (props) => {

    const {
        roleData,
        channelData,
    } = useFormContext()
    
    const [channel, setChannel] = useState({});
    const [values, setValues] = useState({});
    const [channelDataId, setChannelDataId] = useState(-1);
    const [roleDataId, setRoleDataId] = useState(null);

    const [rowNames, setRowNames] = React.useState([]);
    const [rowTypes, setRowTypes] = React.useState([]);
    const [displayedText, setDisplayedText] = React.useState({});

    useEffect(() => {
        for (let i = 0; i < channelData.length; i++) {
            if (channelData[i].id === props.channelId) {
                switch (channelData[i].type) {
                    case 'category':
                        setRowNames(categoryChannelRowNames)
                        setRowTypes(categoryChannelRowTypes)
                        setDisplayedText(categoryDisplayedText)
                        break;
                    case 'voice':
                        setRowNames(voiceChannelRowNames)
                        setRowTypes(voiceChannelRowTypes)
                        setDisplayedText(voiceDisplayedText)
                        break;
                    case 'text':
                        setRowNames(textChannelRowNames)
                        setRowTypes(textChannelRowTypes)
                        setDisplayedText(textDisplayedText)
                        break;
                }
                setChannel(channelData[i])
                setChannelDataId(i)
            }
        }
    }, [props.channelId, channelData])

    useEffect(() => {
        for (let i = 0; i < roleData.length; i++) {
            if (roleData[i].id === props.roleId) {
                setRoleDataId(i)
            }
        }
    }, [props.roleId, roleData])

    useEffect(() => {
        if (!channel || Object.keys(channel).length === 0 || rowTypes.length === 0  
            || rowNames.length === 0 || Object.keys(displayedText).length === 0) {
            return;
        }
        let build = {}
        for (let i = 0; i < rowNames.length; i++) {
            if (!(roleData[roleDataId].id in channel.permissions)) {
                channel.permissions[roleData[roleDataId].id] = {}
            }
            if (rowNames[i] in channel.permissions[roleData[roleDataId].id]) {
                build[rowNames[i]] = channel.permissions[roleData[roleDataId].id][rowNames[i]]
            } else {
                build[rowNames[i]] = 'Inherit'
            }
        }
        setValues(build)
    }, [channel, roleDataId, rowTypes, rowNames, displayedText])


    const handleToggleButtonChange = (event, newOption) => {
        if (!newOption)
            return
        const r = rowNames[event.currentTarget.getAttribute('rownum')]
        let tempChannelData = [...channelData]
        tempChannelData[channelDataId] = {...tempChannelData[channelDataId]}
        tempChannelData[channelDataId].permissions[roleData[roleDataId].id][r] = newOption
        props.setChannelRows(tempChannelData)
    };

    const handleSwitchChange = (event, newOption) => {
        const r = rowNames[event.target.getAttribute('rownum')]
        let tempChannelData = [...channelData]
        tempChannelData[channelDataId] = {...tempChannelData[channelDataId]}
        if (newOption === true)
            tempChannelData[channelDataId].permissions[roleData[roleDataId].id][r] = 'True'
        else
            tempChannelData[channelDataId].permissions[roleData[roleDataId].id][r] = 'False'
        props.setChannelRows(tempChannelData)
    }
    
    return (
        <>  
            <Box sx={{
                flex: '1 1 auto',
                overflow: 'auto',
                margin: '5',
            }}>
                <Typography variant="h6">Role-Specific Permissions for {(roleDataId !== null) && roleData[roleDataId].name}</Typography>
                {rowTypes.map((rowtype, i) => {
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
                            <Typography>{displayedText[rowNames[i]]}</Typography>
                            <MuiSwitchLarge sx={{marginRight: 5}} checked={values[rowNames[i]] === 'True'} onChange={handleSwitchChange} inputProps={{'rownum':i}} />
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
                            <Typography>{displayedText[rowNames[i]]}</Typography>
                            <ToggleButtonGroup 
                                exclusive='true'
                                value={values[rowNames[i]]}
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

export default ConfigurationChannelRoleSpecificPermissions;