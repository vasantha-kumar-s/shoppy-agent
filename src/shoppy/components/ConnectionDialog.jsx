import React, { useState } from 'react';
import { toast } from 'sonner';
import { getApiSetting, setApiBase, testApiBase, PROXY } from '../services/api';

/** Lets the visitor point this app at their own FastAPI + Ollama service. Saved in this browser only. */
export default function ConnectionDialog({ onClose }) {
  const initial = getApiSetting();
  const [mode, setMode] = useState(initial === PROXY ? 'proxy' : initial ? 'url' : 'url');
  const [url, setUrl] = useState(initial && initial !== PROXY ? initial : 'http://localhost:8000');
  const [testing, setTesting] = useState(false);
  const value = mode === 'proxy' ? PROXY : url.trim();

  const valid = mode === 'proxy' || /^https?:\/\/[^\s]+$/i.test(url.trim());
  const test = async () => {
    setTesting(true);
    try {
      const h = await testApiBase(value);
      const ai = h?.services?.ollama?.status === 'online' ? 'AI online' : 'AI offline';
      toast.success('Store service answered', { description: `Status: ${h?.status || 'ok'} · ${ai}` });
    } catch (e) {
      toast.error('Could not reach the store service', { description: e.name === 'TimeoutError' ? 'No answer within 6 seconds.' : 'Check it is running and allows this site (CORS).' });
    } finally { setTesting(false); }
  };
  const save = () => { setApiBase(value); toast.success('Store connection saved'); window.location.reload(); };
  const reset = () => { setApiBase(''); toast('Store connection cleared'); window.location.reload(); };

  return (
    <div className="dialog-backdrop" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="card dialog" style={{maxWidth:480}} role="dialog" aria-modal="true" aria-labelledby="conn-title" onKeyDown={e => e.key === 'Escape' && onClose()}>
        <h3 id="conn-title">Store connection</h3>
        <p style={{ color: 'var(--text-secondary)', fontSize: '.9rem', margin: '6px 0 16px' }}>
          Point the store at your Shoppy FastAPI service (with Ollama). Saved in this browser only.
        </p>
        <div style={{ display: 'grid', gap: 10 }}>
          <label className="conn-option"><input type="radio" checked={mode === 'url'} onChange={() => setMode('url')} /> <span><strong>Service address</strong><br /><small>e.g. http://localhost:8000 or an https tunnel</small></span></label>
          {mode === 'url' && <input className="search-input" aria-label="Service address" value={url} onChange={e => setUrl(e.target.value)} placeholder="http://localhost:8000" autoFocus />}
          <label className="conn-option"><input type="radio" checked={mode === 'proxy'} onChange={() => setMode('proxy')} /> <span><strong>Local proxy</strong><br /><small>Only when you run this app with <code>npm run dev</code> on the same computer as FastAPI.</small></span></label>
        </div>
        {!valid && <p style={{ color: 'var(--error)', fontSize: '.85rem', marginTop: 8 }}>Enter an address starting with http:// or https://</p>}
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginTop: 18, justifyContent: 'flex-end' }}>
          {initial && <button className="btn btn-ghost" onClick={reset}>Disconnect</button>}
          <button className="btn btn-secondary" onClick={test} disabled={!valid || testing}>{testing ? 'Testing…' : 'Test connection'}</button>
          <button className="btn btn-secondary" onClick={onClose}>Cancel</button>
          <button className="btn btn-primary" onClick={save} disabled={!valid}>Save</button>
        </div>
      </div>
    </div>
  );
}
