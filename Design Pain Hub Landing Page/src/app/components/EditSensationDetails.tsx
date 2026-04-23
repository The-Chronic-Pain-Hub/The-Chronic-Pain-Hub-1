import { useState } from 'react';
import { Flame, Activity, Zap, Radio, AlertTriangle, Hand, FileQuestion, X } from 'lucide-react';
import { ColorLegend } from './ColorLegend';

type SensationType = 'burning' | 'aching' | 'stabbing' | 'numbness' | 'tingling' | 'allodynia' | 'other';

interface Sensation {
  type: SensationType;
  label: string;
  description: string;
  clinicalIndicator: string;
  color: string;
  icon: any;
}

const sensations: Sensation[] = [
  {
    type: 'burning',
    label: 'Burning',
    description: 'An intense, heat-like sensation often associated with nerve irritation or localized inflammation.',
    clinicalIndicator: 'High diagnostic indicator for Neuropathic Pain (NeuP)',
    color: '#005EB8',
    icon: Flame,
  },
  {
    type: 'aching',
    label: 'Aching',
    description: 'A dull, persistent discomfort often felt deep within muscles or joints.',
    clinicalIndicator: 'Musculoskeletal / Non-neuropathic pain (NoP)',
    color: '#F1C40F',
    icon: Activity,
  },
  {
    type: 'stabbing',
    label: 'Stabbing',
    description: 'Sudden, sharp shocks or jolts that mimic electrical currents along nerve pathways.',
    clinicalIndicator: 'Sharp, intermittent neuropathic flares',
    color: '#E74C3C',
    icon: AlertTriangle,
  },
  {
    type: 'numbness',
    label: 'Numbness',
    description: 'A partial or complete loss of sensation in a specific area, indicating sensory deficit.',
    clinicalIndicator: 'Sensory deficit associated with nerve damage',
    color: '#191C1E',
    icon: Radio,
  },
  {
    type: 'tingling',
    label: 'Tingling / Pins & Needles',
    description: 'A "pins and needles" sensation indicating nerve recovery or compression.',
    clinicalIndicator: 'Paresthesia; common in NeuP',
    color: '#27AE60',
    icon: Zap,
  },
  {
    type: 'allodynia',
    label: 'Hurts to Touch',
    description: 'A painful or unpleasant feeling to normally non-painful stimuli like light touch.',
    clinicalIndicator: 'Allodynia; a core NeuP marker',
    color: '#E67E22',
    icon: Hand,
  },
  {
    type: 'other',
    label: 'Other',
    description: 'Any unique somatic sensation that doesn\'t fit standard categories.',
    clinicalIndicator: 'Non-standard sensory experience',
    color: '#9B59B6',
    icon: FileQuestion,
  },
];

interface EditSensationDetailsProps {
  onClose?: () => void;
}

