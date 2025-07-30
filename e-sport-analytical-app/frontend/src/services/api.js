// src/services/api.js
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || 'http://127.0.0.1:8001/api/esport',
  headers: {
    'Content-Type': 'application/json',
  },
});

// ===============================
// Original Sample Data Endpoints
// ===============================

// Complete sample datasets
const SAMPLE_MATCHES = [
  {
    id: 1,
    team_name: "TSM",
    opponent_name: "Astralis",
    match_date: "2025-07-28",
    score_team: 16,
    score_opponent: 14,
    result: "win",
    tournament: "ESL Pro League"
  },
  {
    id: 2,
    team_name: "NAVI", 
    opponent_name: "G2 Esports",
    match_date: "2025-07-27",
    score_team: 15,
    score_opponent: 19,
    result: "loss",
    tournament: "BLAST Premier"
  },
  {
    id: 3,
    team_name: "FaZe",
    opponent_name: "Vitality",
    match_date: "2025-07-26", 
    score_team: 19,
    score_opponent: 16,
    result: "win",
    tournament: "IEM Cologne"
  },
  {
    id: 4,
    team_name: "Astralis",
    opponent_name: "TSM",
    match_date: "2025-07-25",
    score_team: 14,
    score_opponent: 16,
    result: "loss",
    tournament: "ESL Pro League"
  },
  {
    id: 5,
    team_name: "G2 Esports",
    opponent_name: "FaZe",
    match_date: "2025-07-24",
    score_team: 16,
    score_opponent: 12,
    result: "win",
    tournament: "BLAST Premier"
  },
  {
    id: 6,
    team_name: "Vitality",
    opponent_name: "NAVI",
    match_date: "2025-07-23",
    score_team: 16,
    score_opponent: 8,
    result: "win",
    tournament: "IEM Cologne"
  }
];

const SAMPLE_PLAYERS = [
  {
    player_id: 1,
    player_name: "s1mple",
    team_name: "NAVI",
    kills: 1245,
    deaths: 892,
    assists: 567,
    kda_ratio: 2.03,
    headshot_percentage: 52.4,
    adr: 89.2
  },
  {
    player_id: 2,
    player_name: "ZywOo",
    team_name: "Vitality",
    kills: 1189,
    deaths: 856,
    assists: 612,
    kda_ratio: 2.10,
    headshot_percentage: 54.1,
    adr: 91.5
  },
  {
    player_id: 3,
    player_name: "device",
    team_name: "Astralis",
    kills: 1034,
    deaths: 789,
    assists: 489,
    kda_ratio: 1.93,
    headshot_percentage: 49.8,
    adr: 85.7
  },
  {
    player_id: 4,
    player_name: "FalleN",
    team_name: "TSM",
    kills: 987,
    deaths: 723,
    assists: 456,
    kda_ratio: 2.00,
    headshot_percentage: 48.3,
    adr: 82.1
  },
  {
    player_id: 5,
    player_name: "NiKo",
    team_name: "G2 Esports",
    kills: 1156,
    deaths: 801,
    assists: 534,
    kda_ratio: 2.11,
    headshot_percentage: 51.7,
    adr: 87.4
  },
  {
    player_id: 6,
    player_name: "rain",
    team_name: "FaZe",
    kills: 1023,
    deaths: 834,
    assists: 498,
    kda_ratio: 1.82,
    headshot_percentage: 47.2,
    adr: 79.8
  }
];

export const getMatches = (teamName = '') => {
  const params = teamName ? `?team=${encodeURIComponent(teamName)}` : '';
  console.log('🔍 Calling backend API:', `/matches/${params}`);
  
  return apiClient.get(`/matches/${params}`).then(response => {
    console.log('✅ Backend API response for matches:', response.data);
    return response;
  }).catch(error => {
    console.error('❌ Backend API failed for matches:', error);
    console.warn('Sample matches API failed, using fallback data for team:', teamName);
    
    // Filter matches based on team name
    let filteredMatches = SAMPLE_MATCHES;
    if (teamName) {
      filteredMatches = SAMPLE_MATCHES.filter(match => 
        match.team_name.toLowerCase().includes(teamName.toLowerCase()) ||
        match.opponent_name.toLowerCase().includes(teamName.toLowerCase())
      );
    }
    
    console.log('Filtered matches for', teamName, ':', filteredMatches);
    return { data: filteredMatches };
  });
};

