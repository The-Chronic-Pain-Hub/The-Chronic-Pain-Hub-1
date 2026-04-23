interface HeaderProps {
  currentTab: string;
  onTabChange: (tab: string) => void;
}

export function Header({ currentTab, onTabChange }: HeaderProps) {
  return (
    <header className="backdrop-blur-[6px] bg-[rgba(255,255,255,0.9)] border-b border-[#E0E3E6] px-6 py-2.5 flex items-center justify-between">
      <div className="flex items-center gap-10">
        <div>
          <h1 className="text-[20px] font-extrabold text-[#00478D] tracking-tight">
            The Pain Hub
          </h1>
        </div>

        <nav className="flex gap-6">
          {['Dashboard', 'History', 'Resources'].map((tab) => (
            <button
              key={tab}
              onClick={() => onTabChange(tab)}
              className={`text-sm font-semibold transition-colors relative pb-1.5 flex items-center gap-2 ${
                currentTab === tab
                  ? 'text-[#005EB8]'
                  : 'text-[#424752] hover:text-[#005EB8]'
              }`}
            >
              {tab}
              {tab === 'Resources' && currentTab !== 'Resources' && (
                <div className="w-1.5 h-1.5 bg-[#E74C3C] rounded-full animate-pulse" />
              )}
              {currentTab === tab && (
                <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#005EB8]" />
              )}
            </button>
          ))}
        </nav>
      </div>

      <div className="flex items-center gap-4">
        <button className="px-5 py-2 bg-[#005EB8] text-white rounded-xl font-semibold text-sm hover:bg-[#00478D] transition-colors">
          Save Session
        </button>
        <div className="w-8 h-8 bg-[#E0E3E6] rounded-xl border-2 border-[rgba(0,94,184,0.2)]" />
      </div>
    </header>
  );
}
