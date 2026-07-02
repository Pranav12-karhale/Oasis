import { AlertTriangle, CloudRain, Info, Wind } from 'lucide-react';

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <header className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">Health & Safety Dashboard</h1>
        <p className="text-gray-500 dark:text-gray-400 mt-2">
          Your personalized risk assessment for <span className="font-semibold text-gray-900 dark:text-gray-100">Delhi, India</span>.
        </p>
      </header>

      {/* Primary Status Card */}
      <div className="bg-gradient-to-br from-orange-500 to-red-600 rounded-2xl p-6 text-white shadow-lg relative overflow-hidden">
        <div className="relative z-10">
          <div className="flex items-center gap-2 mb-2">
            <AlertTriangle size={24} />
            <h2 className="text-xl font-semibold">High Risk Today</h2>
          </div>
          <p className="text-white/90 max-w-lg mb-4 text-lg">
            Air quality is severely poor and a heatwave warning is in effect. Stay indoors if possible.
          </p>
          <div className="flex gap-3">
            <button className="bg-white text-red-600 px-4 py-2 rounded-lg font-medium text-sm hover:bg-gray-50 transition-colors">
              Read Full Advisory
            </button>
            <button className="bg-red-700/50 hover:bg-red-700/70 text-white px-4 py-2 rounded-lg font-medium text-sm transition-colors flex items-center gap-2">
              <span aria-hidden="true">🔊</span> Play Audio
            </button>
          </div>
        </div>
        {/* Background Decoration */}
        <div className="absolute right-0 top-0 opacity-10 pointer-events-none transform translate-x-8 -translate-y-8">
          <AlertTriangle size={200} />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Air Quality */}
        <div className="bg-white dark:bg-gray-900 border border-gray-100 dark:border-gray-800 rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-medium flex items-center gap-2 text-gray-700 dark:text-gray-300">
              <Wind className="text-orange-500" size={20} /> Air Quality
            </h3>
            <span className="text-xs font-semibold bg-orange-100 text-orange-700 px-2 py-1 rounded">Very Poor</span>
          </div>
          <div className="text-3xl font-bold mb-1">287 <span className="text-sm font-normal text-gray-500">AQI</span></div>
          <p className="text-sm text-gray-500">PM2.5 is the primary pollutant.</p>
        </div>

        {/* Weather */}
        <div className="bg-white dark:bg-gray-900 border border-gray-100 dark:border-gray-800 rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-medium flex items-center gap-2 text-gray-700 dark:text-gray-300">
              <CloudRain className="text-blue-500" size={20} /> Weather
            </h3>
            <span className="text-xs font-semibold bg-blue-100 text-blue-700 px-2 py-1 rounded">Heatwave</span>
          </div>
          <div className="text-3xl font-bold mb-1">42°C</div>
          <p className="text-sm text-gray-500">Feels like 46°C. High humidity.</p>
        </div>
      </div>
    </div>
  );
}
