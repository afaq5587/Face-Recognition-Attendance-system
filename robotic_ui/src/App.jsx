import React, { useState, useEffect } from 'react';
import { Shield, Zap, Database, Terminal, UserPlus, Brain, Activity, Clock, X, Trash2, CheckCircle, FileText } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

const CommandCenter = () => {
  const [logs, setLogs] = useState([
    { id: 1, text: "SYSTEM INITIALIZED...", color: "cyan" },
    { id: 2, text: "CONNECTING TO BIOMETRIC SENSORS...", color: "cyan" },
    { id: 3, text: "DATABASE SYNC SUCCESSFUL.", color: "white" }
  ]);

  const [students, setStudents] = useState([]);
  const [attendance, setAttendance] = useState([]);
  const [status, setStatus] = useState({
    cpu_load: 0,
    memory_usage: 0,
    students: 0,
    attendance: 0,
    camera_online: false,
    model_loaded: false
  });
  
  const [showModal, setShowModal] = useState(false);
  const [showReportModal, setShowReportModal] = useState(false);
  const [formData, setFormData] = useState({ student_id: '', name: '' });
  const [isCapturing, setIsCapturing] = useState(false);

  const addLog = (text, color = "cyan") => {
    setLogs(prev => [...prev.slice(-10), { id: Date.now(), text, color }]);
  };

  const fetchData = async () => {
    try {
      const [studentsRes, attendanceRes, statusRes] = await Promise.all([
        axios.get(`${API_BASE}/students`),
        axios.get(`${API_BASE}/attendance`),
        axios.get(`${API_BASE}/system/status`)
      ]);
      setStudents(studentsRes.data);
      setAttendance(attendanceRes.data);
      setStatus(statusRes.data);
    } catch (error) {
      console.error("Error fetching data:", error);
      addLog("CONNECTION ERROR: DATABASE OFFLINE", "red");
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleCapture = async () => {
    if (!formData.student_id || !formData.name) return addLog("ERROR: MISSING DATA", "red");
    setIsCapturing(true);
    addLog(`INITIATING CAPTURE FOR ${formData.name}...`);
    try {
      await axios.post(`${API_BASE}/students/capture`, null, { params: formData });
      addLog("CAPTURE SEQUENCE COMPLETED.", "green");
      setTimeout(() => {
        setIsCapturing(false);
        setShowModal(false);
        setFormData({ student_id: '', name: '' });
      }, 5000);
    } catch (error) {
      addLog("CAPTURE FAILED: SENSOR ERROR", "red");
      setIsCapturing(false);
    }
  };

  const handleTrain = async () => {
    addLog("NEURAL NETWORK TRAINING STARTED...");
    try {
      await axios.post(`${API_BASE}/system/train`);
      addLog("TRAINING IN PROGRESS. PLEASE WAIT...", "white");
    } catch (error) {
      addLog("TRAINING FAILED.", "red");
    }
  };

  const handleSetMode = async (mode) => {
    addLog(`ACTIVATING ${mode} MODE...`, "cyan");
    try {
      await axios.post(`${API_BASE}/attendance/activate_mode`, null, { params: { mode } });
      addLog(`${mode} MODE ACTIVE. STAND IN FRONT OF SENSOR.`, "green");
    } catch (error) {
      addLog(`${mode} MODE ACTIVATION FAILED.`, "red");
    }
  };



  const handleDelete = async (studentId) => {
    if (!window.confirm(`ERASE SUBJECT ${studentId} FROM ARCHIVES?`)) return;
    try {
      await axios.delete(`${API_BASE}/students/${studentId}`);
      addLog(`SUBJECT ${studentId} PURGED.`, "red");
      fetchData();
    } catch (error) {
      addLog("PURGE FAILED.", "red");
    }
  };

  return (
    <div className="command-center">
      {/* Registration Modal */}
      <AnimatePresence>
        {showModal && (
          <motion.div 
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="modal-overlay"
          >
            <motion.div 
              initial={{ scale: 0.8, y: 20 }} animate={{ scale: 1, y: 0 }} exit={{ scale: 0.8, y: 20 }}
              className="glass-panel modal-content"
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h3 style={{ color: '#00ffff', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <UserPlus size={20} /> SUBJECT_REGISTRATION
                </h3>
                <button onClick={() => setShowModal(false)} className="btn-icon"><X size={20} /></button>
              </div>
              
              {!isCapturing ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                  <div className="input-group">
                    <label>ID_CODE</label>
                    <input 
                      type="text" value={formData.student_id} 
                      onChange={e => setFormData({...formData, student_id: e.target.value})}
                      placeholder="e.g. 003"
                    />
                  </div>
                  <div className="input-group">
                    <label>SUBJECT_NAME</label>
                    <input 
                      type="text" value={formData.name} 
                      onChange={e => setFormData({...formData, name: e.target.value})}
                      placeholder="e.g. JOHN_DOE"
                    />
                  </div>
                  <button className="btn-cyber" onClick={handleCapture} style={{ marginTop: '10px' }}>
                    START_CAPTURE_SEQUENCE
                  </button>
                </div>
              ) : (
                <div style={{ textAlign: 'center', padding: '20px' }}>
                  <motion.div 
                    animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
                    style={{ marginBottom: '15px' }}
                  >
                    <Brain size={48} color="#00ffff" />
                  </motion.div>
                  <div className="terminal-text">CAPTURING BIOMETRIC SAMPLES...</div>
                  <div className="progress-bar-container" style={{ marginTop: '15px' }}>
                    <motion.div 
                      initial={{ width: 0 }} animate={{ width: '100%' }} transition={{ duration: 5 }}
                      className="progress-bar"
                    />
                  </div>
                </div>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {showReportModal && (
          <motion.div 
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="modal-overlay"
          >
            <motion.div 
              initial={{ scale: 0.9, y: 20 }} animate={{ scale: 1, y: 0 }} exit={{ scale: 0.9, y: 20 }}
              className="glass-panel modal-content" style={{ maxWidth: '800px', width: '90%' }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', borderBottom: '1px solid #00ffff', paddingBottom: '10px' }}>
                <h2 style={{ color: '#00ffff', display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <FileText size={24} /> ATTENDANCE_REPORT
                </h2>
                <button className="btn-icon" onClick={() => setShowReportModal(false)}><X size={24} color="#00ffff" /></button>
              </div>
              
              <div className="terminal-text" style={{ maxHeight: '60vh', overflowY: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                  <thead>
                    <tr style={{ borderBottom: '1px solid #00ffff', color: '#00ffff' }}>
                      <th style={{ padding: '10px' }}>NAME</th>
                      <th style={{ padding: '10px' }}>DATE</th>
                      <th style={{ padding: '10px' }}>TIME</th>
                      <th style={{ padding: '10px' }}>DIRECTION</th>
                      <th style={{ padding: '10px' }}>ACCURACY</th>
                    </tr>
                  </thead>
                  <tbody>
                    {attendance.map(a => {
                      const studentName = students.find(s => s.student_id === a.student_id)?.name || 'UNKNOWN';
                      return (
                        <tr key={a.id} style={{ borderBottom: '1px solid rgba(0,255,255,0.1)' }}>
                          <td style={{ padding: '10px', color: '#fff' }}>{studentName}</td>
                          <td style={{ padding: '10px', color: '#aaaaaa' }}>{a.date}</td>
                          <td style={{ padding: '10px', color: '#aaaaaa' }}>{a.time}</td>
                          <td style={{ padding: '10px', color: a.direction === 'EXIT' ? '#ff4444' : '#00ff00', fontWeight: 'bold' }}>
                            {a.direction || 'ENTRY'}
                          </td>
                          <td style={{ padding: '10px', color: '#00ffff' }}>{a.accuracy || 'N/A'}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Header */}
      <header className="header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Shield color="#00ffff" size={32} />
          <h1>Biometric Command Center</h1>
        </div>
        <div className="terminal-text" style={{ textAlign: 'right' }}>
          <div>SECURE-ACCESS: {status.camera_online ? 'ACTIVE' : 'OFFLINE'}</div>
          <div>CPU-LOAD: {status.cpu_load.toFixed(1)}%</div>
          {status.active_mode && (
            <motion.div 
              animate={{ opacity: [1, 0.4, 1] }} transition={{ repeat: Infinity, duration: 1 }}
              style={{ color: '#00ff00', fontSize: '0.8rem', fontWeight: 'bold' }}
            >
              SCANNER_MODE: {status.active_mode}
            </motion.div>
          )}
        </div>
      </header>

      {/* Sidebar Left: Control Panel */}
      <aside className="sidebar">
        <div className="glass-panel" style={{ flex: 'none' }}>
          <h3 style={{ color: '#00ffff', marginBottom: '15px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Zap size={18} /> CONTROL_CORE
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <button className="btn-cyber" onClick={() => setShowModal(true)}>
              <UserPlus size={16} /> Capture_Subject
            </button>
            <button className="btn-cyber" onClick={handleTrain}>
              <Brain size={16} /> Init_Neural_Train
            </button>
            <div style={{ height: '10px' }} />
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
              <button 
                className={`btn-cyber ${status.active_mode === 'ENTRY' ? 'active' : ''}`} 
                onClick={() => handleSetMode('ENTRY')}
                style={{ borderColor: status.active_mode === 'ENTRY' ? '#00ff00' : '' }}
              >
                LOG_ENTRY
              </button>
              <button 
                className={`btn-cyber ${status.active_mode === 'EXIT' ? 'active' : ''}`} 
                onClick={() => handleSetMode('EXIT')}
                style={{ borderColor: status.active_mode === 'EXIT' ? '#ff4444' : '' }}
              >
                LOG_EXIT
              </button>
            </div>
            <button className="btn-cyber" onClick={() => setShowReportModal(true)} style={{ borderColor: '#00ff00', color: '#00ff00' }}>
              <FileText size={16} /> View_Report
            </button>
          </div>
        </div>
        
        <div className="glass-panel biometric-data">
          <h3 style={{ color: '#00ffff', marginBottom: '15px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Activity size={18} /> BIOMETRIC_FLUX
          </h3>
          <div className="terminal-text">
            {logs.map(log => (
              <motion.div 
                key={log.id} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }}
                style={{ color: log.color === 'red' ? '#ff4444' : (log.color === 'green' ? '#00ff00' : (log.color === 'cyan' ? '#00ffff' : '#fff')), marginBottom: '5px' }}
              >
                &gt; {log.text}
              </motion.div>
            ))}
          </div>
        </div>
      </aside>

      {/* Main: Scanner View */}
      <main className="scanner-view glass-panel">
        <div className="scanner-overlay">
          <div style={{ position: 'absolute', top: '20px', left: '20px', color: '#00ffff' }}>
            <div style={{ fontSize: '0.6rem' }}>STATUS: ONLINE</div>
            <div style={{ fontSize: '0.6rem' }}>LATITUDE: 42.3601 N</div>
          </div>
          {status.active_mode && (
            <div className="scanner-targeting">
              <div className="target-box" />
              <div className="scanning-line" />
            </div>
          )}
        </div>
        <img 
          src={`${API_BASE}/video_feed?t=${Date.now()}`} 
          alt="Live Feed" 
          style={{ width: '100%', height: '100%', objectFit: 'cover', opacity: 0.8 }} 
          onError={(e) => { e.target.src = "https://via.placeholder.com/640x480?text=SIGNAL_LOST"; }}
        />
      </main>

      {/* Sidebar Right: Data Terminal */}
      <aside className="sidebar">
        <div className="glass-panel" style={{ height: '45%' }}>
          <h3 style={{ color: '#00ffff', marginBottom: '15px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Database size={18} /> SUBJECT_ARCHIVE
          </h3>
          <div className="terminal-text" style={{ maxHeight: '200px', overflowY: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid #00ffff' }}>
                  <th style={{ textAlign: 'left', padding: '5px' }}>SID</th>
                  <th style={{ textAlign: 'left', padding: '5px' }}>NAME</th>
                  <th style={{ textAlign: 'center', padding: '5px' }}>ACTION</th>
                </tr>
              </thead>
              <tbody>
                {students.map(s => (
                  <tr key={s.id}>
                    <td style={{ padding: '5px' }}>{s.student_id}</td>
                    <td style={{ padding: '5px' }}>{s.name}</td>
                    <td style={{ padding: '5px', textAlign: 'center' }}>
                      <button onClick={() => handleDelete(s.student_id)} className="btn-icon" style={{ color: '#ff4444' }}>
                        <Trash2 size={14} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="glass-panel" style={{ height: '52%', marginTop: '3%' }}>
          <h3 style={{ color: '#00ffff', marginBottom: '15px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Clock size={18} /> ATTENDANCE_LOG
          </h3>
          <div className="terminal-text" style={{ maxHeight: '250px', overflowY: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid #00ffff' }}>
                  <th style={{ textAlign: 'left', padding: '5px' }}>SID</th>
                  <th style={{ textAlign: 'left', padding: '5px' }}>TIME</th>
                  <th style={{ textAlign: 'left', padding: '5px' }}>DIR</th>
                  <th style={{ textAlign: 'left', padding: '5px' }}>STATUS</th>
                </tr>
              </thead>
              <tbody>
                {attendance.map(a => (
                  <tr key={a.id}>
                    <td style={{ padding: '5px' }}>{a.student_id}</td>
                    <td style={{ padding: '5px' }}>{a.time}</td>
                    <td style={{ padding: '5px', color: a.direction === 'EXIT' ? '#ff4444' : '#00ffff' }}>
                      {a.direction || 'ENTRY'}
                    </td>
                    <td style={{ padding: '5px', color: '#00ff00' }}>{a.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </aside>

      {/* Footer Logs */}
      <footer className="footer-logs">
        <div style={{ display: 'flex', gap: '20px', overflow: 'hidden' }}>
          <motion.div 
            animate={{ x: [0, -1000] }} transition={{ duration: 30, repeat: Infinity, ease: 'linear' }}
            style={{ whiteSpace: 'nowrap' }}
          >
            SYSTEM STATUS: OPTIMAL | ENCRYPTION: active | DATABASE: {status.students} RECS | MEMORY-USAGE: {status.memory_usage.toFixed(1)}% | 
            SYSTEM STATUS: OPTIMAL | ENCRYPTION: active | DATABASE: {status.students} RECS | MEMORY-USAGE: {status.memory_usage.toFixed(1)}%
          </motion.div>
        </div>
      </footer>
    </div>
  );
};

export default CommandCenter;
