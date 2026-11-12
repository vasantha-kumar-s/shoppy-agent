import { useState, useRef, useCallback } from 'react';

/**
 * Hybrid Voice Recorder with Web Speech API real-time recognition
 * and fallback to raw MediaRecorder audio blob capture.
 */
export function useVoiceRecorder() {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState(null);

  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const recognitionRef = useRef(null);
  const transcriptRef = useRef('');

  const startRecording = useCallback(async () => {
    setError(null);
    setAudioBlob(null);
    setTranscript('');
    transcriptRef.current = '';
    chunksRef.current = [];

    // 1. Initialize browser speech recognition if supported
    const SpeechRecognition = typeof window !== 'undefined'
      ? (window.SpeechRecognition || window.webkitSpeechRecognition)
      : null;

    if (SpeechRecognition) {
      try {
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onresult = (event) => {
          let text = '';
          for (let i = 0; i < event.results.length; i++) {
            text += event.results[i][0].transcript + ' ';
          }
          const clean = text.trim();
          transcriptRef.current = clean;
          setTranscript(clean);
        };

        recognition.onerror = (e) => {
          console.warn('Browser SpeechRecognition notice:', e.error);
        };

        recognition.start();
        recognitionRef.current = recognition;
      } catch (err) {
        console.warn('SpeechRecognition initialization note:', err);
      }
    }

    // 2. Start media stream recording
    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error('Microphone access is not supported in this browser.');
      }

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        setAudioBlob(blob);
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error('Error starting audio recording:', err);
      if (recognitionRef.current) {
        try { recognitionRef.current.stop(); } catch {}
      }
      setError(err.message || 'Microphone access denied.');
      setIsRecording(false);
    }
  }, []);

  const stopRecording = useCallback(() => {
    if (recognitionRef.current) {
      try { recognitionRef.current.stop(); } catch {}
    }
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  }, [isRecording]);

  const resetRecording = useCallback(() => {
    setAudioBlob(null);
    setTranscript('');
    transcriptRef.current = '';
    setError(null);
    chunksRef.current = [];
  }, []);

  return {
    isRecording,
    audioBlob,
    transcript: transcript || transcriptRef.current,
    error,
    startRecording,
    stopRecording,
    resetRecording,
  };
}
