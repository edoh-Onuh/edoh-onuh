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


// Button Component (/components/ui/button.js)
// A highly reusable button with variants for different styles and states.
const Button = forwardRef(({ className, variant, size, asChild = false, ...props }, ref) => {
  const Comp = asChild ? "div" : "button";
  
  // Using class-variance-authority (cva) pattern for defining variants
  const buttonVariants = {
    base: 'inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
    variants: {
      variant: {
        default: 'bg-slate-900 text-slate-50 hover:bg-slate-900/90 dark:bg-slate-50 dark:text-slate-900 dark:hover:bg-slate-50/90',
        destructive: 'bg-red-500 text-slate-50 hover:bg-red-500/90 dark:bg-red-900 dark:text-slate-50 dark:hover:bg-red-900/90',
        outline: 'border border-slate-200 bg-transparent hover:bg-slate-100 hover:text-slate-900 dark:border-slate-800 dark:hover:bg-slate-800 dark:hover:text-slate-50',
        secondary: 'bg-slate-100 text-slate-900 hover:bg-slate-100/80 dark:bg-slate-800 dark:text-slate-50 dark:hover:bg-slate-800/80',
        ghost: 'hover:bg-slate-100 hover:text-slate-900 dark:hover:bg-slate-800 dark:hover:text-slate-50',
        link: 'text-slate-900 underline-offset-4 hover:underline dark:text-slate-50',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  };

  return (
    <Comp
      className={cn(buttonVariants.base, buttonVariants.variants.variant[variant || 'default'], buttonVariants.variants.size[size || 'default'], className)}
      ref={ref}
      {...props}
    />
  );
});
Button.displayName = "Button";
