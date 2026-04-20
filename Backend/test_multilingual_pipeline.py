"""
Test multilingual pipeline with sample inputs from each language
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.pain_assessment_pipeline import PainAssessmentPipeline

def test_multilingual_pipeline():
    """Test pipeline with different languages"""
    
    pipeline = PainAssessmentPipeline(verbose=True)
    
    print("\n" + "=" * 80)
    print("PIPELINE INFORMATION")
    print("=" * 80)
    info = pipeline.get_pipeline_info()
    for key, value in info.items():
        print(f"{key}: {value}")
    
    # Test cases for each language
    test_cases = [
        {
            "language": "Chinese",
            "text": "我有火辣辣的疼痛，已经好几个月了，腰部很难受",
            "llm_entities": {
                "pain_descriptors": ["火辣辣"],
                "location": "腰部",
                "duration_phrase": "好几个月",
                "emotion_keywords": ["难受"],
                "functional_impact": None,
                "intensity": "Moderate to severe"
            }
        },
        {
            "language": "Korean",
            "text": "허리가 따끔거리다",
            "llm_entities": {
                "pain_descriptors": ["따끔거리다"],
                "location": "허리",
                "duration_phrase": None,
                "emotion_keywords": [],
                "functional_impact": None,
                "intensity": "Moderate"
            }
        },
        {
            "language": "Spanish",
            "text": "Tengo un dolor agudo y punzante en la espalda",
            "llm_entities": {
                "pain_descriptors": ["agudo", "punzante"],
                "location": "la espalda",
                "duration_phrase": None,
                "emotion_keywords": [],
                "functional_impact": None,
                "intensity": "Severe"
            }
        },
        {
            "language": "Hmong",
            "text": "Kuv mob Kub Heev heev",
            "llm_entities": {
                "pain_descriptors": ["Kub Heev"],
                "location": None,
                "duration_phrase": None,
                "emotion_keywords": [],
                "functional_impact": None,
                "intensity": "Severe"
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print("\n" + "=" * 80)
        print(f"TEST CASE {i}: {test_case['language']}")
        print("=" * 80)
        print(f"Input: {test_case['text']}")
        print()
        
        try:
            report = pipeline.execute(
                test_case['text'],
                test_case['llm_entities']
            )
            
            print("\n--- STRUCTURED DATA ---")
            print(f"Pain Type: {report.structured_data.pain_type}")
            print(f"Location: {report.structured_data.location}")
            print(f"Temporal Pattern: {report.structured_data.temporal_pattern}")
            
            print("\n--- ONTOLOGY MAPPINGS ---")
            for mapping in report.ontology_mapping_trace:
                print(f"  {mapping.get('original_term', mapping.get('chinese_input', 'N/A'))} "
                      f"→ {mapping['mapped_english']} ({mapping.get('pain_type', 'N/A')})")
            
            print("\n--- RECOMMENDATIONS ---")
            if report.clinical_recommendations:
                for rec in report.clinical_recommendations:
                    print(f"  • {rec.recommendation}")
            else:
                print("  • Standard assessment recommended")
            
            print(f"\n✅ {test_case['language']} test PASSED")
            
        except Exception as e:
            print(f"\n❌ {test_case['language']} test FAILED: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_multilingual_pipeline()
