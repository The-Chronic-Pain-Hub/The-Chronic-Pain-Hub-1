import { useRef, useState } from 'react';
import imgFrontalAnatomicalView from "figma:asset/791c17557c59885990919a7a2e51e93d258ce8f5.png";
import imgPosteriorAnatomicalView from "figma:asset/48838bd13157b8b846bfe3ea9edf6b871628d413.png";

type PainType = 'burning' | 'aching' | 'stabbing' | 'numbness' | 'tingling' | 'allodynia' | 'other' | 'eraser';

interface AnatomicalCanvasProps {
  selectedTool: PainType | null;
  showSkeletal: boolean;
  showNerves: boolean;
  onStrokeAdded: (type: PainType) => void;
  depth: number;
  onDepthChange: (value: number) => void;
}

const painColors = {
  aching: '#F1C40F',
  burning: '#005EB8',
  stabbing: '#E74C3C',
  numbness: '#191C1E',
  tingling: '#27AE60',
  allodynia: '#E67E22',
  other: '#9B59B6',
  eraser: '#FFFFFF',
};

const depthLabels = [
  { value: 0, label: 'Dermal' },
  { value: 33, label: 'Subcutaneous Fascia' },
  { value: 66, label: 'Muscular' },
  { value: 100, label: 'Skeletal' },
];

