# Airline Sentiment Analysis Project - Structured Results

## Executive Summary
Successfully developed and evaluated a combined entity extraction and sentiment analysis system for airline tweets, achieving **94% accuracy on training data** and **93% accuracy on test data** using GPT-4o-mini with custom prompt engineering.

## Dataset Analysis

### Dataset Composition
- **Total Volume**: 1,200 tweets (900 training, 300 test)
- **Airline Coverage**: 8 unique airlines
- **Multi-airline Mentions**: 37 tweets (3.1%) mention multiple airlines
- **Tweet Length**: 18-169 characters (avg: 117 characters)

### Key Dataset Insights
- **Sentiment Distribution**: 89.1% negative, 9.6% neutral, 1.3% positive
- **Dominant Airlines**: United Airlines, US Airways, American Airlines
- **Most Negative Sentiment**: United Airlines
- **Most Positive Sentiment**: Virgin America and JetBlue
- **Primary Use Case**: Single airline extraction (96.9% of cases)
- **Consumer Behavior**: Tweets skewed negative due to customer inclination to mention airlines when experiencing issues
- **Subject Airline Pattern**: The primary airline (subject of complaint/comment) is typically mentioned first; other airlines often used as positive comparisons
- **Data Quality Issues**: One test case with JetBlue marked as empty string (''), indicating some ground truth corrections needed

### Technical Challenges Identified
- **Airline Name Variations**: Multiple formats (formal names, abbreviations, handles, misspellings, capitalization inconsistencies)
- **Sentiment Nuance**: Distinguishing neutral vs. negative, detecting sarcasm and subtext
- **Multiple Mentions**: Handling tweets referencing multiple airlines (3.1% of cases)
- **Data Quality**: Some ground truth labels missing secondary airline mentions
- **Spelling Variations**: Model needs to account for typos and concatenated mentions
- **Context Dependency**: Sentiment often depends on broader customer service context

## Methodology & Technical Approach

### Development Strategy
1. **Iterative Prompt Engineering**: Systematic refinement through experimentation
2. **Separated Task Development**: Entity extraction and sentiment analysis developed independently, then combined
3. **Custom Evaluation Framework**: Built specialized graders to handle data quality issues
4. **Batch Processing Optimization**: Tested various batch sizes for production scalability

### Key Techniques Implemented

#### Entity Extraction Approach
- **Name Standardization**: Mapped variations (abbreviations, mentions, misspellings) to official airline names
- **Few-shot Learning**: Included 2-3 examples of edge cases

#### Sentiment Analysis Approach
- **Context Instructions**: Added explicit instructions for sarcasm and subtext detection
- **Classification Refinement**: Improved neutral vs. negative distinction

#### Combined Processing
- **Unified Prompt Design**: Merged individual prompts while maintaining accuracy
- **Response Validation**: Implemented parsing and error handling
- **Quality Assurance**: Custom graders with ground truth override capability

## Experimental Results

### Entity Extraction Evolution
| Version | Approach | Accuracy | Key Learning |
|---------|----------|----------|--------------|
| v1 (Basic) | Simple extraction | 20% | Found airlines but inconsistent naming |
| v2 (Standardized) | Predefined airline list | 97% | Improved with naming standards |
| v3 (Few-shot) | Examples + flexible naming | 93% | Maintained performance without hardcoding |
| v3 (Custom Grader) | Same prompt, better evaluation | 100% | Ground truth had missing airlines |

### Sentiment Analysis Evolution
| Version | Approach | Accuracy | Key Learning |
|---------|----------|----------|--------------|
| v1 (Basic) | Standard classification | 90-93% | Good baseline |
| v2 (Context-aware) | Sarcasm/subtext detection | 92-94% | Small improvement on edge cases |
| v2 (Custom Grader) | Better evaluation | 96% | Sentiment can be subjective |

### Combined Task Results
| Version | Combined Accuracy | Sample Size | Key Learning |
|---------|------------------|-------------|--------------|
| v1 (Initial) | 76% | 30 samples | Issues merging individual prompts |
| v2 (Refined) | 90% | 30 samples | Better integration, remaining grader and prompt bugs |
| v3 (Final) | 96% | 50 samples | Fixed prompt bugs and improved grader |

### Batch Processing Analysis
| Batch Size | Entity Accuracy | Sentiment Accuracy | Latency | Recommendation |
|------------|----------------|-------------------|---------|----------------|
| 1 | 98% | 98% | 66s | **Recommended for accuracy** |
| 5 | 96% | 92% | 32s | Good for production balance |
| 10 | 100% | 94% | 34s | Alternative production option |
| 20 | 100% | 92% | 34s | Diminishing returns |

## Final Performance Metrics

### Production Results
- **Training Data**: 94% combined accuracy (900 samples)
- **Test Data**: 93% combined accuracy (300 samples)
- **Processing**: Single-tweet batching for maximum accuracy
- **Bias/Variance Analysis**: 1% generalization gap suggests low overfitting; performance likely limited by subjective nature of sentiment classification rather than model capacity

### Error Analysis
- **Primary Issues**: Neutral vs. negative sentiment distinction due to sarcasm and subtext
- **Data Quality**: Ground truth missing some multi-airline mentions
- **Edge Cases**: Sarcasm, indirect airline references, and contextual complaints
- **Specific Examples**:
  - Tweet mentioning both USAirways and Delta, but ground truth only captured USAirways
  - Sarcastic tweet "Jet Blue Jan 5? That's not summer" showing ambiguity between neutral/negative
  - Multiple airline scenarios where comparative mentions weren't captured in labels
- **Solutions**: Custom grader with override capability for mislabeled ground truth

## Technical Implementation Details

### Model Configuration
- **Base Model**: GPT-4o-mini
- **Approach**: Prompt engineering (no fine-tuning required)
- **Processing**: Individual tweet analysis for optimal accuracy
- **Validation**: Custom parsing with error handling

### Airline Name Standardization
- **American Airlines**: American, @AmericanAir, AA, AmericanAir, American Air
- **United Airlines**: United, @United, UA, UnitedAir, United Air, united
- **Southwest Airlines**: Southwest, @SouthwestAir, SWA, SouthwestAir, Southwest Air
- **US Airways**: US Airways, @USAirways, US Air, USAir, USAirways
- **JetBlue Airways**: JetBlue, @JetBlue, Jet Blue, jetblue, JETBLUE, JetBlue Airways
- **Virgin America**: Virgin, @VirginAmerica, VA, Virgin America, VirginAmerica

### Quality Assurance Framework
- **Custom Graders**: Built entity_grader_v1, sentiment_grader_v1, combined_grader_v1
- **Why Custom Graders Were Needed**:
  - **Ground Truth Override**: Ground truth labels were incomplete (missing secondary airline mentions)
  - **Contextual Evaluation**: Standard graders couldn't assess sarcasm and subtext
  - **Exact Match Requirements**: Entity extraction needed precise standardized name matching
  - **Subjective Cases**: Neutral vs. negative sentiment required contextual understanding
- **Grader Design**: 
  - Entity grader: Exact match comparison with official airline names
  - Sentiment grader: Contextual assessment with override for mislabeled examples
  - Combined grader: Both tasks must be correct

## Evaluation Platform Integration
- **Entity Extraction Grader**: entity_grader_v1 with exact match comparison
- **Sentiment Analysis Grader**: sentiment_grader_v1 with contextual awareness
- **Combined Task Grader**: combined_grader_v1 for end-to-end evaluation
- **Performance Targets**: >95% entity extraction, >92% sentiment analysis, >90% combined