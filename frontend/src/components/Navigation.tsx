"use client";

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, MessageSquare, AlertTriangle, Map, Settings } from 'lucide-react';

export default function Navigation({ mobile = false }: { mobile?: boolean }) {
  const pathname = usePathname();

  const links = [
    { name: 'Dashboard', href: '/', icon: Home },
    { name: 'Ask Oasis', href: '/query', icon: MessageSquare },
    { name: 'Alerts', href: '/alerts', icon: AlertTriangle },
    { name: 'Map', href: '/map', icon: Map },
    { name: 'Settings', href: '/settings', icon: Settings },
  ];

  if (mobile) {
    return (
      <nav className="flex justify-around items-center h-16 px-2">
        {links.map((link) => {
          const isActive = pathname === link.href;
          const Icon = link.icon;
          return (
            <Link 
              key={link.name} 
              href={link.href}
              className={`flex flex-col items-center justify-center w-full h-full space-y-1 ${
                isActive ? 'text-teal-600 dark:text-teal-400' : 'text-gray-500 dark:text-gray-400'
              }`}
              aria-current={isActive ? "page" : undefined}
            >
              <Icon size={20} />
              <span className="text-[10px] font-medium">{link.name}</span>
            </Link>
          );
        })}
      </nav>
    );
  }

  return (
    <nav className="space-y-1">
      {links.map((link) => {
        const isActive = pathname === link.href;
        const Icon = link.icon;
        return (
          <Link
            key={link.name}
            href={link.href}
            className={`flex items-center gap-3 px-3 py-2.5 rounded-lg font-medium transition-colors ${
              isActive 
                ? 'bg-teal-50 text-teal-700 dark:bg-teal-900/30 dark:text-teal-300' 
                : 'text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800'
            }`}
            aria-current={isActive ? "page" : undefined}
          >
            <Icon size={20} />
            {link.name}
          </Link>
        );
      })}
    </nav>
  );
}
