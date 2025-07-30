// src/EsportDashboard.jsx
import React, { useEffect, useState, useCallback } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { motion } from 'framer-motion';
import * as api from './services/api'; // Import the API service

export default function EsportDashboard() {
  const [matches, setMatches] = useState([]);
  const [playerStats, setPlayerStats] = useState([]);
  const [team, setTeam] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchDashboardData = useCallback(async (teamName = '') => {
    setLoading(true);
    setError(null);
    try {
      // Use Promise.all to fetch data in parallel
      const [matchesRes, playerStatsRes] = await Promise.all([
        api.getMatches(teamName),
        api.getPlayerStats(),
      ]);
      setMatches(matchesRes.data);
      setPlayerStats(playerStatsRes.data);
    } catch (err) {
      console.error('Error fetching dashboard data', err);
      setError('Failed to load dashboard data. Please try again later.');
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
  
  return (
    <div className="grid gap-4 p-4">
      {/* Search and Title */}
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-bold mb-2">E-sport Data Analytics Dashboard</h1>
        <div className="flex gap-2">
          <Input 
            placeholder="Enter team name to filter"
            value={team}
            onChange={(e) => setTeam(e.target.value)}
          />
          <Button onClick={handleSearch} disabled={loading}>
            {loading ? 'Loading...' : 'Search'}
          </Button>
        </div>
      </motion.div>

      {/* Error Display */}
      {error && <Card className="shadow-lg rounded-lg bg-red-100 text-red-700"><CardContent><p className="p-4">{error}</p></CardContent></Card>}

      {/* Charts */}
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }}>
        {/* Match Performance Chart */}
        <Card className="shadow-xl rounded-2xl">
          <CardContent>
            <h2 className="text-xl font-semibold mb-4">Match Performance Over Time</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={matches}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="match_date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="team_score" stroke="#8884d8" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Player Stats Chart */}
        <Card className="shadow-xl rounded-2xl mt-4">
          <CardContent>
            <h2 className="text-xl font-semibold mb-4">Player Stats</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={playerStats}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="player_name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="kills" fill="#82ca9d" />
                <Bar dataKey="deaths" fill="#ff7f7f" />
                <Bar dataKey="assists" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}