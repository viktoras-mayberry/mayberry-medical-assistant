import React from 'react';
import { Container, Typography, Paper } from '@mui/material';
import { Person } from '@mui/icons-material';

const ProfilePage = () => {
  return (
    <Container maxWidth="md">
      <Paper elevation={1} sx={{ p: 4, textAlign: 'center' }}>
        <Person sx={{ fontSize: 60, color: 'success.main', mb: 2 }} />
        <Typography variant="h4" component="h1" sx={{ mb: 2 }}>
          User Profile
        </Typography>
        <Typography variant="body1" sx={{ color: 'text.secondary' }}>
          Coming soon - Manage your profile and health preferences
        </Typography>
      </Paper>
    </Container>
  );
};

export default ProfilePage;