export const getPlayerStats = (playerName = '') => {
  const params = playerName ? `?player_name=${encodeURIComponent(playerName)}` : '';
  console.log('🔍 Calling backend API:', `/player-stats/${params}`);
  
  return apiClient.get(`/player-stats/${params}`).then(response => {
    console.log('✅ Backend API response for player stats:', response.data);
    return response;
  }).catch(error => {
    console.error('❌ Backend API failed for player stats:', error);
    console.warn('Sample player stats API failed, using fallback data for player:', playerName);
    
    // Filter players based on player name or team name
    let filteredPlayers = SAMPLE_PLAYERS;
    if (playerName) {
      filteredPlayers = SAMPLE_PLAYERS.filter(player => 
        player.player_name.toLowerCase().includes(playerName.toLowerCase()) ||
        player.team_name.toLowerCase().includes(playerName.toLowerCase())
      );
    }
    
    console.log('Filtered players for', playerName, ':', filteredPlayers);
    return { data: filteredPlayers };
  });
};

// Team/Player-specific heatmap data
const SAMPLE_HEATMAP_DATA = {
  'TSM': [
    { x: 15, y: 25, frequency: 12 },
    { x: 20, y: 30, frequency: 8 },
    { x: 25, y: 15, frequency: 15 },
    { x: 30, y: 35, frequency: 10 },
    { x: 18, y: 22, frequency: 6 }
  ],
  'NAVI': [
    { x: 12, y: 28, frequency: 18 },
    { x: 22, y: 32, frequency: 14 },
    { x: 28, y: 18, frequency: 11 },
    { x: 35, y: 25, frequency: 9 },
    { x: 16, y: 35, frequency: 7 }
  ],
  'Astralis': [
    { x: 18, y: 20, frequency: 10 },
    { x: 25, y: 28, frequency: 13 },
    { x: 30, y: 22, frequency: 16 },
    { x: 14, y: 30, frequency: 8 },
    { x: 22, y: 18, frequency: 12 }
  ],
  'FaZe': [
    { x: 20, y: 15, frequency: 14 },
    { x: 28, y: 25, frequency: 11 },
    { x: 32, y: 30, frequency: 9 },
    { x: 16, y: 28, frequency: 13 },
    { x: 24, y: 20, frequency: 8 }
  ],
  'G2 Esports': [
    { x: 14, y: 22, frequency: 15 },
    { x: 26, y: 18, frequency: 12 },
    { x: 30, y: 28, frequency: 10 },
    { x: 18, y: 32, frequency: 9 },
    { x: 22, y: 25, frequency: 11 }
  ],
  'Vitality': [
    { x: 16, y: 18, frequency: 13 },
    { x: 24, y: 32, frequency: 16 },
    { x: 28, y: 20, frequency: 14 },
    { x: 32, y: 26, frequency: 8 },
    { x: 20, y: 28, frequency: 12 }
  ],
  'default': [
    { x: 10, y: 20, frequency: 5 },
    { x: 15, y: 25, frequency: 8 },
    { x: 20, y: 30, frequency: 12 },
    { x: 25, y: 35, frequency: 6 },
    { x: 18, y: 28, frequency: 9 }
  ]
};

export const getHeatmapData = (teamName = '', playerName = '') => {
  const params = new URLSearchParams();
  if (teamName) params.append('team', teamName);
  if (playerName) params.append('player', playerName);
  
  return apiClient.get(`/position-heatmap/?${params.toString()}`).catch(error => {
    console.warn('Heatmap API failed, using fallback data for:', teamName || playerName || 'default');
    
    // Determine which heatmap data to use
    let heatmapData = SAMPLE_HEATMAP_DATA['default'];
    
    if (teamName) {
      heatmapData = SAMPLE_HEATMAP_DATA[teamName] || SAMPLE_HEATMAP_DATA['default'];
    } else if (playerName) {
      // Find player's team and use that team's heatmap
      const player = SAMPLE_PLAYERS.find(p => 
        p.player_name.toLowerCase().includes(playerName.toLowerCase())
      );
      if (player) {
        heatmapData = SAMPLE_HEATMAP_DATA[player.team_name] || SAMPLE_HEATMAP_DATA['default'];
      }
    }
    
    return { data: heatmapData };
  });
};