export function AnatomicalCanvas({
  selectedTool,
  showSkeletal,
  showNerves,
  onStrokeAdded,
  depth,
  onDepthChange,
}: AnatomicalCanvasProps) {
  const frontCanvasRef = useRef<HTMLCanvasElement>(null);
  const backCanvasRef = useRef<HTMLCanvasElement>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [currentCanvas, setCurrentCanvas] = useState<'front' | 'back' | null>(null);

  const clearCanvas = () => {
    const frontCanvas = frontCanvasRef.current;
    const backCanvas = backCanvasRef.current;

    if (frontCanvas) {
      const ctx = frontCanvas.getContext('2d');
      if (ctx) {
        ctx.clearRect(0, 0, frontCanvas.width, frontCanvas.height);
      }
    }

    if (backCanvas) {
      const ctx = backCanvas.getContext('2d');
      if (ctx) {
        ctx.clearRect(0, 0, backCanvas.width, backCanvas.height);
      }
    }
  };

  const startDrawing = (e: React.MouseEvent<HTMLCanvasElement>, view: 'front' | 'back') => {
    if (!selectedTool) return;
    setIsDrawing(true);
    setCurrentCanvas(view);
  };

  const draw = (e: React.MouseEvent<HTMLCanvasElement>, view: 'front' | 'back') => {
    if (!isDrawing || !selectedTool || currentCanvas !== view) return;

    const canvas = view === 'front' ? frontCanvasRef.current : backCanvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX - rect.left) * 2;
    const y = (e.clientY - rect.top) * 2;

    if (selectedTool === 'eraser') {
      // Erase mode - clear the area
      ctx.globalCompositeOperation = 'destination-out';
      ctx.globalAlpha = 1.0;
      ctx.fillStyle = 'rgba(0,0,0,1)';
      ctx.beginPath();
      ctx.arc(x, y, 28, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalCompositeOperation = 'source-over';
    } else {
      // Draw mode - paint with color
      ctx.globalAlpha = 0.3;
      ctx.fillStyle = painColors[selectedTool];
      ctx.beginPath();
      ctx.arc(x, y, 24, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalAlpha = 1.0;
    }

    if (selectedTool !== 'eraser') {
      onStrokeAdded(selectedTool);
    }
  };

  const stopDrawing = () => {
    setIsDrawing(false);
    setCurrentCanvas(null);
  };

  const getCurrentDepthLabel = () => {
    const closest = depthLabels.reduce((prev, curr) =>
      Math.abs(curr.value - depth) < Math.abs(prev.value - depth) ? curr : prev
    );
    return closest.label;
  };

  return (
    <div className="flex-1 flex flex-col bg-white rounded-[40px] border border-[rgba(194,198,212,0.1)] shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)] overflow-hidden">
      <div className="flex-1 grid grid-cols-2 gap-px bg-[rgba(194,198,212,0.1)]">
        <div className="bg-white flex flex-col relative">
          <div className="absolute top-12 left-1/2 -translate-x-1/2 z-10 font-semibold text-[10px] tracking-[3px] uppercase text-[#727783]/40">
            FRONT VIEW
          </div>
          <div className="flex-1 flex items-center justify-center p-12 relative">
            <div className="relative w-full h-full max-w-[270px] max-h-[700px]">
              <img
                src={imgFrontalAnatomicalView}
                alt="Frontal View"
                className="absolute inset-0 w-full h-full object-contain opacity-20"
              />
              <canvas
                ref={frontCanvasRef}
                onMouseDown={(e) => startDrawing(e, 'front')}
                onMouseMove={(e) => draw(e, 'front')}
                onMouseUp={stopDrawing}
                onMouseLeave={stopDrawing}
                className="absolute inset-0 w-full h-full"
                width={540}
                height={1400}
                style={{
                  width: '100%',
                  height: '100%',
                  cursor: selectedTool === 'eraser' ? 'grab' : 'crosshair',
                }}
              />
            </div>
          </div>
        </div>

        <div className="bg-white flex flex-col relative border-l border-[rgba(194,198,212,0.1)]">
          <div className="absolute top-12 left-1/2 -translate-x-1/2 z-10 font-semibold text-[10px] tracking-[3px] uppercase text-[#727783]/40">
            BACK VIEW
          </div>
          <div className="flex-1 flex items-center justify-center p-12 relative">
            <div className="relative w-full h-full max-w-[270px] max-h-[700px]">
              <img
                src={imgPosteriorAnatomicalView}
                alt="Posterior View"
                className="absolute inset-0 w-full h-full object-contain opacity-20"
              />
              <canvas
                ref={backCanvasRef}
                onMouseDown={(e) => startDrawing(e, 'back')}
                onMouseMove={(e) => draw(e, 'back')}
                onMouseUp={stopDrawing}
                onMouseLeave={stopDrawing}
                className="absolute inset-0 w-full h-full"
                width={540}
                height={1400}
                style={{
                  width: '100%',
                  height: '100%',
                  cursor: selectedTool === 'eraser' ? 'grab' : 'crosshair',
                }}
              />
            </div>
          </div>
        </div>
      </div>

      <div className="absolute bottom-6 left-1/2 -translate-x-1/2 backdrop-blur-[6px] bg-[rgba(224,227,230,0.6)] border border-[rgba(255,255,255,0.2)] rounded-2xl p-1.5 flex gap-2">
        <button
          onClick={() => {}}
          className={`px-4 py-2 rounded-lg text-[10px] font-semibold uppercase tracking-tight transition-colors ${
            showSkeletal
              ? 'bg-white text-[#191C1E] shadow-[0px_0px_0px_1px_rgba(0,0,0,0.05),0px_1px_2px_0px_rgba(0,0,0,0.05)]'
              : 'text-[#191C1E]'
          }`}
        >
          Skeletal
          <br />
          Layer
        </button>
        <button
          onClick={() => {}}
          className={`px-4 py-2 rounded-lg text-[10px] font-semibold uppercase tracking-tight transition-colors ${
            showNerves
              ? 'bg-white text-[#191C1E] shadow-[0px_0px_0px_1px_rgba(0,0,0,0.05),0px_1px_2px_0px_rgba(0,0,0,0.05)]'
              : 'text-[#191C1E]'
          }`}
        >
          Nerve
          <br />
          Map
        </button>
        {selectedTool && (
          <>
            <div className="w-px bg-[rgba(194,198,212,0.3)] mx-1" />
            <div className="px-4 py-2 flex flex-col items-center justify-center gap-1">
              {selectedTool === 'eraser' ? (
                <>
                  <div className="w-4 h-4 rounded bg-[#424752] flex items-center justify-center">
                    <div className="w-2 h-2 bg-white rounded" />
                  </div>
                  <span className="text-[9px] font-semibold uppercase tracking-tight text-[#191C1E]">
                    Eraser
                  </span>
                </>
              ) : (
                <>
                  <div
                    className="w-4 h-4 rounded"
                    style={{ backgroundColor: painColors[selectedTool] }}
                  />
                  <span className="text-[9px] font-semibold uppercase tracking-tight text-[#191C1E]">
                    Active
                  </span>
                </>
              )}
            </div>
          </>
        )}
        <div className="w-px bg-[rgba(194,198,212,0.3)] mx-1" />
        <button
          onClick={clearCanvas}
          className="px-4 py-2 rounded-lg text-[10px] font-semibold uppercase tracking-tight transition-colors text-[#E74C3C] hover:bg-white/50"
        >
          Clear
          <br />
          All
        </button>
      </div>

      <div className="border-t border-[#E2E8F0] bg-white">
        <div className="px-6 py-4 flex items-center gap-6 border-b border-[#E2E8F0]">
          <span className="text-sm font-semibold text-[#424752] uppercase tracking-tight">Depth Navigator</span>
          <div className="flex-1">
            <input
              type="range"
              min="0"
              max="100"
              value={depth}
              onChange={(e) => onDepthChange(parseInt(e.target.value))}
              className="w-full h-1.5 bg-[rgba(0,94,184,0.1)] rounded-full appearance-none cursor-pointer border border-[rgba(0,94,184,0.1)] [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:bg-[#005EB8] [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:shadow-md"
            />
          </div>
          <span className="text-sm font-mono text-[#005EB8] min-w-[180px] text-right">
            {getCurrentDepthLabel()}
          </span>
        </div>

        <div className="px-6 py-3">
          <div className="flex items-center gap-4">
            <span className="text-xs font-semibold text-[#727783] uppercase tracking-tight">
              Color Legend:
            </span>
            <div className="flex items-center gap-3 flex-wrap">
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 bg-[#F1C40F] rounded" />
                <span className="text-xs text-[#424752]">Aching</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 bg-[#005EB8] rounded" />
                <span className="text-xs text-[#424752]">Burning</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 bg-[#E74C3C] rounded" />
                <span className="text-xs text-[#424752]">Stabbing</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 bg-[#191C1E] rounded border border-[#E2E8F0]" />
                <span className="text-xs text-[#424752]">Numbness</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 bg-[#27AE60] rounded" />
                <span className="text-xs text-[#424752]">Tingling</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 bg-[#E67E22] rounded" />
                <span className="text-xs text-[#424752]">Touch Pain</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 bg-[#9B59B6] rounded" />
                <span className="text-xs text-[#424752]">Other</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
