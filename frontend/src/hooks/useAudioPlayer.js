import { useState, useRef, useCallback } from 'react';
import { synthesizeSpeech } from '../services/api';

export function useAudioPlayer() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [loadingAudio, setLoadingAudio] = useState(false);
  const audioRef = useRef(null);

  const stopAudio = useCallback(() => {
    // Stop native audio element
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      setIsPlaying(false);
    }
    // Stop browser SpeechSynthesis
    if (typeof window !== 'undefined' && window.speechSynthesis) {
      window.speechSynthesis.cancel();
      setIsPlaying(false);
    }
  }, []);

  const playBlob = useCallback((blob) => {
    stopAudio();
    const url = URL.createObjectURL(blob);
    const audio = new Audio(url);
    audioRef.current = audio;

    audio.onplay = () => setIsPlaying(true);
    audio.onended = () => {
      setIsPlaying(false);
      URL.revokeObjectURL(url);
    };
    audio.onerror = () => {
      setIsPlaying(false);
      URL.revokeObjectURL(url);
    };

    audio.play().catch((err) => {
      console.warn('Audio auto-play blocked or failed:', err);
      setIsPlaying(false);
    });
  }, [stopAudio]);

  const speakWithBrowserTTS = useCallback((text) => {
    if (typeof window === 'undefined' || !window.speechSynthesis) {
      alert('Speech synthesis is not supported in this browser.');
      return;
    }
    stopAudio();

    // Clean markdown symbols from text before speaking
    const cleanText = text
      .replace(/\*\*(.*?)\*\*/g, '$1')
      .replace(/\*(.*?)\*/g, '$1')
      .replace(/•/g, '')
      .replace(/₹/g, 'Rupees ')
      .replace(/[#_`]/g, '');

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.lang = 'en-US';

    // Pick a natural English voice if available
    const voices = window.speechSynthesis.getVoices();
    const englishVoice = voices.find(
      (v) => v.lang.startsWith('en') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Samantha') || v.name.includes('David'))
    ) || voices.find((v) => v.lang.startsWith('en'));

    if (englishVoice) {
      utterance.voice = englishVoice;
    }

    utterance.onstart = () => setIsPlaying(true);
    utterance.onend = () => setIsPlaying(false);
    utterance.onerror = () => setIsPlaying(false);

    window.speechSynthesis.speak(utterance);
  }, [stopAudio]);

  const speakText = useCallback(async (text) => {
    if (!text) return;
    setLoadingAudio(true);

    try {
      // 1. Try local Kokoro TTS first (with a short 5s timeout)
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000);

      const blob = await synthesizeSpeech(text);
      clearTimeout(timeoutId);

      if (blob && blob.size > 100) {
        playBlob(blob);
        setLoadingAudio(false);
        return;
      }
    } catch (err) {
      console.info('Kokoro TTS unavailable, using high-quality browser speech synthesis:', err);
    }

    // 2. Immediate, robust fallback to Web Speech API
    setLoadingAudio(false);
    speakWithBrowserTTS(text);
  }, [playBlob, speakWithBrowserTTS]);

  return {
    isPlaying,
    loadingAudio,
    speakText,
    playBlob,
    stopAudio,
  };
}
