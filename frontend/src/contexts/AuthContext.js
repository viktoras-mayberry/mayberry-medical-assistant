import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../services/api';
import toast from 'react-hot-toast';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('access_token');
    if (token) {
      // Verify token and get user profile
      authAPI.getProfile()
        .then(response => {
          setUser(response.data);
          setIsAuthenticated(true);
        })
        .catch(() => {
          localStorage.removeItem('access_token');
        })
        .finally(() => {
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (credentials) => {
    try {
      setLoading(true);
      const response = await authAPI.login(credentials);
      const { access_token } = response.data;
      
      localStorage.setItem('access_token', access_token);
      
      // Get user profile
      const profileResponse = await authAPI.getProfile();
      setUser(profileResponse.data);
      setIsAuthenticated(true);
      
      toast.success('Successfully logged in!');
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Login failed';
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData) => {
    try {
      setLoading(true);
      await authAPI.register(userData);
      toast.success('Account created successfully! Please log in.');
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Registration failed';
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
    setIsAuthenticated(false);
    toast.success('Successfully logged out!');
  };

  const value = {
    user,
    loading,
    isAuthenticated,
    login,
    register,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
