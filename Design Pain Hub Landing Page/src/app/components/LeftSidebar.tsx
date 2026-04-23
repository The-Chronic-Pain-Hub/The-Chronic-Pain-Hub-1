import { Plus, ExternalLink, Flame, Activity, Radio, Zap, AlertTriangle, Hand, FileQuestion, Eraser } from 'lucide-react';

type PainType = 'burning' | 'aching' | 'stabbing' | 'numbness' | 'tingling' | 'allodynia' | 'other' | 'eraser';

interface PainSpot {
  id: string;
  name: string;
  sensation: string;
  intensity: number;
  isActive: boolean;
}

interface LeftSidebarProps {
  intensity: number;
  onNavigateToResources?: () => void;
  selectedTool: PainType | null;
  onToolSelect: (tool: PainType) => void;
}

const sensationTools = [
  { type: 'aching' as PainType, icon: Activity, label: 'Aching', color: '#F1C40F' },
  { type: 'burning' as PainType, icon: Flame, label: 'Burning', color: '#005EB8' },
  { type: 'stabbing' as PainType, icon: AlertTriangle, label: 'Stabbing', color: '#E74C3C' },
  { type: 'numbness' as PainType, icon: Radio, label: 'Numbness', color: '#191C1E' },
  { type: 'tingling' as PainType, icon: Zap, label: 'Tingling', color: '#27AE60' },
  { type: 'allodynia' as PainType, icon: Hand, label: 'Touch Pain', color: '#E67E22' },
  { type: 'other' as PainType, icon: FileQuestion, label: 'Other', color: '#9B59B6' },
  { type: 'eraser' as PainType, icon: Eraser, label: 'Eraser', color: '#424752' },
];

export function LeftSidebar({ intensity, onNavigateToResources, selectedTool, onToolSelect }: LeftSidebarProps) {
  const painSpots: PainSpot[] = [
    { id: '1', name: 'Left Shoulder', sensation: 'Tingling (Green)', intensity: 7.4, isActive: true },
    { id: '2', name: 'Lower Lumbar', sensation: 'Aching (Yellow)', intensity: 4.2, isActive: false },
  ];

  return (
    <div className="w-64 flex flex-col gap-4">
      <div className="backdrop-blur-[2px] bg-[rgba(224,227,230,0.5)] border border-[rgba(194,198,212,0.3)] rounded-3xl p-4">
        <div className="flex items-center gap-2 mb-3">
          <div className="w-2.5 h-2.5 bg-[#424752] rounded-sm" />
          <h3 className="text-[10px] font-semibold tracking-[1.5px] uppercase text-[#424752]">
            IDENTIFIED PAIN SPOTS
          </h3>
        </div>

        <div className="space-y-2 mb-4 max-h-[300px] overflow-y-auto pr-2">
          {painSpots.map((spot) => (
            <div
              key={spot.id}
              className={`p-3 rounded-2xl transition-all ${
                spot.isActive
                  ? 'bg-white border-l-4 border-[#005EB8] shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)]'
                  : 'bg-[#F2F4F7] border-l-4 border-[rgba(114,119,131,0.3)]'
              }`}
            >
              <div className="font-semibold text-xs text-[#191C1E] mb-0.5">
                {spot.name}
              </div>
              <div className="text-[10px] font-medium text-[#424752] mb-2">
                {spot.sensation} • {spot.intensity}/10
              </div>
              {spot.isActive && onNavigateToResources && (
                <button
                  onClick={onNavigateToResources}
                  className="text-[9px] font-semibold text-[#005EB8] hover:text-[#00478D] flex items-center gap-1 transition-colors"
                >
                  View Resources for this Condition
                  <ExternalLink className="w-3 h-3" />
                </button>
              )}
            </div>
          ))}
        </div>

        <button className="w-full border border-[rgba(0,94,184,0.2)] rounded-lg py-2 flex items-center justify-center gap-2 hover:bg-[rgba(0,94,184,0.05)] transition-colors">
          <Plus className="w-3 h-3 text-[#005EB8]" />
          <span className="text-[10px] font-semibold uppercase tracking-tight text-[#005EB8]">
            TRACK NEW SPOT
          </span>
        </button>
      </div>

      <div className="bg-[#005EB8] rounded-3xl p-5 shadow-[0px_10px_15px_-3px_rgba(0,94,184,0.2),0px_4px_6px_-4px_rgba(0,94,184,0.2)]">
        <div className="text-[10px] font-semibold tracking-[2px] uppercase text-white/80 mb-2">
          INTENSITY INDEX
        </div>
        <div className="flex items-baseline gap-1 mb-2">
          <div className="text-5xl font-extrabold text-white tracking-tight">
            {intensity.toFixed(1)}
          </div>
          <div className="text-sm font-medium text-white/60">/ 10</div>
        </div>
        <div className="h-1.5 bg-white/20 rounded-xl overflow-hidden">
          <div
            className="h-full bg-white shadow-[0px_0px_8px_0px_rgba(255,255,255,0.5)]"
            style={{ width: `${(intensity / 10) * 100}%` }}
          />
        </div>
      </div>

      <div className="bg-white border border-[#E2E8F0] rounded-3xl p-4 shadow-sm">
        <div className="text-[10px] font-semibold tracking-[1.5px] uppercase text-[#424752] mb-3">
          PAINT TOOLS
        </div>
        <div className="grid grid-cols-2 gap-2">
          {sensationTools.map(({ type, icon: Icon, label, color }) => {
            const isEraser = type === 'eraser';
            const isSelected = selectedTool === type;
            return (
              <button
                key={type}
                onClick={() => onToolSelect(type)}
                className={`p-2.5 rounded-xl transition-all flex flex-col items-center gap-1.5 ${
                  isSelected
                    ? 'shadow-[0px_2px_4px_0px_rgba(0,0,0,0.1)] scale-105'
                    : 'hover:bg-[#F7F9FC] border border-[#E2E8F0]'
                }`}
                style={{
                  backgroundColor: isSelected ? color : 'transparent',
                  color: isSelected ? (isEraser || type === 'numbness' ? '#FFFFFF' : '#FFFFFF') : '#424752',
                  borderColor: isSelected ? 'transparent' : '#E2E8F0',
                }}
              >
                <Icon className="w-4 h-4" strokeWidth={2.5} />
                <span className="text-[9px] font-semibold tracking-tight">
                  {label}
                </span>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
