// import React, { useState, useEffect, useRef } from 'react'
// import { useFormContext } from '../context/FormContext';
// import { styled } from '@mui/material/styles';
// import Box from '@mui/material/Box';
// import Switch from '@mui/material/Switch';
// import Stack from '@mui/material/Stack';
// import Button from '@mui/material/Button';
// import Radio from '@mui/material/Radio';
// import RadioGroup from '@mui/material/RadioGroup';
// import FormControlLabel from '@mui/material/FormControlLabel';
// import ToggleButton from '@mui/material/ToggleButton';
// import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
// import Typography from '@mui/material/Typography';
// import TextField from '@mui/material/TextField';
// import Dialog from '@mui/material/Dialog';
// import DialogActions from '@mui/material/DialogActions';
// import DialogContent from '@mui/material/DialogContent';
// import DialogTitle from '@mui/material/DialogTitle';
// import EditIcon from '@mui/icons-material/Edit';
// import CheckIcon from '@mui/icons-material/Check';
// import CloseIcon from '@mui/icons-material/Close';
// import HorizontalRuleIcon from '@mui/icons-material/HorizontalRule';

// const ConfigurationChannelRoleSpecificPermissions = (props) => {

//     const displayedText = {
//         'age_restriction':'Age-Restricted Channel', 
//         'view_channel':'Allow everyone to view this channel by default', 
//     }

//     const channelTypeText = {
//         'announce': 'Announcement Channel',
//         'voice': 'Voice Channel',
//         'text': 'Text Channel'
//     }

//     const {
//         roleData,
//         channelData,
//     } = useFormContext()
    
//     const [channel, setChannel] = useState({});
//     const [values, setValues] = useState({});
//     const [channelDataId, setChannelDataId] = useState(-1);
//     const [roleSelected, setRoleSelected] = useState(null);

//     const [dialogNameValue, setDialogNameValue] = React.useState(null);
//     const [dialogTypeValue, setDialogTypeValue] = React.useState(null);
//     const [openNameDialog, setOpenNameDialog] = React.useState(false);

//     useEffect(() => {
//         for (let i = 0; i < channelData.length; i++) {
//             if (channelData[i].id === props.id) {
//                 setChannel(channelData[i])
//                 setChannelDataId(i)
//             }
//         }
//     }, [props.id, channelData])

//     useEffect(() => {
//         if (!channel || Object.keys(channel).length === 0) {
//             return;
//         }
//         let build = {}
//         for (let i = 0; i < props.rowNames.length; i++) {
//             if (props.rowNames[i] in channel.permissions) {
//                 build[props.rowNames[i]] = channel.permissions[props.rowNames[i]]
//             } else {
//                 build[props.rowNames[i]] = 'Inherit'
//             }
//         }
//         setValues(build)
//         setDialogTypeValue(channel.type)
//         setDialogNameValue(channel.name)
//     }, [channel])


//     const handleToggleButtonChange = (event, newOption) => {
//         if (!newOption)
//             return
//         const r = props.rowNames[event.currentTarget.getAttribute('rownum')]
//         let tempChannelData = [...channelData]
//         tempChannelData[channelDataId] = {...tempChannelData[channelDataId]}
//         tempChannelData[channelDataId].permissions[r] = newOption
//         props.setChannelRows(tempChannelData)
//     };
    
//     const handleRoleToggleButtonSelection = (event, nextRole) => {
//         setRoleSelected(nextRole)
//     }

//     const handleSwitchChange = (event, newOption) => {
//         const r = props.rowNames[event.target.getAttribute('rownum')]
//         let tempChannelData = [...channelData]
//         tempChannelData[channelDataId] = {...tempChannelData[channelDataId]}
//         if (newOption === true)
//             tempChannelData[channelDataId].permissions[r] = 'True'
//         else
//             tempChannelData[channelDataId].permissions[r] = 'False'
//         props.setChannelRows(tempChannelData)
//     }

//     const handleCloseNameDialog = () => {
//         setOpenNameDialog(false);
//     };
    
//     return (
//         <>  
//             <Box sx={{
//                 flex: '1 1 auto',
//                 overflow: 'auto',
//                 margin: '5',
//             }}>
//                 {roleSelected === null && props.rowTypes.map((rowtype, i) => {
//                    if (rowtype === 'slider') {
//                         return (
//                         <Box sx={{
//                             display: 'flex',
//                             'justify-content': 'space-between',
//                             'align-items': 'center',
//                             paddingLeft: '20',
//                             paddingRight: '20',
//                             paddingTop: '20'
//                         }}>
//                             <Typography>{displayedText[props.rowNames[i]]}</Typography>
//                             <MuiSwitchLarge sx={{marginRight: 5}} checked={values[props.rowNames[i]] === 'True'} onChange={handleSwitchChange} inputProps={{'rownum':i}} />
//                         </Box>
//                         )
//                     } else if (rowtype === 'toggleButton') {
//                         return (
//                         <Box sx={{
//                             display: 'flex',
//                             'justify-content': 'space-between',
//                             'align-items': 'center',
//                             paddingLeft: '20',
//                             paddingRight: '20',
//                             paddingTop: '20'
//                         }}>
//                             <Typography>{displayedText[props.rowNames[i]]}</Typography>
//                             <ToggleButtonGroup 
//                                 exclusive='true'
//                                 value={values[props.rowNames[i]]}
//                                 onChange={handleToggleButtonChange}
//                                 rownum={i}
//                             >
//                                 <ToggleButton value="True" rownum={i}>
//                                     <CheckIcon />
//                                 </ToggleButton>
//                                 <ToggleButton value="Inherit" rownum={i}>
//                                     <HorizontalRuleIcon />
//                                 </ToggleButton>
//                                 <ToggleButton value="False" rownum={i}>
//                                     <CloseIcon />
//                                 </ToggleButton>
//                             </ToggleButtonGroup>
//                         </Box>
//                     )}
//                 })}
//                 {roleSelected !== null && <></>}
//             </Box>
            
//         </>
        
//     );
// }

// export const MuiSwitchLarge = styled(Switch)(({ theme }) => ({
//     width: 68,
//     height: 34,
//     padding: 7,
//     "& .MuiSwitch-switchBase": {
//       margin: 1,
//       padding: 0,
//       transform: "translateX(6px)",
//       "&.Mui-checked": {
//         transform: "translateX(30px)",
//       },
//     },
//     "& .MuiSwitch-thumb": {
//       width: 32,
//       height: 32,
//     },
//     "& .MuiSwitch-track": {
//       borderRadius: 20 / 2,
//     },
//   }));

// export default ConfigurationChannelRoleSpecificPermissions;