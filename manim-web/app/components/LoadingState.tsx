import React from 'react';
import { motion } from 'framer-motion';

export default function LoadingState() {
  return (
    <div className="flex flex-col items-center justify-center space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col items-center space-y-6"
      >
        <div className="flex items-center space-x-2">
          <motion.span
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="text-2xl font-medium text-gray-700"
          >
            Generating video
          </motion.span>
          <div className="flex space-x-1">
            {[0, 1, 2].map((i) => (
              <motion.span
                key={i}
                initial={{ opacity: 0, y: 0 }}
                animate={{ 
                  opacity: [0, 1, 1, 0],
                  y: [0, -10, -10, 0]
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  delay: i * 0.2,
                  times: [0, 0.2, 0.8, 1],
                  ease: "easeInOut"
                }}
                className="text-2xl text-blue-500 font-medium"
              >
                .
              </motion.span>
            ))}
          </div>
        </div>

        <motion.div 
          className="w-48 h-48 relative"
          animate={{ rotate: 360 }}
          transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
        >
          <motion.div
            className="absolute inset-0 border-4 border-blue-500/30 rounded-full"
            style={{ borderTopColor: 'rgb(59, 130, 246)' }}
          />
        </motion.div>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="text-sm text-gray-500 text-center max-w-sm"
        >
          Generating educational video. Might take a minute or so...
        </motion.p>
      </motion.div>
    </div>
  );
} 