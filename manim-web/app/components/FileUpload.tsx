import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'framer-motion';
import { FiUpload, FiFile, FiX, FiImage } from 'react-icons/fi';

interface FileUploadProps {
  files: File[];
  setFiles: (files: File[]) => void;
}

export default function FileUpload({ files, setFiles }: FileUploadProps) {
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg']
    },
    onDrop: (acceptedFiles) => {
      setFiles(acceptedFiles);
    }
  });

  const removeFile = (index: number) => {
    setFiles(files.filter((_, i) => i !== index));
  };

  const previewFile = (file: File) => {
    const reader = new FileReader();
    reader.onload = () => {
      setPreviewUrl(reader.result as string);
    };
    reader.readAsDataURL(file);
  };

  return (
    <div className="space-y-6">
      <div
        {...getRootProps()}
        className={`relative overflow-hidden transition-all duration-300 ease-in-out
          ${isDragActive ? 'bg-blue-50 border-blue-500' : 'bg-white border-gray-300'}
          border-2 border-dashed rounded-xl p-8 text-center cursor-pointer group`}
      >
        <input {...getInputProps()} />
        
        <motion.div
          initial={{ scale: 1 }}
          animate={{ scale: isDragActive ? 1.05 : 1 }}
          className="flex flex-col items-center justify-center space-y-4"
        >
          <motion.div
            animate={{ y: isDragActive ? -10 : 0 }}
            className="w-16 h-16 text-gray-400 group-hover:text-blue-500 transition-colors"
          >
            <FiUpload className="w-full h-full" />
          </motion.div>
          
          <div className="space-y-2">
            <p className="text-lg font-medium text-gray-700">
              {isDragActive ? 'Drop your images here' : 'Drag & drop your images here'}
            </p>
            <p className="text-sm text-gray-500">
              or <span className="text-blue-500 hover:text-blue-600">choose files</span>
            </p>
          </div>
        </motion.div>
      </div>

      <AnimatePresence>
        {files.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="space-y-4"
          >
            <h3 className="text-lg font-semibold text-gray-700">Selected Files</h3>
            <div className="space-y-3">
              {files.map((file, index) => (
                <motion.div
                  key={file.name}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  className="flex items-center justify-between p-3 bg-white rounded-lg border border-gray-200 shadow-sm"
                >
                  <div className="flex items-center space-x-3">
                    <FiFile className="w-5 h-5 text-gray-400" />
                    <span className="text-sm text-gray-700">{file.name}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => previewFile(file)}
                      className="p-1.5 text-gray-500 hover:text-blue-500 transition-colors"
                    >
                      <FiImage className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => removeFile(index)}
                      className="p-1.5 text-gray-500 hover:text-red-500 transition-colors"
                    >
                      <FiX className="w-4 h-4" />
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {previewUrl && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setPreviewUrl(null)}
            className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50"
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
              className="relative max-w-3xl w-full bg-white rounded-xl p-2 shadow-2xl"
            >
              <img 
                src={previewUrl} 
                alt="Preview" 
                className="w-full h-auto max-h-[80vh] object-contain rounded-lg" 
              />
              <button
                onClick={() => setPreviewUrl(null)}
                className="absolute -top-3 -right-3 p-2 bg-white rounded-full shadow-lg hover:bg-gray-100 transition-colors"
              >
                <FiX className="w-5 h-5 text-gray-600" />
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
} 