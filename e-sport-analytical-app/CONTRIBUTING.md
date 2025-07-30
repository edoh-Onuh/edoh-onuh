# Contributing to E-Sport Analytics Platform

First off, thank you for considering contributing to our e-sport analytics platform! It's people like you that make this project a great tool for the e-sport community.

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed and what behavior you expected**
- **Include screenshots or GIFs if possible**
- **Include your environment details** (OS, browser, Python/Node versions)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and the behavior you expected**
- **Explain why this enhancement would be useful**

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## 🔧 Development Process

### Setting Up Your Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/JohnEdohOnuh/e-sport-analytical-app.git
   cd e-sport-analytical-app
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If exists
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Database Setup**
   ```bash
   cd backend
   python populate_data.py  # Generate sample data
   ```

### Code Style Guidelines

#### Python (Backend)
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write docstrings for all functions and classes
- Use meaningful variable and function names
- Keep functions small and focused

**Example:**
```python
def calculate_kda_ratio(kills: int, deaths: int, assists: int) -> float:
    """
    Calculate K/D/A ratio for a player.
    
    Args:
        kills: Number of kills
        deaths: Number of deaths  
        assists: Number of assists
        
    Returns:
        KDA ratio as float
    """
    return (kills + assists) / max(deaths, 1)
```

#### JavaScript/React (Frontend)
- Use ES6+ features (arrow functions, destructuring, etc.)
- Follow React hooks best practices
- Use meaningful component and variable names
- Keep components small and focused
- Use PropTypes or TypeScript for type checking

**Example:**
```javascript
const PlayerStats = ({ player, onPlayerClick }) => {
  const { kills, deaths, assists } = player;
  const kdaRatio = (kills + assists) / Math.max(deaths, 1);
  
  return (
    <div className="player-card" onClick={() => onPlayerClick(player)}>
      <h3>{player.name}</h3>
      <p>KDA: {kdaRatio.toFixed(2)}</p>
    </div>
  );
};
```

### Testing Guidelines

#### Backend Testing
```bash
cd backend
python -m pytest tests/ -v
```

#### Frontend Testing
```bash
cd frontend
npm test
```

### Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` A new feature
- `fix:` A bug fix
- `docs:` Documentation only changes
- `style:` Changes that do not affect the meaning of the code
- `refactor:` A code change that neither fixes a bug nor adds a feature
- `test:` Adding missing tests or correcting existing tests
- `chore:` Changes to the build process or auxiliary tools

**Examples:**
```
feat: add player efficiency scatter plot visualization
fix: resolve API timeout issues for large datasets
docs: update installation guide with MySQL setup
style: format code according to PEP 8 guidelines
refactor: extract common chart components
test: add unit tests for KDA calculation functions
chore: update dependencies to latest versions
```

## 🎯 Areas Where We Need Help

### High Priority
- **Performance Optimization** - Frontend chart rendering improvements
- **Mobile Responsiveness** - Better mobile UI/UX
- **Test Coverage** - Unit and integration tests
- **Documentation** - API documentation and user guides

### Medium Priority
- **New Visualizations** - Additional chart types and analytics
- **Export Features** - PDF/Excel export functionality
- **Real-time Updates** - WebSocket integration for live data
- **User Authentication** - Login and user management system

### Good First Issues
- **UI Improvements** - Better loading states and error messages
- **Code Documentation** - Adding comments and docstrings
- **Sample Data** - More realistic and diverse test data
- **Bug Fixes** - Small bug fixes and improvements

## 🌟 Recognition

Contributors are recognized in several ways:

- **README Credits** - All contributors listed in README
- **Release Notes** - Significant contributions mentioned in releases
- **GitHub Profiles** - Contributor status on GitHub

## 📚 Resources

- **React Documentation** - https://reactjs.org/docs/
- **FastAPI Documentation** - https://fastapi.tiangolo.com/
- **Recharts Documentation** - https://recharts.org/
- **Tailwind CSS Documentation** - https://tailwindcss.com/docs

## ❓ Questions?

Don't hesitate to ask questions! You can:

- Open an issue with the `question` label
- Join our community discussions
- Reach out to maintainers directly

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the E-Sport Analytics Platform! 🎮🚀
