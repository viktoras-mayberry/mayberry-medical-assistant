import React from 'react';
import { Container, Typography, Paper } from '@mui/material';
import { VisibilityOff } from '@mui/icons-material';

const SecondOpinionPage = () => {
  return (
    <Container maxWidth="md">
      <Paper elevation={1} sx={{ p: 4, textAlign: 'center' }}>
        <VisibilityOff sx={{ fontSize: 60, color: 'tertiary.main', mb: 2 }} />
        <Typography variant="h4" component="h1" sx={{ mb: 2 }}>
          Expert Second Opinion
        </Typography>
        <Typography variant="body1" sx={{ color: 'text.secondary' }}>
          Coming soon - Get expert validation of your diagnosis and treatment plan
        </Typography>
      </Paper>
    </Container>
  );
};

export default SecondOpinionPage;
