import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './contexts/AuthContext';
import theme from './theme/theme';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import ChatPage from './pages/ChatPage';
import SymptomCheckerPage from './pages/SymptomCheckerPage';
import SecondOpinionPage from './pages/SecondOpinionPage';
import LabAnalysisPage from './pages/LabAnalysisPage';
import DashboardPage from './pages/DashboardPage';
import ProfilePage from './pages/ProfilePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <AuthProvider>
            <Layout>
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/chat" element={<ChatPage />} />
                <Route path="/symptom-checker" element={<SymptomCheckerPage />} />
                <Route path="/second-opinion" element={<SecondOpinionPage />} />
                <Route path="/lab-analysis" element={<LabAnalysisPage />} />
                <Route path="/dashboard" element={<DashboardPage />} />
                <Route path="/profile" element={<ProfilePage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
              </Routes>
            </Layout>
          </AuthProvider>
        </Router>
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
            success: {
              duration: 3000,
              theme: {
                primary: '#4aed88',
              },
            },
          }}
        />
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