export const getPrediction = (teamName) => {
  const params = teamName ? `?team=${encodeURIComponent(teamName)}` : '';
  return apiClient.get(`/predict/${params}`).catch(error => {
    console.warn('Prediction API failed, using fallback data');
    return {
      data: {
        team: teamName || "TSM",
        win_probability: 0.72,
        confidence: 0.85,
        prediction: "win"
      }
    };
  });
};

// ===============================
// NEW: Live Data API Endpoints
// ===============================

// Live Matches from Real E-Sports APIs
export const getLiveMatches = (game = null, limit = 50, forceRefresh = false) => {
  const params = new URLSearchParams();
  if (game) params.append('game', game);
  params.append('limit', limit);
  if (forceRefresh) params.append('force_refresh', 'true');
  
  return apiClient.get(`/live/matches/live?${params.toString()}`).catch(error => {
    console.warn('Live matches API failed, using mock data');
    return { data: generateMockMatches(limit) };
  });
};

// Live Player Statistics from Real E-Sports APIs
export const getLivePlayerStats = (game = null, playerId = null, limit = 50, forceRefresh = false) => {
  const params = new URLSearchParams();
  if (game) params.append('game', game);
  if (playerId) params.append('player_id', playerId);
  params.append('limit', limit);
  if (forceRefresh) params.append('force_refresh', 'true');
  
  return apiClient.get(`/live/players/live?${params.toString()}`).catch(error => {
    console.warn('Live player stats API failed, using mock data');
    return { data: generateMockPlayers(limit) };
  });
};

// Live Tournament Data
export const getLiveTournaments = (game = null, status = 'upcoming', limit = 20) => {
  const params = new URLSearchParams();
  if (game) params.append('game', game);
  params.append('status', status);
  params.append('limit', limit);
  
  return apiClient.get(`/live/tournaments?${params.toString()}`).catch(error => {
    console.warn('Live tournaments API failed, using mock data');
    return { data: generateMockTournaments() };
  });
};

// API Status and Health Check
export const getApiStatus = () => {
  return apiClient.get('/live/status').catch(error => {
    console.warn('API status check failed, using mock status');
    return {
      data: {
        apis_available: [
          {"name": "Mock Data", "game": "All", "status": "active"}
        ],
        service_status: "mock_data"
      }
    };
  });
};

// Supported Games Information
export const getSupportedGames = () => {
  return apiClient.get('/live/games/supported');
};

// Trending Analytics
export const getTrendingAnalytics = (game = null, timeframe = '24h') => {
  const params = new URLSearchParams();
  if (game) params.append('game', game);
  params.append('timeframe', timeframe);
  
  return apiClient.get(`/live/analytics/trends?${params.toString()}`).catch(error => {
    console.warn('Analytics API failed, using mock data');
    return { data: generateMockAnalytics() };
  });
};

// Trigger Data Sync
export const triggerDataSync = (force = false) => {
  const params = force ? '?force=true' : '';
  return apiClient.post(`/live/sync${params}`);
};

// Health Check
export const healthCheck = () => {
  return apiClient.get('/live/health');
};

// ===============================
// Game-Specific API Functions
// ===============================

// CS:GO specific data
export const getCSGOMatches = (limit = 50, forceRefresh = false) => {
  return getLiveMatches('csgo', limit, forceRefresh);
};

export const getCSGOPlayerStats = (playerId = null, limit = 50, forceRefresh = false) => {
  return getLivePlayerStats('csgo', playerId, limit, forceRefresh);
};

// Valorant specific data
export const getValorantMatches = (limit = 50, forceRefresh = false) => {
  return getLiveMatches('valorant', limit, forceRefresh);
};

