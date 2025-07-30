import React, { useEffect, useState, useCallback, forwardRef } from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { 
  XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, 
  BarChart, Bar, PieChart, Pie, Cell, Legend, Area, AreaChart, ScatterChart, Scatter,
  ReferenceLine
} from 'recharts';
import { motion, AnimatePresence } from 'framer-motion';
import * as api from './services/api';
import LiveDataToggle from './components/LiveDataToggle';

// --- UTILITY ---
// This utility function is crucial for merging Tailwind CSS classes without conflicts.
function cn(...inputs) {
  return twMerge(clsx(inputs));
}


// --- UI COMPONENTS ---
// In a larger app, these would be in separate files (e.g., /components/ui/Button.js)

const Button = forwardRef(({ className, variant, size, ...props }, ref) => (
  <button
    className={cn(
      'inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
      {
        'bg-slate-900 text-slate-50 hover:bg-slate-900/90 dark:bg-slate-50 dark:text-slate-900 dark:hover:bg-slate-50/90': variant === 'default' || !variant,
        'border border-slate-200 bg-transparent hover:bg-slate-100 hover:text-slate-900 dark:border-slate-800 dark:hover:bg-slate-800 dark:hover:text-slate-50': variant === 'outline',
      },
      {
        'h-10 px-4 py-2': size === 'default' || !size,
        'h-9 rounded-md px-3': size === 'sm',
      },
      className
    )}
    ref={ref}
    {...props}
  />
));

const Input = forwardRef(({ className, type, ...props }, ref) => (
  <input
    type={type}
    className={cn(
      'flex h-10 w-full rounded-md border border-slate-300 bg-transparent px-3 py-2 text-sm ring-offset-white file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-slate-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-400 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-700 dark:text-slate-50 dark:ring-offset-slate-950 dark:placeholder:text-slate-400 dark:focus-visible:ring-slate-600',
      className
    )}
    ref={ref}
    {...props}
  />
));

const Card = forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('rounded-xl border border-slate-200 bg-white text-slate-950 shadow-sm dark:border-slate-800 dark:bg-slate-950 dark:text-slate-50', className)}
    {...props}
  />
));

const CardHeader = forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('flex flex-col space-y-1.5 p-6', className)} {...props} />
));

const CardTitle = forwardRef(({ className, children, ...props }, ref) => (
  <h3 ref={ref} className={cn('text-2xl font-semibold leading-none tracking-tight', className)} {...props}>
    {children}
  </h3>
));

const CardDescription = forwardRef(({ className, ...props }, ref) => (
  <p ref={ref} className={cn('text-sm text-slate-500 dark:text-slate-400', className)} {...props} />
));

const CardContent = forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('p-6 pt-0', className)} {...props} />
));

