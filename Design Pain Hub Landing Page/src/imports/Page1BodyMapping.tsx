import svgPaths from "./svg-pv4y1rwowu";
import imgFrontalAnatomicalView from "figma:asset/791c17557c59885990919a7a2e51e93d258ce8f5.png";
import imgPosteriorAnatomicalView from "figma:asset/48838bd13157b8b846bfe3ea9edf6b871628d413.png";
import imgUserAvatar from "figma:asset/854228ff475e9cd0422f1bb6d3e600b176c53dc9.png";

function Heading() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0 w-full" data-name="Heading 1">
      <div className="flex flex-col font-['Manrope:ExtraBold',sans-serif] font-extrabold justify-center leading-[0] relative shrink-0 text-[#191c1e] text-[30px] tracking-[-0.75px] whitespace-nowrap">
        <p className="leading-[36px]">Sensation Profile</p>
      </div>
    </div>
  );
}

function Container2() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0 w-full" data-name="Container">
      <div className="flex flex-col font-['Inter:Medium',sans-serif] font-medium justify-center leading-[0] not-italic relative shrink-0 text-[#424752] text-[14px] whitespace-nowrap">
        <p className="leading-[20px]">Current Focus: Left Shoulder Neuropathy</p>
      </div>
    </div>
  );
}

function Container1() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0 w-[275px]" data-name="Container">
      <Heading />
      <Container2 />
    </div>
  );
}

function Container4() {
  return (
    <div className="relative shrink-0" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col items-start relative size-full">
        <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[#005eb8] text-[10px] tracking-[1px] uppercase whitespace-nowrap">
          <p className="leading-[15px]">ACTIVE SCAN</p>
        </div>
      </div>
    </div>
  );
}

function OverlayBorder() {
  return (
    <div className="bg-[rgba(0,94,184,0.1)] relative rounded-[12px] self-stretch shrink-0" data-name="Overlay+Border">
      <div aria-hidden="true" className="absolute border border-[rgba(0,94,184,0.2)] border-solid inset-0 pointer-events-none rounded-[12px]" />
      <div className="flex flex-row items-center size-full">
        <div className="content-stretch flex gap-[8px] items-center px-[13px] py-[7px] relative size-full">
          <div className="bg-[#005eb8] rounded-[12px] shrink-0 size-[8px]" data-name="Background" />
          <Container4 />
        </div>
      </div>
    </div>
  );
}

function Container3() {
  return (
    <div className="content-stretch flex h-[29px] items-start relative shrink-0" data-name="Container">
      <OverlayBorder />
    </div>
  );
}

function HeaderSection() {
  return (
    <div className="content-stretch flex items-start justify-between relative shrink-0 w-full" data-name="Header Section">
      <Container1 />
      <Container3 />
    </div>
  );
}

function HeaderSectionMargin() {
  return (
    <div className="content-stretch flex flex-col items-start pb-[16px] relative shrink-0 w-full" data-name="Header Section:margin">
      <HeaderSection />
    </div>
  );
}

function Container5() {
  return (
    <div className="relative shrink-0 size-[10.5px]" data-name="Container">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 10.5 10.5">
        <g id="Container">
          <path d={svgPaths.p3f18d400} fill="var(--fill-0, #424752)" id="Icon" />
        </g>
      </svg>
    </div>
  );
}

function Heading1() {
  return (
    <div className="content-stretch flex gap-[8px] items-center relative shrink-0 w-full" data-name="Heading 3">
      <Container5 />
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[#424752] text-[10px] tracking-[1.5px] uppercase whitespace-nowrap">
        <p className="leading-[15px]">IDENTIFIED PAIN SPOTS</p>
      </div>
    </div>
  );
}

function Heading3Margin() {
  return (
    <div className="relative shrink-0 w-full" data-name="Heading 3:margin">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col items-start pb-[12px] relative size-full">
        <Heading1 />
      </div>
    </div>
  );
}

function Container8() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0 w-full" data-name="Container">
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[#191c1e] text-[12px] whitespace-nowrap">
        <p className="leading-[16px]">Left Shoulder</p>
      </div>
    </div>
  );
}

function Container9() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0 w-full" data-name="Container">
      <div className="flex flex-col font-['Inter:Medium',sans-serif] font-medium justify-center leading-[0] not-italic relative shrink-0 text-[#424752] text-[10px] whitespace-nowrap">
        <p className="leading-[15px]">Tingling • 7.4/10</p>
      </div>
    </div>
  );
}

function Container7() {
  return (
    <div className="relative shrink-0 w-[79px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col items-start relative size-full">
        <Container8 />
        <Container9 />
      </div>
    </div>
  );
}

function Container10() {
  return (
    <div className="h-[7px] relative shrink-0 w-[4.317px]" data-name="Container">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 32 32">
        <g id="Container" opacity="0">
          <path d={svgPaths.p35022f90} fill="var(--fill-0, #191C1E)" id="Icon" />
        </g>
      </svg>
    </div>
  );
}

function BackgroundVerticalBorderShadow() {
  return (
    <div className="bg-white relative rounded-[16px] shrink-0 w-full" data-name="Background+VerticalBorder+Shadow">
      <div aria-hidden="true" className="absolute border-[#005eb8] border-l-4 border-solid inset-0 pointer-events-none rounded-[16px] shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)]" />
      <div className="flex flex-row items-center size-full">
        <div className="content-stretch flex items-center justify-between pl-[16px] pr-[12px] py-[12px] relative size-full">
          <Container7 />
          <Container10 />
        </div>
      </div>
    </div>
  );
}

function Container12() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0 w-full" data-name="Container">
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[#191c1e] text-[12px] whitespace-nowrap">
        <p className="leading-[16px]">Lower Lumbar</p>
      </div>
    </div>
  );
}

function Container13() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0 w-full" data-name="Container">
      <div className="flex flex-col font-['Inter:Medium',sans-serif] font-medium justify-center leading-[0] not-italic relative shrink-0 text-[#424752] text-[10px] whitespace-nowrap">
        <p className="leading-[15px]">Aching • 4.2/10</p>
      </div>
    </div>
  );
}

function Container11() {
  return (
    <div className="relative shrink-0 w-[82.89px]" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col items-start relative size-full">
        <Container12 />
        <Container13 />
      </div>
    </div>
  );
}

function Container14() {
  return (
    <div className="h-[7px] relative shrink-0 w-[4.317px]" data-name="Container">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 32 32">
        <g id="Container" opacity="0">
          <path d={svgPaths.p35022f90} fill="var(--fill-0, #191C1E)" id="Icon" />
        </g>
      </svg>
    </div>
  );
}

function BackgroundVerticalBorder() {
  return (
    <div className="bg-[#f2f4f7] relative rounded-[16px] shrink-0 w-full" data-name="Background+VerticalBorder">
      <div aria-hidden="true" className="absolute border-[rgba(114,119,131,0.3)] border-l-4 border-solid inset-0 pointer-events-none rounded-[16px]" />
      <div className="flex flex-row items-center size-full">
        <div className="content-stretch flex items-center justify-between pl-[16px] pr-[12px] py-[12px] relative size-full">
          <Container11 />
          <Container14 />
        </div>
      </div>
    </div>
  );
}

