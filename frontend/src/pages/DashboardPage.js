import React from 'react';
import { Container, Typography, Paper } from '@mui/material';
import { Dashboard } from '@mui/icons-material';

const DashboardPage = () => {
  return (
    <Container maxWidth="md">
      <Paper elevation={1} sx={{ p: 4, textAlign: 'center' }}>
        <Dashboard sx={{ fontSize: 60, color: 'info.main', mb: 2 }} />
        <Typography variant="h4" component="h1" sx={{ mb: 2 }}>
          Health Dashboard
        </Typography>
        <Typography variant="body1" sx={{ color: 'text.secondary' }}>
          Coming soon - Personalized health insights and analytics
        </Typography>
      </Paper>
    </Container>
  );
};

export default DashboardPage;
