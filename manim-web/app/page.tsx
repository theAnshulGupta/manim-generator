'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiHome } from 'react-icons/fi';
import FileUpload from './components/FileUpload';
import LoadingState from './components/LoadingState';

export default function Home() {
  const [files, setFiles] = useState<File[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [buttonProgress, setButtonProgress] = useState(0);
  const [showGenerating, setShowGenerating] = useState(false);

  const handleSubmit = async () => {
    if (files.length === 0) {
      setError('Please upload at least one image');
      return;
    }
    
    setIsProcessing(true);
    setError(null);

    // Start button animation
    const animationDuration = 2000; // 2 seconds
    const startTime = Date.now();
    
    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / animationDuration, 1);
      setButtonProgress(progress);
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        setShowGenerating(true);
        processFiles();
      }
    };
    
    requestAnimationFrame(animate);
  };

  const processFiles = async () => {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('images', file);
    });

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        setVideoUrl(url);
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Failed to generate video');
      }
    } catch (error) {
      setError('An error occurred while generating the video');
      console.error('Error:', error);
    } finally {
      setIsProcessing(false);
      setShowGenerating(false);
      setButtonProgress(0);
    }
  };

  const resetState = () => {
    setFiles([]);
    setVideoUrl(null);
    setError(null);
    setIsProcessing(false);
    setButtonProgress(0);
    setShowGenerating(false);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-12">
        <AnimatePresence mode="wait">
          {!showGenerating && !videoUrl ? (
            <motion.div
              key="upload"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-8"
            >
              <h1 className="text-4xl font-bold text-gray-900 text-center">
                Manim Video Generator
              </h1>
              
              <div className="bg-white rounded-2xl shadow-xl p-8">
                <FileUpload files={files} setFiles={setFiles} />

                {files.length > 0 && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="mt-8"
                  >
                    <button
                      onClick={handleSubmit}
                      disabled={isProcessing}
                      className="w-full relative overflow-hidden bg-blue-500 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-600 disabled:bg-gray-400 transition-colors"
                    >
                      {buttonProgress > 0 && (
                        <motion.div
                          className="absolute inset-0 bg-blue-600"
                          initial={{ width: "0%" }}
                          animate={{ 
                            width: `${buttonProgress * 100}%`,
                          }}
                          transition={{ duration: 0.1, ease: "linear" }}
                        />
                      )}
                      <span className="relative">
                        {isProcessing ? 'Preparing...' : 'Generate Video'}
                      </span>
                    </button>
                  </motion.div>
                )}
              </div>

              {error && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-center"
                >
                  {error}
                </motion.div>
              )}
            </motion.div>
          ) : showGenerating ? (
            <motion.div
              key="generating"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="flex flex-col items-center justify-center min-h-[400px]"
            >
              <LoadingState />
            </motion.div>
          ) : (
            <motion.div
              key="video"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-8"
            >
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold text-gray-900">Generated Video</h2>
                <button
                  onClick={resetState}
                  className="flex items-center space-x-2 text-gray-600 hover:text-blue-500 transition-colors"
                >
                  <FiHome className="w-5 h-5" />
                  <span>Start Over</span>
                </button>
              </div>

              <div className="bg-white rounded-2xl shadow-xl p-6">
                <video
                  src={videoUrl}
                  controls
                  className="w-full rounded-lg"
                />
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
} 