import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import {
  sendMessage,
  transcribeAudio,
  addToCart,
  getConversations,
  createConversation,
  getConversationMessages,
  deleteConversation,
} from '../services/api';
import { useVoiceRecorder } from '../hooks/useVoiceRecorder';
import { useAudioPlayer } from '../hooks/useAudioPlayer';
import VoiceControls from '../components/VoiceControls';

const WELCOME_MESSAGE = {
  id: 'welcome',
  role: 'assistant',
  content:
    "Welcome! I'm your shopping assistant. I can help you find products, compare specs, check stock, manage your cart, or answer questions about returns and shipping.\n\nTry asking:\n• \"Find laptops under ₹70,000\"\n• \"Show wireless headphones under 5k\"\n• \"What's the return policy?\"",
  tool_activities: [],
  products: [],
};

// Markdown renderer for bold, italics, bullets, and inline code
function renderMarkdown(text) {
  if (!text) return null;
  const lines = text.split('\n');
  const elements = [];
  let key = 0;

  for (const line of lines) {
    let processed = line;
    // Bold: **text**
    processed = processed.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    // Italic: *text*
    processed = processed.replace(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/g, '<em>$1</em>');
    // Inline code: `text`
    processed = processed.replace(
      /`(.+?)`/g,
      '<code style="background:var(--bg-tertiary);padding:1px 5px;border-radius:3px;font-size:0.85em">$1</code>'
    );

    if (processed.trim() === '') {
      elements.push(<br key={key++} />);
    } else if (processed.trim().startsWith('- ') || processed.trim().startsWith('• ')) {
      const content = processed.trim().replace(/^[-•]\s*/, '');
      elements.push(
        <div key={key++} style={{ display: 'flex', gap: '8px', marginBottom: '3px', paddingLeft: '4px' }}>
          <span style={{ color: 'var(--accent-primary)', flexShrink: 0, fontWeight: 600 }}>•</span>
          <span dangerouslySetInnerHTML={{ __html: content }} />
        </div>
      );
    } else {
      elements.push(
        <div key={key++} style={{ marginBottom: '2px' }} dangerouslySetInnerHTML={{ __html: processed }} />
      );
    }
  }
  return <>{elements}</>;
}

