import React from 'react';

export default function Loading() {
  return (
    <div className="flex items-center justify-center p-8">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      <span className="ml-4 text-lg text-gray-600">Generating video...</span>
    </div>
  );
} 