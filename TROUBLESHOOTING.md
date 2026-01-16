# Troubleshooting Guide

Common issues and solutions for AI Incident Commander.

---

## 🔧 Installation Issues

### Issue: Python version error
```
❌ Python 3.11+ required
```

**Solution:**
1. Check your Python version: `python --version`
2. Download Python 3.11+ from: https://www.python.org/downloads/
3. Make sure to check "Add Python to PATH" during installation
4. Restart your terminal and try again

---

### Issue: Node.js not found
```
❌ Node.js not found
```

**Solution:**
1. Download Node.js 18+ from: https://nodejs.org/
2. Install and restart your terminal
3. Verify: `node --version`

---

### Issue: pip install fails
```
ERROR: Could not find a version that satisfies the requirement...
```

**Solution:**
1. Make sure you're in the virtual environment:
   - Linux/Mac: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
2. Update pip: `pip install --upgrade pip`
3. Try installing again: `pip install -r requirements.txt`

---

### Issue: npm install fails
```
npm ERR! network timeout
```

**Solution:**
1. Clear npm cache: `npm cache clean --force`
2. Try again: `npm install`
3. If still fails, try: `npm install --legacy-peer-deps`

---

## 🚀 Runtime Issues

### Issue: Backend won't start
```
Address already in use
```

**Solution:**
Port 8000 is already in use.

**Option 1:** Kill the existing process
- Linux/Mac: `lsof -ti:8000 | xargs kill -9`
- Windows: `netstat -ano | findstr :8000` then `taskkill /PID <PID> /F`

**Option 2:** Change the port
- Edit `backend/run.py` and change `port=8000` to `port=8001`
- Update frontend to use new port in `frontend/vite.config.js`

---

### Issue: Frontend won't start
```
Port 3000 is already in use
```

**Solution:**
1. Kill the process using port 3000 (see above)
2. Or change port in `frontend/vite.config.js`

---

### Issue: CORS errors in browser console
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
1. Make sure backend is running on port 8000
2. Check `backend/app/main.py` has correct CORS settings
3. Clear browser cache and refresh

---

### Issue: WebSocket connection fails
```
WebSocket connection to 'ws://localhost:8000' failed
```

**Solution:**
1. Verify backend is running: http://localhost:8000/health
2. Check browser console for detailed error
3. Make sure no firewall is blocking WebSocket connections

---

## 🤖 AI Commander Issues

### Issue: AI Commander not working
```
AI Commander disabled: LangChain or API key not available
```

**Solution:**
This is **normal** if you don't have an OpenAI API key!

The system runs in **Demo Mode** with intelligent pattern-based analysis.

To enable full AI features:
1. Get an OpenAI API key: https://platform.openai.com/api-keys
2. Add to `backend/.env`: `OPENAI_API_KEY=sk-...`
3. Restart the backend

**Note:** Demo mode works great for testing and still provides useful suggestions!

---

### Issue: AI analysis is slow
```
AI analysis taking >30 seconds
```

**Solution:**
1. Check your internet connection (if using OpenAI)
2. OpenAI API might be rate-limited - wait a few minutes
3. Check OpenAI status: https://status.openai.com/
4. Demo mode is instant - works without API key!

---

## 📊 Data Issues

### Issue: No demo data showing
```
Empty dashboard, no incidents
```

**Solution:**
Load demo data:
```bash
cd backend
python seed_data.py
```

Refresh the browser.

---

### Issue: Data disappears after restart
```
All incidents gone after restarting backend
```

**Solution:**
This is **expected behavior**! The system uses **in-memory storage** by default.

Data is lost when you restart the backend. This is fine for:
- Testing and development
- Demos and learning

For production, you would:
1. Replace in-memory storage with PostgreSQL
2. See `docs/DEPLOYMENT.md` for production setup

---

## 🐳 Docker Issues

### Issue: Docker build fails
```
ERROR: failed to solve: failed to compute cache key
```

**Solution:**
1. Make sure Docker is running
2. Try: `docker system prune -a` (removes old images)
3. Build again: `docker-compose build`

