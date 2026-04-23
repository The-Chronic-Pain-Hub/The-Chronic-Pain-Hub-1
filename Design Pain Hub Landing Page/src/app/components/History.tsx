import { Calendar, Clock, MapPin, TrendingUp, TrendingDown, Minus, ExternalLink, Download } from 'lucide-react';

interface HistorySession {
  id: string;
  date: string;
  time: string;
  primaryLocation: string;
  dominantSensation: string;
  dominantColor: string;
  intensityIndex: number;
  intensityTrend: 'up' | 'down' | 'stable';
  totalStrokes: number;
  neuropathicRisk: 'HIGH' | 'MODERATE' | 'LOW';
  sessionDuration: string;
}

export function History() {
  const sessions: HistorySession[] = [
    {
      id: 'S-042',
      date: 'Apr 19, 2026',
      time: '14:23',
      primaryLocation: 'Left Shoulder',
      dominantSensation: 'Burning',
      dominantColor: '#005EB8',
      intensityIndex: 7.4,
      intensityTrend: 'up',
      totalStrokes: 100,
      neuropathicRisk: 'HIGH',
      sessionDuration: '18m 34s',
    },
    {
      id: 'S-041',
      date: 'Apr 18, 2026',
      time: '09:15',
      primaryLocation: 'Left Shoulder',
      dominantSensation: 'Tingling',
      dominantColor: '#27AE60',
      intensityIndex: 6.8,
      intensityTrend: 'stable',
      totalStrokes: 84,
      neuropathicRisk: 'HIGH',
      sessionDuration: '15m 12s',
    },
    {
      id: 'S-040',
      date: 'Apr 17, 2026',
      time: '16:42',
      primaryLocation: 'Lower Lumbar',
      dominantSensation: 'Aching',
      dominantColor: '#F1C40F',
      intensityIndex: 4.2,
      intensityTrend: 'down',
      totalStrokes: 56,
      neuropathicRisk: 'LOW',
      sessionDuration: '12m 08s',
    },
    {
      id: 'S-039',
      date: 'Apr 16, 2026',
      time: '11:30',
      primaryLocation: 'Lower Lumbar',
      dominantSensation: 'Aching',
      dominantColor: '#F1C40F',
      intensityIndex: 5.1,
      intensityTrend: 'up',
      totalStrokes: 68,
      neuropathicRisk: 'LOW',
      sessionDuration: '14m 45s',
    },
    {
      id: 'S-038',
      date: 'Apr 15, 2026',
      time: '08:20',
      primaryLocation: 'Left Shoulder',
      dominantSensation: 'Burning',
      dominantColor: '#005EB8',
      intensityIndex: 6.9,
      intensityTrend: 'stable',
      totalStrokes: 92,
      neuropathicRisk: 'HIGH',
      sessionDuration: '16m 23s',
    },
    {
      id: 'S-037',
      date: 'Apr 14, 2026',
      time: '19:05',
      primaryLocation: 'Right Knee',
      dominantSensation: 'Stabbing',
      dominantColor: '#E74C3C',
      intensityIndex: 8.2,
      intensityTrend: 'up',
      totalStrokes: 45,
      neuropathicRisk: 'MODERATE',
      sessionDuration: '9m 18s',
    },
  ];

  const getTrendIcon = (trend: 'up' | 'down' | 'stable') => {
    if (trend === 'up') return <TrendingUp className="w-3 h-3 text-[#E74C3C]" />;
    if (trend === 'down') return <TrendingDown className="w-3 h-3 text-[#27AE60]" />;
    return <Minus className="w-3 h-3 text-[#727783]" />;
  };

  const getRiskBadge = (risk: 'HIGH' | 'MODERATE' | 'LOW') => {
    const config = {
      HIGH: { bg: 'bg-[#E74C3C]/10', border: 'border-[#E74C3C]/30', text: 'text-[#E74C3C]' },
      MODERATE: { bg: 'bg-[#F1C40F]/10', border: 'border-[#F1C40F]/30', text: 'text-[#F1C40F]' },
      LOW: { bg: 'bg-[#727783]/10', border: 'border-[#727783]/30', text: 'text-[#727783]' },
    };
    const { bg, border, text } = config[risk];
    return (
      <div className={`${bg} ${border} border px-2 py-0.5 rounded-md`}>
        <span className={`text-[9px] font-bold tracking-tight uppercase ${text}`}>
          {risk} NeuP
        </span>
      </div>
    );
  };

  return (
    <div className="size-full flex flex-col overflow-auto">
      <div className="flex-1 p-8 max-w-[1600px] mx-auto w-full">
        <div className="mb-6">
          <div className="flex items-start justify-between mb-4">
            <div>
              <h1 className="text-3xl font-extrabold text-[#191C1E] tracking-tight mb-2">
                Session History
              </h1>
              <p className="text-sm font-medium text-[#424752]">
                Chronological record of pain mapping sessions with diagnostic patterns
              </p>
            </div>
            <div className="flex gap-3">
              <button className="px-4 py-2 border border-[#E2E8F0] rounded-xl text-sm font-semibold text-[#424752] hover:bg-[#F7F9FC] transition-colors flex items-center gap-2">
                <Download className="w-4 h-4" />
                Export History
              </button>
              <button className="px-4 py-2 bg-[#005EB8] text-white rounded-xl text-sm font-semibold hover:bg-[#00478D] transition-colors">
                Generate Clinical Report
              </button>
            </div>
          </div>

          <div className="grid grid-cols-4 gap-4 mb-6">
            <div className="bg-white border border-[#E2E8F0] rounded-2xl p-4">
              <div className="text-[10px] font-semibold tracking-[1.5px] uppercase text-[#727783] mb-2">
                TOTAL SESSIONS
              </div>
              <div className="text-3xl font-extrabold text-[#191C1E]">42</div>
              <div className="text-xs text-[#424752] mt-1">Last 30 days</div>
            </div>
            <div className="bg-white border border-[#E2E8F0] rounded-2xl p-4">
              <div className="text-[10px] font-semibold tracking-[1.5px] uppercase text-[#727783] mb-2">
                AVG INTENSITY
              </div>
              <div className="text-3xl font-extrabold text-[#005EB8]">6.8</div>
              <div className="text-xs text-[#E74C3C] mt-1 flex items-center gap-1">
                <TrendingUp className="w-3 h-3" />
                +0.4 from last week
              </div>
            </div>
            <div className="bg-white border border-[#E2E8F0] rounded-2xl p-4">
              <div className="text-[10px] font-semibold tracking-[1.5px] uppercase text-[#727783] mb-2">
                HIGH NeuP RISK
              </div>
              <div className="text-3xl font-extrabold text-[#E74C3C]">18</div>
              <div className="text-xs text-[#424752] mt-1">43% of sessions</div>
            </div>
            <div className="bg-white border border-[#E2E8F0] rounded-2xl p-4">
              <div className="text-[10px] font-semibold tracking-[1.5px] uppercase text-[#727783] mb-2">
                TRACKED AREAS
              </div>
              <div className="text-3xl font-extrabold text-[#191C1E]">5</div>
              <div className="text-xs text-[#424752] mt-1">Active pain spots</div>
            </div>
          </div>
        </div>

        <div className="space-y-3">
          {sessions.map((session) => (
            <div
              key={session.id}
              className="bg-white border border-[rgba(194,198,212,0.2)] rounded-2xl p-5 hover:border-[#005EB8]/30 hover:shadow-[0px_4px_6px_-1px_rgba(0,0,0,0.05)] transition-all cursor-pointer group"
            >
              <div className="flex items-start gap-6">
                <div className="flex flex-col items-center gap-1 min-w-[80px]">
                  <div className="text-xs font-semibold text-[#191C1E]">{session.date}</div>
                  <div className="flex items-center gap-1.5 text-[#727783]">
                    <Clock className="w-3 h-3" />
                    <span className="text-xs font-medium">{session.time}</span>
                  </div>
                  <div className="mt-1 font-mono text-[9px] text-[#727783] bg-[#F7F9FC] px-2 py-1 rounded">
                    {session.id}
                  </div>
                </div>

                <div className="flex-1 grid grid-cols-[1fr_auto_auto_auto_auto] gap-6 items-center">
                  <div>
                    <div className="flex items-center gap-2 mb-1.5">
                      <MapPin className="w-4 h-4 text-[#005EB8]" />
                      <span className="text-sm font-semibold text-[#191C1E]">
                        {session.primaryLocation}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div
                        className="w-3 h-3 rounded"
                        style={{ backgroundColor: session.dominantColor }}
                      />
                      <span className="text-xs text-[#424752]">
                        Dominant: {session.dominantSensation}
                      </span>
                      <span className="text-xs text-[#727783]">
                        • {session.totalStrokes} strokes
                      </span>
                      <span className="text-xs text-[#727783]">
                        • {session.sessionDuration}
                      </span>
                    </div>
                  </div>

                  <div className="text-center">
                    <div className="text-2xl font-extrabold text-[#005EB8] mb-1">
                      {session.intensityIndex.toFixed(1)}
                    </div>
                    <div className="text-[9px] font-semibold uppercase tracking-tight text-[#727783]">
                      Intensity
                    </div>
                  </div>

                  <div className="flex flex-col items-center gap-1">
                    {getTrendIcon(session.intensityTrend)}
                    <div className="text-[9px] font-semibold uppercase tracking-tight text-[#727783]">
                      Trend
                    </div>
                  </div>

                  <div>{getRiskBadge(session.neuropathicRisk)}</div>

                  <button className="opacity-0 group-hover:opacity-100 transition-opacity px-4 py-2 border border-[#005EB8]/20 rounded-lg text-xs font-semibold text-[#005EB8] hover:bg-[#005EB8]/5 flex items-center gap-2">
                    View Details
                    <ExternalLink className="w-3 h-3" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
