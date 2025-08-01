import React, { useState } from 'react';
import {
  Container,
  Typography,
  Paper,
  TextField,
  Button,
  Box,
  Alert,
  CircularProgress,
  Link as MuiLink,
  InputAdornment,
  IconButton,
  FormControlLabel,
  Checkbox,
} from '@mui/material';
import {
  PersonAdd,
  Email,
  Lock,
  Person,
  Visibility,
  VisibilityOff,
} from '@mui/icons-material';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useForm } from 'react-hook-form';

const RegisterPage = () => {
  const navigate = useNavigate();
  const { register: registerUser, loading } = useAuth();
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm();

  const password = watch('password');

  const onSubmit = async (data) => {
    setError('');
    setSuccess(false);
    
    const { confirmPassword, agreeToTerms, ...userData } = data;
    
    if (!agreeToTerms) {
      setError('You must agree to the terms and conditions');
      return;
    }
    
    const result = await registerUser(userData);
    if (result.success) {
      setSuccess(true);
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } else {
      setError(result.error);
    }
  };

  const handleTogglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const handleToggleConfirmPasswordVisibility = () => {
    setShowConfirmPassword(!showConfirmPassword);
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8, mb: 4 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Box sx={{ textAlign: 'center', mb: 3 }}>
            <PersonAdd sx={{ fontSize: 60, color: 'secondary.main', mb: 2 }} />
            <Typography variant="h4" component="h1" sx={{ mb: 1 }}>
              Create Account
            </Typography>
            <Typography variant="body1" sx={{ color: 'text.secondary' }}>
              Join MAYBERRY for personalized healthcare guidance
            </Typography>
          </Box>

          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          {success && (
            <Alert severity="success" sx={{ mb: 3 }}>
              Account created successfully! Redirecting to login...
            </Alert>
          )}

          <Box component="form" onSubmit={handleSubmit(onSubmit)}>
            <TextField
              fullWidth
              label="Full Name"
              margin="normal"
              {...register('full_name', {
                required: 'Full name is required',
                minLength: {
                  value: 2,
                  message: 'Name must be at least 2 characters',
                },
              })}
              error={!!errors.full_name}
              helperText={errors.full_name?.message}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Person color="action" />
                  </InputAdornment>
                ),
              }}
            />

            <TextField
              fullWidth
              label="Email Address"
              type="email"
              margin="normal"
              {...register('email', {
                required: 'Email is required',
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                  message: 'Invalid email address',
                },
              })}
              error={!!errors.email}
              helperText={errors.email?.message}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Email color="action" />
                  </InputAdornment>
                ),
              }}
            />

            <TextField
              fullWidth
              label="Password"
              type={showPassword ? 'text' : 'password'}
              margin="normal"
              {...register('password', {
                required: 'Password is required',
                minLength: {
                  value: 8,
                  message: 'Password must be at least 8 characters',
                },
                pattern: {
                  value: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$/,
                  message: 'Password must contain at least one uppercase letter, one lowercase letter, and one number',
                },
              })}
              error={!!errors.password}
              helperText={errors.password?.message}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Lock color="action" />
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="toggle password visibility"
                      onClick={handleTogglePasswordVisibility}
                      edge="end"
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />

            <TextField
              fullWidth
              label="Confirm Password"
              type={showConfirmPassword ? 'text' : 'password'}
              margin="normal"
              {...register('confirmPassword', {
                required: 'Please confirm your password',
                validate: (value) =>
                  value === password || 'Passwords do not match',
              })}
              error={!!errors.confirmPassword}
              helperText={errors.confirmPassword?.message}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Lock color="action" />
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="toggle confirm password visibility"
                      onClick={handleToggleConfirmPasswordVisibility}
                      edge="end"
                    >
                      {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />

            <FormControlLabel
              control={
                <Checkbox
                  {...register('agreeToTerms', {
                    required: 'You must agree to the terms and conditions',
                  })}
                  color="primary"
                />
              }
              label={
                <Typography variant="body2">
                  I agree to the{' '}
                  <MuiLink href="#" sx={{ color: 'primary.main' }}>
                    Terms of Service
                  </MuiLink>{' '}
                  and{' '}
                  <MuiLink href="#" sx={{ color: 'primary.main' }}>
                    Privacy Policy
                  </MuiLink>
                </Typography>
              }
              sx={{ mt: 2, alignItems: 'flex-start' }}
            />
            {errors.agreeToTerms && (
              <Typography variant="caption" color="error" sx={{ ml: 2 }}>
                {errors.agreeToTerms.message}
              </Typography>
            )}

            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={loading || success}
              sx={{ mt: 3, mb: 2, py: 1.5 }}
            >
              {loading ? (
                <CircularProgress size={24} color="inherit" />
              ) : (
                'Create Account'
              )}
            </Button>

            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                Already have an account?{' '}
                <MuiLink
                  component={Link}
                  to="/login"
                  sx={{ color: 'primary.main', textDecoration: 'none' }}
                >
                  Sign in here
                </MuiLink>
              </Typography>
            </Box>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default RegisterPage;