export function EditSensationDetails({ onClose }: EditSensationDetailsProps) {
  const [activeSensation, setActiveSensation] = useState<SensationType>('burning');
  const [intensity, setIntensity] = useState(8.4);
  const [notes, setNotes] = useState('');

  // Mock data for sensation composition (in real app, would come from painted areas)
  const [sensationComposition] = useState({
    burning: 58,
    tingling: 24,
    aching: 12,
    stabbing: 6,
    numbness: 0,
    allodynia: 0,
    other: 0,
  });

  const activeSensationData = sensations.find((s) => s.type === activeSensation);

  const calculateNeuropathyRisk = () => {
    const neuropathicSensations = ['burning', 'stabbing', 'tingling', 'allodynia'];
    const neuropathicPercentage =
      neuropathicSensations.reduce(
        (sum, type) => sum + (sensationComposition[type as SensationType] || 0),
        0
      );

    if (neuropathicPercentage >= 50) {
      return { level: 'HIGH', percentage: neuropathicPercentage };
    } else if (neuropathicPercentage >= 25) {
      return { level: 'MODERATE', percentage: neuropathicPercentage };
    }
    return { level: 'LOW', percentage: neuropathicPercentage };
  };

  const neuropathyRisk = calculateNeuropathyRisk();

  return (
    <div className="size-full flex flex-col overflow-auto bg-white">
      <div className="flex-1 p-8 max-w-[1400px] mx-auto w-full">
        <div className="mb-8">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <h1 className="text-4xl font-extrabold text-[#191C1E] tracking-tight">
                  Edit Sensation Details
                </h1>
                <span className="font-mono text-xs text-[#727783] bg-[#F2F4F7] px-2 py-1 rounded">
                  REF_SES-7042
                </span>
              </div>
              <p className="text-lg font-medium text-[#424752] mb-2">
                Modify the character and intensity of the active sensation layer.
              </p>
              <div className="flex items-center gap-2 text-xs text-[#727783]">
                <div className="flex items-center gap-1">
                  <div className="w-1.5 h-1.5 bg-[#27AE60] rounded-full animate-pulse" />
                  <span>Diagnostic Engine Active</span>
                </div>
                <span>•</span>
                <span>Session: Left Shoulder Mapping</span>
              </div>
            </div>
            {onClose && (
              <button
                onClick={onClose}
                className="w-10 h-10 rounded-xl bg-[#F2F4F7] hover:bg-[#E2E8F0] transition-colors flex items-center justify-center"
              >
                <X className="w-5 h-5 text-[#424752]" />
              </button>
            )}
          </div>
        </div>

        <div className="flex gap-8">
          <div className="flex-1">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-[#191C1E]">Sensation Quality</h2>
              <div className="text-xs font-semibold tracking-wider uppercase text-[#424752]">
                ACTIVE SELECTION: {activeSensationData?.label.toUpperCase()}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-8">
              {sensations.map((sensation) => {
                const Icon = sensation.icon;
                const isActive = sensation.type === activeSensation;

                return (
                  <button
                    key={sensation.type}
                    onClick={() => setActiveSensation(sensation.type)}
                    className={`backdrop-blur-[6px] bg-[rgba(255,255,255,0.7)] rounded-lg p-6 text-left transition-all ${
                      isActive
                        ? 'shadow-[0px_0px_0px_2px_var(--ring-color),0px_1px_2px_0px_rgba(0,0,0,0.05)]'
                        : 'shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)] hover:shadow-[0px_4px_6px_-1px_rgba(0,0,0,0.1)]'
                    }`}
                    style={{
                      '--ring-color': isActive ? `${sensation.color}66` : 'transparent',
                    } as React.CSSProperties}
                  >
                    {isActive && (
                      <div
                        className="absolute inset-0 opacity-30 rounded-lg pointer-events-none"
                        style={{
                          background: `radial-gradient(ellipse 188.05px 188.05px at 50% 50%, ${sensation.color}1A 0%, ${sensation.color}00 70%)`,
                        }}
                      />
                    )}
                    <div className="flex items-start gap-4 relative">
                      <div
                        className="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0"
                        style={{
                          backgroundColor: isActive ? sensation.color : '#ECEEF1',
                          boxShadow: isActive
                            ? '0px 2px 4px -2px rgba(0,0,0,0.1), 0px 4px 6px -1px rgba(0,0,0,0.1)'
                            : 'none',
                        }}
                      >
                        <Icon
                          className="w-6 h-6"
                          style={{ color: isActive ? '#FFFFFF' : '#424752' }}
                        />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="text-base font-bold text-[#191C1E] mb-1">
                          {sensation.label}
                        </h3>
                        <p className="text-sm text-[#424752] leading-relaxed mb-2">
                          {sensation.description}
                        </p>
                        <div
                          className="inline-block px-2 py-0.5 rounded text-[9px] font-semibold uppercase tracking-tight"
                          style={{
                            backgroundColor: `${sensation.color}15`,
                            color: sensation.color,
                          }}
                        >
                          {sensation.clinicalIndicator}
                        </div>
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>

            <div className="bg-white border border-[#E2E8F0] rounded-2xl p-6 mb-8 shadow-sm">
              <h3 className="text-xs font-semibold tracking-wider uppercase text-[#424752] mb-4">
                Sensation Quality Composition
              </h3>
              <div className="space-y-3 mb-4">
                {sensations
                  .filter((s) => sensationComposition[s.type] > 0)
                  .sort((a, b) => sensationComposition[b.type] - sensationComposition[a.type])
                  .map((sensation) => {
                    const percentage = sensationComposition[sensation.type];
                    return (
                      <div key={sensation.type}>
                        <div className="flex items-center justify-between mb-1.5">
                          <div className="flex items-center gap-2">
                            <div
                              className="w-3 h-3 rounded"
                              style={{ backgroundColor: sensation.color }}
                            />
                            <span className="text-sm font-semibold text-[#191C1E]">
                              {sensation.label}
                            </span>
                          </div>
                          <span className="text-sm font-bold" style={{ color: sensation.color }}>
                            {percentage}%
                          </span>
                        </div>
                        <div className="h-2 bg-[#F2F4F7] rounded-full overflow-hidden">
                          <div
                            className="h-full transition-all"
                            style={{
                              width: `${percentage}%`,
                              backgroundColor: sensation.color,
                            }}
                          />
                        </div>
                      </div>
                    );
                  })}
              </div>

              <div
                className={`border-t pt-4 ${
                  neuropathyRisk.level === 'HIGH'
                    ? 'border-[#E74C3C]/20'
                    : neuropathyRisk.level === 'MODERATE'
                    ? 'border-[#E67E22]/20'
                    : 'border-[#27AE60]/20'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold uppercase tracking-tight text-[#424752]">
                    Neuropathic Pain Risk
                  </span>
                  <div
                    className="px-3 py-1 rounded-full text-xs font-bold uppercase"
                    style={{
                      backgroundColor:
                        neuropathyRisk.level === 'HIGH'
                          ? '#E74C3C15'
                          : neuropathyRisk.level === 'MODERATE'
                          ? '#E67E2215'
                          : '#27AE6015',
                      color:
                        neuropathyRisk.level === 'HIGH'
                          ? '#E74C3C'
                          : neuropathyRisk.level === 'MODERATE'
                          ? '#E67E22'
                          : '#27AE60',
                    }}
                  >
                    {neuropathyRisk.level} ({neuropathyRisk.percentage}%)
                  </div>
                </div>
              </div>
            </div>

            {neuropathyRisk.level === 'HIGH' && (
              <div className="bg-gradient-to-r from-[#E74C3C]/10 to-[#E67E22]/10 border-l-4 border-[#E74C3C] rounded-lg p-4 mb-8">
                <div className="flex items-start gap-3">
                  <AlertTriangle className="w-5 h-5 text-[#E74C3C] flex-shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-sm font-bold text-[#191C1E] mb-1">
                      Discordance Alert: Neuropathy Flag Detected
                    </h4>
                    <p className="text-xs text-[#424752] leading-relaxed mb-3">
                      Your mapped sensation profile shows {neuropathyRisk.percentage}% neuropathic
                      indicators (Burning, Stabbing, Tingling, Allodynia). This pattern suggests
                      nerve involvement rather than purely musculoskeletal pain.
                    </p>
                    <div className="flex gap-2">
                      <button className="text-xs font-semibold text-[#E74C3C] hover:text-[#C0392B] transition-colors">
                        View Resources →
                      </button>
                      <span className="text-[#E2E8F0]">|</span>
                      <button className="text-xs font-semibold text-[#E74C3C] hover:text-[#C0392B] transition-colors">
                        Request Clinical Review
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="w-96 space-y-6">
            <div className="bg-white border border-[#E2E8F0] rounded-2xl p-6 shadow-sm">
              <h3 className="text-xs font-semibold tracking-wider uppercase text-[#424752] mb-4">
                Intensity Index
              </h3>
              <div className="mb-4">
                <div className="text-xs font-medium text-[#727783] mb-2">
                  VISUAL ANALOG SCALE
                </div>
                <div className="flex items-baseline gap-2 mb-4">
                  <div className="text-5xl font-extrabold text-[#E74C3C]">
                    {intensity.toFixed(1)}
                  </div>
                  <div className="text-xl text-[#727783]">/ 10</div>
                </div>
                <input
                  type="range"
                  min="0"
                  max="10"
                  step="0.1"
                  value={intensity}
                  onChange={(e) => setIntensity(parseFloat(e.target.value))}
                  className="w-full h-2 bg-[#F2F4F7] rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-5 [&::-webkit-slider-thumb]:h-5 [&::-webkit-slider-thumb]:bg-[#E74C3C] [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:shadow-lg"
                />
                <div className="flex justify-between mt-2 text-[9px] font-medium text-[#727783] uppercase">
                  <span>Mild</span>
                  <span>Moderate</span>
                  <span>Severe</span>
                </div>
              </div>
              <div className="text-xs italic text-[#424752] leading-relaxed">
                Very severe, intense discomfort; focal, is only on pain.
              </div>
            </div>

            <div className="bg-white border border-[#E2E8F0] rounded-2xl p-6 shadow-sm">
              <h3 className="text-xs font-semibold tracking-wider uppercase text-[#424752] mb-3">
                Patient/Clinical Notes
              </h3>
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="Describe the onset or specific triggers for this sensation..."
                className="w-full h-32 p-3 bg-[#F7F9FC] border border-[#E2E8F0] rounded-lg text-sm resize-none focus:outline-none focus:ring-2 focus:ring-[#005EB8]/20 placeholder:text-[#727783]/50"
              />
            </div>

            <div className="space-y-3">
              <button
                onClick={() => {
                  // In real app, would save changes and update the main canvas
                  if (onClose) onClose();
                }}
                className="w-full py-4 bg-[#005EB8] text-white rounded-xl font-semibold hover:bg-[#00478D] transition-colors shadow-[0px_4px_6px_-1px_rgba(0,0,0,0.1)] flex items-center justify-center gap-2"
              >
                <span>Apply Updates</span>
                {neuropathyRisk.level === 'HIGH' && (
                  <div className="w-2 h-2 bg-[#E74C3C] rounded-full animate-pulse" />
                )}
              </button>
              <button
                onClick={onClose}
                className="w-full py-3 bg-white border-2 border-[#E2E8F0] text-[#424752] rounded-xl font-semibold hover:bg-[#F7F9FC] transition-colors"
              >
                Discard Changes
              </button>

              {neuropathyRisk.level === 'HIGH' && (
                <div className="text-xs text-center text-[#727783] italic pt-2">
                  Applying will flag this session for clinical review
                </div>
              )}
            </div>

            <div className="bg-[#F7F9FC] border border-[#E2E8F0] rounded-2xl p-6">
              <h3 className="text-xs font-semibold tracking-wider uppercase text-[#424752] mb-4">
                Sensation Overlay
              </h3>
              <div className="aspect-[3/4] bg-white rounded-lg border border-[#E2E8F0] flex items-center justify-center">
                <div className="text-center p-8">
                  <div
                    className="w-16 h-16 rounded-full mx-auto mb-3 flex items-center justify-center"
                    style={{ backgroundColor: `${activeSensationData?.color}15` }}
                  >
                    {activeSensationData && (
                      <div
                        className="w-8 h-8 rounded-full"
                        style={{ backgroundColor: activeSensationData.color }}
                      />
                    )}
                  </div>
                  <div className="text-sm font-semibold text-[#424752]">
                    {activeSensationData?.label} Layer
                  </div>
                  <div className="text-xs text-[#727783] mt-1">
                    Body map preview
                  </div>
                </div>
              </div>
            </div>

            <ColorLegend />
          </div>
        </div>
      </div>
    </div>
  );
}
