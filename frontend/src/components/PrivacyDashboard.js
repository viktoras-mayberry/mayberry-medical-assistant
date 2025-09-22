import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  LinearProgress,
  Alert,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Paper,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  Security,
  PrivacyTip,
  Shield,
  Lock,
  CheckCircle,
  Warning,
  Info,
  Download,
  Delete,
  Refresh,
  Visibility,
  VisibilityOff
} from '@mui/icons-material';
import { medicalAPI } from '../services/api';
import toast from 'react-hot-toast';

const PrivacyDashboard = () => {
  const [privacyStatus, setPrivacyStatus] = useState(null);
  const [privacyMetrics, setPrivacyMetrics] = useState(null);
  const [complianceStatus, setComplianceStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [exportDialogOpen, setExportDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);

  useEffect(() => {
    fetchPrivacyData();
  }, []);

  const fetchPrivacyData = async () => {
    try {
      setLoading(true);
      const [statusResponse, metricsResponse, complianceResponse] = await Promise.all([
        medicalAPI.get('/privacy/status'),
        medicalAPI.get('/privacy/metrics'),
        medicalAPI.get('/privacy/compliance')
      ]);

      setPrivacyStatus(statusResponse.data.data);
      setPrivacyMetrics(metricsResponse.data.data);
      setComplianceStatus(complianceResponse.data.data);
    } catch (error) {
      console.error('Failed to fetch privacy data:', error);
      toast.error('Failed to load privacy information');
    } finally {
      setLoading(false);
    }
  };

  const handleDataExport = async () => {
    try {
      const response = await medicalAPI.post('/privacy/data-export');
      toast.success('Data export prepared successfully');
      setExportDialogOpen(false);
      // In a real app, this would trigger a download
    } catch (error) {
      toast.error('Failed to prepare data export');
    }
  };

  const handleDataDeletion = async () => {
    try {
      const response = await medicalAPI.delete('/privacy/data-deletion');
      toast.success('Data deletion completed');
      setDeleteDialogOpen(false);
      // In a real app, this would log the user out
    } catch (error) {
      toast.error('Failed to delete data');
    }
  };

  if (loading) {
    return (
      <Box sx={{ p: 3 }}>
        <LinearProgress />
        <Typography sx={{ mt: 2 }}>Loading privacy dashboard...</Typography>
      </Box>
    );
  }

  const SecurityScore = ({ score }) => (
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
      <Typography variant="h6">{score}/100</Typography>
      <LinearProgress
        variant="determinate"
        value={score}
        sx={{ width: 100, height: 8, borderRadius: 4 }}
        color={score >= 80 ? 'success' : score >= 60 ? 'warning' : 'error'}
      />
    </Box>
  );

  const ComplianceBadge = ({ type, compliant }) => (
    <Chip
      icon={compliant ? <CheckCircle /> : <Warning />}
      label={`${type.toUpperCase()}: ${compliant ? 'COMPLIANT' : 'NON-COMPLIANT'}`}
      color={compliant ? 'success' : 'error'}
      variant="outlined"
    />
  );

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Security color="primary" />
        Privacy & Security Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        {/* Security Overview */}
        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Shield color="primary" />
                Security Overview
              </Typography>
              
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Overall Security Score
                </Typography>
                <SecurityScore score={privacyMetrics?.security_score || 0} />
              </Box>

              <Divider sx={{ my: 2 }} />

              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Data Processing
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Typography variant="body2">
                    Local: {privacyMetrics?.local_processing_percentage || 0}%
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={privacyMetrics?.local_processing_percentage || 0}
                    sx={{ flexGrow: 1, height: 6, borderRadius: 3 }}
                    color="success"
                  />
                </Box>
              </Box>

              <Typography variant="body2" color="text.secondary" gutterBottom>
                Data Encrypted: {privacyMetrics?.data_encrypted_count || 0} times
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Anonymous Sessions: {privacyMetrics?.anonymous_sessions || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Compliance Status */}
        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <PrivacyTip color="primary" />
                Compliance Status
              </Typography>
              
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <ComplianceBadge 
                  type="HIPAA" 
                  compliant={complianceStatus?.hipaa?.compliant} 
                />
                <ComplianceBadge 
                  type="GDPR" 
                  compliant={complianceStatus?.gdpr?.compliant} 
                />
              </Box>

              <Divider sx={{ my: 2 }} />

              <Typography variant="body2" color="text.secondary" gutterBottom>
                Security Features
              </Typography>
              <List dense>
                {Object.entries(complianceStatus?.security_features || {}).map(([feature, enabled]) => (
                  <ListItem key={feature} sx={{ py: 0 }}>
                    <ListItemIcon>
                      {enabled ? <CheckCircle color="success" /> : <Warning color="error" />}
                    </ListItemIcon>
                    <ListItemText 
                      primary={feature.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      secondary={enabled ? 'Enabled' : 'Disabled'}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Privacy Features */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Lock color="primary" />
                Privacy Features
              </Typography>
              
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <CheckCircle color="success" />
                  <Typography variant="body2">End-to-End Encryption</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <CheckCircle color="success" />
                  <Typography variant="body2">Local Processing</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <CheckCircle color="success" />
                  <Typography variant="body2">Zero-Knowledge Architecture</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <CheckCircle color="success" />
                  <Typography variant="body2">Anonymous Mode</Typography>
                </Box>
              </Box>

              <Alert severity="success" sx={{ mt: 2 }}>
                Your data is protected with military-grade encryption and processed locally when possible.
              </Alert>
            </CardContent>
          </Card>
        </Grid>

        {/* Data Management */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Info color="primary" />
                Data Management
              </Typography>
              
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Button
                  variant="outlined"
                  startIcon={<Download />}
                  onClick={() => setExportDialogOpen(true)}
                  fullWidth
                >
                  Export My Data
                </Button>
                
                <Button
                  variant="outlined"
                  color="error"
                  startIcon={<Delete />}
                  onClick={() => setDeleteDialogOpen(true)}
                  fullWidth
                >
                  Delete All Data
                </Button>
              </Box>

              <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                You have full control over your data. Export it anytime or delete it permanently.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Export Dialog */}
      <Dialog open={exportDialogOpen} onClose={() => setExportDialogOpen(false)}>
        <DialogTitle>Export Your Data</DialogTitle>
        <DialogContent>
          <Typography>
            This will prepare a complete export of all your data including:
          </Typography>
          <List>
            <ListItem>Profile information</ListItem>
            <ListItem>Conversation history</ListItem>
            <ListItem>Health records</ListItem>
            <ListItem>Privacy settings</ListItem>
          </List>
          <Typography variant="body2" color="text.secondary">
            The export will be available for download within 24 hours.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setExportDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleDataExport} variant="contained">Export Data</Button>
        </DialogActions>
      </Dialog>

      {/* Delete Dialog */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Delete All Data</DialogTitle>
        <DialogContent>
          <Alert severity="warning" sx={{ mb: 2 }}>
            This action cannot be undone. All your data will be permanently deleted.
          </Alert>
          <Typography>
            This will delete:
          </Typography>
          <List>
            <ListItem>All conversation history</ListItem>
            <ListItem>Health records and analyses</ListItem>
            <ListItem>Profile information</ListItem>
            <ListItem>Privacy settings</ListItem>
          </List>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleDataDeletion} color="error" variant="contained">
            Delete All Data
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PrivacyDashboard;
