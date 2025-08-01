import React, { useState } from 'react';
import {
  Container,
  Typography,
  Paper,
  Box,
  TextField,
  Button,
  Chip,
  Grid,
  Card,
  CardContent,
  Alert,
  LinearProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Slider,
  CircularProgress,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
} from '@mui/material';
import {
  Psychology,
  Add,
  Delete,
  ExpandMore,
  Warning,
  CheckCircle,
  Info,
  LocalHospital,
  AccessTime,
  Thermostat,
  FitnessCenter,
} from '@mui/icons-material';
import { medicalAPI } from '../services/api';
import toast from 'react-hot-toast';

const commonSymptoms = [
  'Headache', 'Fever', 'Cough', 'Sore throat', 'Fatigue', 'Nausea',
  'Dizziness', 'Chest pain', 'Shortness of breath', 'Abdominal pain',
  'Back pain', 'Joint pain', 'Rash', 'Vomiting', 'Diarrhea', 'Insomnia'
];

const SymptomCheckerPage = () => {
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [customSymptom, setCustomSymptom] = useState('');
  const [duration, setDuration] = useState('');
  const [severity, setSeverity] = useState(5);
  const [age, setAge] = useState('');
  const [gender, setGender] = useState('');
  const [additionalInfo, setAdditionalInfo] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysis, setAnalysis] = useState(null);

  const handleSymptomSelect = (symptom) => {
    if (!selectedSymptoms.includes(symptom)) {
      setSelectedSymptoms([...selectedSymptoms, symptom]);
    }
  };

  const handleSymptomRemove = (symptom) => {
    setSelectedSymptoms(selectedSymptoms.filter(s => s !== symptom));
  };

  const handleAddCustomSymptom = () => {
    if (customSymptom.trim() && !selectedSymptoms.includes(customSymptom.trim())) {
      setSelectedSymptoms([...selectedSymptoms, customSymptom.trim()]);
      setCustomSymptom('');
    }
  };

  const handleAnalyzeSymptoms = async () => {
    if (selectedSymptoms.length === 0) {
      toast.error('Please select at least one symptom');
      return;
    }

    setIsAnalyzing(true);
    try {
      const response = await medicalAPI.analyzeSymptoms({
        symptoms: selectedSymptoms,
        duration,
        severity,
        age: age ? parseInt(age) : null,
        gender,
        additional_info: additionalInfo
      });
      setAnalysis(response.data);
    } catch (error) {
      toast.error('Failed to analyze symptoms. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getRiskColor = (level) => {
    switch (level) {
      case 'low': return 'success';
      case 'medium': return 'warning';
      case 'high': return 'error';
      case 'critical': return 'error';
      default: return 'info';
    }
  };

  const getRiskIcon = (level) => {
    switch (level) {
      case 'low': return <CheckCircle />;
      case 'medium': return <Warning />;
      case 'high': return <LocalHospital />;
      case 'critical': return <LocalHospital />;
      default: return <Info />;
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" component="h1" align="center" sx={{ mb: 2, color: 'primary.main' }}>
          AI Symptom Checker
        </Typography>
        <Typography variant="h6" align="center" sx={{ color: 'text.secondary', mb: 4 }}>
          Describe your symptoms and get AI-powered health insights
        </Typography>
        
        <Alert severity="info" sx={{ mb: 4 }}>
          <strong>Medical Disclaimer:</strong> This tool is for informational purposes only and should not replace professional medical advice. 
          Always consult with a healthcare provider for accurate diagnosis and treatment.
        </Alert>
      </Box>

      <Grid container spacing={4}>
        {/* Input Section */}
        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 3 }}>
            <Typography variant="h5" sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
              <Psychology color="primary" />
              Symptom Selection
            </Typography>

            {/* Common Symptoms */}
            <Typography variant="h6" sx={{ mb: 2 }}>Common Symptoms</Typography>
            <Box sx={{ mb: 3 }}>
              {commonSymptoms.map((symptom) => (
                <Chip
                  key={symptom}
                  label={symptom}
                  onClick={() => handleSymptomSelect(symptom)}
                  color={selectedSymptoms.includes(symptom) ? 'primary' : 'default'}
                  sx={{ m: 0.5, cursor: 'pointer' }}
                />
              ))}
            </Box>

            {/* Custom Symptom Input */}
            <Box sx={{ display: 'flex', gap: 1, mb: 3 }}>
              <TextField
                fullWidth
                label="Add custom symptom"
                value={customSymptom}
                onChange={(e) => setCustomSymptom(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleAddCustomSymptom()}
              />
              <Button
                variant="outlined"
                onClick={handleAddCustomSymptom}
                startIcon={<Add />}
              >
                Add
              </Button>
            </Box>

            {/* Selected Symptoms */}
            {selectedSymptoms.length > 0 && (
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" sx={{ mb: 1 }}>Selected Symptoms</Typography>
                {selectedSymptoms.map((symptom) => (
                  <Chip
                    key={symptom}
                    label={symptom}
                    onDelete={() => handleSymptomRemove(symptom)}
                    color="primary"
                    sx={{ m: 0.5 }}
                  />
                ))}
              </Box>
            )}

            {/* Additional Information */}
            <Accordion sx={{ mb: 2 }}>
              <AccordionSummary expandIcon={<ExpandMore />}>
                <Typography>Additional Information (Optional)</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <FormControl fullWidth>
                      <InputLabel>Duration</InputLabel>
                      <Select
                        value={duration}
                        onChange={(e) => setDuration(e.target.value)}
                        label="Duration"
                      >
                        <MenuItem value="hours">A few hours</MenuItem>
                        <MenuItem value="1-2days">1-2 days</MenuItem>
                        <MenuItem value="3-7days">3-7 days</MenuItem>
                        <MenuItem value="1-2weeks">1-2 weeks</MenuItem>
                        <MenuItem value="3-4weeks">3-4 weeks</MenuItem>
                        <MenuItem value="months">Several months</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Age"
                      type="number"
                      value={age}
                      onChange={(e) => setAge(e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <FormControl fullWidth>
                      <InputLabel>Gender</InputLabel>
                      <Select
                        value={gender}
                        onChange={(e) => setGender(e.target.value)}
                        label="Gender"
                      >
                        <MenuItem value="male">Male</MenuItem>
                        <MenuItem value="female">Female</MenuItem>
                        <MenuItem value="other">Other</MenuItem>
                        <MenuItem value="prefer_not_to_say">Prefer not to say</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Box>
                      <Typography gutterBottom>Severity (1-10)</Typography>
                      <Slider
                        value={severity}
                        onChange={(e, value) => setSeverity(value)}
                        valueLabelDisplay="auto"
                        step={1}
                        marks
                        min={1}
                        max={10}
                      />
                    </Box>
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      multiline
                      rows={3}
                      label="Additional Information"
                      value={additionalInfo}
                      onChange={(e) => setAdditionalInfo(e.target.value)}
                      placeholder="Any other symptoms, medical history, or relevant information..."
                    />
                  </Grid>
                </Grid>
              </AccordionDetails>
            </Accordion>

            <Button
              fullWidth
              variant="contained"
              size="large"
              onClick={handleAnalyzeSymptoms}
              disabled={isAnalyzing || selectedSymptoms.length === 0}
              sx={{ py: 1.5 }}
            >
              {isAnalyzing ? (
                <CircularProgress size={24} color="inherit" />
              ) : (
                'Analyze Symptoms'
              )}
            </Button>
          </Paper>
        </Grid>

        {/* Results Section */}
        <Grid item xs={12} md={6}>
          {analysis ? (
            <Paper elevation={2} sx={{ p: 3 }}>
              <Typography variant="h5" sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                <LocalHospital color="primary" />
                Analysis Results
              </Typography>

              {/* Risk Level */}
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                    {getRiskIcon(analysis.risk_level)}
                    <Typography variant="h6">
                      Risk Level: <Chip label={analysis.risk_level.toUpperCase()} color={getRiskColor(analysis.risk_level)} />
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={analysis.confidence_score * 100}
                    sx={{ mb: 1 }}
                  />
                  <Typography variant="body2" color="text.secondary">
                    Confidence: {Math.round(analysis.confidence_score * 100)}%
                  </Typography>
                </CardContent>
              </Card>

              {/* Possible Conditions */}
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="h6" sx={{ mb: 2 }}>Possible Conditions</Typography>
                  <List>
                    {analysis.possible_conditions.map((condition, index) => (
                      <React.Fragment key={index}>
                        <ListItem>
                          <ListItemIcon>
                            <FitnessCenter color="primary" />
                          </ListItemIcon>
                          <ListItemText
                            primary={condition.name}
                            secondary={`Probability: ${Math.round(condition.probability * 100)}%`}
                          />
                        </ListItem>
                        {index < analysis.possible_conditions.length - 1 && <Divider />}
                      </React.Fragment>
                    ))}
                  </List>
                </CardContent>
              </Card>

              {/* Recommendations */}
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="h6" sx={{ mb: 2 }}>Recommendations</Typography>
                  <List>
                    {analysis.recommendations.map((recommendation, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <CheckCircle color="success" />
                        </ListItemIcon>
                        <ListItemText primary={recommendation} />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>

              {/* Emergency Warning */}
              {analysis.should_seek_immediate_care && (
                <Alert severity="error" sx={{ mb: 3 }}>
                  <Typography variant="h6" sx={{ mb: 1 }}>⚠️ Seek Immediate Medical Care</Typography>
                  <Typography>
                    Based on your symptoms, you should consult with a healthcare provider immediately or visit an emergency room.
                  </Typography>
                </Alert>
              )}

              {/* Disclaimer */}
              <Alert severity="warning">
                <Typography variant="body2">
                  {analysis.disclaimer}
                </Typography>
              </Alert>
            </Paper>
          ) : (
            <Paper elevation={2} sx={{ p: 3, textAlign: 'center', color: 'text.secondary' }}>
              <Psychology sx={{ fontSize: 80, mb: 2, opacity: 0.3 }} />
              <Typography variant="h6" sx={{ mb: 2 }}>
                Analysis Results Will Appear Here
              </Typography>
              <Typography>
                Select your symptoms and click "Analyze Symptoms" to get AI-powered health insights.
              </Typography>
            </Paper>
          )}
        </Grid>
      </Grid>
    </Container>
  );
};

export default SymptomCheckerPage;
