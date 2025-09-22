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
  Chip,
  Alert,
  Avatar,
  Badge,
  Divider,
  LinearProgress,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import {
  ArrowForward,
  LocalHospital,
  VerifiedUser,
  Speed,
  Biotech,
  Psychology,
  Security,
  Emergency,
  Lock,
  Shield,
  PrivacyTip,
  TrendingUp,
  Verified,
  Star,
  CheckCircle,
  Warning,
  Info,
  Chat,
  Science,
  VisibilityOff,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const competitiveAdvantages = [
  {
    icon: <Security sx={{ fontSize: 40, color: 'success.main' }} />,
    title: 'HIPAA & GDPR Compliant',
    description: 'Unlike competitors like Leny.ai, we are fully compliant with healthcare privacy regulations.',
    advantage: 'Security First',
    badge: 'EXCLUSIVE'
  },
  {
    icon: <Lock sx={{ fontSize: 40, color: 'primary.main' }} />,
    title: 'Local Processing',
    description: 'Process your data on-device for complete privacy. No competitor offers this level of privacy.',
    advantage: 'Privacy First',
    badge: 'UNIQUE'
  },
  {
    icon: <TrendingUp sx={{ fontSize: 40, color: 'secondary.main' }} />,
    title: 'Advanced Medical AI',
    description: 'BioBERT & ClinicalBERT models for superior medical text understanding.',
    advantage: 'AI Superiority',
    badge: 'ADVANCED'
  },
  {
    icon: <Emergency sx={{ fontSize: 40, color: 'error.main' }} />,
    title: 'Emergency Detection',
    description: 'Real-time emergency symptom detection with immediate action recommendations.',
    advantage: 'Life-Saving',
    badge: 'CRITICAL'
  }
];

const featureCards = [
  {
    icon: <Chat sx={{ fontSize: 40, color: 'primary.main' }} />,
    title: 'AI Medical Chat',
    description: 'Advanced conversational AI with medical memory and personalized responses.',
    path: '/chat',
    features: ['Medical Memory', 'Emergency Detection', 'Privacy-First']
  },
  {
    icon: <Psychology sx={{ fontSize: 40, color: 'secondary.main' }} />,
    title: 'Symptom Checker',
    description: 'Interactive body map and advanced symptom analysis with predictive insights.',
    path: '/symptom-checker',
    features: ['Body Map', 'Predictive Analytics', 'Risk Assessment']
  },
  {
    icon: <VerifiedUser sx={{ fontSize: 40, color: 'success.main' }} />,
    title: 'Expert Second Opinion',
    description: 'AI-powered second opinion with expert panel validation and consensus building.',
    path: '/second-opinion',
    features: ['Expert Panel', 'Consensus Building', 'Confidence Scoring']
  },
  {
    icon: <Biotech sx={{ fontSize: 40, color: 'info.main' }} />,
    title: 'Lab Analysis',
    description: 'AI-powered lab result interpretation with biomarker trend analysis.',
    path: '/lab-analysis',
    features: ['Biomarker Trends', 'File Upload', 'Risk Indicators']
  },
  {
    icon: <Shield sx={{ fontSize: 40, color: 'warning.main' }} />,
    title: 'Privacy Dashboard',
    description: 'Complete control over your data with transparent privacy metrics.',
    path: '/privacy',
    features: ['Data Export', 'Deletion Rights', 'Security Metrics']
  },
  {
    icon: <Science sx={{ fontSize: 40, color: 'error.main' }} />,
    title: 'Health Timeline',
    description: 'Visual timeline of your health journey with AI insights and trends.',
    path: '/dashboard',
    features: ['Health Timeline', 'Trend Analysis', 'Predictive Insights']
  },
];

const competitorComparison = [
  { feature: 'HIPAA Compliant', mayberry: true, docus: true, leny: false },
  { feature: 'Advanced AI Models', mayberry: true, docus: false, leny: false },
  { feature: 'Local Processing', mayberry: true, docus: false, leny: false },
  { feature: 'Medical Memory', mayberry: true, docus: false, leny: false },
  { feature: 'Emergency Detection', mayberry: true, docus: false, leny: false },
  { feature: 'Privacy Dashboard', mayberry: true, docus: false, leny: false },
  { feature: 'Interactive Body Map', mayberry: true, docus: false, leny: false },
  { feature: 'Predictive Analytics', mayberry: true, docus: false, leny: false },
];

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth="lg">
      {/* Hero Section */}
      <Paper
        elevation={0}
        sx={{
          textAlign: 'center',
          py: { xs: 8, md: 12 },
          px: { xs: 2, md: 4 },
          my: 4,
          borderRadius: 4,
          background: `linear-gradient(135deg, rgba(14, 165, 233, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%)`,
          position: 'relative',
          overflow: 'hidden'
        }}
      >
        <Box sx={{ position: 'absolute', top: 0, right: 0, opacity: 0.1 }}>
          <Typography variant="h1" sx={{ fontSize: '200px', color: 'primary.main' }}>
            AI
          </Typography>
        </Box>
        
        <Box sx={{ position: 'relative', zIndex: 1 }}>
          <Badge 
            badgeContent="NEW" 
            color="error" 
            sx={{ mb: 2 }}
          >
            <Chip 
              icon={<Verified />} 
              label="v2.0 - Advanced Medical AI" 
              color="primary" 
              variant="outlined" 
            />
          </Badge>
          
          <Typography variant="h1" component="h1" sx={{ mb: 2, color: 'primary.dark', fontWeight: 700 }}>
            MAYBERRY Medical AI
          </Typography>
          <Typography variant="h4" component="p" sx={{ mb: 1, color: 'text.primary', fontWeight: 600 }}>
            The World's Most Private & Intelligent Medical Assistant
        </Typography>
          <Typography variant="h6" component="p" sx={{ mb: 4, color: 'text.secondary', maxWidth: '800px', mx: 'auto' }}>
            Advanced medical AI with BioBERT/ClinicalBERT models, HIPAA compliance, local processing, 
            and emergency detection. Outperforming competitors like Docus.ai and Leny.ai.
        </Typography>
          
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap', mb: 4 }}>
        <Button
          variant="contained"
          color="primary"
          size="large"
          endIcon={<ArrowForward />}
          onClick={() => navigate('/chat')}
              sx={{ px: 4, py: 1.5, fontSize: '1.1rem' }}
            >
              Start Free Consultation
            </Button>
            <Button
              variant="outlined"
              color="secondary"
              size="large"
              endIcon={<Security />}
              onClick={() => navigate('/privacy')}
              sx={{ px: 4, py: 1.5, fontSize: '1.1rem' }}
            >
              View Privacy Dashboard
        </Button>
          </Box>

          {/* Security Score */}
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 2, mb: 2 }}>
            <Typography variant="body1" color="text.secondary">Security Score:</Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Typography variant="h6" color="success.main" fontWeight="bold">95/100</Typography>
              <LinearProgress 
                variant="determinate" 
                value={95} 
                sx={{ width: 100, height: 8, borderRadius: 4 }}
                color="success"
              />
            </Box>
          </Box>
        </Box>
      </Paper>

      {/* Competitive Advantages */}
      <Box sx={{ my: 8 }}>
        <Typography variant="h3" component="h2" align="center" sx={{ mb: 2, color: 'text.primary', fontWeight: 700 }}>
          Why Choose MAYBERRY Over Competitors?
        </Typography>
        <Typography variant="h6" align="center" sx={{ mb: 6, color: 'text.secondary', maxWidth: '600px', mx: 'auto' }}>
          We outperform Docus.ai and Leny.ai with unique features and superior technology
        </Typography>
        
        <Grid container spacing={4}>
          {competitiveAdvantages.map((advantage, index) => (
            <Grid item xs={12} md={6} key={advantage.title}>
              <Card 
                sx={{ 
                  height: '100%', 
                  position: 'relative',
                  border: '2px solid',
                  borderColor: advantage.badge === 'EXCLUSIVE' ? 'success.main' : 'transparent',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    transition: 'transform 0.3s ease-in-out'
                  }
                }}
              >
                {advantage.badge === 'EXCLUSIVE' && (
                  <Chip 
                    label="EXCLUSIVE" 
                    color="success" 
                    size="small" 
                    sx={{ 
                      position: 'absolute', 
                      top: 8, 
                      right: 8, 
                      fontWeight: 'bold' 
                    }} 
                  />
                )}
                <CardContent sx={{ p: 3 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                    {advantage.icon}
                    <Box>
                      <Typography variant="h6" component="h3" sx={{ fontWeight: 600 }}>
                        {advantage.title}
                      </Typography>
                      <Chip 
                        label={advantage.advantage} 
                        size="small" 
                        color="primary" 
                        variant="outlined" 
                      />
                    </Box>
                  </Box>
                  <Typography variant="body1" sx={{ color: 'text.secondary' }}>
                    {advantage.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Features Grid */}
      <Box sx={{ my: 8 }}>
        <Typography variant="h3" component="h2" align="center" sx={{ mb: 6, color: 'text.primary', fontWeight: 700 }}>
          Comprehensive Medical AI Features
        </Typography>
        <Grid container spacing={4}>
          {featureCards.map((card) => (
            <Grid item xs={12} md={6} lg={4} key={card.title}>
              <Card sx={{ 
                height: '100%', 
                display: 'flex', 
                flexDirection: 'column',
                '&:hover': {
                  transform: 'translateY(-2px)',
                  transition: 'transform 0.2s ease-in-out'
                }
              }}>
                <CardContent sx={{ textAlign: 'center', flexGrow: 1, p: 3 }}>
                  <Box sx={{ mb: 2 }}>{card.icon}</Box>
                  <Typography variant="h5" component="h3" sx={{ mb: 1, color: 'text.primary', fontWeight: 600 }}>
                    {card.title}
                  </Typography>
                  <Typography variant="body1" sx={{ color: 'text.secondary', mb: 2 }}>
                    {card.description}
                  </Typography>
                  
                  {/* Feature Tags */}
                  <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap', justifyContent: 'center' }}>
                    {card.features.map((feature) => (
                      <Chip 
                        key={feature} 
                        label={feature} 
                        size="small" 
                        variant="outlined" 
                        color="primary"
                      />
                    ))}
                  </Box>
                </CardContent>
                <CardActions sx={{ justifyContent: 'center', p: 2 }}>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={() => navigate(card.path)}
                    endIcon={<ArrowForward />}
                  >
                    Try Now
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Competitor Comparison */}
      <Box sx={{ my: 8 }}>
        <Typography variant="h3" component="h2" align="center" sx={{ mb: 6, color: 'text.primary', fontWeight: 700 }}>
          How We Compare to Competitors
        </Typography>
        
        <Paper elevation={2} sx={{ p: 3, borderRadius: 2 }}>
          <Grid container spacing={2} sx={{ mb: 2 }}>
            <Grid item xs={4}>
              <Typography variant="h6" fontWeight="bold" color="primary">
                Feature
              </Typography>
            </Grid>
            <Grid item xs={3}>
              <Typography variant="h6" fontWeight="bold" color="success.main" align="center">
                MAYBERRY
              </Typography>
            </Grid>
            <Grid item xs={2}>
              <Typography variant="h6" fontWeight="bold" color="text.secondary" align="center">
                Docus.ai
              </Typography>
            </Grid>
            <Grid item xs={3}>
              <Typography variant="h6" fontWeight="bold" color="text.secondary" align="center">
                Leny.ai
              </Typography>
            </Grid>
          </Grid>
          
          <Divider sx={{ mb: 2 }} />
          
          {competitorComparison.map((item, index) => (
            <Grid container spacing={2} key={index} sx={{ py: 1 }}>
              <Grid item xs={4}>
                <Typography variant="body1">{item.feature}</Typography>
              </Grid>
              <Grid item xs={3}>
                <Box sx={{ display: 'flex', justifyContent: 'center' }}>
                  {item.mayberry ? (
                    <CheckCircle color="success" />
                  ) : (
                    <Warning color="error" />
                  )}
                </Box>
              </Grid>
              <Grid item xs={2}>
                <Box sx={{ display: 'flex', justifyContent: 'center' }}>
                  {item.docus ? (
                    <CheckCircle color="success" />
                  ) : (
                    <Warning color="error" />
                  )}
                </Box>
              </Grid>
              <Grid item xs={3}>
                <Box sx={{ display: 'flex', justifyContent: 'center' }}>
                  {item.leny ? (
                    <CheckCircle color="success" />
                  ) : (
                    <Warning color="error" />
                  )}
                </Box>
              </Grid>
            </Grid>
          ))}
        </Paper>
        
        <Alert severity="success" sx={{ mt: 3 }}>
          <Typography variant="h6" sx={{ mb: 1 }}>
            🏆 MAYBERRY leads in 8/8 key features!
          </Typography>
          <Typography>
            We offer the most comprehensive medical AI platform with unique features like local processing, 
            medical memory, and emergency detection that no competitor provides.
          </Typography>
        </Alert>
      </Box>

      {/* Security & Privacy Section */}
      <Box sx={{ my: 8, textAlign: 'center' }}>
        <Typography variant="h3" component="h2" sx={{ mb: 4, color: 'text.primary', fontWeight: 700 }}>
          Your Privacy is Our Priority
        </Typography>
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <Avatar sx={{ width: 80, height: 80, bgcolor: 'success.main', mx: 'auto', mb: 2 }}>
              <Security sx={{ fontSize: 40 }} />
            </Avatar>
            <Typography variant="h6" sx={{ mb: 1, fontWeight: 600 }}>HIPAA & GDPR Compliant</Typography>
            <Typography variant="body2" color="text.secondary">
              Unlike Leny.ai, we are fully compliant with healthcare privacy regulations from day one.
            </Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <Avatar sx={{ width: 80, height: 80, bgcolor: 'primary.main', mx: 'auto', mb: 2 }}>
              <Lock sx={{ fontSize: 40 }} />
            </Avatar>
            <Typography variant="h6" sx={{ mb: 1, fontWeight: 600 }}>Local Processing</Typography>
            <Typography variant="body2" color="text.secondary">
              Process your data on-device for complete privacy. No competitor offers this level of protection.
            </Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <Avatar sx={{ width: 80, height: 80, bgcolor: 'secondary.main', mx: 'auto', mb: 2 }}>
              <PrivacyTip sx={{ fontSize: 40 }} />
            </Avatar>
            <Typography variant="h6" sx={{ mb: 1, fontWeight: 600 }}>Zero-Knowledge Architecture</Typography>
            <Typography variant="body2" color="text.secondary">
              We don't store your medical data. You have complete control with our privacy dashboard.
            </Typography>
          </Grid>
        </Grid>
      </Box>

      {/* Call to Action */}
      <Box sx={{ my: 8, textAlign: 'center' }}>
        <Paper 
          elevation={3} 
          sx={{ 
            p: 6, 
            borderRadius: 3, 
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white'
          }}
        >
          <Typography variant="h4" component="h2" sx={{ mb: 2, fontWeight: 700 }}>
            Ready to Experience the Future of Medical AI?
          </Typography>
          <Typography variant="h6" sx={{ mb: 4, opacity: 0.9 }}>
            Join thousands of users who trust MAYBERRY for their healthcare needs
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
            <Button
              variant="contained"
              color="secondary"
              size="large"
              endIcon={<ArrowForward />}
              onClick={() => navigate('/chat')}
              sx={{ px: 4, py: 1.5, fontSize: '1.1rem' }}
            >
              Start Free Consultation
            </Button>
            <Button
              variant="outlined"
              color="inherit"
              size="large"
              onClick={() => navigate('/register')}
              sx={{ px: 4, py: 1.5, fontSize: '1.1rem', borderColor: 'white', color: 'white' }}
            >
              Create Account
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default HomePage;