import React from 'react';
import {
  Container,
  Typography,
  Button,
  Box,
  Paper,
  Grid,
  Card,
  CardContent,
  CardActions,
} from '@mui/material';
import {
  ArrowForward,
  LocalHospital,
  VerifiedUser,
  Speed,
  Biotech,
  Psychology,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const featureCards = [
  {
    icon: <Psychology sx={{ fontSize: 40, color: 'secondary.main' }} />,
    title: 'AI Symptom Checker',
    description: 'Get an AI-powered analysis of your symptoms to understand possible causes and next steps.',
    path: '/symptom-checker',
  },
  {
    icon: <VerifiedUser sx={{ fontSize: 40, color: 'tertiary.main' }} />,
    title: 'Expert Second Opinion',
    description: 'Validate your diagnosis or treatment plan with a second opinion from our AI-powered expert panel.',
    path: '/second-opinion',
  },
  {
    icon: <Biotech sx={{ fontSize: 40, color: 'primary.main' }} />,
    title: 'Lab Result Analysis',
    description: 'Upload your lab results to get a clear, easy-to-understand explanation of what they mean.',
    path: '/lab-analysis',
  },
];

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth="lg">
      <Paper
        elevation={0}
        sx={{
          textAlign: 'center',
          py: { xs: 8, md: 12 },
          px: { xs: 2, md: 4 },
          my: 4,
          borderRadius: 4,
          background: `linear-gradient(135deg, rgba(14, 165, 233, 0.05) 0%, rgba(16, 185, 129, 0.05) 100%)`,
        }}
      >
        <Typography variant="h1" component="h1" sx={{ mb: 2, color: 'primary.dark' }}>
          Welcome to MAYBERRY Medical AI
        </Typography>
        <Typography variant="h5" component="p" sx={{ mb: 4, color: 'text.secondary', maxWidth: '700px', mx: 'auto' }}>
          Your trusted partner for intelligent, private, and accessible healthcare guidance. Get instant answers,
          symptom analysis, and expert-level insights.
        </Typography>
        <Button
          variant="contained"
          color="primary"
          size="large"
          endIcon={<ArrowForward />}
          onClick={() => navigate('/chat')}
        >
          Start Your Consultation
        </Button>
      </Paper>

      <Box sx={{ my: 8 }}>
        <Typography variant="h3" component="h2" align="center" sx={{ mb: 6, color: 'text.primary' }}>
          How MAYBERRY Can Help You
        </Typography>
        <Grid container spacing={4}>
          {featureCards.map((card) => (
            <Grid item xs={12} md={4} key={card.title}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardContent sx={{ textAlign: 'center', flexGrow: 1 }}>
                  <Box sx={{ mb: 2 }}>{card.icon}</Box>
                  <Typography variant="h5" component="h3" sx={{ mb: 1, color: 'text.primary' }}>
                    {card.title}
                  </Typography>
                  <Typography variant="body1" sx={{ color: 'text.secondary' }}>
                    {card.description}
                  </Typography>
                </CardContent>
                <CardActions sx={{ justifyContent: 'center', p: 2 }}>
                  <Button
                    variant="outlined"
                    color="secondary"
                    onClick={() => navigate(card.path)}
                  >
                    Learn More
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      <Box sx={{ my: 8, textAlign: 'center', color: 'text.primary' }}>
        <Typography variant="h3" component="h2" sx={{ mb: 4 }}>
          Your Health, Your Data, Your Privacy
        </Typography>
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <LocalHospital sx={{ fontSize: 48, mb: 1, color: 'primary.main' }} />
            <Typography variant="h6">HIPAA & GDPR Compliant</Typography>
            <Typography variant="body2">We follow the strictest data privacy regulations to keep your information secure.</Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <VerifiedUser sx={{ fontSize: 48, mb: 1, color: 'success.main' }} />
            <Typography variant="h6">Anonymous Access</Typography>
            <Typography variant="body2">Use our core features without creating an account or providing personal information.</Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <Speed sx={{ fontSize: 48, mb: 1, color: 'tertiary.main' }} />
            <Typography variant="h6">Local Processing</Typography>
            <Typography variant="body2">Your health data can be processed on your own device, ensuring complete privacy.</Typography>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default HomePage;
