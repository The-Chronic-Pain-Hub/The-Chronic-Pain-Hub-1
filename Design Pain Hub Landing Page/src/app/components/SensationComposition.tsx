interface SensationCompositionProps {
  breakdown: {
    aching: number;
    burning: number;
    tingling: number;
    stabbing: number;
  };
}

const sensationColors = {
  aching: { color: '#F1C40F', label: 'Aching (Yellow)' },
  burning: { color: '#005EB8', label: 'Burning (Blue)' },
  stabbing: { color: '#E74C3C', label: 'Stabbing (Red)' },
  tingling: { color: '#27AE60', label: 'Tingling (Green)' },
};

export function SensationComposition({ breakdown }: SensationCompositionProps) {
  const entries = Object.entries(breakdown)
    .filter(([_, value]) => value > 0)
    .sort(([, a], [, b]) => b - a);

  if (entries.length === 0) {
    return (
      <div className="text-xs text-[#727783] text-center py-4">
        No sensation data mapped yet
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {entries.map(([type, percentage]) => {
        const sensation = sensationColors[type as keyof typeof sensationColors];
        return (
          <div key={type}>
            <div className="flex items-center justify-between mb-1.5">
              <div className="flex items-center gap-2">
                <div
                  className="w-3 h-3 rounded"
                  style={{ backgroundColor: sensation.color }}
                />
                <span className="text-xs font-semibold text-[#191C1E]">
                  {sensation.label}
                </span>
              </div>
              <span
                className="text-sm font-bold"
                style={{ color: sensation.color }}
              >
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
  );
}
