import { toast } from 'sonner';
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
      return;
    }
    stopAudio();

    // Clean markdown symbols from text before speaking
    const cleanText = text
      .replace(/\*\*(.*?)\*\*/g, '$1')
      .replace(/\*(.*?)\*/g, '$1')
      .replace(/•/g, '')
      .replace(/₹/g, 'Rupees ')
      .replace(/[#_`]/g, '')
      .replace(/⭐/g, 'rating');

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 1.05;
    utterance.pitch = 1.0;
    utterance.lang = 'en-US';

    // Pick a natural English voice if available
    const voices = window.speechSynthesis.getVoices();
    const englishVoice = voices.find(
      (v) => v.lang.startsWith('en') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Samantha') || v.name.includes('David') || v.name.includes('Zira'))
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
      // 1. Try local Kokoro TTS first with a fast 1.5s timeout
      const blob = await Promise.race([
        synthesizeSpeech(text),
        new Promise((_, reject) => setTimeout(() => reject(new Error('Kokoro TTS timeout')), 1500))
      ]);

      if (blob && blob.size > 100) {
        playBlob(blob);
        setLoadingAudio(false);
        return;
      }
    } catch (err) {
      // Kokoro TTS container offline or timed out — fallback immediately to native SpeechSynthesis
    }

    // 2. Immediate, zero-delay fallback to Web Speech API
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
