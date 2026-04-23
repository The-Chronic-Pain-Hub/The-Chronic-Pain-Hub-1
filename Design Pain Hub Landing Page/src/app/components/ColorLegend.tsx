export function ColorLegend() {
  const colorMapping = [
    { color: '#F1C40F', label: 'Yellow', sensation: 'Aching', indicator: 'Musculoskeletal / NoP' },
    { color: '#005EB8', label: 'Blue', sensation: 'Burning', indicator: 'High NeuP Indicator' },
    { color: '#E74C3C', label: 'Red', sensation: 'Stabbing', indicator: 'Sharp Neuropathic' },
    { color: '#191C1E', label: 'Black', sensation: 'Numbness', indicator: 'Nerve Damage' },
    { color: '#27AE60', label: 'Green', sensation: 'Tingling', indicator: 'Paresthesia (NeuP)' },
    { color: '#E67E22', label: 'Orange', sensation: 'Touch Pain', indicator: 'Allodynia (NeuP)' },
    { color: '#9B59B6', label: 'Purple', sensation: 'Other', indicator: 'Non-standard' },
  ];

  return (
    <div className="bg-white border border-[#E2E8F0] rounded-2xl p-6 shadow-sm">
      <h3 className="text-xs font-semibold tracking-wider uppercase text-[#424752] mb-4">
        Clinical Color Mapping
      </h3>
      <div className="space-y-2.5">
        {colorMapping.map(({ color, label, sensation, indicator }) => (
          <div key={color} className="flex items-start gap-3">
            <div
              className="w-6 h-6 rounded flex-shrink-0 mt-0.5"
              style={{ backgroundColor: color }}
            />
            <div className="flex-1">
              <div className="flex items-baseline gap-2">
                <span className="text-sm font-bold text-[#191C1E]">{label}:</span>
                <span className="text-sm text-[#424752]">{sensation}</span>
              </div>
              <div className="text-xs text-[#727783] italic mt-0.5">{indicator}</div>
            </div>
          </div>
        ))}
      </div>
      <div className="mt-4 pt-4 border-t border-[#E2E8F0]">
        <p className="text-xs text-[#424752] leading-relaxed">
          <span className="font-semibold">NeuP</span> = Neuropathic Pain •{' '}
          <span className="font-semibold">NoP</span> = Non-neuropathic Pain
        </p>
      </div>
    </div>
  );
}
