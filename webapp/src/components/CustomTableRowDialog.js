import React, { useState, useEffect } from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import FormGroup from '@mui/material/FormGroup';
import Switch from '@mui/material/Switch';
import FormControlLabel from '@mui/material/FormControlLabel';


const CustomTableRowDialog = (props) => {

    const [row, setRow] = useState({});

    const handleAddRow = () => {
        const intersection = props.rownames.filter(rowname => !(rowname in row))
        const red = intersection.reduce(function(map, inter) {
            map[inter] = 'False';
            return map;
        }, {})
        const fullRow = {...row, 
            ...red
        }
        console.log(fullRow)
        props.setRows([...props.rows, fullRow]);
        props.setOpen(false);
    }
    
    const handleSwitchChange = (event) => {
        const string = event.target.checked.toString()
        setRow({
            ...row,
            [event.target.name]: string.charAt(0).toUpperCase() + string.slice(1)
        });
    }

    const handleTextFieldChange = (event) => {
        setRow({
            ...row,
            [event.target.name]: event.target.value
        })
    }

    useEffect(() => {
        if (!props.open)
            setRow({});
    }, [props.open])

    return (
        <Dialog
            open={props.open}
            onClose={()=>{props.setOpen(false);}}
            fullWidth
            maxWidth="sm"
        >
            <DialogTitle>{props.title}</DialogTitle>
                <DialogContent >
                    <FormGroup>
                        {props.rowtypes.map((rowtype, i) => {
                            if (rowtype === 'text') {
                                return (
                                    <TextField
                                        id="filled-search"
                                        name={props.rownames[i]}
                                        label={props.headings[i]}
                                        variant="filled"
                                        fullWidth
                                        onChange={handleTextFieldChange}
                                    />
                                )
                            } else if (rowtype === 'slider') {
                                return (
                                    <FormControlLabel control={<Switch onChange={handleSwitchChange} name={props.rownames[i]} />} label={props.headings[i]} />
                                )
                                // FIXME: enum/locales for label with more text (to rownames)
                            }
                        })}
                    </FormGroup>
            </DialogContent>
            <DialogActions>
                <Button onClick={()=>{props.setOpen(false);}}>Cancel</Button>
                <Button onClick={handleAddRow}>Add Row</Button>
            </DialogActions>
        </Dialog>
    )
}

export default CustomTableRowDialog;