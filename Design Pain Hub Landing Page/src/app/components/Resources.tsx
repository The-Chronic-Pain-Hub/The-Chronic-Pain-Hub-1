import { BookOpen, FileText, Activity, AlertCircle, Download, ExternalLink, Stethoscope, CheckSquare, Video, FileBarChart } from 'lucide-react';

interface Resource {
  id: string;
  title: string;
  description: string;
  category: 'education' | 'preparation' | 'action';
  diagnosticId: string;
  icon: any;
  isPriority?: boolean;
  estimatedTime?: string;
  relatedCondition?: string;
}

export function Resources() {
  const priorityRecommendation = {
    title: 'Neuropathy Care: Recommended 15min Cooling Session',
    description: 'Based on your recent Left Shoulder mapping session showing Tingling (Green) and Burning (Blue) patterns, this protocol addresses paresthesia and nerve irritation through targeted temperature modulation.',
    relatedScan: 'Session #042 - Left Shoulder Neuropathic Pattern',
    diagnosticId: 'REC_P-9042',
    confidence: '94% Match',
  };

  const resources: Resource[] = [
    {
      id: 'edu-1',
      title: "Understanding 'Neuropathic Discordance'",
      description: 'Clinical guide to identifying when sensory descriptions diverge from expected anatomical patterns.',
      category: 'education',
      diagnosticId: 'EDU_ND-7834',
      icon: BookOpen,
      estimatedTime: '8 min read',
    },
    {
      id: 'edu-2',
      title: 'Sensation Quality: Clinical Taxonomy',
      description: 'Reference documentation for precise pain descriptors including burning, tingling, electric, and aching sensations.',
      category: 'education',
      diagnosticId: 'EDU_SQ-2190',
      icon: FileText,
      estimatedTime: '12 min read',
    },
    {
      id: 'edu-3',
      title: 'Visual Analog Scale Interpretation',
      description: 'How to accurately self-assess pain intensity using standardized clinical scales (0-10).',
      category: 'education',
      diagnosticId: 'EDU_VAS-4421',
      icon: Activity,
      estimatedTime: '6 min read',
    },
    {
      id: 'prep-1',
      title: 'Pre-Appointment Checklist',
      description: 'Comprehensive preparation guide ensuring all critical data points are documented before your clinical review.',
      category: 'preparation',
      diagnosticId: 'CHK_PA-1103',
      icon: CheckSquare,
      estimatedTime: '5 min',
    },
    {
      id: 'prep-2',
      title: 'Generate Clinical Report',
      description: 'Export a standardized medical report containing all mapped pain sessions, intensity trends, and clinical notes.',
      category: 'preparation',
      diagnosticId: 'GEN_CR-8856',
      icon: FileBarChart,
      estimatedTime: '2 min',
    },
    {
      id: 'prep-3',
      title: 'Medication & Trigger Log',
      description: 'Track correlations between pain episodes, medications, and environmental/activity triggers.',
      category: 'preparation',
      diagnosticId: 'LOG_MT-3394',
      icon: FileText,
      estimatedTime: '10 min',
    },
    {
      id: 'action-1',
      title: 'Shoulder Mobility Protocol',
      description: 'Physical therapy exercises designed for neuropathic shoulder conditions. Includes video demonstrations.',
      category: 'action',
      diagnosticId: 'PTX_SH-6721',
      icon: Video,
      estimatedTime: '15 min session',
      relatedCondition: 'Left Shoulder',
    },
    {
      id: 'action-2',
      title: 'Lower Lumbar Stabilization Routine',
      description: 'Core strengthening and pain management exercises for chronic lower back conditions.',
      category: 'action',
      diagnosticId: 'PTX_LL-9012',
      icon: Video,
      estimatedTime: '20 min session',
      relatedCondition: 'Lower Lumbar',
    },
    {
      id: 'action-3',
      title: 'Cooling Therapy Application Guide',
      description: 'Step-by-step protocol for applying controlled cooling to reduce burning sensations and inflammation.',
      category: 'action',
      diagnosticId: 'THR_CT-4487',
      icon: Activity,
      estimatedTime: '15 min',
      relatedCondition: 'Burning Sensation',
    },
  ];

  const getCategoryTitle = (category: string) => {
    switch (category) {
      case 'education':
        return 'Education & Understanding';
      case 'preparation':
        return 'Clinical Preparation';
      case 'action':
        return 'Direct Action & Therapy';
      default:
        return category;
    }
  };

  const getCategoryResources = (category: Resource['category']) => {
    return resources.filter((r) => r.category === category);
  };

  return (
    <div className="size-full flex flex-col overflow-auto bg-white">
      <div className="flex-1 p-8 max-w-[1400px] mx-auto w-full">
        <div className="mb-8">
          <div className="flex items-start justify-between mb-2">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <h1 className="text-3xl font-extrabold text-[#191C1E] tracking-tight">
                  Clinical Resources
                </h1>
                <div className="bg-[#E74C3C] text-white text-[10px] font-bold px-2 py-1 rounded-md">
                  NEW
                </div>
              </div>
              <p className="text-sm font-medium text-[#424752]">
                Personalized documentation and care protocols based on your active session
              </p>
            </div>
            <div className="bg-[rgba(0,94,184,0.1)] border border-[rgba(0,94,184,0.2)] rounded-xl px-3 py-1.5">
              <div className="text-[10px] font-semibold tracking-tight uppercase text-[#005EB8]">
                ACTIVE SCAN
              </div>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-[#005EB8] to-[#00478D] rounded-3xl p-6 mb-8 relative overflow-hidden shadow-[0px_10px_15px_-3px_rgba(0,94,184,0.3),0px_4px_6px_-4px_rgba(0,94,184,0.3)]">
          <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/2" />
          <div className="relative">
            <div className="flex items-start justify-between mb-4">
              <div>
                <div className="text-[10px] font-semibold tracking-[2px] uppercase text-white/80 mb-2">
                  PRIORITY CARE RECOMMENDATION
                </div>
                <h2 className="text-2xl font-extrabold text-white mb-2">
                  {priorityRecommendation.title}
                </h2>
                <p className="text-sm text-white/90 leading-relaxed max-w-2xl">
                  {priorityRecommendation.description}
                </p>
              </div>
              <div className="bg-white/20 backdrop-blur-sm border border-white/30 rounded-xl px-3 py-2 text-center min-w-[100px]">
                <div className="text-xs font-medium text-white/80">Match Rate</div>
                <div className="text-lg font-extrabold text-white">{priorityRecommendation.confidence}</div>
              </div>
            </div>

            <div className="flex items-center gap-4 mb-4 flex-wrap">
              <div className="flex items-center gap-2 text-white/90 text-xs">
                <AlertCircle className="w-4 h-4" />
                <span>Related: {priorityRecommendation.relatedScan}</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="flex items-center gap-1 bg-white/20 backdrop-blur-sm px-2 py-1 rounded">
                  <div className="w-2 h-2 bg-[#27AE60] rounded-full" />
                  <span className="text-white text-[10px] font-semibold">Green</span>
                </div>
                <div className="flex items-center gap-1 bg-white/20 backdrop-blur-sm px-2 py-1 rounded">
                  <div className="w-2 h-2 bg-[#005EB8] rounded-full" />
                  <span className="text-white text-[10px] font-semibold">Blue</span>
                </div>
              </div>
              <div className="font-mono text-[10px] text-white/60">
                {priorityRecommendation.diagnosticId}
              </div>
            </div>

            <div className="flex gap-3">
              <button className="bg-white text-[#005EB8] px-6 py-3 rounded-xl font-semibold text-sm hover:bg-white/90 transition-colors shadow-lg">
                Start Protocol Now
              </button>
              <button className="bg-white/10 backdrop-blur-sm border border-white/20 text-white px-6 py-3 rounded-xl font-semibold text-sm hover:bg-white/20 transition-colors">
                View Full Details
              </button>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-6 mb-8">
          {['education', 'preparation', 'action'].map((category) => (
            <div key={category} className="flex flex-col">
              <div className="mb-4">
                <h3 className="text-xs font-semibold tracking-[1.5px] uppercase text-[#727783] flex items-center gap-2">
                  <div className="w-1.5 h-1.5 bg-[#005EB8] rounded-full" />
                  {getCategoryTitle(category)}
                </h3>
              </div>

              <div className="space-y-3 flex-1">
                {getCategoryResources(category as Resource['category']).map((resource) => {
                  const Icon = resource.icon;
                  return (
                    <div
                      key={resource.id}
                      className="bg-white border border-[rgba(194,198,212,0.2)] rounded-2xl p-4 hover:border-[#005EB8]/30 hover:shadow-[0px_4px_6px_-1px_rgba(0,0,0,0.05)] transition-all cursor-pointer group"
                    >
                      <div className="flex items-start gap-3 mb-2">
                        <div className="w-10 h-10 bg-[rgba(0,94,184,0.1)] rounded-xl flex items-center justify-center flex-shrink-0">
                          <Icon className="w-5 h-5 text-[#005EB8]" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-start justify-between gap-2 mb-1">
                            <h4 className="text-sm font-semibold text-[#191C1E] leading-tight group-hover:text-[#005EB8] transition-colors">
                              {resource.title}
                            </h4>
                            <ExternalLink className="w-3.5 h-3.5 text-[#727783] flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity" />
                          </div>
                          <p className="text-xs text-[#424752] leading-relaxed mb-2">
                            {resource.description}
                          </p>
                          <div className="flex items-center justify-between">
                            <span className="font-mono text-[9px] text-[#727783]">
                              {resource.diagnosticId}
                            </span>
                            {resource.estimatedTime && (
                              <span className="text-[10px] text-[#005EB8] font-medium">
                                {resource.estimatedTime}
                              </span>
                            )}
                          </div>
                          {resource.relatedCondition && (
                            <div className="mt-2 inline-flex items-center gap-1 bg-[#005EB8]/10 px-2 py-1 rounded-md">
                              <div className="w-1 h-1 bg-[#005EB8] rounded-full" />
                              <span className="text-[9px] font-semibold text-[#005EB8] uppercase tracking-tight">
                                {resource.relatedCondition}
                              </span>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>

        <div className="bg-[#F7F9FC] border-2 border-[#E0E3E6] rounded-3xl p-8">
          <div className="flex items-start justify-between">
            <div className="flex items-start gap-4">
              <div className="w-14 h-14 bg-[#005EB8] rounded-2xl flex items-center justify-center">
                <Stethoscope className="w-7 h-7 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-extrabold text-[#191C1E] mb-1">
                  Request Clinical Review
                </h3>
                <p className="text-sm text-[#424752] leading-relaxed max-w-xl">
                  Submit your mapping data and clinical notes for professional medical evaluation.
                  A certified provider will review your pain profile and provide diagnostic recommendations
                  within 24-48 hours.
                </p>
                <div className="mt-3 flex items-center gap-4">
                  <div className="flex items-center gap-2 text-xs text-[#727783]">
                    <CheckSquare className="w-4 h-4" />
                    <span>HIPAA Compliant</span>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-[#727783]">
                    <Download className="w-4 h-4" />
                    <span>Auto-generates Clinical Report</span>
                  </div>
                </div>
              </div>
            </div>
            <button className="bg-[#005EB8] text-white px-8 py-4 rounded-2xl font-semibold text-sm hover:bg-[#00478D] transition-colors shadow-[0px_4px_6px_-1px_rgba(0,0,0,0.1),0px_2px_4px_-2px_rgba(0,0,0,0.1)] whitespace-nowrap">
              Submit for Review
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
