import React, { useState, useEffect } from 'react';
import { getHealth } from '../services/api';

export default function HealthIndicator() {
  const [health, setHealth] = useState(null);

  const fetchHealth = async () => {
    try {
      const data = await getHealth();
      setHealth(data);
    } catch {
      setHealth({
        status: 'offline',
        services: {
          database: { status: 'offline' },
          ollama: { status: 'offline' },
          whisper_stt: { status: 'offline' },
          kokoro_tts: { status: 'offline' }
        }
      });
    }
  };

  useEffect(() => {
    fetchHealth();
    const interval = setInterval(fetchHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  const dbOnline = health?.services?.database?.status === 'online';
  const ollamaOnline = health?.services?.ollama?.status === 'online';
  const sttOnline = health?.services?.whisper_stt?.status === 'online';
  const ttsOnline = health?.services?.kokoro_tts?.status === 'online';

  return (
    <div className="health-indicators" title="Service Status">
      <span className={`health-dot ${dbOnline ? 'online' : 'offline'}`}>
        DB: {dbOnline ? 'Online' : 'Offline'}
      </span>
      <span className={`health-dot ${ollamaOnline ? 'online' : 'offline'}`}>
        AI: {ollamaOnline ? 'Online' : 'Offline'}
      </span>
      <span className={`health-dot ${sttOnline ? 'online' : 'offline'}`}>
        STT: {sttOnline ? 'Online' : 'Offline'}
      </span>
      <span className={`health-dot ${ttsOnline ? 'online' : 'offline'}`}>
        TTS: {ttsOnline ? 'Online' : 'Offline'}
      </span>
    </div>
  );
}
