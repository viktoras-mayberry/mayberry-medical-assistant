import React, { useState } from 'react';
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
} from '@mui/material';
import { Send, Psychology } from '@mui/icons-material';

const ChatPage = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'assistant',
      content: 'Hello! I\'m MAYBERRY, your AI medical assistant. How can I help you today?',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    // Simulate API call
    setTimeout(() => {
      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: 'Thank you for your question. I understand you\'re asking about your health concerns. While I can provide general health information, I recommend consulting with a healthcare professional for personalized medical advice.',
        timestamp: new Date(),
        riskLevel: 'low',
        confidence: 0.85,
      };
      setMessages(prev => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 1000);
  };

  return (
    <Container maxWidth="md">
      <Paper elevation={1} sx={{ height: '70vh', display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ p: 2, borderBottom: '1px solid', borderColor: 'divider', bgcolor: 'primary.main', color: 'white' }}>
          <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Psychology />
            AI Medical Chat
          </Typography>
          <Typography variant="body2" sx={{ opacity: 0.9 }}>
            Get instant medical guidance and health information
          </Typography>
        </Box>

        <Box sx={{ flex: 1, overflow: 'auto', p: 1 }}>
          <List>
            {messages.map((message) => (
              <ListItem
                key={message.id}
                sx={{
                  flexDirection: 'column',
                  alignItems: message.type === 'user' ? 'flex-end' : 'flex-start',
                }}
              >
                <Paper
                  elevation={1}
                  sx={{
                    p: 2,
                    maxWidth: '80%',
                    bgcolor: message.type === 'user' ? 'primary.main' : 'background.paper',
                    color: message.type === 'user' ? 'white' : 'text.primary',
                  }}
                >
                  <ListItemText
                    primary={message.content}
                    secondary={message.timestamp.toLocaleTimeString()}
                    secondaryTypographyProps={{
                      color: message.type === 'user' ? 'rgba(255,255,255,0.7)' : 'text.secondary',
                    }}
                  />
                  {message.riskLevel && (
                    <Box sx={{ mt: 1 }}>
                      <Chip
                        label={`Risk: ${message.riskLevel}`}
                        size="small"
                        color={message.riskLevel === 'low' ? 'success' : 'warning'}
                      />
                      <Chip
                        label={`Confidence: ${Math.round(message.confidence * 100)}%`}
                        size="small"
                        sx={{ ml: 1 }}
                      />
                    </Box>
                  )}
                </Paper>
              </ListItem>
            ))}
            {isLoading && (
              <ListItem>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <CircularProgress size={20} />
                  <Typography variant="body2">MAYBERRY is thinking...</Typography>
                </Box>
              </ListItem>
            )}
          </List>
        </Box>

        <Box sx={{ p: 2, borderTop: '1px solid', borderColor: 'divider' }}>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="Describe your symptoms or ask a health question..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              disabled={isLoading}
            />
            <Button
              variant="contained"
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
              endIcon={<Send />}
            >
              Send
            </Button>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default ChatPage;
