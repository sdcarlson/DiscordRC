import React, { useState } from 'react';
import { Container, TextField, Button, Typography} from '@mui/material';

const LoginPage = ({ onLoginSuccess, onRegisterClick }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        const response = await fetch('http://localhost:8000/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ username: email, password }),
        });

        if (response.ok) {
            const data = await response.json();
            console.log('Login successful:', data);
            onLoginSuccess(data);
        } else {
            console.error('Login failed');
        }
    };

    return (
        <Container component="main" maxWidth="xs" sx={{ mt: 8 }}>
            <Typography component="h1" variant="h2" sx={{ mb: 4, textAlign: 'center' }}>
                DiscordRC
            </Typography>
            <Typography component="h1" variant="h5">
                Login
            </Typography>
            <form onSubmit={handleSubmit}>
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
                    name="password"
                    label="Password"
                    type="password"
                    id="password"
                    autoComplete="current-password"
                    value={password}
                    sx={{backgroundColor: 'primary.light', color: 'text.primary' }}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    sx={{ mt: 3, mb: 2,backgroundColor: 'primary.dark', color: 'text.primary' }}
                >
                    Sign In
                </Button>
                <Button
                    fullWidth
                    variant="outlined"
                    sx={{ mt: 2, mb: 2, backgroundColor: 'primary.dark', color: 'text.primary' }}
                    onClick={onRegisterClick}
                >
                    Register
                </Button>
            </form>
        </Container>
    );
};

export default LoginPage;