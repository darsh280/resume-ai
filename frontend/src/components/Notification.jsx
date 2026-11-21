import { CheckCircle, XCircle, AlertCircle, Info, X } from 'lucide-react';
import { useState, useEffect } from 'react';

export default function Notification({ type = 'info', message, onClose, duration = 4000 }) {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    if (duration) {
      const timer = setTimeout(() => {
        setVisible(false);
        onClose?.();
      }, duration);
      return () => clearTimeout(timer);
    }
  }, [duration, onClose]);

  if (!visible) return null;

  const styles = {
    success: {
      bg: 'bg-emerald-50 border-emerald-200 text-emerald-800',
      icon: CheckCircle,
      iconColor: 'text-emerald-500',
    },
    error: {
      bg: 'bg-rose-50 border-rose-200 text-rose-800',
      icon: XCircle,
      iconColor: 'text-rose-500',
    },
    warning: {
      bg: 'bg-amber-50 border-amber-200 text-amber-800',
      icon: AlertCircle,
      iconColor: 'text-amber-500',
    },
    info: {
      bg: 'bg-blue-50 border-blue-200 text-blue-800',
      icon: Info,
      iconColor: 'text-blue-500',
    },
  };

  const scheme = styles[type] || styles.info;
  const Icon = scheme.icon;

  return (
    <div className={`flex items-center gap-3 p-3.5 rounded-xl border ${scheme.bg} text-xs shadow-sm`}>
      <Icon className={`w-4 h-4 shrink-0 ${scheme.iconColor}`} />
      <span className="flex-1 font-medium leading-relaxed">{message}</span>
      <button
        onClick={() => {
          setVisible(false);
          onClose?.();
        }}
        className="text-slate-400 hover:text-slate-600 p-0.5"
      >
        <X className="w-3.5 h-3.5" />
      </button>
    </div>
  );
}
