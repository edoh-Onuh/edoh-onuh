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


//  Card Component (/components/ui/card.js)
// A set of composable components to build flexible card layouts.
const Card = forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('rounded-xl border border-slate-200 bg-white text-slate-950 shadow-sm dark:border-slate-800 dark:bg-slate-950 dark:text-slate-50', className)}
    {...props}
  />
));
Card.displayName = "Card";

const CardHeader = forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('flex flex-col space-y-1.5 p-6', className)} {...props} />
));
CardHeader.displayName = "CardHeader";

const CardTitle = forwardRef(({ className, ...props }, ref) => (
  <h3 ref={ref} className={cn('text-2xl font-semibold leading-none tracking-tight', className)} {...props} />
));
CardTitle.displayName = "CardTitle";

const CardDescription = forwardRef(({ className, ...props }, ref) => (
  <p ref={ref} className={cn('text-sm text-slate-500 dark:text-slate-400', className)} {...props} />
));
CardDescription.displayName = "CardDescription";

const CardContent = forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('p-6 pt-0', className)} {...props} />
));
CardContent.displayName = "CardContent";

const CardFooter = forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('flex items-center p-6 pt-0', className)} {...props} />
));
CardFooter.displayName = "CardFooter";


// --- DASHBOARD COMPONENT ---
// The main dashboard view, now using the robust UI components.
function EsportDashboard() {
  const [matches, setMatches] = useState([]);
  const [playerStats, setPlayerStats] = useState([]);
  const [team, setTeam] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchDashboardData = useCallback(async (teamName = '') => {
    setLoading(true);
    setError(null);
    try {
      const [matchesRes, playerStatsRes] = await Promise.all([
        getMatches(teamName),
        getPlayerStats(),
      ]);
      // Mock data for demonstration as API is not live
      setMatches(matchesRes.data.length > 0 ? matchesRes.data : [
          { match_date: '2025-07-01', team_score: 16, opponent_score: 10 },
          { match_date: '2025-07-02', team_score: 12, opponent_score: 16 },
          { match_date: '2025-07-03', team_score: 16, opponent_score: 5 },
      ]);
      setPlayerStats(playerStatsRes.data.length > 0 ? playerStatsRes.data : [
          { player_name: 'Player A', kills: 22, deaths: 15, assists: 7 },
          { player_name: 'Player B', kills: 18, deaths: 18, assists: 10 },
          { player_name: 'Player C', kills: 25, deaths: 12, assists: 5 },
      ]);
    } catch (err) {
      console.error('Error fetching dashboard data', err);
      setError('Failed to load dashboard data. Please check the API and try again.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  const handleSearch = () => {
    fetchDashboardData(team);
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="container mx-auto p-4 md:p-8">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>E-sport Data Analytics Dashboard</CardTitle>
            <CardDescription>Filter match history and view player statistics.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex w-full max-w-sm items-center space-x-2">
              <Input 
                placeholder="Enter team name to filter"
                value={team}
                onChange={(e) => setTeam(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={loading}
              />
              <Button onClick={handleSearch} disabled={loading}>
                {loading ? 'Searching...' : 'Search'}
              </Button>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {error && (
        <Card className="bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800/50 mb-6">
            <CardContent className="p-4">
                <p className="text-sm font-medium text-red-600 dark:text-red-400">{error}</p>
            </CardContent>
        </Card>
      )}

      {loading ? (
         <div className="text-center p-10">Loading dashboard...</div>
      ) : (
        <div className="grid gap-6 lg:grid-cols-2">
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2, duration: 0.5 }}>
            <Card>
              <CardHeader>
                <CardTitle>Match Performance Over Time</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={matches}>
                    <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--muted))" />
                    <XAxis dataKey="match_date" stroke="hsl(var(--muted-foreground))" />
                    <YAxis stroke="hsl(var(--muted-foreground))" />
                    <Tooltip contentStyle={{ backgroundColor: 'hsl(var(--background))', border: '1px solid hsl(var(--border))' }} />
                    <Line type="monotone" dataKey="team_score" stroke="hsl(var(--primary))" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.4, duration: 0.5 }}>
            <Card>
              <CardHeader>
                <CardTitle>Player Stats (KDA)</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={playerStats}>
                    <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--muted))" />
                    <XAxis dataKey="player_name" stroke="hsl(var(--muted-foreground))" />
                    <YAxis stroke="hsl(var(--muted-foreground))" />
                    <Tooltip contentStyle={{ backgroundColor: 'hsl(var(--background))', border: '1px solid hsl(var(--border))' }} />
                    <Bar dataKey="kills" fill="#4ade80" />
                    <Bar dataKey="deaths" fill="#f87171" />
                    <Bar dataKey="assists" fill="#60a5fa" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      )}
    </div>
  );
}