function Container6() {
  return (
    <div className="max-h-[300px] relative shrink-0 w-full" data-name="Container">
      <div className="max-h-[inherit] overflow-clip rounded-[inherit] size-full">
        <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col gap-[8px] items-start max-h-[inherit] pr-[8px] relative size-full">
          <BackgroundVerticalBorderShadow />
          <BackgroundVerticalBorder />
        </div>
      </div>
    </div>
  );
}

function Container15() {
  return (
    <div className="h-[11.667px] relative shrink-0 w-[9.333px]" data-name="Container">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 9.33333 11.6667">
        <g id="Container">
          <path d={svgPaths.p7a77700} fill="var(--fill-0, #005EB8)" id="Icon" />
        </g>
      </svg>
    </div>
  );
}

function Button() {
  return (
    <div className="content-stretch flex gap-[7.99px] items-center justify-center px-[54.88px] py-[9px] relative rounded-[8px] shrink-0" data-name="Button">
      <div aria-hidden="true" className="absolute border border-[rgba(0,94,184,0.2)] border-solid inset-0 pointer-events-none rounded-[8px]" />
      <Container15 />
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[#005eb8] text-[10px] text-center uppercase whitespace-nowrap">
        <p className="leading-[15px]">TRACK NEW SPOT</p>
      </div>
    </div>
  );
}

function ButtonMargin() {
  return (
    <div className="relative shrink-0" data-name="Button:margin">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col items-start pt-[16px] relative size-full">
        <Button />
      </div>
    </div>
  );
}

function OverlayBorderOverlayBlur() {
  return (
    <div className="backdrop-blur-[2px] bg-[rgba(224,227,230,0.5)] relative rounded-[24px] shrink-0 w-full" data-name="Overlay+Border+OverlayBlur">
      <div aria-hidden="true" className="absolute border border-[rgba(194,198,212,0.3)] border-solid inset-0 pointer-events-none rounded-[24px]" />
      <div className="content-stretch flex flex-col items-start p-[17px] relative size-full">
        <Heading3Margin />
        <Container6 />
        <ButtonMargin />
      </div>
    </div>
  );
}

function Container16() {
  return (
    <div className="content-stretch flex flex-col items-start opacity-80 relative shrink-0 w-full" data-name="Container">
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[10px] text-white tracking-[2px] uppercase w-full">
        <p className="leading-[15px]">INTENSITY INDEX</p>
      </div>
    </div>
  );
}

function Paragraph() {
  return (
    <div className="content-stretch flex gap-[4px] items-baseline leading-[0] relative shrink-0 text-white w-full whitespace-nowrap" data-name="Paragraph">
      <div className="flex flex-col font-['Manrope:ExtraBold',sans-serif] font-extrabold justify-center relative shrink-0 text-[48px] tracking-[-2.4px]">
        <p className="leading-[48px]">7.4</p>
      </div>
      <div className="flex flex-col font-['Inter:Medium',sans-serif] font-medium justify-center not-italic opacity-60 relative shrink-0 text-[14px]">
        <p className="leading-[20px]">/ 10</p>
      </div>
    </div>
  );
}

function Margin() {
  return (
    <div className="content-stretch flex flex-col items-start py-[8px] relative shrink-0 w-full" data-name="Margin">
      <Paragraph />
    </div>
  );
}

function Overlay() {
  return (
    <div className="bg-[rgba(255,255,255,0.2)] h-[6px] overflow-clip relative rounded-[12px] shrink-0 w-full" data-name="Overlay">
      <div className="absolute bg-white inset-[0_26%_0_0] shadow-[0px_0px_8px_0px_rgba(255,255,255,0.5)]" data-name="Background+Shadow" />
    </div>
  );
}

function IntensityCardMovedHereToFreeUpCentralSpace() {
  return (
    <div className="bg-[#005eb8] relative rounded-[24px] shrink-0 w-full" data-name="Intensity Card moved here to free up central space">
      <div className="content-stretch flex flex-col items-start justify-between p-[20px] relative size-full">
        <div className="absolute bg-[rgba(255,255,255,0)] inset-0 rounded-[24px] shadow-[0px_10px_15px_-3px_rgba(0,94,184,0.2),0px_4px_6px_-4px_rgba(0,94,184,0.2)]" data-name="Intensity Card moved here to free up central space:shadow" />
        <Container16 />
        <Margin />
        <Overlay />
      </div>
    </div>
  );
}

function LeftMultiplePainSpotsSection() {
  return (
    <div className="content-stretch flex flex-col gap-[16px] h-full items-start relative shrink-0 w-[256px]" data-name="Left: Multiple Pain Spots Section">
      <OverlayBorderOverlayBlur />
      <IntensityCardMovedHereToFreeUpCentralSpace />
    </div>
  );
}

function FrontalAnatomicalView() {
  return (
    <div className="flex-[1_0_0] min-h-px opacity-20 relative w-full" data-name="Frontal anatomical view">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <img alt="" className="absolute h-[52.36%] left-0 max-w-none top-[27.33%] w-[101.74%]" src={imgFrontalAnatomicalView} />
      </div>
    </div>
  );
}

function OverlayBorder1() {
  return (
    <div className="relative shrink-0 size-[40px]" data-name="Overlay+Border">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 40 40">
        <g id="Overlay+Border">
          <rect fill="var(--fill-0, #005EB8)" fillOpacity="0.3" height="40" rx="12" width="40" />
          <rect height="38" rx="11" stroke="var(--stroke-0, #005EB8)" strokeOpacity="0.4" strokeWidth="2" width="38" x="1" y="1" />
          <path d={svgPaths.p186990f0} fill="var(--fill-0, #005EB8)" id="Exclude" />
        </g>
      </svg>
    </div>
  );
}

function KneeIndicatorWithMagnifiedSubregionCta() {
  return (
    <div className="absolute backdrop-blur-[4px] content-stretch flex inset-[34.37%_6.02%_57.55%_59.6%] items-center justify-center rounded-[12px]" style={{ backgroundImage: "url('data:image/svg+xml;utf8,<svg viewBox=\\'0 0 60 60\\' xmlns=\\'http://www.w3.org/2000/svg\\' preserveAspectRatio=\\'none\\'><rect x=\\'0\\' y=\\'0\\' height=\\'100%\\' width=\\'100%\\' fill=\\'url(%23grad)\\' opacity=\\'1\\'/><defs><radialGradient id=\\'grad\\' gradientUnits=\\'userSpaceOnUse\\' cx=\\'0\\' cy=\\'0\\' r=\\'10\\' gradientTransform=\\'matrix(4.2426 0 0 4.2426 30 30)\\'><stop stop-color=\\'rgba(0,94,184,0.3)\\' offset=\\'0\\'/><stop stop-color=\\'rgba(0,94,184,0)\\' offset=\\'0.7\\'/></radialGradient></defs></svg>')" }} data-name="Knee Indicator with Magnified Subregion CTA">
      <OverlayBorder1 />
    </div>
  );
}

function Container18() {
  return (
    <div className="content-stretch flex flex-[1_0_0] flex-col items-start justify-center min-h-px relative w-full" data-name="Container">
      <FrontalAnatomicalView />
      <KneeIndicatorWithMagnifiedSubregionCta />
    </div>
  );
}

function FrontView() {
  return (
    <div className="h-full relative shrink-0 w-[270.5px]" data-name="Front View">
      <div className="flex flex-col items-center justify-center size-full">
        <div className="content-stretch flex flex-col items-center justify-center p-[48px] relative size-full">
          <div className="-translate-y-1/2 absolute flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] left-[88.69px] not-italic opacity-40 text-[#727783] text-[10px] top-[31.5px] tracking-[3px] uppercase whitespace-nowrap">
            <p className="leading-[15px]">FRONT VIEW</p>
          </div>
          <Container18 />
        </div>
      </div>
    </div>
  );
}

function OverlayBorder2() {
  return (
    <div className="bg-[#005eb8] content-stretch flex items-center justify-center p-[2px] relative rounded-[12px] shrink-0 size-[40px]" data-name="Overlay+Border">
      <div aria-hidden="true" className="absolute border-2 border-[#005eb8] border-solid inset-0 pointer-events-none rounded-[12px]" />
      <div className="bg-[#005eb8] rounded-[12px] shrink-0 size-[12px]" data-name="Background" />
    </div>
  );
}

function KneeIndicatorWithMagnifiedSubregionCta1() {
  return (
    <div className="absolute backdrop-blur-[4px] content-stretch flex inset-[34.23%_56.16%_57.68%_9.46%] items-center justify-center rounded-[12px]" style={{ backgroundImage: "url('data:image/svg+xml;utf8,<svg viewBox=\\'0 0 60 60\\' xmlns=\\'http://www.w3.org/2000/svg\\' preserveAspectRatio=\\'none\\'><rect x=\\'0\\' y=\\'0\\' height=\\'100%\\' width=\\'100%\\' fill=\\'url(%23grad)\\' opacity=\\'1\\'/><defs><radialGradient id=\\'grad\\' gradientUnits=\\'userSpaceOnUse\\' cx=\\'0\\' cy=\\'0\\' r=\\'10\\' gradientTransform=\\'matrix(4.2426 0 0 4.2426 30 30)\\'><stop stop-color=\\'rgba(0,94,184,0.3)\\' offset=\\'0\\'/><stop stop-color=\\'rgba(0,94,184,0)\\' offset=\\'0.7\\'/></radialGradient></defs></svg>')" }} data-name="Knee Indicator with Magnified Subregion CTA">
      <OverlayBorder2 />
    </div>
  );
}

function PosteriorAnatomicalView() {
  return (
    <div className="flex-[1_0_0] min-h-px opacity-20 relative w-full" data-name="Posterior anatomical view">
      <div className="absolute bg-clip-padding border-0 border-[transparent] border-solid inset-0 overflow-hidden pointer-events-none">
        <img alt="" className="absolute h-[51.4%] left-[1.7%] max-w-none top-[27.12%] w-[98.3%]" src={imgPosteriorAnatomicalView} />
      </div>
      <div className="bg-clip-padding border-0 border-[transparent] border-solid overflow-clip relative rounded-[inherit] size-full">
        <KneeIndicatorWithMagnifiedSubregionCta1 />
      </div>
    </div>
  );
}

function BackView() {
  return (
    <div className="h-full relative shrink-0 w-[271.5px]" data-name="Back View">
      <div aria-hidden="true" className="absolute border-[rgba(194,198,212,0.1)] border-l border-solid inset-0 pointer-events-none" />
      <div className="flex flex-col items-center justify-center size-full">
        <div className="content-stretch flex flex-col items-center justify-center pl-[49px] pr-[48px] py-[48px] relative size-full">
          <div className="-translate-y-1/2 absolute flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] left-[94.39px] not-italic opacity-40 text-[#727783] text-[10px] top-[31.5px] tracking-[3px] uppercase whitespace-nowrap">
            <p className="leading-[15px]">BACK VIEW</p>
          </div>
          <PosteriorAnatomicalView />
        </div>
      </div>
    </div>
  );
}

function Container17() {
  return (
    <div className="absolute content-stretch flex inset-px items-start justify-center" data-name="Container">
      <FrontView />
      <BackView />
    </div>
  );
}

function Container20() {
  return (
    <div className="content-stretch flex flex-col items-center relative shrink-0" data-name="Container">
      <div className="flex flex-col font-['Manrope:ExtraBold',sans-serif] font-extrabold justify-center leading-[0] relative shrink-0 text-[#eff1f4] text-[9.081px] text-center tracking-[-0.227px] whitespace-nowrap">
        <p className="leading-[12.973px]">Magnify Focus Area</p>
      </div>
    </div>
  );
}

function Container21() {
  return (
    <div className="content-stretch flex flex-col items-center opacity-70 relative shrink-0" data-name="Container">
      <div className="flex flex-col font-['Inter:Medium',sans-serif] font-medium justify-center leading-[0] not-italic relative shrink-0 text-[#eff1f4] text-[6.486px] text-center whitespace-nowrap">
        <p className="leading-[9.73px]">Fine-tune marker placement</p>
      </div>
    </div>
  );
}

function Container19() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0" data-name="Container">
      <Container20 />
      <Container21 />
    </div>
  );
}

