import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Container, MenuItem, FormControl, Select } from '@mui/material';

const HomePage = () => {
    const [selectedServer, setSelectedServer] = useState('');
    const navigate = useNavigate();

    const servers = [
        { id: '1', name: 'Server 1' },
        { id: '2', name: 'Server 2' },
    ];

    const handleServerChange = (event) => {
        setSelectedServer(event.target.value);
    };


    return (
        <Container component="main" maxWidth="xs" sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <Button
                variant="contained"
                sx={{ mt: 3, mb: 2, backgroundColor: 'primary.main', color: 'text.primary', width: '100%' }}
                onClick={() => navigate('/')}
            >
                Create Server from Scratch
            </Button> 
            <Button
                variant="contained"
                sx={{ mt: 3, mb: 2, backgroundColor: 'primary.main', color: 'text.primary', width: '100%' }}
                onClick={() => navigate('/')}
            >
                Upload JSON
            </Button>
            <FormControl fullWidth sx={{ mt: 3, mb: 2, backgroundColor: 'primary.light', color: 'text.primary' }}>
                <Select
                    value={selectedServer}
                    onChange={handleServerChange}
                    displayEmpty
                    inputProps={{ 'aria-label': 'Without label' }}
                >
                    <MenuItem value="" disabled>
                        Edit Your Saved Servers
                    </MenuItem>
                    {servers.map((server) => (
                        <MenuItem key={server.id} value={server.id}>
                            {server.name}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
        </Container>
    );
};

export default HomePage;