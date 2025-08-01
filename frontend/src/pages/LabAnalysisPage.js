import React, { useState } from 'react';
import {
  Container,
  Typography,
  Paper,
  Box,
  Button,
  Grid,
  Card,
  CardContent,
  Alert,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  CircularProgress,
  LinearProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import {
  Science,
  CloudUpload,
  CheckCircle,
  Warning,
  Info,
  TrendingUp,
  TrendingDown,
  Remove,
  ExpandMore,
  GetApp,
  Share,
  Print,
} from '@mui/icons-material';
import { useDropzone } from 'react-dropzone';
import { medicalAPI } from '../services/api';
import toast from 'react-hot-toast';

const commonLabTests = [
  'Complete Blood Count (CBC)',
  'Basic Metabolic Panel (BMP)',
  'Comprehensive Metabolic Panel (CMP)',
  'Lipid Panel',
  'Thyroid Function Tests',
  'Liver Function Tests',
  'Hemoglobin A1C',
  'Vitamin D',
  'Vitamin B12',
  'Iron Studies',
  'Urinalysis',
  'PSA (Prostate-Specific Antigen)',
];

const LabAnalysisPage = () => {
  const [testType, setTestType] = useState('');
  const [testName, setTestName] = useState('');
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [manualData, setManualData] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.pdf'],
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
    },
    maxFiles: 5,
    maxSize: 10485760, // 10MB
    onDrop: (acceptedFiles) => {
      setUploadedFiles(acceptedFiles);
    },
  });

  const handleAnalyze = async () => {
    if (!testType || (!uploadedFiles.length && !manualData.trim())) {
      toast.error('Please select a test type and provide lab data');
      return;
    }

    setIsAnalyzing(true);
    try {
      const response = await medicalAPI.analyzeLabResults({
        test_name: testName || testType,
        test_type: testType,
        raw_data: manualData,
        // file_data would be base64 encoded file data in real implementation
      });
      setAnalysisResult(response.data);
      toast.success('Lab results analyzed successfully!');
    } catch (error) {
      toast.error('Failed to analyze lab results. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getBiomarkerStatus = (value, range) => {
    // Simplified logic for demonstration
    if (value.includes('Normal') || value.includes('normal')) return 'normal';
    if (value.includes('High') || value.includes('high')) return 'high';
    if (value.includes('Low') || value.includes('low')) return 'low';
    return 'normal';
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'normal': return <CheckCircle color="success" />;
      case 'high': return <TrendingUp color="error" />;
      case 'low': return <TrendingDown color="warning" />;
      default: return <Remove color="disabled" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'normal': return 'success';
      case 'high': return 'error';
      case 'low': return 'warning';
      default: return 'default';
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" component="h1" align="center" sx={{ mb: 2, color: 'primary.main' }}>
          Lab Result Analysis
        </Typography>
        <Typography variant="h6" align="center" sx={{ color: 'text.secondary', mb: 4 }}>
          Upload your lab results and get AI-powered insights and explanations
        </Typography>
        
        <Alert severity="info" sx={{ mb: 4 }}>
          <strong>Privacy Notice:</strong> Your lab results are processed securely and are not stored permanently. 
          This analysis is for educational purposes and should not replace professional medical interpretation.
        </Alert>
      </Box>

      <Grid container spacing={4}>
        {/* Upload Section */}
        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 3 }}>
            <Typography variant="h5" sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
              <Science color="primary" />
              Lab Data Input
            </Typography>

            {/* Test Type Selection */}
            <FormControl fullWidth sx={{ mb: 3 }}>
              <InputLabel>Test Type</InputLabel>
              <Select
                value={testType}
                onChange={(e) => setTestType(e.target.value)}
                label="Test Type"
              >
                {commonLabTests.map((test) => (
                  <MenuItem key={test} value={test}>
                    {test}
                  </MenuItem>
                ))}
                <MenuItem value="other">Other</MenuItem>
              </Select>
            </FormControl>

            {testType === 'other' && (
              <TextField
                fullWidth
                label="Custom Test Name"
                value={testName}
                onChange={(e) => setTestName(e.target.value)}
                sx={{ mb: 3 }}
              />
            )}

            {/* File Upload */}
            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" sx={{ mb: 2 }}>Upload Lab Report</Typography>
              <Paper
                {...getRootProps()}
                sx={{
                  p: 3,
                  textAlign: 'center',
                  borderStyle: 'dashed',
                  borderWidth: 2,
                  borderColor: isDragActive ? 'primary.main' : 'grey.300',
                  backgroundColor: isDragActive ? 'primary.light' : 'background.paper',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                }}
              >
                <input {...getInputProps()} />
                <CloudUpload sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
                <Typography variant="h6" sx={{ mb: 1 }}>
                  {isDragActive ? 'Drop files here' : 'Drag & drop files here'}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  or click to browse (PDF, Images, Text files)
                </Typography>
                <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                  Max 5 files, 10MB each
                </Typography>
              </Paper>

              {uploadedFiles.length > 0 && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="subtitle2" sx={{ mb: 1 }}>Uploaded Files:</Typography>
                  {uploadedFiles.map((file, index) => (
                    <Chip
                      key={index}
                      label={`${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`}
                      onDelete={() => {
                        const newFiles = uploadedFiles.filter((_, i) => i !== index);
                        setUploadedFiles(newFiles);
                      }}
                      sx={{ m: 0.5 }}
                    />
                  ))}
                </Box>
              )}
            </Box>

            {/* Manual Data Entry */}
            <Typography variant="h6" sx={{ mb: 2 }}>Or Enter Data Manually</Typography>
            <TextField
              fullWidth
              multiline
              rows={6}
              label="Lab Results Data"
              value={manualData}
              onChange={(e) => setManualData(e.target.value)}
              placeholder="Paste your lab results here...\n\nExample:\nHemoglobin: 14.5 g/dL (Normal: 12.0-15.5)\nHematocrit: 42% (Normal: 36-46%)\nWhite Blood Cells: 7.2 K/uL (Normal: 4.0-11.0)"
              sx={{ mb: 3 }}
            />

            <Button
              fullWidth
              variant="contained"
              size="large"
              onClick={handleAnalyze}
              disabled={isAnalyzing || (!uploadedFiles.length && !manualData.trim())}
              sx={{ py: 1.5 }}
            >
              {isAnalyzing ? (
                <CircularProgress size={24} color="inherit" />
              ) : (
                'Analyze Lab Results'
              )}
            </Button>
          </Paper>
        </Grid>

        {/* Results Section */}
        <Grid item xs={12} md={6}>
          {analysisResult ? (
            <Paper elevation={2} sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Typography variant="h5" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Science color="primary" />
                  Analysis Results
                </Typography>
                <Box>
                  <Button startIcon={<GetApp />} size="small" sx={{ mr: 1 }}>Export</Button>
                  <Button startIcon={<Share />} size="small" sx={{ mr: 1 }}>Share</Button>
                  <Button startIcon={<Print />} size="small">Print</Button>
                </Box>
              </Box>

              {/* Test Overview */}
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="h6" sx={{ mb: 2 }}>{analysisResult.test_name}</Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                    <LinearProgress
                      variant="determinate"
                      value={analysisResult.confidence_score * 100}
                      sx={{ flexGrow: 1 }}
                    />
                    <Typography variant="body2">
                      Confidence: {Math.round(analysisResult.confidence_score * 100)}%
                    </Typography>
                  </Box>
                </CardContent>
              </Card>

              {/* Biomarker Results */}
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="h6" sx={{ mb: 2 }}>Biomarker Analysis</Typography>
                  <List>
                    {Object.entries(analysisResult.results).map(([key, value], index) => {
                      const status = getBiomarkerStatus(value, null);
                      return (
                        <React.Fragment key={key}>
                          <ListItem>
                            <ListItemIcon>
                              {getStatusIcon(status)}
                            </ListItemIcon>
                            <ListItemText
                              primary={key.charAt(0).toUpperCase() + key.slice(1)}
                              secondary={
                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 0.5 }}>
                                  <Typography variant="body2">{value}</Typography>
                                  <Chip size="small" label={status} color={getStatusColor(status)} />
                                </Box>
                              }
                            />
                          </ListItem>
                          {index < Object.entries(analysisResult.results).length - 1 && <Divider />}
                        </React.Fragment>
                      );
                    })}
                  </List>
                </CardContent>
              </Card>

              {/* Interpretation */}
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="h6" sx={{ mb: 2 }}>Interpretation</Typography>
                  <Typography variant="body1" sx={{ mb: 2 }}>
                    {analysisResult.interpretation}
                  </Typography>
                  
                  {analysisResult.risk_indicators && analysisResult.risk_indicators.length > 0 && (
                    <Alert severity="warning" sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" sx={{ mb: 1 }}>Risk Indicators:</Typography>
                      <List dense>
                        {analysisResult.risk_indicators.map((indicator, index) => (
                          <ListItem key={index}>
                            <ListItemIcon>
                              <Warning color="warning" />
                            </ListItemIcon>
                            <ListItemText primary={indicator} />
                          </ListItem>
                        ))}
                      </List>
                    </Alert>
                  )}
                </CardContent>
              </Card>

              {/* Recommendations */}
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="h6" sx={{ mb: 2 }}>Recommendations</Typography>
                  <List>
                    {analysisResult.recommendations.map((recommendation, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <CheckCircle color="success" />
                        </ListItemIcon>
                        <ListItemText primary={recommendation} />
                      </ListItem>
                    ))}
                  </List>
                  
                  {analysisResult.requires_followup && (
                    <Alert severity="info" sx={{ mt: 2 }}>
                      <Typography variant="subtitle2">Follow-up Required</Typography>
                      <Typography variant="body2">
                        Based on these results, we recommend scheduling a follow-up appointment with your healthcare provider.
                      </Typography>
                    </Alert>
                  )}
                </CardContent>
              </Card>

              {/* Educational Content */}
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMore />}>
                  <Typography variant="h6">Understanding Your Results</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2" sx={{ mb: 2 }}>
                    This section provides educational information about your lab results. 
                    Always consult with your healthcare provider for professional medical interpretation.
                  </Typography>
                  <Alert severity="info">
                    <Typography variant="body2">
                      Lab values can vary based on individual factors, laboratory methods, and reference ranges. 
                      This analysis is for informational purposes only.
                    </Typography>
                  </Alert>
                </AccordionDetails>
              </Accordion>
            </Paper>
          ) : (
            <Paper elevation={2} sx={{ p: 3, textAlign: 'center', color: 'text.secondary' }}>
              <Science sx={{ fontSize: 80, mb: 2, opacity: 0.3 }} />
              <Typography variant="h6" sx={{ mb: 2 }}>
                Analysis Results Will Appear Here
              </Typography>
              <Typography>
                Upload your lab results or enter data manually, then click "Analyze Lab Results" to get detailed insights.
              </Typography>
            </Paper>
          )}
        </Grid>
      </Grid>
    </Container>
  );
};

export default LabAnalysisPage;
