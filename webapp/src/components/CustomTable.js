import React, { useState, useEffect } from 'react'
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Container, Stack, Button, Checkbox } from '@mui/material'
import CustomTableRowDialog from './CustomTableRowDialog'

const CustomTable = (props) => {

  // ['name', 'display_separately', 'allow_mention', 'roleperm1', 'roleperm2']
  const [rows, setRows] = useState([{
    name: 'temp',
    display_separately: 'False',
    allow_mention: 'False',
    roleperm1: 'True',
    roleperm2: 'True'
  }, {
    name: 'temp2',
    display_separately: 'True',
    allow_mention: 'True',
    roleperm1: 'True',
    roleperm2: 'True'
  }, {
    name: 'temp3',
    display_separately: 'True',
    allow_mention: 'False',
    roleperm1: 'False',
    roleperm2: 'True'
  }, {
    name: 'temp4',
    display_separately: 'True',
    allow_mention: 'True',
    roleperm1: 'True',
    roleperm2: 'False'
  }]) // FIXME: replace with []
    
  const [checkbox, setCheckbox] = useState([])
  const [openAddDialog, setOpenAddDialog] = useState(false);

  const handleParentCheckbox = (event) => {
    if (event.target.checked) 
      setCheckbox([...Array(rows.length).keys()]);
    else
      setCheckbox([]);
  };

  const handleChildCheckbox = (event) => {
    const id = parseInt(event.target.name);
    if (event.target.checked) 
      setCheckbox([...checkbox, id]);
    else 
      setCheckbox(checkbox.filter(item => item !== id));
  };

  const deleteSelectedRow = () => {
    setRows(rows.filter((row, i) => !checkbox.includes(i)));
    setCheckbox([]);
  }

  return (
    <Container sx={{ padding: 5 }}>
      <CustomTableRowDialog rows={rows} setRows={setRows} open={openAddDialog} setOpen={setOpenAddDialog} 
        headings={props.headings} rownames={props.rownames} rowtypes={props.rowtypes} title='Add Role'/>
      <Stack spacing={5} direction="row" justifyContent="center">
        <Button variant="contained" style={{maxWidth: '175px', maxHeight: '40px', minWidth: '175px', minHeight: '40px'}} 
        onClick={()=>{setOpenAddDialog(true);}}>Add Row</Button>
        <Button variant="contained" style={{maxWidth: '175px', maxHeight: '40px', minWidth: '175px', minHeight: '40px'}}>Edit Row</Button>
        <Button variant="contained" style={{maxWidth: '175px', maxHeight: '40px', minWidth: '175px', minHeight: '40px'}} 
          onClick={deleteSelectedRow}>Delete Row(s)</Button>
      </Stack>
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }}>
          <TableHead>
            <TableRow>
              <TableCell> 
                <Checkbox
                  checked={checkbox.length !== 0}
                  indeterminate={checkbox.length !== 0 && rows.length !== checkbox.length}
                  onChange={handleParentCheckbox}
                />
              </TableCell>
              {props.headings.map((headings) => (<TableCell><b>{headings}</b></TableCell>))}
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((row, i) => (
              <TableRow
                key={row.name}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell> 
                  <Checkbox
                    checked={checkbox.includes(i)}
                    onChange={handleChildCheckbox}
                    name={i}
                  />
                </TableCell>
                {props.rownames.map((rowname, j) => {
                  if (j == 0)
                    return (<TableCell component="th" scope="row">{row[rowname]}</TableCell>)
                  else
                    return (<TableCell>{row[rowname]}</TableCell>)
                })}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
}

export default CustomTable;