function Container22() {
  return (
    <div className="relative shrink-0 size-[11.676px]" data-name="Container">
      <div className="absolute inset-[0_-54.17%_-54.17%_0]">
        <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 18 18">
          <g id="Container">
            <path d={svgPaths.p3fc48a20} fill="var(--fill-0, #EFF1F4)" id="Icon" />
          </g>
        </svg>
      </div>
    </div>
  );
}

function Button1() {
  return (
    <div className="bg-[#2d3133] content-stretch flex gap-[7.777px] items-center px-[15.568px] py-[10.378px] relative rounded-[15.568px] shrink-0" data-name="Button">
      <div className="absolute bg-[rgba(255,255,255,0)] inset-[0_-0.89px_-0.7px_0] rounded-[15.568px] shadow-[0px_16.216px_32.432px_-7.784px_rgba(0,0,0,0.25)]" data-name="Button:shadow" />
      <Container19 />
      <Container22 />
    </div>
  );
}

function FloatingZoomSubregionFeature() {
  return (
    <div className="absolute bottom-[68px] content-stretch flex flex-col h-[48px] items-start right-[31.43px] w-[135.568px]" data-name="Floating Zoom Subregion Feature">
      <Button1 />
    </div>
  );
}

function Container23() {
  return (
    <div className="h-[8.75px] relative shrink-0 w-[12.833px]" data-name="Container">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 12.8333 8.75">
        <g id="Container">
          <path d={svgPaths.p1b1e2a00} fill="var(--fill-0, #191C1E)" id="Icon" />
        </g>
      </svg>
    </div>
  );
}

