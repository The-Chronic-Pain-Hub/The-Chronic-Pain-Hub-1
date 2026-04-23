import { useState } from 'react';
import { Sparkles, Plus, FileText, Save, Loader2 } from 'lucide-react';
import { SensationComposition } from './SensationComposition';

interface RightSidebarProps {
  sensationBreakdown: {
    burning: number;
    aching: number;
    tingling: number;
    stabbing: number;
  };
  onEditSensation?: () => void;
  onGenerateReport?: () => void;
  onSaveProgress?: () => void;
  isGeneratingReport?: boolean;
  isSaving?: boolean;
}

export function RightSidebar({ 
  sensationBreakdown, 
  onEditSensation,
  onGenerateReport,
  onSaveProgress,
  isGeneratingReport = false,
  isSaving = false
}: RightSidebarProps) {
  const [notes, setNotes] = useState('');

  return (
    <div className="w-80 bg-white rounded-[40px] border border-[rgba(194,198,212,0.2)] shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)] p-6 flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-extrabold text-[#191C1E]">
          Current Sensation
        </h2>
        <div className="w-8 h-8 bg-[rgba(0,94,184,0.1)] rounded-xl flex items-center justify-center">
          <Sparkles className="w-4 h-4 text-[#005EB8]" />
        </div>
      </div>

      <div className="space-y-5 flex-1">
        <div>
          <div className="flex items-center justify-between mb-3">
            <div className="text-[10px] font-semibold tracking-tight uppercase text-[#727783]">
              SENSATION COMPOSITION
            </div>
            {onEditSensation && (
              <button
                onClick={onEditSensation}
                className="text-[9px] font-semibold text-[#005EB8] hover:text-[#00478D] transition-colors uppercase tracking-tight"
              >
                EDIT DETAILS
              </button>
            )}
          </div>
          <SensationComposition breakdown={sensationBreakdown} />
          <div className="mt-3 p-2 bg-[#F7F9FC] rounded-lg">
            <p className="text-[9px] text-[#727783] leading-relaxed">
              <span className="font-semibold text-[#005EB8]">58% Burning (Blue)</span> +
              <span className="font-semibold text-[#27AE60]"> 24% Tingling (Green)</span> =
              High neuropathic pattern
            </p>
          </div>
        </div>

        <div>
          <div className="text-[10px] font-semibold tracking-tight uppercase text-[#727783] mb-2">
            DURATION
          </div>
          <div className="font-medium text-sm text-[#191C1E]">
            Persistent (4h+)
          </div>
        </div>

        <div>
          <div className="text-[10px] font-semibold tracking-tight uppercase text-[#727783] mb-2">
            CLINICAL NOTES & SYMPTOMS
          </div>
          <div className="bg-[#F7F9FC] border-l-4 border-[#005EB8] rounded-2xl p-4 shadow-[inset_0px_2px_4px_0px_rgba(0,0,0,0.05)]">
            <p className="text-xs italic text-[#424752] leading-relaxed">
              "Patient describes a 'static' feeling that intensifies during flexion. No visible
              inflammation observed. Reported sensitivity to cold drafts."
            </p>
          </div>
        </div>

        <div className="flex-1">
          <div className="text-[10px] font-semibold tracking-tight uppercase text-[#727783] mb-2">
            ADD OBSERVATION
          </div>
          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="Add any additional notes about the sensation..."
            className="w-full h-24 p-3 text-xs border border-[rgba(194,198,212,0.2)] rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-[#005EB8] focus:border-transparent"
          />
        </div>
      </div>

      <div className="space-y-3 mt-4">
        {onGenerateReport && (
          <button 
            onClick={onGenerateReport}
            disabled={isGeneratingReport}
            className="w-full py-4 bg-[#005EB8] text-white rounded-2xl font-semibold text-xs uppercase tracking-wider shadow-[0px_4px_6px_-1px_rgba(0,0,0,0.1),0px_2px_4px_-2px_rgba(0,0,0,0.1)] hover:bg-[#00478D] transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isGeneratingReport ? (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                GENERATING...
              </>
            ) : (
              <>
                <FileText className="w-3.5 h-3.5" />
                GENERATE REPORT
              </>
            )}
          </button>
        )}

        {onSaveProgress && (
          <button 
            onClick={onSaveProgress}
            disabled={isSaving}
            className="w-full py-3 bg-white border-2 border-[#005EB8] text-[#005EB8] rounded-2xl font-semibold text-xs uppercase tracking-wider hover:bg-[rgba(0,94,184,0.05)] transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSaving ? (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                SAVING...
              </>
            ) : (
              <>
                <Save className="w-3.5 h-3.5" />
                SAVE PROGRESS
              </>
            )}
          </button>
        )}

        <button className="w-full py-3 bg-[#F7F9FC] text-[#424752] rounded-2xl font-semibold text-xs uppercase tracking-wider hover:bg-[#E2E8F0] transition-colors flex items-center justify-center gap-2">
          <Plus className="w-3.5 h-3.5" />
          ADD CUSTOM SYMPTOM
        </button>
      </div>
    </div>
  );
}
