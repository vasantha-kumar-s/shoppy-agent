import React from 'react';

export default function VoiceControls({
  isRecording,
  onStartRecord,
  onStopRecord,
  voiceMode,
  onToggleVoiceMode,
  voiceState, // 'IDLE' | 'LISTENING' | 'TRANSCRIBING' | 'THINKING' | 'SPEAKING' | 'ERROR'
  isPlaying,
  onStopAudio,
}) {
  const getStatusLabel = () => {
    switch (voiceState) {
      case 'LISTENING':
        return <span className="voice-status listening">🎙️ Listening... Click to stop</span>;
      case 'TRANSCRIBING':
        return <span className="voice-status transcribing">✍️ Transcribing speech...</span>;
      case 'THINKING':
        return <span className="voice-status thinking">🧠 Agent reasoning & tool use...</span>;
      case 'SPEAKING':
        return <span className="voice-status speaking">🔊 Speaking response...</span>;
      default:
        return null;
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 'var(--space-md)',
        flexWrap: 'wrap',
      }}
    >
      {/* Mic Button */}
      <button
        type="button"
        className={`voice-btn ${isRecording ? 'recording' : ''}`}
        onClick={isRecording ? onStopRecord : onStartRecord}
        title={isRecording ? 'Stop recording' : 'Speak to Assistant'}
      >
        {isRecording ? '⏹️' : '🎙️'}
      </button>

      {/* Voice mode toggle */}
      <button
        type="button"
        className={`btn btn-sm ${voiceMode ? 'btn-primary' : 'btn-secondary'}`}
        onClick={onToggleVoiceMode}
        title="Toggle automatic spoken voice replies"
        style={{ fontSize: '0.8rem' }}
      >
        {voiceMode ? '🔊 Voice Replies: ON' : '🔈 Voice Replies: OFF'}
      </button>

      {/* Stop audio button when playing */}
      {isPlaying && (
        <button
          type="button"
          className="btn btn-secondary btn-sm"
          onClick={onStopAudio}
          style={{ fontSize: '0.8rem' }}
        >
          ⏹️ Mute Speech
        </button>
      )}

      {/* Live Status indicator */}
      {getStatusLabel()}
    </div>
  );
}
