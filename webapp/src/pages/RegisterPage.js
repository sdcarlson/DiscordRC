import React, { useState } from 'react';
import { Container, TextField, Button, Typography } from '@mui/material';

const RegisterPage = ({ onRegistrationSuccess, onRegistrationFailure }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [name, setName] = useState('');
    

    const handleRegister = async (event) => {
        event.preventDefault();

        const response = await fetch('http://localhost:8000/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ email, name, password, confirmPassword }),
        });

        if (response.ok) {
            const data = await response.json();
            console.log('Registration successful:', data);
            onRegistrationSuccess(data);
        } else {
            console.error('Registration failed');
            onRegistrationFailure();
        }
    };

    return (
        <Container component="main" maxWidth="xs" sx={{ mt: 8 }}>
            <Typography component="h1" variant="h2" sx={{ mb: 4, textAlign: 'center' }}>
                DiscordRC
            </Typography>
            <Typography component="h1" variant="h5">
                Register
            </Typography>
            <form onSubmit={handleRegister}>
                <TextField
                    margin="normal"
                    required
                    fullWidth
                    id="email"
                    label="Email Address"
                    name="email"
                    autoComplete="email"
                    autoFocus
                    value={email}
                    sx={{backgroundColor: 'primary.light', color: 'text.primary' }}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <TextField
                    margin="normal"
                    required
                    fullWidth
                    id="name"
                    label="Name"
                    name="name"
                    autoComplete="name"
                    autoFocus
                    value={name}
                    sx={{backgroundColor: 'primary.light', color: 'text.primary' }}
                    onChange={(e) => setName(e.target.value)}
                />
                <TextField
                    margin="normal"
                    required
                    fullWidth
                    name="password"
                    label="Password"
                    type="password"
                    id="password"
                    autoComplete="new-password"
                    value={password}
                    sx={{backgroundColor: 'primary.light', color: 'text.primary' }}
                    onChange={(e) => setPassword(e.target.value)}
                />
                    <TextField
                    margin="normal"
                    required
                    fullWidth
                    name="confirmpassword"
                    label="Confirm-Password"
                    type="confirmpassword"
                    id="confirmpassword"
                    autoComplete="confirm-password"
                    value={confirmPassword}
                    sx={{backgroundColor: 'primary.light', color: 'text.primary' }}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                />
                <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    sx={{ mt: 3, mb: 2, backgroundColor: 'primary.dark', color: 'text.primary' }}
                >
                    Register
                </Button>
            </form>
        </Container>
    );
};

export default RegisterPage;