export default function AssistantPage({ onCartUpdate }) {
  const [messages, setMessages] = useState([WELCOME_MESSAGE]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [currentStatus, setCurrentStatus] = useState('');
  const [liveActivities, setLiveActivities] = useState([]);
  const [voiceMode, setVoiceMode] = useState(false);
  const [voiceState, setVoiceState] = useState('IDLE');

  // Session state
  const [conversationId, setConversationId] = useState(() => {
    const saved = localStorage.getItem('agentcart_active_conv_id');
    return saved ? parseInt(saved, 10) : null;
  });
  const [sessions, setSessions] = useState([]);
  const [showSessions, setShowSessions] = useState(true);

  const messagesEndRef = useRef(null);

  const { isRecording, audioBlob, startRecording, stopRecording, resetRecording } = useVoiceRecorder();
  const { isPlaying, speakText, stopAudio } = useAudioPlayer();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, voiceState, loading, currentStatus, liveActivities]);

  // Load sessions list
  const loadSessions = async () => {
    try {
      const list = await getConversations();
      setSessions(list);
    } catch (err) {
      console.warn('Failed to load chat sessions:', err);
    }
  };

  useEffect(() => {
    loadSessions();
  }, []);

  // Restore active session messages from DB
  useEffect(() => {
    async function loadActiveSession() {
      if (!conversationId) {
        setMessages([WELCOME_MESSAGE]);
        return;
      }
      try {
        const res = await getConversationMessages(conversationId);
        if (res.messages && res.messages.length > 0) {
          setMessages(
            res.messages.map((m) => ({
              id: m.id,
              role: m.role,
              content: m.content,
              tool_activities: m.metadata?.tools?.map((t) => ({ tool_name: t, display_text: t })) || [],
              products: [],
            }))
          );
        } else {
          setMessages([WELCOME_MESSAGE]);
        }
      } catch (err) {
        console.warn('Failed to load session messages:', err);
      }
    }
    loadActiveSession();
  }, [conversationId]);

  // Handle Voice input
  useEffect(() => {
    if (isRecording) {
      setVoiceState('LISTENING');
    }
  }, [isRecording]);

  useEffect(() => {
    if (audioBlob) {
      handleAudioSubmit(audioBlob);
    }
  }, [audioBlob]);

  const handleAudioSubmit = async (blob) => {
    setVoiceState('TRANSCRIBING');
    try {
      const res = await transcribeAudio(blob);
      if (res.transcript && res.transcript.trim()) {
        const transcriptText = res.transcript.trim();
        resetRecording();
        await handleSend(transcriptText);
      } else {
        alert('Could not transcribe audio. Please speak clearly and try again.');
        setVoiceState('IDLE');
        resetRecording();
      }
    } catch (err) {
      console.error('Transcription error:', err);
      alert('Speech transcription error: ' + (err.message || 'Please check microphone permissions.'));
      setVoiceState('IDLE');
      resetRecording();
    }
  };

  // Start new session
  const handleNewChat = async () => {
    try {
      const newConv = await createConversation();
      setConversationId(newConv.id);
      localStorage.setItem('agentcart_active_conv_id', String(newConv.id));
      setMessages([WELCOME_MESSAGE]);
      await loadSessions();
    } catch (err) {
      setConversationId(null);
      localStorage.removeItem('agentcart_active_conv_id');
      setMessages([WELCOME_MESSAGE]);
    }
  };

  // Switch session
  const handleSelectSession = (id) => {
    setConversationId(id);
    localStorage.setItem('agentcart_active_conv_id', String(id));
  };

  // Delete session
  const handleDeleteSession = async (e, id) => {
    e.stopPropagation();
    if (!confirm('Delete this chat session?')) return;
    try {
      await deleteConversation(id);
      if (conversationId === id) {
        setConversationId(null);
        localStorage.removeItem('agentcart_active_conv_id');
        setMessages([WELCOME_MESSAGE]);
      }
      await loadSessions();
    } catch (err) {
      alert('Failed to delete session');
    }
  };

  const handleSend = async (textToSend) => {
    const text = (textToSend || input).trim();
    if (!text || loading) return;

    const userMsg = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
      tool_activities: [],
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);
    setCurrentStatus('Processing...');
    setLiveActivities([]);
    setVoiceState('THINKING');

    const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

    try {
      const response = await fetch(`${API_BASE}/api/chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-ID': '1',
        },
        body: JSON.stringify({
          message: text,
          user_id: 1,
          conversation_id: conversationId,
        }),
      });

      if (!response.ok) throw new Error(`HTTP error ${response.status}`);

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let buffer = '';
      let streamCompleted = false;

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const event = JSON.parse(line.substring(6));

              if (event.type === 'init' && event.conversation_id) {
                setConversationId(event.conversation_id);
                localStorage.setItem('agentcart_active_conv_id', String(event.conversation_id));
              } else if (event.type === 'status') {
                setCurrentStatus(event.text || 'Processing...');
              } else if (event.type === 'tool_activity') {
                setCurrentStatus(event.display_text || 'Running tool...');
                setLiveActivities((prev) => [
                  ...prev,
                  {
                    tool_name: event.tool_name,
                    status: 'completed',
                    display_text: event.display_text,
                  },
                ]);
              } else if (event.type === 'done') {
                streamCompleted = true;
                const assistantMsg = {
                  id: (Date.now() + 1).toString(),
                  role: 'assistant',
                  content: event.response || 'I have completed your request.',
                  tool_activities: event.tool_activities || [],
                  products: event.products || [],
                };

                setMessages((prev) => [...prev, assistantMsg]);
                loadSessions(); // refresh session list

                if (
                  event.tool_activities?.some((t) =>
                    ['add_to_cart', 'remove_from_cart', 'clear_cart', 'create_order'].includes(
                      t.tool_name
                    )
                  )
                ) {
                  if (onCartUpdate) onCartUpdate();
                }

                if (voiceMode && event.response) {
                  setVoiceState('SPEAKING');
                  await speakText(event.response);
                }
              }
            } catch (e) {
              console.warn('SSE JSON parse error:', e);
            }
          }
        }
      }

      if (!streamCompleted) {
        const res = await sendMessage(text, conversationId);
        if (res.conversation_id) {
          setConversationId(res.conversation_id);
          localStorage.setItem('agentcart_active_conv_id', String(res.conversation_id));
        }

        const assistantMsg = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: res.response || 'I have completed your request.',
          tool_activities: res.tool_activities || [],
          products: res.products || [],
        };
        setMessages((prev) => [...prev, assistantMsg]);
        loadSessions();
      }
    } catch (err) {
      console.warn('Streaming failed, trying standard endpoint:', err);
      try {
        const res = await sendMessage(text, conversationId);
        if (res.conversation_id) {
          setConversationId(res.conversation_id);
          localStorage.setItem('agentcart_active_conv_id', String(res.conversation_id));
        }

        const assistantMsg = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: res.response || 'I have completed your request.',
          tool_activities: res.tool_activities || [],
          products: res.products || [],
        };
        setMessages((prev) => [...prev, assistantMsg]);
        loadSessions();

        if (
          res.tool_activities?.some((t) =>
            ['add_to_cart', 'remove_from_cart', 'clear_cart', 'create_order'].includes(t.tool_name)
          )
        ) {
          if (onCartUpdate) onCartUpdate();
        }

        if (voiceMode && res.response) {
          setVoiceState('SPEAKING');
          await speakText(res.response);
        }
      } catch (fallbackErr) {
        console.error('Agent chat error:', fallbackErr);
        const errorMsg = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content:
            'Sorry, I encountered an issue connecting to the AI agent or database. Please verify Ollama and the backend are running.',
          tool_activities: [],
        };
        setMessages((prev) => [...prev, errorMsg]);
      }
    } finally {
      setLoading(false);
      setCurrentStatus('');
      setLiveActivities([]);
      setVoiceState('IDLE');
    }
  };

  const handleAddToCartInline = async (productId) => {
    try {
      await addToCart(productId, 1);
      if (onCartUpdate) onCartUpdate();
      alert('Added to cart!');
    } catch (err) {
      alert(err.message || 'Failed to add item');
    }
  };

  return (
    <div style={{ display: 'flex', gap: 'var(--space-md)', height: 'calc(100vh - 2 * var(--space-xl))' }}>
      {/* Session History Sidebar */}
      {showSessions && (
        <aside
          className="card"
          style={{
            width: '240px',
            display: 'flex',
            flexDirection: 'column',
            padding: '14px',
            flexShrink: 0,
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
            <span style={{ fontSize: '0.82rem', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-secondary)' }}>
              Sessions
            </span>
            <button
              className="btn btn-primary btn-sm"
              style={{ fontSize: '0.75rem', padding: '4px 10px' }}
              onClick={handleNewChat}
            >
              + New Chat
            </button>
          </div>

          {/* Session items list */}
          <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '4px' }}>
            {sessions.length === 0 ? (
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textAlign: 'center', marginTop: '20px' }}>
                No past sessions
              </div>
            ) : (
              sessions.map((s) => {
                const isActive = conversationId === s.id;
                return (
                  <div
                    key={s.id}
                    onClick={() => handleSelectSession(s.id)}
                    style={{
                      padding: '8px 10px',
                      borderRadius: 'var(--radius-md)',
                      background: isActive ? 'rgba(180, 130, 60, 0.12)' : 'var(--bg-tertiary)',
                      border: `1px solid ${isActive ? 'var(--accent-primary)' : 'transparent'}`,
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      transition: 'all 0.15s ease',
                    }}
                  >
                    <div style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', flex: 1, marginRight: '6px' }}>
                      <div style={{ fontSize: '0.82rem', fontWeight: isActive ? '700' : '500', color: 'var(--text-primary)', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                        {s.title}
                      </div>
                      <div style={{ fontSize: '0.68rem', color: 'var(--text-muted)' }}>
                        {s.message_count || 0} msgs
                      </div>
                    </div>
                    <button
                      type="button"
                      style={{
                        background: 'none',
                        border: 'none',
                        color: 'var(--text-muted)',
                        cursor: 'pointer',
                        fontSize: '0.8rem',
                        padding: '2px 4px',
                      }}
                      title="Delete session"
                      onClick={(e) => handleDeleteSession(e, s.id)}
                    >
                      ✕
                    </button>
                  </div>
                );
              })
            )}
          </div>
        </aside>
      )}

      {/* Main Chat Container */}
      <div className="chat-container" style={{ flex: 1, maxWidth: '100%', margin: 0 }}>
        {/* Chat Header */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            paddingBottom: 'var(--space-md)',
            borderBottom: '1px solid var(--border-color)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              style={{ fontSize: '0.75rem', padding: '4px 8px' }}
              title={showSessions ? 'Hide Sessions' : 'Show Sessions'}
              onClick={() => setShowSessions(!showSessions)}
            >
              {showSessions ? '◀' : '☰ Sessions'}
            </button>
            <div>
              <h2 style={{ fontSize: '1.25rem', fontWeight: '700', letterSpacing: '-0.02em' }}>
                Shopping Assistant
              </h2>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                Session #{conversationId || 'New'} • Real-time Catalog Memory
              </p>
            </div>
          </div>

          <VoiceControls
            isRecording={isRecording}
            onStartRecord={startRecording}
            onStopRecord={stopRecording}
            voiceMode={voiceMode}
            onToggleVoiceMode={() => setVoiceMode(!voiceMode)}
            voiceState={voiceState}
            isPlaying={isPlaying}
            onStopAudio={stopAudio}
          />
        </div>

        {/* Messages Scroll Area */}
        <div className="chat-messages">
          {messages.map((msg) => (
            <div key={msg.id} className={`chat-message ${msg.role}`}>
              <div className="chat-message-avatar">
                {msg.role === 'user' ? '👤' : '🛒'}
              </div>

              <div className="chat-message-content">
                {/* Tool Activity Indicators */}
                {msg.tool_activities && msg.tool_activities.length > 0 && (
                  <div
                    style={{
                      display: 'flex',
                      flexWrap: 'wrap',
                      gap: '4px',
                      marginBottom: '10px',
                    }}
                  >
                    {msg.tool_activities.map((tool, idx) => (
                      <div key={idx} className="tool-activity">
                        <span style={{ fontSize: '0.72rem' }}>⚙</span>
                        <span>{tool.display_text || tool.tool_name}</span>
                      </div>
                    ))}
                  </div>
                )}

                {/* Message text */}
                <div>{renderMarkdown(msg.content)}</div>

                {/* Inline Products */}
                {msg.products && msg.products.length > 0 && (
                  <div className="chat-product-cards">
                    {msg.products.map((p) => (
                      <div key={p.id} className="chat-product-card">
                        <div
                          style={{
                            fontSize: '0.68rem',
                            color: 'var(--accent-primary)',
                            fontWeight: '700',
                            textTransform: 'uppercase',
                            letterSpacing: '0.05em',
                          }}
                        >
                          {p.brand}
                        </div>
                        <div className="product-name">{p.name}</div>
                        <div className="product-price">
                          ₹{p.price?.toLocaleString('en-IN')}
                        </div>
                        <div
                          style={{
                            fontSize: '0.78rem',
                            color: 'var(--warning)',
                            marginBottom: '8px',
                            fontWeight: '600',
                          }}
                        >
                          ★ {p.rating?.toFixed(1)}
                        </div>
                        <div style={{ display: 'flex', gap: '6px' }}>
                          <button
                            className="btn btn-primary btn-sm"
                            style={{ flex: 1, fontSize: '0.75rem' }}
                            onClick={() => handleAddToCartInline(p.id)}
                          >
                            Add to Cart
                          </button>
                          <Link
                            to={`/products/${p.id}`}
                            className="btn btn-secondary btn-sm"
                            style={{ fontSize: '0.75rem' }}
                          >
                            View
                          </Link>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {/* Read Aloud Button */}
                {msg.role === 'assistant' && msg.id !== 'welcome' && (
                  <div style={{ marginTop: '8px', display: 'flex', justifyContent: 'flex-end' }}>
                    <button
                      type="button"
                      style={{
                        background: 'none',
                        color: 'var(--text-muted)',
                        cursor: 'pointer',
                        fontSize: '0.78rem',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '4px',
                      }}
                      title="Read aloud"
                      onClick={() => speakText(msg.content)}
                    >
                      🔊 Read Aloud
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))}

          {/* Real-time live execution progress */}
          {loading && (
            <div className="chat-message assistant">
              <div className="chat-message-avatar">🛒</div>
              <div className="chat-message-content">
                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  {liveActivities.map((act, idx) => (
                    <div key={idx} className="tool-activity" style={{ background: 'var(--bg-tertiary)' }}>
                      <span>✓</span>
                      <span>{act.display_text}</span>
                    </div>
                  ))}
                  <div className="tool-activity" style={{ borderColor: 'var(--border-hover)' }}>
                    <div className="spinner"></div>
                    <span>{currentStatus || 'Processing request...'}</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <form
          className="chat-input-area"
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
        >
          <textarea
            className="chat-input"
            rows={1}
            placeholder="Ask about products, check stock, compare items..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
          />
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading || !input.trim()}
            style={{ padding: '0 22px' }}
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
