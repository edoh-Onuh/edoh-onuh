import React, { useEffect, useState, useCallback, forwardRef } from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { motion } from 'framer-motion';
import axios from 'axios';

// --- UTILITY ---
// This utility function is crucial for merging Tailwind CSS classes without conflicts.
// It's a best practice for building reusable and customizable components.
function cn(...inputs) {
  return twMerge(clsx(inputs));
}


// --- API SERVICE ---
// Centralizes all API calls for better organization and reusability.
const apiClient = axios.create({
  // FIX: Use an absolute URL for the backend API.
  // In a real-world application, this should be configured via environment variables.
  // For example: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/esport'
  baseURL: 'http://localhost:8000/api/esport',
  headers: {
    'Content-Type': 'application/json',
  },
});

const getMatches = (teamName = '') => {
  // The query parameter is added only if teamName is provided.
  return apiClient.get(`/matches${teamName ? `?team=${teamName}` : ''}`);
};

const getPlayerStats = () => {
  return apiClient.get('/player-stats');
};


//  Input Component (/components/ui/input.js)
// A styled input component that is consistent across the application.
const Input = forwardRef(({ className, type, ...props }, ref) => {
  return (
    <input
      type={type}
      className={cn(
        'flex h-10 w-full rounded-md border border-slate-300 bg-transparent px-3 py-2 text-sm ring-offset-white file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-slate-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-400 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-700 dark:text-slate-50 dark:ring-offset-slate-950 dark:placeholder:text-slate-400 dark:focus-visible:ring-slate-600',
        className
      )}
      ref={ref}
      {...props}
    />
  );
});
Input.displayName = "Input";
