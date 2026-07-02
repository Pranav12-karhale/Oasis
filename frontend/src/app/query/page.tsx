"use client";

import { useState } from 'react';
import { Mic, Send, Volume2 } from 'lucide-react';

export default function QueryInterface() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! Ask me any questions about health, safety, or disaster protocols in your area.' }
  ]);
  const [isRecording, setIsRecording] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    // Add user message
    setMessages([...messages, { role: 'user', content: query }]);
    
    // Simulate response
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: "Based on current AQI levels in Delhi, it is recommended to stay indoors and keep windows closed. If you must go outside, wear an N95 mask."
      }]);
    }, 1000);

    setQuery('');
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] max-h-[800px] border rounded-2xl bg-white dark:bg-gray-900 overflow-hidden shadow-sm">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] rounded-2xl p-4 ${
              msg.role === 'user' 
                ? 'bg-teal-600 text-white rounded-tr-sm' 
                : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 rounded-tl-sm'
            }`}>
              <p className="leading-relaxed">{msg.content}</p>
              
              {msg.role === 'assistant' && (
                <button className="mt-3 flex items-center gap-1.5 text-xs font-medium text-teal-600 dark:text-teal-400 hover:underline" aria-label="Read aloud">
                  <Volume2 size={14} /> Read aloud
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="p-3 bg-gray-50 dark:bg-gray-950 border-t">
        <form onSubmit={handleSubmit} className="relative flex items-end gap-2">
          <div className="relative flex-1">
            <textarea 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Type your question..."
              className="w-full resize-none rounded-xl border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 pr-12 py-3 pl-4 focus:ring-2 focus:ring-teal-500 min-h-[52px] max-h-32"
              rows={1}
            />
            <button 
              type="button"
              onClick={() => setIsRecording(!isRecording)}
              className={`absolute right-2 bottom-2 p-1.5 rounded-lg transition-colors ${
                isRecording ? 'bg-red-100 text-red-600' : 'text-gray-400 hover:text-gray-600 hover:bg-gray-100 dark:hover:bg-gray-800'
              }`}
              aria-label={isRecording ? "Stop recording" : "Start voice input"}
            >
              <Mic size={20} className={isRecording ? 'animate-pulse' : ''} />
            </button>
          </div>
          <button 
            type="submit"
            disabled={!query.trim()}
            className="p-3.5 bg-teal-600 text-white rounded-xl hover:bg-teal-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shrink-0"
            aria-label="Send message"
          >
            <Send size={20} className="ml-0.5" />
          </button>
        </form>
      </div>
    </div>
  );
}