// --- MAIN APP COMPONENT ---
// Enhanced dashboard with robust visualizations and better UX
export default function App() {
  const [matches, setMatches] = useState([]);
  const [playerStats, setPlayerStats] = useState([]);
  const [heatmapData, setHeatmapData] = useState([]);
  const [team, setTeam] = useState('');
  const [player, setPlayer] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchType, setSearchType] = useState('team'); // 'team' or 'player'
  const [totalMatches, setTotalMatches] = useState(0);
  const [winRate, setWinRate] = useState(0);
  const [dataSource, setDataSource] = useState('sample'); // 'sample' or 'live'
  // eslint-disable-next-line no-unused-vars
  const [tournaments, setTournaments] = useState([]);
  // eslint-disable-next-line no-unused-vars
  const [analytics, setAnalytics] = useState(null);

  // Enhanced data processing functions
  const processMatchData = (matchData) => {
    if (!Array.isArray(matchData) || matchData.length === 0) return [];
    
    return matchData.map(match => ({
      ...match,
      match_date: new Date(match.match_date).toLocaleDateString(),
      team_score: match.score_team || 0,
      opponent_score: match.score_opponent || 0,
      win: match.result === 'win' ? 1 : 0,
      scoreMargin: (match.score_team || 0) - (match.score_opponent || 0)
    }));
  };

  const processPlayerData = (playerData) => {
    if (!Array.isArray(playerData) || playerData.length === 0) return [];
    
    return playerData.map(player => ({
      ...player,
      kda_ratio: player.kda_ratio || ((player.kills + player.assists) / Math.max(player.deaths, 1)),
      efficiency: ((player.kills * 2 + player.assists) / Math.max(player.deaths, 1))
    }));
  };

  const calculateStats = (matchData) => {
    if (!Array.isArray(matchData) || matchData.length === 0) {
      setTotalMatches(0);
      setWinRate(0);
      return;
    }
    
    const total = matchData.length;
    const wins = matchData.filter(match => match.result === 'win').length;
    const rate = total > 0 ? ((wins / total) * 100).toFixed(1) : 0;
    
    setTotalMatches(total);
    setWinRate(rate);
  };

  const fetchDashboardData = useCallback(async (searchValue = '', type = 'team') => {
    setLoading(true);
    setError(null);
    
    try {
      // Use the new unified API function
      const dashboardData = await api.getDashboardData({
        useLiveData: dataSource === 'live',
        team: type === 'team' ? searchValue : '',
        player: type === 'player' ? searchValue : '',
        limit: 50
      });
      
      console.log('Dashboard data received:', dashboardData);
      console.log('Data source:', dataSource, 'Live data:', dataSource === 'live');
      
      // Process and set the data
      const processedMatches = processMatchData(dashboardData.matches);
      const processedPlayers = processPlayerData(dashboardData.players);
      
      console.log('Processed matches:', processedMatches);
      console.log('Processed players:', processedPlayers);
      
      setMatches(processedMatches);
      setPlayerStats(processedPlayers);
      setTournaments(dashboardData.tournaments || []);
      setAnalytics(dashboardData.analytics);
      
      calculateStats(dashboardData.matches);
      
      // Try to get heatmap data (sample data endpoint)
      try {
        const heatmapRes = await api.getHeatmapData(
          type === 'team' ? searchValue : '',
          type === 'player' ? searchValue : ''
        );
        setHeatmapData(heatmapRes.data || []);
      } catch (heatmapError) {
        console.warn('Heatmap data not available:', heatmapError);
        setHeatmapData([]);
      }
      
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
      setError(`Failed to load ${dataSource} data. Please check the API and try again.`);
      
      // Fallback to sample data
      setMatches([
        { match_id: 1, match_date: '2025-07-01', team_score: 16, opponent_score: 10, result: 'win' },
        { match_id: 2, match_date: '2025-07-02', team_score: 12, opponent_score: 16, result: 'loss' },
        { match_id: 3, match_date: '2025-07-03', team_score: 16, opponent_score: 5, result: 'win' },
      ]);
      setPlayerStats([
        { player_id: 1, player_name: 'Player A', kills: 22, deaths: 15, assists: 7, kda_ratio: 1.9 },
        { player_id: 2, player_name: 'Player B', kills: 18, deaths: 18, assists: 10, kda_ratio: 1.6 },
        { player_id: 3, player_name: 'Player C', kills: 25, deaths: 12, assists: 5, kda_ratio: 2.5 },
      ]);
    } finally {
      setLoading(false);
    }
  }, [dataSource]);

  // Data source change handler
  const handleDataSourceChange = (useLiveData) => {
    setDataSource(useLiveData ? 'live' : 'sample');
  };

  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  const handleSearch = () => {
    const searchValue = searchType === 'team' ? team : player;
    fetchDashboardData(searchValue, searchType);
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  };

  const handleReset = () => {
    setTeam('');
    setPlayer('');
    fetchDashboardData('', searchType);
  };

  // Color schemes for charts
  const colors = {
    primary: '#3B82F6',
    secondary: '#10B981', 
    tertiary: '#F59E0B',
    danger: '#EF4444',
    success: '#22C55E',
    warning: '#F97316'
  };

  // eslint-disable-next-line no-unused-vars
  const pieColors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899'];

  // Custom tooltip components
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white dark:bg-slate-800 p-3 border border-slate-200 dark:border-slate-700 rounded-lg shadow-lg">
          <p className="font-medium">{`Date: ${label}`}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color }}>
              {`${entry.dataKey}: ${entry.value}`}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  const PlayerTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white dark:bg-slate-800 p-3 border border-slate-200 dark:border-slate-700 rounded-lg shadow-lg">
          <p className="font-medium">{`Player: ${label}`}</p>
          <p style={{ color: colors.success }}>{`Kills: ${data.kills}`}</p>
          <p style={{ color: colors.danger }}>{`Deaths: ${data.deaths}`}</p>
          <p style={{ color: colors.primary }}>{`Assists: ${data.assists}`}</p>
          <p style={{ color: colors.tertiary }}>{`KDA: ${data.kda_ratio?.toFixed(2)}`}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-950 dark:to-slate-900 text-slate-900 dark:text-slate-50">
      <div className="container mx-auto p-4 md:p-8">
        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
          <Card className="mb-6 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950/20 dark:to-indigo-950/20 border-blue-200 dark:border-blue-800">
            <CardHeader>
              <CardTitle className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                🎮 E-Sport Analytics Dashboard
              </CardTitle>
              <CardDescription className="text-lg">
                Advanced match analytics and player performance insights
              </CardDescription>
            </CardHeader>
          </Card>
        </motion.div>

        {/* Live Data Toggle Component */}
        <LiveDataToggle 
          onDataSourceChange={handleDataSourceChange}
          currentDataSource={dataSource}
        />

        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, delay: 0.1 }}>
          <Card className="mb-6">
            <CardContent>
              <div className="space-y-4">
                {/* Search Type Selector */}
                <div className="flex space-x-4 mb-4">
                  <Button
                    variant={searchType === 'team' ? 'default' : 'outline'}
                    onClick={() => setSearchType('team')}
                    className="flex-1"
                  >
                    🏆 Team Search
                  </Button>
                  <Button
                    variant={searchType === 'player' ? 'default' : 'outline'}
                    onClick={() => setSearchType('player')}
                    className="flex-1"
                  >
                    👤 Player Search
                  </Button>
                </div>
                
                {/* Search Input */}
                <div className="flex w-full items-center space-x-2">
                  <Input
                    placeholder={searchType === 'team' ? "Enter team name (e.g., TSM, Astralis)..." : "Enter player name (e.g., device, s1mple)..."}
                    value={searchType === 'team' ? team : player}
                    onChange={(e) => searchType === 'team' ? setTeam(e.target.value) : setPlayer(e.target.value)}
                    onKeyPress={handleKeyPress}
                    disabled={loading}
                    className="flex-1"
                  />
                  <Button onClick={handleSearch} disabled={loading} className="px-6">
                    {loading ? '🔄 Searching...' : '🔍 Search'}
                  </Button>
                  <Button onClick={handleReset} variant="outline" disabled={loading}>
                    🔄 Reset
                  </Button>
                </div>
                
                {/* Quick Stats */}
                {!loading && totalMatches > 0 && (
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
                    <div className="bg-blue-100 dark:bg-blue-900/30 rounded-lg p-3 text-center">
                      <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">{totalMatches}</div>
                      <div className="text-sm text-blue-600 dark:text-blue-400">Total Matches</div>
                    </div>
                    <div className="bg-green-100 dark:bg-green-900/30 rounded-lg p-3 text-center">
                      <div className="text-2xl font-bold text-green-600 dark:text-green-400">{winRate}%</div>
                      <div className="text-sm text-green-600 dark:text-green-400">Win Rate</div>
                    </div>
                    <div className="bg-purple-100 dark:bg-purple-900/30 rounded-lg p-3 text-center">
                      <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">{playerStats.length}</div>
                      <div className="text-sm text-purple-600 dark:text-purple-400">Players</div>
                    </div>
                    <div className="bg-orange-100 dark:bg-orange-900/30 rounded-lg p-3 text-center">
                      <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                        {playerStats.length > 0 ? (playerStats.reduce((sum, p) => sum + (p.kda_ratio || 0), 0) / playerStats.length).toFixed(1) : '0.0'}
                      </div>
                      <div className="text-sm text-orange-600 dark:text-orange-400">Avg KDA</div>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Error Display */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
            >
              <Card className="bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800/50 mb-6">
                <CardContent className="p-4">
                  <div className="flex items-center space-x-2">
                    <span className="text-red-500">⚠️</span>
                    <p className="text-sm font-medium text-red-600 dark:text-red-400">{error}</p>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Loading State */}
        {loading ? (
          <div className="flex flex-col items-center justify-center p-20">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
              className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full mb-4"
            />
            <p className="text-lg font-medium">Loading dashboard data...</p>
          </div>
        ) : (
          <div className="grid gap-6">
            {/* Match Performance Charts Row */}
            <div className="grid gap-6 lg:grid-cols-2">
              {/* Enhanced Match Performance Over Time */}
              <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.2, duration: 0.5 }}>
                <Card className="h-full">
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <span>📊</span>
                      <span>Match Performance Timeline</span>
                    </CardTitle>
                    <CardDescription>Score trends and performance over time</CardDescription>
                  </CardHeader>
                  <CardContent>
                    {matches.length > 0 ? (
                      <ResponsiveContainer width="100%" height={350}>
                        <AreaChart data={matches}>
                          <defs>
                            <linearGradient id="teamScore" x1="0" y1="0" x2="0" y2="1">
                              <stop offset="5%" stopColor={colors.primary} stopOpacity={0.8}/>
                              <stop offset="95%" stopColor={colors.primary} stopOpacity={0.1}/>
                            </linearGradient>
                            <linearGradient id="opponentScore" x1="0" y1="0" x2="0" y2="1">
                              <stop offset="5%" stopColor={colors.danger} stopOpacity={0.8}/>
                              <stop offset="95%" stopColor={colors.danger} stopOpacity={0.1}/>
                            </linearGradient>
                          </defs>
                          <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                          <XAxis dataKey="match_date" stroke="#6B7280" fontSize={12} />
                          <YAxis stroke="#6B7280" fontSize={12} />
                          <Tooltip content={<CustomTooltip />} />
                          <Legend />
                          <Area type="monotone" dataKey="team_score" stroke={colors.primary} fillOpacity={1} fill="url(#teamScore)" name="Team Score" />
                          <Area type="monotone" dataKey="opponent_score" stroke={colors.danger} fillOpacity={1} fill="url(#opponentScore)" name="Opponent Score" />
                          <ReferenceLine y={15} stroke="#F59E0B" strokeDasharray="8 8" label="Average Score" />
                        </AreaChart>
                      </ResponsiveContainer>
                    ) : (
                      <div className="flex flex-col items-center justify-center h-[350px] text-slate-500">
                        <span className="text-4xl mb-2">📈</span>
                        <p>No match data available</p>
                        <p className="text-sm">Try searching for a team</p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </motion.div>

              {/* Win/Loss Distribution */}
              <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3, duration: 0.5 }}>
                <Card className="h-full">
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <span>🎯</span>
                      <span>Win/Loss Distribution</span>
                    </CardTitle>
                    <CardDescription>Match outcome breakdown</CardDescription>
                  </CardHeader>
                  <CardContent>
                    {matches.length > 0 ? (
                      <ResponsiveContainer width="100%" height={350}>
                        <PieChart>
                          <Pie
                            data={[
                              { name: 'Wins', value: matches.filter(m => m.result === 'win').length, fill: colors.success },
                              { name: 'Losses', value: matches.filter(m => m.result === 'loss').length, fill: colors.danger },
                              { name: 'Draws', value: matches.filter(m => m.result === 'draw').length, fill: colors.warning }
                            ].filter(item => item.value > 0)}
                            cx="50%"
                            cy="50%"
                            labelLine={false}
                            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                            outerRadius={120}
                            fill="#8884d8"
                            dataKey="value"
                          >
                            {[
                              { name: 'Wins', value: matches.filter(m => m.result === 'win').length, fill: colors.success },
                              { name: 'Losses', value: matches.filter(m => m.result === 'loss').length, fill: colors.danger },
                              { name: 'Draws', value: matches.filter(m => m.result === 'draw').length, fill: colors.warning }
                            ].filter(item => item.value > 0).map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={entry.fill} />
                            ))}
                          </Pie>
                          <Tooltip />
                          <Legend />
                        </PieChart>
                      </ResponsiveContainer>
                    ) : (
                      <div className="flex flex-col items-center justify-center h-[350px] text-slate-500">
                        <span className="text-4xl mb-2">🎯</span>
                        <p>No match outcomes to display</p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </motion.div>
            </div>

            {/* Player Statistics Row */}
            <div className="grid gap-6 lg:grid-cols-2">
              {/* Enhanced Player KDA Stats */}
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4, duration: 0.5 }}>
                <Card className="h-full">
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <span>⚔️</span>
                      <span>Player KDA Performance</span>
                    </CardTitle>
                    <CardDescription>Kills, Deaths, and Assists breakdown</CardDescription>
                  </CardHeader>
                  <CardContent>
                    {playerStats.length > 0 ? (
                      <ResponsiveContainer width="100%" height={400}>
                        <BarChart data={playerStats.slice(0, 10)} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
                          <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                          <XAxis 
                            dataKey="player_name" 
                            stroke="#6B7280" 
                            fontSize={11}
                            angle={-45}
                            textAnchor="end"
                            height={80}
                          />
                          <YAxis stroke="#6B7280" fontSize={12} />
                          <Tooltip content={<PlayerTooltip />} />
                          <Legend />
                          <Bar dataKey="kills" fill={colors.success} name="Kills" radius={[2, 2, 0, 0]} />
                          <Bar dataKey="deaths" fill={colors.danger} name="Deaths" radius={[2, 2, 0, 0]} />
                          <Bar dataKey="assists" fill={colors.primary} name="Assists" radius={[2, 2, 0, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    ) : (
                      <div className="flex flex-col items-center justify-center h-[400px] text-slate-500">
                        <span className="text-4xl mb-2">⚔️</span>
                        <p>No player statistics available</p>
                        <p className="text-sm">Try searching for a player or team</p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </motion.div>

              {/* Player Efficiency Scatter Plot */}
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.5, duration: 0.5 }}>
                <Card className="h-full">
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <span>💎</span>
                      <span>Player Efficiency Analysis</span>
                    </CardTitle>
                    <CardDescription>KDA Ratio vs Overall Efficiency</CardDescription>
                  </CardHeader>
                  <CardContent>
                    {playerStats.length > 0 ? (
                      <ResponsiveContainer width="100%" height={400}>
                        <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                          <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                          <XAxis dataKey="kda_ratio" name="KDA Ratio" stroke="#6B7280" fontSize={12} />
                          <YAxis dataKey="efficiency" name="Efficiency" stroke="#6B7280" fontSize={12} />
                          <Tooltip cursor={{ strokeDasharray: '3 3' }} content={<PlayerTooltip />} />
                          <Scatter 
                            name="Players" 
                            data={playerStats} 
                            fill={colors.secondary}
                            stroke={colors.primary}
                            strokeWidth={2}
                          />
                          <ReferenceLine x={1.0} stroke={colors.warning} strokeDasharray="5 5" label="Avg KDA" />
                          <ReferenceLine y={2.0} stroke={colors.warning} strokeDasharray="5 5" label="Avg Efficiency" />
                        </ScatterChart>
                      </ResponsiveContainer>
                    ) : (
                      <div className="flex flex-col items-center justify-center h-[400px] text-slate-500">
                        <span className="text-4xl mb-2">💎</span>
                        <p>No efficiency data available</p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </motion.div>
            </div>

            {/* Additional Analytics Row */}
            {heatmapData.length > 0 && (
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.6, duration: 0.5 }}>
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <span>🗺️</span>
                      <span>Position Heatmap Data</span>
                    </CardTitle>
                    <CardDescription>Player positioning frequency analysis</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={heatmapData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                        <XAxis dataKey="position" stroke="#6B7280" fontSize={12} />
                        <YAxis stroke="#6B7280" fontSize={12} />
                        <Tooltip />
                        <Bar dataKey="frequency" fill={colors.tertiary} radius={[4, 4, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>
              </motion.div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}
