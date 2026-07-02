import { AlertTriangle, Info } from 'lucide-react';

export default function AlertsPage() {
  const alerts = [
    {
      id: 1,
      type: 'Flash Flood Warning',
      severity: 'high',
      time: '10:00 AM',
      description: 'Heavy rainfall has caused flash flooding in low-lying areas. Evacuate to higher ground immediately.'
    },
    {
      id: 2,
      type: 'Heat Wave Advisory',
      severity: 'medium',
      time: '08:00 AM',
      description: 'Temperatures expected to exceed 42°C. Stay hydrated and avoid outdoor activities during afternoon hours.'
    },
    {
      id: 3,
      type: 'Air Quality Alert',
      severity: 'low',
      time: 'Yesterday',
      description: 'AQI has crossed 250 (Poor). Sensitive groups should reduce prolonged heavy exertion.'
    }
  ];

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-3xl font-bold tracking-tight">Active Alerts</h1>
        <p className="text-gray-500 mt-2">Emergency and health warnings for your area.</p>
      </header>

      <div className="space-y-4">
        {alerts.map(alert => (
          <div 
            key={alert.id}
            className={`p-5 rounded-xl border-l-4 shadow-sm bg-white dark:bg-gray-900 ${
              alert.severity === 'high' ? 'border-red-500' :
              alert.severity === 'medium' ? 'border-orange-500' : 'border-yellow-400'
            }`}
          >
            <div className="flex items-start gap-3">
              <div className={`mt-0.5 ${
                alert.severity === 'high' ? 'text-red-500' :
                alert.severity === 'medium' ? 'text-orange-500' : 'text-yellow-500'
              }`}>
                {alert.severity === 'high' ? <AlertTriangle /> : <Info />}
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-lg">{alert.type}</h3>
                  <span className="text-xs text-gray-500 font-medium">{alert.time}</span>
                </div>
                <p className="text-gray-600 dark:text-gray-300 mt-1">
                  {alert.description}
                </p>
                <div className="mt-3">
                  <button className="text-sm font-medium text-teal-600 dark:text-teal-400 hover:underline focus:outline-none focus:ring-2 focus:ring-teal-500 rounded px-1 -mx-1">
                    Play Audio Announcement
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
