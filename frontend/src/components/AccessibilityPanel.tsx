"use client";

import { useState } from 'react';
import { Eye, Ear, Mic, Volume2 } from 'lucide-react';

export default function AccessibilityPanel() {
  const [isOpen, setIsOpen] = useState(false);

  // In a real implementation, these would update a global context/store
  const [mode, setMode] = useState('standard'); 

  return (
    <div className="relative">
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
        aria-label="Accessibility Settings"
        aria-expanded={isOpen}
      >
        <Eye className="w-5 h-5" />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-72 bg-white dark:bg-gray-900 rounded-xl shadow-lg border border-gray-200 dark:border-gray-800 p-4 z-50">
          <h3 className="text-sm font-semibold mb-3">Accessibility Modes</h3>
          
          <div className="space-y-2">
            <button 
              className={`w-full flex items-center gap-3 p-3 rounded-lg border text-left transition-colors ${
                mode === 'standard' ? 'border-teal-500 bg-teal-50 dark:bg-teal-900/20' : 'border-gray-200 dark:border-gray-700'
              }`}
              onClick={() => setMode('standard')}
            >
              <div className="flex-1">
                <div className="font-medium">Standard</div>
                <div className="text-xs text-gray-500">Default interface</div>
              </div>
            </button>

            <button 
              className={`w-full flex items-center gap-3 p-3 rounded-lg border text-left transition-colors ${
                mode === 'voice' ? 'border-teal-500 bg-teal-50 dark:bg-teal-900/20' : 'border-gray-200 dark:border-gray-700'
              }`}
              onClick={() => setMode('voice')}
            >
              <Mic className="w-5 h-5 text-blue-500" />
              <div className="flex-1">
                <div className="font-medium">Voice / Blind</div>
                <div className="text-xs text-gray-500">Auto-narration & voice controls</div>
              </div>
            </button>

            <button 
              className={`w-full flex items-center gap-3 p-3 rounded-lg border text-left transition-colors ${
                mode === 'isl' ? 'border-teal-500 bg-teal-50 dark:bg-teal-900/20' : 'border-gray-200 dark:border-gray-700'
              }`}
              onClick={() => setMode('isl')}
            >
              <Ear className="w-5 h-5 text-orange-500" />
              <div className="flex-1">
                <div className="font-medium">Deaf / ISL</div>
                <div className="text-xs text-gray-500">Visual alerts & simplified text</div>
              </div>
            </button>
          </div>
          
          <div className="mt-4 pt-4 border-t dark:border-gray-700">
            <div className="flex items-center justify-between">
              <span className="text-sm">Narration Speed</span>
              <Volume2 className="w-4 h-4 text-gray-400" />
            </div>
            <input type="range" min="0.5" max="2" step="0.25" defaultValue="1" className="w-full mt-2" />
          </div>
        </div>
      )}
    </div>
  );
}