export const getValorantLeaderboard = (limit = 50, forceRefresh = false) => {
  return getLivePlayerStats('valorant', null, limit, forceRefresh);
};

// Dota 2 specific data
export const getDota2Matches = (limit = 50, forceRefresh = false) => {
  return getLiveMatches('dota2', limit, forceRefresh);
};

export const getDota2PlayerStats = (playerId = null, limit = 50, forceRefresh = false) => {
  return getLivePlayerStats('dota2', playerId, limit, forceRefresh);
};

// ===============================
// Utility Functions
// ===============================

// Check if live data APIs are available
export const checkLiveDataAvailability = async () => {
  try {
    const response = await getApiStatus();
    return {
      available: true,
      status: response.data
    };
  } catch (error) {
    // If API is not available, still allow live data mode with mock data
    return {
      available: true,
      status: {
        apis_available: [
          {"name": "Mock Data", "game": "All", "status": "active"}
        ],
        service_status: "mock_data"
      },
      fallback: true
    };
  }
};

// Get all available data for dashboard
export const getDashboardData = async (options = {}) => {
  const {
    useLiveData = false,
    game = null,
    team = '',
    player = '',
    limit = 50
  } = options;

  try {
    if (useLiveData) {
      // Try to fetch from live APIs, but fall back to mock data if they fail
      try {
        const [matchesRes, playersRes, tournamentsRes, analyticsRes] = await Promise.all([
          getLiveMatches(game, limit),
          getLivePlayerStats(game, player || null, limit),
          getLiveTournaments(game),
          getTrendingAnalytics(game)
        ]);

        return {
          matches: matchesRes.data,
          players: playersRes.data,
          tournaments: tournamentsRes.data,
          analytics: analyticsRes.data,
          dataSource: 'live'
        };
      } catch (liveError) {
        console.warn('Live APIs failed, using mock data:', liveError);
        // Return mock live data
        return {
          matches: generateMockMatches(limit),
          players: generateMockPlayers(limit),
          tournaments: generateMockTournaments(),
          analytics: generateMockAnalytics(),
          dataSource: 'mock'
        };
      }
    } else {
      // Fetch from sample data
      try {
        const [matchesRes, playersRes] = await Promise.all([
          getMatches(team),
          getPlayerStats(player)
        ]);

        console.log('Raw API responses:', { matchesRes, playersRes, team, player });
        
        // Check if we got meaningful data, otherwise use fallback
        const hasMatches = matchesRes.data && matchesRes.data.length > 0;
        const hasPlayers = playersRes.data && playersRes.data.length > 0;
        
        if (!hasMatches && !hasPlayers) {
          console.log('No data from APIs, using comprehensive fallback');
          throw new Error('No data returned from APIs');
        }

        return {
          matches: matchesRes.data || [],
          players: playersRes.data || [],
          tournaments: [],
          analytics: null,
          dataSource: 'sample'
        };
      } catch (sampleError) {
        console.warn('Sample data API failed, using fallback data for team/player:', team, player);
        
        // Filter the comprehensive sample data based on search criteria
        let filteredMatches = SAMPLE_MATCHES;
        let filteredPlayers = SAMPLE_PLAYERS;
        
        if (team) {
          filteredMatches = SAMPLE_MATCHES.filter(match => 
            match.team_name.toLowerCase().includes(team.toLowerCase()) ||
            match.opponent_name.toLowerCase().includes(team.toLowerCase())
          );
          filteredPlayers = SAMPLE_PLAYERS.filter(p => 
            p.team_name.toLowerCase().includes(team.toLowerCase())
          );
        }
        
        if (player) {
          filteredPlayers = SAMPLE_PLAYERS.filter(p => 
            p.player_name.toLowerCase().includes(player.toLowerCase())
          );
          // Also filter matches for the player's team
          const playerTeams = filteredPlayers.map(p => p.team_name);
          if (playerTeams.length > 0) {
            filteredMatches = SAMPLE_MATCHES.filter(match => 
              playerTeams.some(teamName => 
                match.team_name === teamName || match.opponent_name === teamName
              )
            );
          }
        }
        
        // Return filtered fallback sample data
        return {
          matches: filteredMatches,
          players: filteredPlayers,
          tournaments: [],
          analytics: null,
          dataSource: 'fallback'
        };
      }
    }
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
    throw error;
  }
};

