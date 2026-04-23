import { useState, useRef } from 'react';
import { Header } from './components/Header';
import { LeftSidebar } from './components/LeftSidebar';
import { AnatomicalCanvas } from './components/AnatomicalCanvas';
import { RightSidebar } from './components/RightSidebar';
import { Resources } from './components/Resources';
import { EditSensationDetails } from './components/EditSensationDetails';
import { History } from './components/History';
import { painMappingAPI, type PainMapData } from '../services/painMappingAPI';

type PainType = 'burning' | 'aching' | 'stabbing' | 'numbness' | 'tingling' | 'allodynia' | 'other' | 'eraser';

export default function App() {
  const [currentTab, setCurrentTab] = useState('History');
  const [showEditSensation, setShowEditSensation] = useState(false);
  const [selectedTool, setSelectedTool] = useState<PainType | null>('burning');
  const [showSkeletal, setShowSkeletal] = useState(true);
  const [showNerves, setShowNerves] = useState(false);
  const [intensity, setIntensity] = useState(7.4);
  const [depth, setDepth] = useState(75);
  const [strokeCounts, setStrokeCounts] = useState({
    aching: 12,
    burning: 58,
    stabbing: 6,
    numbness: 0,
    tingling: 24,
    allodynia: 0,
    other: 0,
  });
  const [isGeneratingReport, setIsGeneratingReport] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [sessionId] = useState(() => `session-${Date.now()}`);
  
  // Refs to access canvas data
  const frontCanvasRef = useRef<HTMLCanvasElement>(null);
  const backCanvasRef = useRef<HTMLCanvasElement>(null);

  const handleStrokeAdded = (type: PainType) => {
    if (type !== 'eraser') {
      setStrokeCounts((prev) => ({
        ...prev,
        [type]: prev[type] + 1,
      }));
    }
  };

  const calculateSensationBreakdown = () => {
    const total = Object.values(strokeCounts).reduce((sum, count) => sum + count, 0);
    if (total === 0) {
      return { burning: 0, aching: 0, tingling: 0, stabbing: 0 };
    }

    return {
      aching: Math.round((strokeCounts.aching / total) * 100),
      burning: Math.round((strokeCounts.burning / total) * 100),
      tingling: Math.round((strokeCounts.tingling / total) * 100),
      stabbing: Math.round((strokeCounts.stabbing / total) * 100),
    };
  };

  const collectPainData = (): PainMapData => {
    const breakdown = calculateSensationBreakdown();
    const total = Object.values(strokeCounts).reduce((sum, count) => sum + count, 0);

    return {
      session_id: sessionId,
      patient_id: null,
      pain_regions: [],
      overall_intensity: intensity,
      sensation_breakdown: breakdown,
      total_strokes: total,
    };
  };

  const handleGenerateReport = async () => {
    setIsGeneratingReport(true);
    try {
      const painData = collectPainData();
      const result = await painMappingAPI.generateReport(painData);
      
      if (result.status === 'success') {
        alert(`✅ Report Generated!\n\nSummary: ${result.report.summary}\n\nNeuropathic Probability: ${result.report.neuropathic_probability.toUpperCase()}\n\nRecommended Specialists:\n${result.report.recommended_specialists.join('\n')}`);
      }
    } catch (error) {
      console.error('Error generating report:', error);
      alert('❌ Failed to generate report. Make sure the backend server is running at http://localhost:8000');
    } finally {
      setIsGeneratingReport(false);
    }
  };

  const handleSaveProgress = async () => {
    setIsSaving(true);
    try {  onGenerateReport={handleGenerateReport}
            onSaveProgress={handleSaveProgress}
            isGeneratingReport={isGeneratingReport}
            isSaving={isSaving}
          
      const painData = collectPainData();
      const result = await painMappingAPI.savePainMapping(painData);
      
      if (result.status === 'success') {
        alert('✅ Pain mapping saved successfully!');
      }
    } catch (error) {
      console.error('Error saving progress:', error);
      alert('❌ Failed to save progress. Make sure the backend server is running at http://localhost:8000');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div
      className="size-full flex flex-col"
      style={{
        background: `radial-gradient(ellipse 774.64px 774.64px at 50% 50%, rgba(242,244,247,1) 0%, rgba(247,249,252,1) 100%)`,
      }}
    >
      <Header currentTab={currentTab} onTabChange={setCurrentTab} />
      {showEditSensation ? (
        <EditSensationDetails onClose={() => setShowEditSensation(false)} />
      ) : currentTab === 'Resources' ? (
        <Resources />
      ) : currentTab === 'History' ? (
        <History />
      ) : (
        <div className="flex-1 flex gap-6 p-6 overflow-hidden">
          <LeftSidebar
            intensity={intensity}
            onNavigateToResources={() => setCurrentTab('Resources')}
            selectedTool={selectedTool}
            onToolSelect={setSelectedTool}
          />
          <AnatomicalCanvas
            selectedTool={selectedTool}
            showSkeletal={showSkeletal}
            showNerves={showNerves}
            onStrokeAdded={handleStrokeAdded}
            depth={depth}
            onDepthChange={setDepth}
          />
          <RightSidebar
            sensationBreakdown={calculateSensationBreakdown()}
            onEditSensation={() => setShowEditSensation(true)}
            onGenerateReport={handleGenerateReport}
            onSaveProgress={handleSaveProgress}
            isGeneratingReport={isGeneratingReport}
            isSaving={isSaving}
          />
        </div>
      )}
    </div>
  );
}