function Button2() {
  return (
    <div className="bg-white relative rounded-[8px] shrink-0" data-name="Button">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex gap-[8px] items-center px-[16px] py-[8px] relative size-full">
        <div className="absolute bg-[rgba(255,255,255,0)] inset-[0_-0.19px_0_0] rounded-[8px] shadow-[0px_0px_0px_1px_rgba(0,0,0,0.05),0px_1px_2px_0px_rgba(0,0,0,0.05)]" data-name="Button:shadow" />
        <Container23 />
        <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[#191c1e] text-[10px] text-center uppercase whitespace-nowrap">
          <p className="leading-[15px] mb-0">SKELETAL</p>
          <p className="leading-[15px]">LAYER</p>
        </div>
      </div>
    </div>
  );
}

function Container24() {
  return (
    <div className="relative shrink-0 size-[10.5px]" data-name="Container">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 10.5 10.5">
        <g id="Container">
          <path d={svgPaths.p1bef900} fill="var(--fill-0, #191C1E)" id="Icon" />
        </g>
      </svg>
    </div>
  );
}

function Button3() {
  return (
    <div className="relative rounded-[8px] shrink-0" data-name="Button">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex gap-[8px] items-center px-[16px] py-[8px] relative size-full">
        <Container24 />
        <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[#191c1e] text-[10px] text-center uppercase whitespace-nowrap">
          <p className="leading-[15px] mb-0">NERVE</p>
          <p className="leading-[15px]">MAP</p>
        </div>
      </div>
    </div>
  );
}

function Margin1() {
  return (
    <div className="h-[24px] relative shrink-0 w-[8.59px]" data-name="Margin">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col items-start px-[4px] relative size-full">
        <div className="bg-[rgba(194,198,212,0.3)] h-[24px] shrink-0 w-[0.59px]" data-name="Vertical Divider" />
      </div>
    </div>
  );
}

function Container25() {
  return (
    <div className="relative shrink-0 size-[10.5px]" data-name="Container">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 10.5 10.5">
        <g id="Container">
          <path d={svgPaths.p1c1607c0} fill="var(--fill-0, #191C1E)" id="Icon" />
        </g>
      </svg>
    </div>
  );
}

function Button4() {
  return (
    <div className="relative rounded-[8px] shrink-0" data-name="Button">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex gap-[8.19px] items-center px-[16px] py-[8px] relative size-full">
        <Container25 />
        <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[#191c1e] text-[10px] text-center uppercase whitespace-nowrap">
          <p className="leading-[15px] mb-0">SESSION</p>
          <p className="leading-[15px]">HISTORY</p>
        </div>
      </div>
    </div>
  );
}

function OverlayLayerControlsAtBottomOfMap() {
  return (
    <div className="absolute backdrop-blur-[6px] bg-[rgba(224,227,230,0.6)] bottom-[25px] content-stretch flex gap-[8px] items-center left-[19.45%] p-[5px] right-[19.45%] rounded-[16px]" data-name="Overlay Layer Controls at Bottom of Map">
      <div aria-hidden="true" className="absolute border border-[rgba(255,255,255,0.2)] border-solid inset-0 pointer-events-none rounded-[16px]" />
      <Button2 />
      <Button3 />
      <Margin1 />
      <Button4 />
    </div>
  );
}

function CenterEnhancedAnatomicalMapping() {
  return (
    <div className="bg-white flex-[1_0_0] h-full min-w-px relative rounded-[40px]" data-name="Center: Enhanced Anatomical Mapping">
      <div className="overflow-clip relative rounded-[inherit] size-full">
        <Container17 />
        <FloatingZoomSubregionFeature />
        <OverlayLayerControlsAtBottomOfMap />
      </div>
      <div aria-hidden="true" className="absolute border border-[rgba(194,198,212,0.1)] border-solid inset-0 pointer-events-none rounded-[40px] shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)]" />
    </div>
  );
}

function Container27() {
  return (
    <div className="relative shrink-0 size-[13.333px]" data-name="Container">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 13.3333 13.3333">
        <g id="Container">
          <path d={svgPaths.p326ab500} fill="var(--fill-0, #005EB8)" id="Icon" />
        </g>
      </svg>
    </div>
  );
}

function Overlay1() {
  return (
    <div className="bg-[rgba(0,94,184,0.1)] content-stretch flex items-center justify-center relative rounded-[12px] shrink-0 size-[32px]" data-name="Overlay">
      <Container27 />
    </div>
  );
}

function Container26() {
  return (
    <div className="content-stretch flex items-start justify-between relative shrink-0 w-full" data-name="Container">
      <div className="flex flex-col font-['Manrope:ExtraBold',sans-serif] font-extrabold justify-center leading-[0] relative shrink-0 text-[#191c1e] text-[18px] whitespace-nowrap">
        <p className="leading-[28px]">Current Sensation</p>
      </div>
      <Overlay1 />
    </div>
  );
}

function Margin2() {
  return (
    <div className="relative shrink-0 w-full" data-name="Margin">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col items-start pb-[16px] relative size-full">
        <Container26 />
      </div>
    </div>
  );
}

function Container30() {
  return (
    <div className="content-stretch flex flex-col items-start pb-[3.5px] relative shrink-0 w-full" data-name="Container">
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[#191c1e] text-[14px] w-full">
        <p className="leading-[20px]">{`Tingling & Paresthesia`}</p>
      </div>
    </div>
  );
}

function OverlayBorder3() {
  return (
    <div className="bg-[rgba(0,94,184,0.05)] h-[32px] relative rounded-[8px] shrink-0 w-full" data-name="Overlay+Border">
      <div className="content-stretch flex flex-col items-start justify-center overflow-clip p-px relative rounded-[inherit] size-full">
        <div className="flex-[1_0_0] min-h-px opacity-30 w-full" style={{ backgroundImage: "url('data:image/svg+xml;utf8,<svg viewBox=\\'0 0 260 30\\' xmlns=\\'http://www.w3.org/2000/svg\\' preserveAspectRatio=\\'none\\'><rect x=\\'0\\' y=\\'0\\' height=\\'100%\\' width=\\'100%\\' fill=\\'url(%23grad)\\' opacity=\\'1\\'/><defs><radialGradient id=\\'grad\\' gradientUnits=\\'userSpaceOnUse\\' cx=\\'0\\' cy=\\'0\\' r=\\'10\\' gradientTransform=\\'matrix(18.385 0 0 2.1213 130 15)\\'><stop stop-color=\\'rgba(0,94,184,1)\\' offset=\\'0.17678\\'/><stop stop-color=\\'rgba(0,94,184,0)\\' offset=\\'0.17678\\'/></radialGradient></defs></svg>')" }} data-name="Gradient" />
      </div>
      <div aria-hidden="true" className="absolute border border-[rgba(0,94,184,0.1)] border-solid inset-0 pointer-events-none rounded-[8px]" />
    </div>
  );
}

function Container29() {
  return (
    <div className="content-stretch flex flex-col gap-[4.5px] items-start relative shrink-0 w-full" data-name="Container">
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[#727783] text-[10px] tracking-[1px] uppercase whitespace-nowrap">
        <p className="leading-[15px]">QUALITY</p>
      </div>
      <Container30 />
      <OverlayBorder3 />
    </div>
  );
}

function Container32() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0 w-full" data-name="Container">
      <div className="flex flex-col font-['Inter:Medium',sans-serif] font-medium justify-center leading-[0] not-italic relative shrink-0 text-[#191c1e] text-[14px] w-full">
        <p className="leading-[20px]">Persistent (4h+)</p>
      </div>
    </div>
  );
}

function Container31() {
  return (
    <div className="content-stretch flex flex-col gap-[4.5px] items-start relative shrink-0 w-full" data-name="Container">
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[#727783] text-[10px] tracking-[1px] uppercase whitespace-nowrap">
        <p className="leading-[15px]">DURATION</p>
      </div>
      <Container32 />
    </div>
  );
}

function Container34() {
  return (
    <div className="relative shrink-0 w-full" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col items-start relative size-full">
        <div className="flex flex-col font-['Inter:Italic',sans-serif] font-normal italic justify-center leading-[0] relative shrink-0 text-[#424752] text-[12px] w-full">
          <p className="leading-[19.5px] mb-0">{`"Patient describes a 'static' feeling that`}</p>
          <p className="leading-[19.5px] mb-0">intensifies during flexion. No visible</p>
          <p className="leading-[19.5px] mb-0">inflammation observed. Reported</p>
          <p className="leading-[19.5px]">{`sensitivity to cold drafts."`}</p>
        </div>
      </div>
    </div>
  );
}

function BackgroundVerticalBorderShadow1() {
  return (
    <div className="relative rounded-[16px] shrink-0 w-full" data-name="Background+VerticalBorder+Shadow">
      <div aria-hidden="true" className="absolute bg-[#f7f9fc] inset-0 pointer-events-none rounded-[16px]" />
      <div aria-hidden="true" className="absolute border-[#005eb8] border-l-4 border-solid inset-0 pointer-events-none rounded-[16px]" />
      <div className="content-stretch flex flex-col items-start pl-[20px] pr-[16px] py-[16px] relative size-full">
        <Container34 />
      </div>
      <div className="absolute inset-0 pointer-events-none rounded-[inherit] shadow-[inset_0px_2px_4px_0px_rgba(0,0,0,0.05)]" />
    </div>
  );
}

function Container33() {
  return (
    <div className="content-stretch flex flex-col gap-[8.5px] items-start pt-[8px] relative shrink-0 w-full" data-name="Container">
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[#727783] text-[10px] tracking-[1px] uppercase whitespace-nowrap">
        <p className="leading-[15px]">{`CLINICAL NOTES & SYMPTOMS`}</p>
      </div>
      <BackgroundVerticalBorderShadow1 />
    </div>
  );
}

function Container35() {
  return (
    <div className="content-stretch flex flex-[1_0_0] flex-col items-start min-w-px relative" data-name="Container">
      <div className="flex flex-col font-['Inter:Medium',sans-serif] font-medium justify-center leading-[0] not-italic relative shrink-0 text-[12px] text-[rgba(114,119,131,0.5)] w-full">
        <p className="leading-[16px]">Type notes here for your appointment...</p>
      </div>
    </div>
  );
}

function Textarea() {
  return (
    <div className="bg-[#f2f4f7] min-h-[100px] relative rounded-[16px] shrink-0 w-full" data-name="Textarea">
      <div className="flex flex-row justify-center min-h-[inherit] overflow-clip rounded-[inherit] size-full">
        <div className="content-stretch flex items-start justify-center min-h-[inherit] pb-[68px] pt-[16px] px-[16px] relative size-full">
          <Container35 />
        </div>
      </div>
    </div>
  );
}

function ExpandedNotesInputSection() {
  return (
    <div className="content-stretch flex flex-col gap-[8.5px] items-start relative shrink-0 w-full" data-name="Expanded Notes Input Section">
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[#727783] text-[10px] tracking-[1px] uppercase whitespace-nowrap">
        <p className="leading-[15px]">ADD OBSERVATION</p>
      </div>
      <Textarea />
    </div>
  );
}

function Container28() {
  return (
    <div className="relative shrink-0 w-full" data-name="Container">
      <div className="overflow-clip rounded-[inherit] size-full">
        <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col gap-[20px] items-start pr-[8px] relative size-full">
          <Container29 />
          <Container31 />
          <Container33 />
          <ExpandedNotesInputSection />
        </div>
      </div>
    </div>
  );
}

function Container36() {
  return (
    <div className="relative shrink-0 size-[11.667px]" data-name="Container">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 11.6667 11.6667">
        <g id="Container">
          <path d={svgPaths.p957df70} fill="var(--fill-0, white)" id="Icon" />
        </g>
      </svg>
    </div>
  );
}

function Button5() {
  return (
    <div className="bg-[#005eb8] content-stretch flex gap-[8px] items-center justify-center py-[16px] relative rounded-[16px] shrink-0 w-full" data-name="Button">
      <div className="absolute bg-[rgba(255,255,255,0)] inset-0 rounded-[16px] shadow-[0px_4px_6px_-1px_rgba(0,0,0,0.1),0px_2px_4px_-2px_rgba(0,0,0,0.1)]" data-name="Button:shadow" />
      <Container36 />
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[12px] text-center text-white tracking-[1.2px] uppercase whitespace-nowrap">
        <p className="leading-[16px]">ADD CUSTOM SYMPTOM</p>
      </div>
    </div>
  );
}

function ButtonMargin1() {
  return (
    <div className="relative shrink-0 w-full" data-name="Button:margin">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col items-start pt-[16px] relative size-full">
        <Button5 />
      </div>
    </div>
  );
}

function BackgroundBorderShadow() {
  return (
    <div className="bg-white flex-[1_0_0] min-h-px relative rounded-[40px] w-full" data-name="Background+Border+Shadow">
      <div className="overflow-clip rounded-[inherit] size-full">
        <div className="content-stretch flex flex-col items-start p-[25px] relative size-full">
          <Margin2 />
          <Container28 />
          <ButtonMargin1 />
        </div>
      </div>
      <div aria-hidden="true" className="absolute border border-[rgba(194,198,212,0.2)] border-solid inset-0 pointer-events-none rounded-[40px] shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)]" />
    </div>
  );
}

function RightExpandedClinicalNotesSensationDetails() {
  return (
    <div className="content-stretch flex flex-col h-full items-start justify-center relative shrink-0 w-[320px]" data-name="Right: Expanded Clinical Notes & Sensation Details">
      <BackgroundBorderShadow />
    </div>
  );
}

function MainLayout3Columns() {
  return (
    <div className="content-stretch flex flex-[1_0_0] gap-[24px] items-start min-h-px relative w-full" data-name="Main Layout: 3 Columns">
      <LeftMultiplePainSpotsSection />
      <CenterEnhancedAnatomicalMapping />
      <RightExpandedClinicalNotesSensationDetails />
    </div>
  );
}

function MainContentArea() {
  return (
    <div className="flex-[1_0_0] h-full min-w-px relative" style={{ backgroundImage: "url('data:image/svg+xml;utf8,<svg viewBox=\\'0 0 1216 960\\' xmlns=\\'http://www.w3.org/2000/svg\\' preserveAspectRatio=\\'none\\'><rect x=\\'0\\' y=\\'0\\' height=\\'100%\\' width=\\'100%\\' fill=\\'url(%23grad)\\' opacity=\\'1\\'/><defs><radialGradient id=\\'grad\\' gradientUnits=\\'userSpaceOnUse\\' cx=\\'0\\' cy=\\'0\\' r=\\'10\\' gradientTransform=\\'matrix(77.464 0 0 77.464 608 480)\\'><stop stop-color=\\'rgba(242,244,247,1)\\' offset=\\'0\\'/><stop stop-color=\\'rgba(247,249,252,1)\\' offset=\\'1\\'/></radialGradient></defs></svg>')" }} data-name="Main Content Area">
      <div className="overflow-clip rounded-[inherit] size-full">
        <div className="content-stretch flex flex-col items-start p-[24px] relative size-full">
          <HeaderSectionMargin />
          <MainLayout3Columns />
        </div>
      </div>
    </div>
  );
}

function Container() {
  return (
    <div className="h-[1024px] relative shrink-0 w-full" data-name="Container">
      <div className="flex flex-row justify-center size-full">
        <div className="content-stretch flex items-start justify-center pl-[64px] pt-[64px] relative size-full">
          <MainContentArea />
        </div>
      </div>
    </div>
  );
}

function Container40() {
  return (
    <div className="h-[20px] relative shrink-0 w-[18px]" data-name="Container">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 18 20">
        <g id="Container">
          <path d={svgPaths.p21ae1ac0} fill="var(--fill-0, #00478D)" id="Icon" />
        </g>
      </svg>
    </div>
  );
}

function Background() {
  return (
    <div className="bg-[#e0e3e6] content-stretch flex items-center justify-center relative rounded-[12px] shrink-0 size-[40px]" data-name="Background">
      <Container40 />
    </div>
  );
}

function Margin4() {
  return (
    <div className="content-stretch flex flex-col h-[44px] items-start pb-[4px] relative shrink-0 w-[40px]" data-name="Margin">
      <Background />
    </div>
  );
}

function Container41() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0" data-name="Container">
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[#424752] text-[10px] tracking-[-0.5px] uppercase whitespace-nowrap">
        <p className="leading-[15px]">VIEW</p>
      </div>
    </div>
  );
}

function Container39() {
  return (
    <div className="content-stretch flex flex-col items-center relative shrink-0" data-name="Container">
      <Margin4 />
      <Container41 />
    </div>
  );
}

function Margin3() {
  return (
    <div className="content-stretch flex flex-col h-[86px] items-start pb-[32px] relative shrink-0" data-name="Margin">
      <Container39 />
    </div>
  );
}

function Container42() {
  return (
    <div className="h-[19px] relative shrink-0 w-[16px]" data-name="Container">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 16 19">
        <g id="Container">
          <path d={svgPaths.p38fbbc00} fill="var(--fill-0, #424752)" id="Icon" />
        </g>
      </svg>
    </div>
  );
}

function Button6() {
  return (
    <div className="content-stretch flex items-center justify-center relative rounded-[4px] shrink-0 size-[48px]" data-name="Button">
      <Container42 />
    </div>
  );
}

function Container43() {
  return (
    <div className="-translate-x-1/2 -translate-y-1/2 absolute h-[16px] left-1/2 top-1/2 w-[20px]" data-name="Container">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 20 16">
        <g id="Container">
          <path d={svgPaths.p3e7e25c0} fill="var(--fill-0, #424752)" id="Icon" />
        </g>
      </svg>
    </div>
  );
}

function Button7() {
  return (
    <div className="relative rounded-[4px] shrink-0 size-[48px]" data-name="Button">
      <Container43 />
    </div>
  );
}

function Container44() {
  return (
    <div className="h-[20px] relative shrink-0 w-[16px]" data-name="Container">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 16 20">
        <g id="Container">
          <path d={svgPaths.p12df5c00} fill="var(--fill-0, #424752)" id="Icon" />
        </g>
      </svg>
    </div>
  );
}

function Button8() {
  return (
    <div className="content-stretch flex items-center justify-center relative rounded-[4px] shrink-0 size-[48px]" data-name="Button">
      <Container44 />
    </div>
  );
}

function Container38() {
  return (
    <div className="content-stretch flex flex-col gap-[16px] h-[169px] items-center relative shrink-0" data-name="Container">
      <Margin3 />
      <Button6 />
      <Button7 />
      <Button8 />
    </div>
  );
}

function Button9() {
  return (
    <div className="content-stretch flex flex-col items-center relative shrink-0" data-name="Button">
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic opacity-0 relative shrink-0 text-[#424752] text-[8px] text-center uppercase whitespace-nowrap">
        <p className="leading-[12px]">REGION</p>
      </div>
    </div>
  );
}

function Button10() {
  return (
    <div className="content-stretch flex flex-col gap-[4px] items-center relative shrink-0" data-name="Button">
      <div className="h-[15px] relative shrink-0 w-[15.833px]" data-name="Icon">
        <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 15.8333 15">
          <path d={svgPaths.p251be100} fill="var(--fill-0, #424752)" id="Icon" />
        </svg>
      </div>
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic opacity-0 relative shrink-0 text-[#424752] text-[8px] text-center uppercase whitespace-nowrap">
        <p className="leading-[12px]">DRAW</p>
      </div>
    </div>
  );
}

function Button11() {
  return (
    <div className="content-stretch flex flex-col gap-[4px] items-center relative shrink-0" data-name="Button">
      <div className="relative shrink-0 size-[15.833px]" data-name="Icon">
        <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 15.8333 15.8333">
          <path d={svgPaths.p8062180} fill="var(--fill-0, #424752)" id="Icon" />
        </svg>
      </div>
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic opacity-0 relative shrink-0 text-[#424752] text-[8px] text-center uppercase whitespace-nowrap">
        <p className="leading-[12px]">REGION</p>
      </div>
    </div>
  );
}

function Container46() {
  return (
    <div className="content-stretch flex flex-col gap-[32px] h-[258.417px] items-center relative shrink-0 w-[63px]" data-name="Container">
      <div className="bg-[#e0e3e6] h-px shrink-0 w-[32px]" data-name="Horizontal Divider" />
      <Button10 />
      <Button11 />
    </div>
  );
}

function Container45() {
  return (
    <div className="content-stretch flex flex-col gap-[32px] h-[148px] items-center relative shrink-0 w-[63px]" data-name="Container">
      <div className="bg-[#e0e3e6] h-px shrink-0 w-[32px]" data-name="Horizontal Divider" />
      <Button9 />
      <Container46 />
    </div>
  );
}

function Margin5() {
  return (
    <div className="h-[317px] min-h-[64px] relative shrink-0 w-[18px]" data-name="Margin">
      <div className="flex flex-col justify-end min-h-[inherit] size-full">
        <div className="min-h-[inherit] size-full" />
      </div>
    </div>
  );
}

function Container48() {
  return (
    <div className="h-[21.5px] relative shrink-0 w-[13px]" data-name="Container">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 13 21.5">
        <g id="Container">
          <path d={svgPaths.p239f6000} fill="var(--fill-0, #94A3B8)" id="Icon" />
        </g>
      </svg>
    </div>
  );
}

function Container49() {
  return (
    <div className="relative shrink-0 size-[14px]" data-name="Container">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 14 14">
        <g id="Container">
          <path d={svgPaths.p2bb32400} fill="var(--fill-0, #00478D)" id="Icon" />
        </g>
      </svg>
    </div>
  );
}

function Background1() {
  return (
    <div className="bg-[#d6e3ff] content-stretch flex items-center justify-center relative rounded-[4px] shrink-0 size-[40px]" data-name="Background">
      <Container49 />
    </div>
  );
}

function Container47() {
  return (
    <div className="content-stretch flex flex-col gap-[16px] h-[45px] items-center relative shrink-0" data-name="Container">
      <Container48 />
      <Background1 />
    </div>
  );
}

function Container37() {
  return (
    <div className="relative shrink-0 w-full" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col gap-[32px] items-center pt-[54px] relative size-full">
        <Container38 />
        <Container45 />
        <Margin5 />
        <Container47 />
      </div>
    </div>
  );
}

function AsideLeftNavigationBarToolsOnly() {
  return (
    <div className="absolute bg-white content-stretch flex flex-col h-[1024px] items-center left-0 pr-px py-[80px] top-[10px] w-[64px]" data-name="Aside - Left Navigation Bar (Tools Only)">
      <div aria-hidden="true" className="absolute border-[#e0e3e6] border-r border-solid inset-0 pointer-events-none" />
      <Container37 />
    </div>
  );
}

function Container51() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0" data-name="Container">
      <div className="flex flex-col font-['Manrope:Bold',sans-serif] font-bold justify-center leading-[0] relative shrink-0 text-[#00478d] text-[20px] tracking-[-1px] whitespace-nowrap">
        <p className="leading-[28px]">The Pain Hub</p>
      </div>
    </div>
  );
}

function Link() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0" data-name="Link">
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[#424752] text-[14px] whitespace-nowrap">
        <p className="leading-[20px]">Dashboard</p>
      </div>
    </div>
  );
}

function Link1() {
  return (
    <div className="content-stretch flex flex-col items-start pb-[6px] relative shrink-0" data-name="Link">
      <div aria-hidden="true" className="absolute border-[#005eb8] border-b-2 border-solid inset-0 pointer-events-none" />
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[#005eb8] text-[14px] whitespace-nowrap">
        <p className="leading-[20px]">History</p>
      </div>
    </div>
  );
}

function Link2() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0" data-name="Link">
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[#424752] text-[14px] whitespace-nowrap">
        <p className="leading-[20px]">Resources</p>
      </div>
    </div>
  );
}

function Nav() {
  return (
    <div className="content-stretch flex gap-[24px] items-center relative shrink-0" data-name="Nav">
      <Link />
      <Link1 />
      <Link2 />
    </div>
  );
}

function Container50() {
  return (
    <div className="relative shrink-0" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex gap-[40px] items-center relative size-full">
        <Container51 />
        <Nav />
      </div>
    </div>
  );
}

function Container52() {
  return (
    <div className="h-[19px] relative w-[16px]" data-name="Container">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 16 19">
        <g id="Container">
          <path d={svgPaths.p38fbbc00} fill="var(--fill-0, #727783)" id="Icon" />
        </g>
      </svg>
    </div>
  );
}

function ContainerCssTransform() {
  return (
    <div className="content-stretch flex flex-col items-center justify-center pl-[10.08px] pr-[10.1px] relative shrink-0 w-[38.19px]" data-name="Container:css-transform">
      <div className="flex h-[14.25px] items-center justify-center relative shrink-0 w-[12px]" style={{ "--transform-inner-width": "1200", "--transform-inner-height": "19" } as React.CSSProperties}>
        <div className="flex-none scale-x-75 scale-y-75">
          <Container52 />
        </div>
      </div>
    </div>
  );
}

function Container53() {
  return (
    <div className="content-stretch flex flex-col items-center relative shrink-0" data-name="Container">
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[#727783] text-[9px] text-center tracking-[-0.45px] uppercase whitespace-nowrap">
        <p className="leading-[13.5px]">BURNING</p>
      </div>
    </div>
  );
}

function Button12() {
  return (
    <div className="-translate-y-1/2 absolute content-stretch flex flex-col gap-[3px] items-center justify-center left-[5px] pb-[4px] pt-[7px] px-[12px] rounded-[12px] top-1/2" data-name="Button">
      <ContainerCssTransform />
      <Container53 />
    </div>
  );
}

function Container54() {
  return (
    <div className="h-[16px] relative w-[20px]" data-name="Container">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 20 16">
        <g id="Container">
          <path d={svgPaths.p3e7e25c0} fill="var(--fill-0, #727783)" id="Icon" />
        </g>
      </svg>
    </div>
  );
}

function ContainerCssTransform1() {
  return (
    <div className="content-stretch flex flex-col items-center justify-center pl-[7.44px] pr-[7.45px] relative shrink-0 w-[32.91px]" data-name="Container:css-transform">
      <div className="flex h-[12px] items-center justify-center relative shrink-0 w-[15px]" style={{ "--transform-inner-width": "1200", "--transform-inner-height": "19" } as React.CSSProperties}>
        <div className="flex-none scale-x-75 scale-y-75">
          <Container54 />
        </div>
      </div>
    </div>
  );
}

function Container55() {
  return (
    <div className="content-stretch flex flex-col items-center relative shrink-0" data-name="Container">
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[#727783] text-[9px] text-center tracking-[-0.45px] uppercase whitespace-nowrap">
        <p className="leading-[13.5px]">ACHING</p>
      </div>
    </div>
  );
}

function Button13() {
  return (
    <div className="-translate-y-1/2 absolute content-stretch flex flex-col gap-[3px] items-center justify-center left-[75.18px] pb-[4px] pt-[7px] px-[12px] rounded-[12px] top-1/2" data-name="Button">
      <ContainerCssTransform1 />
      <Container55 />
    </div>
  );
}

function Container56() {
  return (
    <div className="relative size-[16px]" data-name="Container">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 16 16">
        <g id="Container">
          <path d={svgPaths.p2e7d3180} fill="var(--fill-0, white)" id="Icon" />
        </g>
      </svg>
    </div>
  );
}

function ContainerCssTransform2() {
  return (
    <div className="content-stretch flex flex-col items-center justify-center px-[10.781px] relative shrink-0 w-[39.581px]" data-name="Container:css-transform">
      <div className="flex items-center justify-center relative shrink-0 size-[12px]" style={{ "--transform-inner-width": "1200", "--transform-inner-height": "19" } as React.CSSProperties}>
        <div className="flex-none scale-x-75 scale-y-75">
          <Container56 />
        </div>
      </div>
    </div>
  );
}

function Container57() {
  return (
    <div className="content-stretch flex flex-col items-center relative shrink-0" data-name="Container">
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[9px] text-center text-white tracking-[-0.45px] uppercase whitespace-nowrap">
        <p className="leading-[13.5px]">TINGLING</p>
      </div>
    </div>
  );
}

function Button14() {
  return (
    <div className="bg-[#005eb8] content-stretch flex flex-col gap-[3px] items-center justify-center pb-[3.99px] pt-[7px] px-[12px] relative rounded-[12px] shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)]" data-name="Button">
      <ContainerCssTransform2 />
      <Container57 />
    </div>
  );
}

function Container58() {
  return (
    <div className="h-[20px] relative w-[16px]" data-name="Container">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 16 20">
        <g id="Container">
          <path d={svgPaths.p12df5c00} fill="var(--fill-0, #727783)" id="Icon" />
        </g>
      </svg>
    </div>
  );
}

function ContainerCssTransform3() {
  return (
    <div className="content-stretch flex flex-col items-center justify-center pl-[10.97px] pr-[10.99px] relative shrink-0 w-[39.97px]" data-name="Container:css-transform">
      <div className="flex h-[15px] items-center justify-center relative shrink-0 w-[12px]" style={{ "--transform-inner-width": "1200", "--transform-inner-height": "19" } as React.CSSProperties}>
        <div className="flex-none scale-x-75 scale-y-75">
          <Container58 />
        </div>
      </div>
    </div>
  );
}

function Container59() {
  return (
    <div className="content-stretch flex flex-col items-center relative shrink-0" data-name="Container">
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[#727783] text-[9px] text-center tracking-[-0.45px] uppercase whitespace-nowrap">
        <p className="leading-[13.5px]">ELECTRIC</p>
      </div>
    </div>
  );
}

function Button15() {
  return (
    <div className="-translate-y-1/2 absolute content-stretch flex flex-col gap-[3px] items-center justify-center left-[211.67px] pb-[4px] pt-[7px] px-[12px] rounded-[12px] top-1/2" data-name="Button">
      <ContainerCssTransform3 />
      <Container59 />
    </div>
  );
}

function Container60() {
  return (
    <div className="h-[18px] relative w-[18.025px]" data-name="Container">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 18.025 18">
        <g id="Container">
          <path d={svgPaths.p1ebc0d40} fill="var(--fill-0, #727783)" id="Icon" />
        </g>
      </svg>
    </div>
  );
}

function ContainerCssTransform4() {
  return (
    <div className="content-stretch flex flex-col items-center justify-center px-[3.94px] relative shrink-0 w-[25.89px]" data-name="Container:css-transform">
      <div className="flex h-[13.5px] items-center justify-center relative shrink-0 w-[13.519px]" style={{ "--transform-inner-width": "1200", "--transform-inner-height": "19" } as React.CSSProperties}>
        <div className="flex-none scale-x-75 scale-y-75">
          <Container60 />
        </div>
      </div>
    </div>
  );
}

function Container61() {
  return (
    <div className="content-stretch flex flex-col items-center relative shrink-0" data-name="Container">
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[#727783] text-[9px] text-center tracking-[-0.45px] uppercase whitespace-nowrap">
        <p className="leading-[13.5px]">NUMB</p>
      </div>
    </div>
  );
}

function Button16() {
  return (
    <div className="-translate-y-1/2 absolute content-stretch flex flex-col gap-[3px] items-center justify-center left-[283.64px] pb-[4px] pt-[7px] px-[12px] rounded-[12px] top-1/2" data-name="Button">
      <ContainerCssTransform4 />
      <Container61 />
    </div>
  );
}

function ActiveSensationSelection() {
  return (
    <div className="bg-[#f2f4f7] h-[55.5px] relative rounded-[12px] shrink-0 w-[338.53px]" data-name="Active Sensation Selection">
      <div aria-hidden="true" className="absolute border border-[rgba(194,198,212,0.3)] border-solid inset-0 pointer-events-none rounded-[12px]" />
      <div className="bg-clip-padding border-0 border-[transparent] border-solid relative size-full">
        <Button12 />
        <Button13 />
        <div className="-translate-y-1/2 absolute flex h-[41.99px] items-center justify-center left-[138.5px] top-[calc(50%-0.01px)] w-[66.76px]" style={{ "--transform-inner-width": "1200", "--transform-inner-height": "38" } as React.CSSProperties}>
          <div className="flex-none scale-x-105 scale-y-105">
            <Button14 />
          </div>
        </div>
        <Button15 />
        <Button16 />
      </div>
    </div>
  );
}

function Button17() {
  return (
    <div className="h-[20px] relative shrink-0 w-[16px]" data-name="Button">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 16 20">
        <g id="Button">
          <path d={svgPaths.p164b49c0} fill="var(--fill-0, #424752)" id="Icon" />
        </g>
      </svg>
    </div>
  );
}

function Button18() {
  return (
    <div className="h-[20px] relative shrink-0 w-[20.1px]" data-name="Button">
      <svg className="absolute block inset-0 size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 20.1 20">
        <g id="Button">
          <path d={svgPaths.p3cdadd00} fill="var(--fill-0, #424752)" id="Icon" />
        </g>
      </svg>
    </div>
  );
}

function Button19() {
  return (
    <div className="bg-[#005eb8] content-stretch flex flex-col items-center justify-center px-[20px] py-[6px] relative rounded-[12px] shrink-0" data-name="Button">
      <div className="flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[14px] text-center text-white whitespace-nowrap">
        <p className="leading-[20px]">Save Session</p>
      </div>
    </div>
  );
}

function UserAvatar() {
  return (
    <div className="flex-[1_0_0] min-h-px relative w-full" data-name="User avatar">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <img alt="" className="absolute left-0 max-w-none size-full top-0" src={imgUserAvatar} />
      </div>
    </div>
  );
}

function BackgroundShadow() {
  return (
    <div className="bg-[#e0e3e6] content-stretch flex flex-col items-start justify-center overflow-clip relative rounded-[12px] shadow-[0px_0px_0px_2px_rgba(0,94,184,0.2)] shrink-0 size-[32px]" data-name="Background+Shadow">
      <UserAvatar />
    </div>
  );
}

function Container62() {
  return (
    <div className="relative shrink-0" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex gap-[16px] items-center relative size-full">
        <Button17 />
        <Button18 />
        <Button19 />
        <BackgroundShadow />
      </div>
    </div>
  );
}

function RefinedHeaderCombinedWithSidebarFunctionality() {
  return (
    <div className="absolute backdrop-blur-[6px] bg-[rgba(255,255,255,0.9)] content-stretch flex items-center justify-between left-0 pb-[11px] pl-[24px] pr-[24.02px] pt-[10px] top-0 w-[1280px]" data-name="Refined Header (Combined with Sidebar functionality)">
      <div aria-hidden="true" className="absolute border-[#e0e3e6] border-b border-solid inset-0 pointer-events-none" />
      <Container50 />
      <ActiveSensationSelection />
      <Container62 />
    </div>
  );
}

export default function Page1BodyMapping() {
  return (
    <div className="bg-[#f7f9fc] content-stretch flex flex-col items-start relative size-full" data-name="Page 1: Body Mapping">
      <Container />
      <AsideLeftNavigationBarToolsOnly />
      <RefinedHeaderCombinedWithSidebarFunctionality />
    </div>
  );
}