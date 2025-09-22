import React, { useState, useEffect, useRef } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  List,
  ListItem,
  ListItemText,
  Chip,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  Grid,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  ListItemIcon,
  Divider,
  Fade,
  Zoom,
  Avatar,
  Badge
} from '@mui/material';
import {
  Send,
  Psychology,
  Security,
  Emergency,
  Warning,
  CheckCircle,
  Info,
  Mic,
  MicOff,
  AttachFile,
  CameraAlt,
  Settings,
  Person,
  LocalHospital,
  Phone,
  LocationOn,
  Timer
} from '@mui/icons-material';
import { medicalAPI } from '../services/api';
import toast from 'react-hot-toast';

const ChatPage = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'assistant',
      content: 'Hello! I\'m MAYBERRY, your AI medical assistant. How can I help you today?',
      timestamp: new Date(),
      riskLevel: 'low',
      confidence: 1.0,
      privacyStatus: {
        localProcessing: true,
        dataEncrypted: true,
        hipaaCompliant: true
      }
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [emergencyDialogOpen, setEmergencyDialogOpen] = useState(false);
  const [emergencyResponse, setEmergencyResponse] = useState(null);
  const [privacyStatus, setPrivacyStatus] = useState({
    localProcessing: true,
    dataEncrypted: true,
    hipaaCompliant: true,
    securityScore: 95
  });
  const messagesEndRef = useRef(null);
  const sessionId = useRef(`session_${Date.now()}`);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = input;
    setInput('');
    setIsLoading(true);

    try {
      const response = await medicalAPI.post('/medical/chat', {
        content: currentInput,
        session_id: sessionId.current
      });

      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: response.data.content,
        timestamp: new Date(response.data.created_at),
        riskLevel: response.data.risk_level,
        confidence: response.data.confidence_score,
        recommendations: response.data.recommendations,
        sources: response.data.sources,
        emergencyInfo: response.data.emergency_info,
        emergencyResponse: response.data.emergency_response,
        privacyStatus: response.data.privacy_status,
        medicalMemoryUsed: response.data.medical_memory_used,
        aiPersonality: response.data.ai_personality,
        modelVersion: response.data.model_version
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Handle emergency responses
      if (response.data.emergency_response) {
        setEmergencyResponse(response.data.emergency_response);
        setEmergencyDialogOpen(true);
      }

      // Update privacy status
      if (response.data.privacy_status) {
        setPrivacyStatus(prev => ({
          ...prev,
          ...response.data.privacy_status
        }));
      }

    } catch (error) {
      console.error('Chat error:', error);
      toast.error('Failed to get AI response');
      
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: 'I apologize, but I encountered an error processing your request. Please try again or contact support if the issue persists.',
        timestamp: new Date(),
        riskLevel: 'low',
        confidence: 0.0,
        error: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleVoiceInput = () => {
    setIsRecording(!isRecording);
    // Voice input implementation would go here
    toast.info('Voice input feature coming soon!');
  };

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'critical': return 'error';
      case 'high': return 'warning';
      case 'medium': return 'info';
      default: return 'success';
    }
  };

  const getRiskIcon = (riskLevel) => {
    switch (riskLevel) {
      case 'critical': return <Emergency />;
      case 'high': return <Warning />;
      case 'medium': return <Info />;
      default: return <CheckCircle />;
    }
  };

  return (
    <Container maxWidth="md">
      <Paper elevation={3} sx={{ height: '80vh', display: 'flex', flexDirection: 'column', borderRadius: 2 }}>
        {/* Enhanced Header */}
        <Box sx={{ 
          p: 2, 
          borderBottom: '1px solid', 
          borderColor: 'divider', 
          bgcolor: 'primary.main', 
          color: 'white',
          borderRadius: '8px 8px 0 0'
        }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Avatar sx={{ bgcolor: 'rgba(255,255,255,0.2)' }}>
                <Psychology />
              </Avatar>
              <Box>
                <Typography variant="h6">MAYBERRY AI Medical Assistant</Typography>
                <Typography variant="body2" sx={{ opacity: 0.9 }}>
                  Advanced Medical AI • HIPAA Compliant • Privacy-First
                </Typography>
              </Box>
            </Box>
            
            {/* Privacy Status Indicators */}
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Tooltip title="Local Processing Active">
                <Badge color="success" variant="dot">
                  <Security />
                </Badge>
              </Tooltip>
              <Tooltip title="Data Encrypted">
                <Badge color="success" variant="dot">
                  <CheckCircle />
                </Badge>
              </Tooltip>
              <Typography variant="caption" sx={{ opacity: 0.8 }}>
                Security: {privacyStatus.securityScore}%
              </Typography>
            </Box>
          </Box>
        </Box>

        {/* Messages Area */}
        <Box sx={{ flex: 1, overflow: 'auto', p: 1, bgcolor: 'grey.50' }}>
          <List sx={{ py: 0 }}>
            {messages.map((message, index) => (
              <Fade in={true} key={message.id}>
                <ListItem
                  sx={{
                    flexDirection: 'column',
                    alignItems: message.type === 'user' ? 'flex-end' : 'flex-start',
                    py: 1.5,
                  }}
                >
                  <Paper
                    elevation={message.type === 'assistant' ? 2 : 1}
                    sx={{
                      p: 2,
                      maxWidth: '85%',
                      bgcolor: message.type === 'user' 
                        ? 'primary.main' 
                        : message.error 
                          ? 'error.light' 
                          : 'white',
                      color: message.type === 'user' ? 'white' : 'text.primary',
                      borderRadius: 2,
                      border: message.type === 'assistant' && message.riskLevel === 'critical' 
                        ? '2px solid' 
                        : 'none',
                      borderColor: message.riskLevel === 'critical' ? 'error.main' : 'transparent'
                    }}
                  >
                    <ListItemText
                      primary={message.content}
                      secondary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                          <Typography variant="caption" sx={{ opacity: 0.7 }}>
                            {message.timestamp.toLocaleTimeString()}
                          </Typography>
                          {message.medicalMemoryUsed && (
                            <Chip label="Memory" size="small" color="info" />
                          )}
                        </Box>
                      }
                      secondaryTypographyProps={{
                        color: message.type === 'user' ? 'rgba(255,255,255,0.7)' : 'text.secondary',
                      }}
                    />
                    
                    {/* Enhanced Message Metadata */}
                    {message.type === 'assistant' && (
                      <Box sx={{ mt: 2, display: 'flex', flexDirection: 'column', gap: 1 }}>
                        {message.riskLevel && (
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Chip
                              icon={getRiskIcon(message.riskLevel)}
                              label={`Risk: ${message.riskLevel.toUpperCase()}`}
                              size="small"
                              color={getRiskColor(message.riskLevel)}
                              variant={message.riskLevel === 'critical' ? 'filled' : 'outlined'}
                            />
                            <Chip
                              label={`Confidence: ${Math.round((message.confidence || 0) * 100)}%`}
                              size="small"
                              color="default"
                              variant="outlined"
                            />
                          </Box>
                        )}
                        
                        {/* Recommendations */}
                        {message.recommendations && message.recommendations.length > 0 && (
                          <Box sx={{ mt: 1 }}>
                            <Typography variant="caption" color="text.secondary">
                              Recommendations:
                            </Typography>
                            {message.recommendations.slice(0, 2).map((rec, idx) => (
                              <Typography key={idx} variant="body2" sx={{ fontSize: '0.75rem', mt: 0.5 }}>
                                • {rec}
                              </Typography>
                            ))}
                          </Box>
                        )}
                        
                        {/* Sources */}
                        {message.sources && message.sources.length > 0 && (
                          <Typography variant="caption" color="text.secondary" sx={{ mt: 1 }}>
                            Sources: {message.sources.slice(0, 2).join(', ')}
                          </Typography>
                        )}
                      </Box>
                    )}
                  </Paper>
                </ListItem>
              </Fade>
            ))}
            
            {isLoading && (
              <Zoom in={isLoading}>
                <ListItem>
                  <Paper elevation={1} sx={{ p: 2, bgcolor: 'grey.100', borderRadius: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                      <CircularProgress size={24} />
                      <Box>
                        <Typography variant="body2">MAYBERRY is analyzing...</Typography>
                        <Typography variant="caption" color="text.secondary">
                          Using advanced medical AI models
                        </Typography>
                      </Box>
                    </Box>
                  </Paper>
                </ListItem>
              </Zoom>
            )}
          </List>
          <div ref={messagesEndRef} />
        </Box>

        {/* Enhanced Input Area */}
        <Box sx={{ 
          p: 2, 
          borderTop: '1px solid', 
          borderColor: 'divider',
          bgcolor: 'white',
          borderRadius: '0 0 8px 8px'
        }}>
          <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-end' }}>
            <TextField
              fullWidth
              multiline
              maxRows={4}
              variant="outlined"
              placeholder="Describe your symptoms or ask a health question..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSend()}
              disabled={isLoading}
              sx={{ 
                '& .MuiOutlinedInput-root': { 
                  borderRadius: 2,
                  bgcolor: 'grey.50'
                } 
              }}
            />
            
            {/* Action Buttons */}
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              <Tooltip title="Voice Input">
                <IconButton 
                  color={isRecording ? 'error' : 'primary'}
                  onClick={handleVoiceInput}
                  disabled={isLoading}
                >
                  {isRecording ? <MicOff /> : <Mic />}
                </IconButton>
              </Tooltip>
              
              <Tooltip title="Attach File">
                <IconButton disabled={isLoading}>
                  <AttachFile />
                </IconButton>
              </Tooltip>
              
              <Button
                variant="contained"
                onClick={handleSend}
                disabled={!input.trim() || isLoading}
                sx={{ 
                  minWidth: 'auto',
                  px: 2,
                  borderRadius: 2,
                  bgcolor: 'primary.main',
                  '&:hover': {
                    bgcolor: 'primary.dark'
                  }
                }}
              >
                <Send />
              </Button>
            </Box>
          </Box>
          
          {/* Quick Actions */}
          <Box sx={{ mt: 1, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            {['Headache', 'Fever', 'Chest pain', 'Fatigue'].map((symptom) => (
              <Chip
                key={symptom}
                label={symptom}
                size="small"
                variant="outlined"
                onClick={() => setInput(prev => prev + (prev ? ', ' : '') + symptom)}
                sx={{ cursor: 'pointer' }}
              />
            ))}
          </Box>
        </Box>
      </Paper>

      {/* Emergency Dialog */}
      <Dialog 
        open={emergencyDialogOpen} 
        onClose={() => setEmergencyDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle sx={{ bgcolor: 'error.main', color: 'white' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Emergency />
            EMERGENCY DETECTED
          </Box>
        </DialogTitle>
        <DialogContent sx={{ p: 3 }}>
          {emergencyResponse && (
            <>
              <Alert severity="error" sx={{ mb: 2 }}>
                {emergencyResponse.message}
              </Alert>
              
              <Typography variant="h6" gutterBottom>
                Immediate Actions Required:
              </Typography>
              <List>
                {emergencyResponse.immediate_actions?.map((action, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <Warning color="error" />
                    </ListItemIcon>
                    <ListItemText primary={action} />
                  </ListItem>
                ))}
              </List>
              
              <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                Emergency Contacts:
              </Typography>
              <Grid container spacing={2}>
                {emergencyResponse.emergency_contacts?.map((contact, index) => (
                  <Grid item xs={12} sm={6} key={index}>
                    <Card>
                      <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Phone color="error" />
                          <Typography variant="body2">{contact}</Typography>
                        </Box>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </>
          )}
        </DialogContent>
        <DialogActions sx={{ p: 3 }}>
          <Button onClick={() => setEmergencyDialogOpen(false)} variant="outlined">
            I Understand
          </Button>
          <Button 
            variant="contained" 
            color="error"
            startIcon={<Phone />}
            href="tel:911"
          >
            Call 911
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default ChatPage;