---

### Issue: Docker containers exit immediately
```
Error: Container exited with code 1
```

**Solution:**
1. Check logs: `docker-compose logs backend`
2. Most common: Missing environment variables
3. Make sure `.env` file exists with required vars
4. Try: `docker-compose up` (without `-d` to see errors)

---

### Issue: Can't access localhost in Docker
```
Connection refused when accessing http://localhost:8000
```

**Solution:**
1. Check container is running: `docker-compose ps`
2. Check port mapping: `docker-compose ps` (should show `0.0.0.0:8000->8000/tcp`)
3. Try `http://127.0.0.1:8000` instead

---

## 🌐 Browser Issues

### Issue: Page not loading
```
This site can't be reached
```

**Solution:**
1. Check frontend is running: Terminal should show `Local: http://localhost:3000`
2. Check backend is running: Visit http://localhost:8000/health
3. Try different browser
4. Clear browser cache

---

### Issue: UI looks broken / no styling
```
Plain white page with no colors
```

**Solution:**
1. Check browser console for errors
2. Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
3. Make sure frontend built correctly: `npm run build`

---

## 🔍 Common Error Messages

### Error: "Module not found"
**Solution:** Install dependencies
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

---

### Error: "Permission denied"
**Solution:** Check file permissions
```bash
# Linux/Mac
chmod +x setup.sh quickstart.sh

# Windows: Run as Administrator
```

---

### Error: "Cannot find module 'react'"
**Solution:** Reinstall frontend dependencies
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 🆘 Still Having Issues?

### Steps to get help:

1. **Check the logs:**
   - Backend logs: Check terminal where backend is running
   - Frontend logs: Check browser console (F12)
   - Docker logs: `docker-compose logs`

2. **Try the full reset:**
   ```bash
   # Stop everything
   # Delete virtual environment
   rm -rf backend/venv

   # Delete node_modules
   rm -rf frontend/node_modules

   # Run setup again
   ./setup.sh  # or setup.bat on Windows
   ```

3. **Check the documentation:**
   - README.md - Getting started
   - docs/API.md - API reference
   - docs/DEPLOYMENT.md - Deployment guide

4. **Create an issue:**
   - Go to: https://github.com/AmjadAlthabteh/Opsmind/issues
   - Describe your problem
   - Include error messages
   - Mention your OS and versions

---

## ✅ Verification Checklist

Use this to verify everything is working:

- [ ] Python 3.11+ installed: `python --version`
- [ ] Node.js 18+ installed: `node --version`
- [ ] Backend dependencies installed: `pip list | grep fastapi`
- [ ] Frontend dependencies installed: `ls frontend/node_modules`
- [ ] Backend starts: http://localhost:8000/health returns `{"status":"healthy"}`
- [ ] Frontend starts: http://localhost:3000 shows dashboard
- [ ] Demo data loaded: Dashboard shows 4 incidents
- [ ] API works: Can create new incident
- [ ] WebSocket works: Real-time updates in incident detail view
- [ ] AI Commander works: Demo mode provides suggestions

---

## 📝 Useful Commands

```bash
# Check Python version
python --version

# Check Node version
node --version

# Check if backend is running
curl http://localhost:8000/health

# Check what's using port 8000
# Linux/Mac
lsof -i :8000
# Windows
netstat -ano | findstr :8000

# Restart everything
# Kill backend & frontend, then run quickstart again

# View backend logs in real-time
cd backend
python run.py

# View frontend logs in real-time
cd frontend
npm run dev

# Clear all caches
# Backend
rm -rf backend/__pycache__ backend/app/__pycache__
# Frontend
rm -rf frontend/.vite frontend/node_modules/.vite

# Fresh install
rm -rf backend/venv frontend/node_modules
./setup.sh  # or setup.bat
```

---

**Remember:** Most issues are resolved by:
1. Making sure dependencies are installed
2. Checking ports aren't already in use
3. Verifying environment variables are set
4. Reading error messages carefully

The system is designed to work out-of-the-box with demo mode. You should be able to run it without any API keys!