// Error interceptor for better error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    
    if (error.response?.status === 429) {
      console.warn('API rate limit exceeded. Please wait before making more requests.');
    } else if (error.response?.status >= 500) {
      console.error('Server error. The API service may be temporarily unavailable.');
    }
    
    return Promise.reject(error);
  }
);

// Mock data generators for when backend is not available
const generateMockMatches = (limit = 10) => {
  return Array.from({ length: Math.min(limit, 10) }, (_, i) => ({
    id: `match_${i}`,
    team1: `Team Alpha ${i}`,
    team2: `Team Beta ${i}`,
    team_name: `Team Alpha ${i}`,
    opponent_name: `Team Beta ${i}`,
    match_date: new Date(Date.now() - i * 86400000).toISOString(), // Past dates
    score_team: i < 5 ? 16 : Math.floor(Math.random() * 16),
    score_opponent: i < 5 ? 14 : Math.floor(Math.random() * 16),
    result: i < 5 ? 'win' : (Math.random() > 0.5 ? 'win' : 'loss'),
    game: "csgo",
    status: i < 3 ? "completed" : "upcoming",
    tournament: `Championship ${i}`,
    start_time: new Date(Date.now() - i * 86400000).toISOString()
  }));
};

const generateMockPlayers = (limit = 10) => {
  const playerNames = ['s1mple', 'ZywOo', 'device', 'NiKo', 'sh1ro', 'electronic', 'Perfecto', 'Ax1Le', 'interz', 'sdy'];
  const teamNames = ['NAVI', 'G2', 'Astralis', 'FaZe', 'Cloud9', 'Vitality', 'FURIA', 'Heroic', 'NIP', 'Liquid'];
  
  return Array.from({ length: Math.min(limit, 10) }, (_, i) => ({
    id: `player_${i}`,
    player_name: playerNames[i] || `Pro Player ${i}`,
    team_name: teamNames[i] || `Team ${String.fromCharCode(65 + i)}`,
    game: "csgo",
    rating: Math.round((1.0 + i * 0.1) * 100) / 100,
    kills: 25 + i,
    deaths: 15 + i,
    assists: 10 + i,
    kda_ratio: Math.round(((25 + i + 10 + i) / Math.max(15 + i, 1)) * 100) / 100,
    match_date: new Date(Date.now() - i * 3600000).toISOString(),
    last_match: new Date(Date.now() - i * 3600000).toISOString()
  }));
};

const generateMockTournaments = () => {
  return Array.from({ length: 5 }, (_, i) => ({
    id: `tournament_${i}`,
    name: `Championship Series ${i}`,
    game: "csgo",
    status: "upcoming",
    start_date: new Date(Date.now() + i * 86400000).toISOString(),
    end_date: new Date(Date.now() + (i + 7) * 86400000).toISOString(),
    prize_pool: `$${(i + 1) * 50000}`,
    teams: (i + 1) * 8,
    organizer: `ESL Gaming ${i}`,
    location: i % 2 === 0 ? "Online" : `City ${i}`
  }));
};

const generateMockAnalytics = () => {
  return {
    top_teams: [
      { name: "Astralis", wins: 15, trend: "up" },
      { name: "NAVI", wins: 14, trend: "stable" },
      { name: "G2 Esports", wins: 12, trend: "down" }
    ],
    top_players: [
      { name: "s1mple", rating: 1.35, game: "csgo" },
      { name: "ZywOo", rating: 1.32, game: "csgo" },
      { name: "device", rating: 1.28, game: "csgo" }
    ],
    match_frequency: {
      total_matches_today: 45,
      csgo: 20,
      valorant: 15,
      dota2: 10
    },
    tournament_activity: {
      active_tournaments: 8,
      upcoming_tournaments: 12,
      total_prize_pool: "$2,500,000"
    },
    timeframe: "24h",
    game_filter: null,
    last_updated: new Date().toISOString()
  };
};
