# Trauma-Informed Research Script Analyzer

A comprehensive web application that analyzes user research scripts and provides evidence-based recommendations to improve participant experiences through trauma-informed design principles.

## 🎯 Purpose

This tool helps researchers, UX professionals, and anyone conducting human-centered research to create safer, more inclusive experiences for participants. It evaluates research scripts against established trauma-informed principles and provides specific, actionable improvements with detailed justifications.

## 🧠 Trauma-Informed Principles

The analyzer is built around five core trauma-informed principles developed by organizations like Chayn:

### 1. 🛡️ Safety
- **Goal**: Create predictable, secure environments with clear boundaries
- **Implementation**: Describe topics in advance, incorporate frequent check-ins, set clear expectations
- **Why it matters**: Trauma can take away feelings of safety and be easily triggered

### 2. 🤝 Trust & Accountability
- **Goal**: Build transparent, reliable relationships through honest communication
- **Implementation**: Be transparent about processes, follow through on commitments, avoid overpromising
- **Why it matters**: Trauma can lead to loss of faith in people and processes

### 3. 👥 Collaboration & Equity
- **Goal**: Ensure genuine partnership and inclusive participation
- **Implementation**: Include marginalized voices, offer flexible participation methods, promote genuine partnership
- **Why it matters**: Trauma greatly affects marginalized people who are often spoken for rather than heard

### 4. ✊ Empowerment
- **Goal**: Provide meaningful choices and validate participant agency
- **Implementation**: Offer choices without overwhelming, validate feelings and concerns
- **Why it matters**: Trauma can reduce feelings of control and lead to low self-worth

### 5. 🌱 Hope
- **Goal**: Highlight positive impact and future possibilities
- **Implementation**: Show how participation will create positive change, focus on meaningful outcomes
- **Why it matters**: Trauma can diminish capacity to look forward in life

## 🚀 Features

### Real-Time Script Analysis
- **Pattern Recognition**: Advanced regex-based analysis identifies positive and concerning language patterns
- **Scoring System**: Each principle receives a 0-100 score with color-coded feedback
- **Overall Assessment**: Comprehensive scoring with grades (Poor/Fair/Good/Excellent)

### Detailed Recommendations
- **Priority-Based Suggestions**: High, medium, and low priority improvements
- **Specific Examples**: Concrete language examples for each suggestion
- **Evidence-Based Justifications**: Detailed explanations of why each change matters
- **Principle Mapping**: Each suggestion clearly links to specific trauma-informed principles

### Script Improvement
- **Before/After Comparison**: Side-by-side view of original and improved scripts
- **Automatic Enhancement**: AI-generated improvements with clear labeling
- **Copy Functionality**: Easy copying of improved scripts for immediate use

### User Experience
- **Intuitive Interface**: Clean, accessible design with trauma-informed UX principles
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Educational Sidebar**: Built-in reference guide for trauma-informed principles
- **Accessibility**: Screen reader friendly with proper ARIA labels and keyboard navigation

## 🔧 How It Works

### 1. Analysis Engine
The analyzer uses sophisticated pattern matching to identify:
- **Positive Indicators**: Language that supports trauma-informed principles
- **Concerning Patterns**: Language that may undermine participant safety and comfort
- **Missing Elements**: Important components that should be included

### 2. Scoring Algorithm
```javascript
// Simplified scoring logic
score = positiveMatches - (negativeMatches * 2)
// Adjusts for script length and context
// Provides granular feedback per principle
```

### 3. Suggestion Generation
- Analyzes gaps in each principle
- Prioritizes suggestions based on impact and urgency
- Provides specific, actionable improvements
- Includes evidence-based justifications

## 🎨 Design Philosophy

This application embodies trauma-informed design in its own interface:

- **Calming Colors**: Soft gradient backgrounds and gentle color schemes
- **Clear Information Hierarchy**: Easy-to-scan layouts with appropriate spacing
- **Predictable Interactions**: Consistent UI patterns and clear feedback
- **Choice and Control**: Users control when and how to analyze scripts
- **Transparent Process**: Clear explanations of what the tool does and why

## 📋 Usage Examples

### Poor Script Example
```
Tell us about your experience. We need to understand what happened to you. 
You must answer all questions. This is required for our research.
```
**Result**: Low scores across all principles, multiple high-priority suggestions

### Excellent Script Example
```
Welcome, and thank you for choosing to participate. Your participation is 
completely voluntary, and you can stop at any time. This session will last 
60 minutes with a break halfway through.

You are the expert in your own experience. We'll discuss [topic] but won't 
ask about [sensitive areas]. You can respond however feels comfortable - 
verbally, in writing, or through drawings.

Your insights will directly help improve services for others in similar 
situations. All responses are valid - there are no right or wrong answers.
```
**Result**: High scores across all principles, minimal suggestions needed

## 🧪 Built-in Testing

The application includes sample scripts for testing:
- **Poor**: Demonstrates problematic language patterns
- **Fair**: Basic research script with some good elements
- **Good**: Well-structured script with most trauma-informed elements
- **Excellent**: Comprehensive trauma-informed script example

Access these via the browser console:
```javascript
// Load a sample script
loadSampleScript('excellent');
```

## 🛠️ Technical Implementation

### Frontend Technologies
- **HTML5**: Semantic, accessible markup
- **CSS3**: Modern styling with CSS Grid and Flexbox
- **Vanilla JavaScript**: No dependencies, fast loading
- **Font Awesome**: Consistent iconography
- **Google Fonts**: Professional typography

### Architecture
- **Modular Design**: Separated analysis engine and UI components
- **Class-Based Structure**: Clean, maintainable code organization
- **Event-Driven**: Responsive to user interactions
- **Progressive Enhancement**: Works without JavaScript for basic functionality

### Browser Compatibility
- Chrome/Edge 88+
- Firefox 85+
- Safari 14+
- Mobile browsers with modern JavaScript support

## 🚀 Getting Started

1. **Clone or Download**: Get the project files
2. **Open `index.html`**: No build process required
3. **Start Analyzing**: Paste your research script and click "Analyze Script"
4. **Review Results**: Examine scores, suggestions, and improved script
5. **Implement Changes**: Use the provided examples and justifications

## 🔄 Development Roadmap

### Current Features ✅
- Core analysis engine with 5 trauma-informed principles
- Real-time script analysis and scoring
- Detailed suggestions with justifications
- Script improvement generation
- Responsive, accessible interface

### Future Enhancements 🔮
- Save/load functionality for scripts
- Export reports as PDF
- Integration with research tools
- Collaborative features for teams
- Custom principle weights
- Multi-language support

## 🤝 Contributing

This tool was built to support trauma-informed research practices. Contributions are welcome:

1. **Research Insights**: Share evidence-based improvements
2. **Pattern Recognition**: Suggest additional language patterns
3. **UX Improvements**: Enhance accessibility and usability
4. **Documentation**: Improve examples and explanations

## 📚 References

- **Chayn**: Trauma-informed design principles and practices
- **SAMHSA**: Trauma-Informed Care guidelines
- **Research**: Evidence-based approaches to participant safety
- **UX Community**: Inclusive design best practices

## ⚠️ Important Notes

- This tool provides guidance, not definitive assessment
- Always consider individual participant needs
- Combine with human expertise and ethical review
- Continuously update based on latest research
- Test with diverse participant groups

## 📧 Support

For questions, suggestions, or issues:
- Review the built-in principle guide
- Check sample scripts for examples
- Consider trauma-informed research training
- Consult with ethics boards and accessibility experts

---

**Remember**: The goal is creating research experiences that honor participant dignity, promote safety, and generate meaningful insights through respectful collaboration.