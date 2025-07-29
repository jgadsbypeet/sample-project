// Trauma-Informed Research Script Analyzer
class TraumaInformedAnalyzer {
    constructor() {
        this.principles = {
            safety: {
                name: 'Safety',
                icon: 'fas fa-shield-alt',
                description: 'Creating predictable, secure environments with clear boundaries',
                patterns: {
                    positive: [
                        /we will (discuss|cover|explore)/gi,
                        /you can (stop|pause|take a break)/gi,
                        /this session will last/gi,
                        /we won't ask about/gi,
                        /you don't have to/gi,
                        /feel free to/gi,
                        /at any time you can/gi,
                        /we will begin by/gi,
                        /this is voluntary/gi,
                        /confidential/gi
                    ],
                    negative: [
                        /you must/gi,
                        /required to answer/gi,
                        /have to tell us/gi,
                        /can't leave until/gi,
                        /unexpected/gi,
                        /surprise/gi,
                        /without warning/gi,
                        /suddenly/gi
                    ]
                }
            },
            trust: {
                name: 'Trust & Accountability',
                icon: 'fas fa-handshake',
                description: 'Building transparent, reliable relationships through honest communication',
                patterns: {
                    positive: [
                        /we will use this for/gi,
                        /your data will be/gi,
                        /we promise/gi,
                        /committed to/gi,
                        /transparent about/gi,
                        /honest about/gi,
                        /follow up/gi,
                        /keep you informed/gi,
                        /our process is/gi,
                        /we will not/gi
                    ],
                    negative: [
                        /might use/gi,
                        /could potentially/gi,
                        /not sure how/gi,
                        /may or may not/gi,
                        /depends on/gi,
                        /we'll see/gi,
                        /uncertain/gi,
                        /can't guarantee/gi
                    ]
                }
            },
            collaboration: {
                name: 'Collaboration & Equity',
                icon: 'fas fa-users',
                description: 'Ensuring genuine partnership and inclusive participation',
                patterns: {
                    positive: [
                        /your perspective/gi,
                        /what matters to you/gi,
                        /your experience/gi,
                        /you are the expert/gi,
                        /we value your/gi,
                        /different ways to participate/gi,
                        /choose how you/gi,
                        /work together/gi,
                        /partnership/gi,
                        /co-design/gi
                    ],
                    negative: [
                        /we need you to/gi,
                        /follow our/gi,
                        /standard procedure/gi,
                        /one way to do this/gi,
                        /same for everyone/gi,
                        /our research/gi,
                        /we are studying/gi,
                        /subject/gi
                    ]
                }
            },
            empowerment: {
                name: 'Empowerment',
                icon: 'fas fa-hand-fist',
                description: 'Providing meaningful choices and validating participant agency',
                patterns: {
                    positive: [
                        /you can choose/gi,
                        /up to you/gi,
                        /your decision/gi,
                        /you have options/gi,
                        /you might prefer/gi,
                        /whatever feels right/gi,
                        /your feelings are valid/gi,
                        /makes sense/gi,
                        /you're the expert/gi,
                        /control over/gi
                    ],
                    negative: [
                        /you should/gi,
                        /you need to/gi,
                        /correct answer/gi,
                        /wrong way/gi,
                        /better if you/gi,
                        /don't understand/gi,
                        /that's not right/gi,
                        /you're wrong/gi
                    ]
                }
            },
            hope: {
                name: 'Hope',
                icon: 'fas fa-seedling',
                description: 'Highlighting positive impact and future possibilities',
                patterns: {
                    positive: [
                        /will help/gi,
                        /make a difference/gi,
                        /positive impact/gi,
                        /improve/gi,
                        /benefit others/gi,
                        /your contribution/gi,
                        /valuable insight/gi,
                        /meaningful change/gi,
                        /better future/gi,
                        /support others/gi
                    ],
                    negative: [
                        /might not work/gi,
                        /could fail/gi,
                        /no guarantee/gi,
                        /probably won't/gi,
                        /unlikely to/gi,
                        /don't expect/gi,
                        /waste of time/gi,
                        /pointless/gi
                    ]
                }
            }
        };

        this.suggestions = {
            safety: [
                {
                    trigger: /no mention of time|duration|length/gi,
                    improvement: "Add clear time expectations",
                    example: "This session will last approximately 60 minutes, and we'll take a break halfway through.",
                    justification: "Predictable timeframes reduce anxiety and help participants feel safe by knowing what to expect."
                },
                {
                    trigger: /no mention of voluntary|optional|choice to participate/gi,
                    improvement: "Emphasize voluntary participation",
                    example: "Your participation is completely voluntary, and you can stop at any time without any consequences.",
                    justification: "Explicitly stating voluntary participation helps participants feel they have control and agency."
                },
                {
                    trigger: /no mention of topics|subjects|areas we will cover/gi,
                    improvement: "Outline topics in advance",
                    example: "Today we'll be discussing your experience with [topic], but we won't ask about [sensitive areas].",
                    justification: "Knowing topics in advance prevents unexpected triggers and allows participants to prepare mentally."
                }
            ],
            trust: [
                {
                    trigger: /no mention of data use|purpose|how information will be used/gi,
                    improvement: "Explain data usage clearly",
                    example: "We will use your responses to improve our services and will anonymize all data before analysis.",
                    justification: "Transparency about data usage builds trust and helps participants make informed decisions."
                },
                {
                    trigger: /vague promises|unclear commitments/gi,
                    improvement: "Make specific, achievable commitments",
                    example: "We commit to sharing our findings with you within 3 months and will not use your data for any other purpose.",
                    justification: "Specific commitments demonstrate reliability and help build trust through accountability."
                }
            ],
            collaboration: [
                {
                    trigger: /no acknowledgment of expertise|experience/gi,
                    improvement: "Acknowledge participant expertise",
                    example: "You are the expert in your own experience, and we're here to learn from your perspective.",
                    justification: "Recognizing participants as experts validates their knowledge and promotes genuine collaboration."
                },
                {
                    trigger: /no flexibility in participation/gi,
                    improvement: "Offer multiple participation options",
                    example: "You can respond verbally, in writing, or through drawings - whatever feels most comfortable for you.",
                    justification: "Flexible participation methods ensure equity and accommodate different communication preferences."
                }
            ],
            empowerment: [
                {
                    trigger: /no choice|options|flexibility mentioned/gi,
                    improvement: "Provide meaningful choices",
                    example: "You can choose which questions to answer, take breaks whenever you need, or end the session at any point.",
                    justification: "Offering choices helps participants feel empowered and maintains their sense of control."
                },
                {
                    trigger: /no validation of feelings|concerns/gi,
                    improvement: "Validate participant feelings",
                    example: "All of your feelings and responses are valid - there are no right or wrong answers here.",
                    justification: "Validation helps participants feel heard and respected, countering trauma's impact on self-worth."
                }
            ],
            hope: [
                {
                    trigger: /no mention of impact|benefit|positive outcome/gi,
                    improvement: "Highlight positive impact",
                    example: "Your insights will directly help us improve support for others in similar situations.",
                    justification: "Connecting participation to positive outcomes helps participants see meaning and hope in their contribution."
                },
                {
                    trigger: /no future focus|forward-looking statements/gi,
                    improvement: "Include hope-building language",
                    example: "This research will contribute to creating better resources and support systems for the future.",
                    justification: "Future-focused language helps participants envision positive possibilities and builds hope."
                }
            ]
        };
    }

    analyzeScript(script) {
        const results = {
            overall: { score: 0, grade: '', feedback: '' },
            principles: {},
            suggestions: [],
            improvedScript: ''
        };

        // Analyze each principle
        for (const [key, principle] of Object.entries(this.principles)) {
            const analysis = this.analyzePrinciple(script, principle);
            results.principles[key] = analysis;
            results.overall.score += analysis.score;
        }

        // Calculate overall score
        results.overall.score = Math.round(results.overall.score / Object.keys(this.principles).length);
        results.overall.grade = this.getGrade(results.overall.score);
        results.overall.feedback = this.generateOverallFeedback(results.overall.score);

        // Generate suggestions
        results.suggestions = this.generateSuggestions(script, results.principles);

        // Generate improved script
        results.improvedScript = this.generateImprovedScript(script, results.suggestions);

        return results;
    }

    analyzePrinciple(script, principle) {
        let positiveMatches = 0;
        let negativeMatches = 0;

        // Count positive indicators
        principle.patterns.positive.forEach(pattern => {
            const matches = script.match(pattern);
            if (matches) positiveMatches += matches.length;
        });

        // Count negative indicators
        principle.patterns.negative.forEach(pattern => {
            const matches = script.match(pattern);
            if (matches) negativeMatches += matches.length;
        });

        // Calculate score (0-100)
        const totalWords = script.split(/\s+/).length;
        const positiveScore = Math.min((positiveMatches / Math.max(totalWords / 50, 1)) * 100, 100);
        const negativeScore = Math.min((negativeMatches / Math.max(totalWords / 50, 1)) * 100, 100);
        
        let score = Math.max(0, positiveScore - negativeScore * 2);
        
        // Boost score if script is very short but has good indicators
        if (totalWords < 100 && positiveMatches > 0) {
            score = Math.min(score * 1.5, 100);
        }

        const grade = this.getGrade(score);

        return {
            score: Math.round(score),
            grade,
            positiveMatches,
            negativeMatches,
            feedback: this.generatePrincipleFeedback(principle.name, score, positiveMatches, negativeMatches)
        };
    }

    getGrade(score) {
        if (score >= 80) return 'excellent';
        if (score >= 60) return 'good';
        if (score >= 40) return 'fair';
        return 'poor';
    }

    generateOverallFeedback(score) {
        if (score >= 80) {
            return "Excellent! Your script demonstrates strong trauma-informed principles. Minor refinements could make it even better.";
        } else if (score >= 60) {
            return "Good foundation with trauma-informed elements. Several improvements would enhance participant safety and comfort.";
        } else if (score >= 40) {
            return "Some trauma-informed elements present, but significant improvements needed to create a truly safe and empowering experience.";
        } else {
            return "Script needs substantial revision to incorporate trauma-informed principles. Focus on safety, choice, and transparency.";
        }
    }

    generatePrincipleFeedback(principleName, score, positive, negative) {
        const feedback = [];
        
        if (positive > 0) {
            feedback.push(`Found ${positive} positive indicator${positive > 1 ? 's' : ''} for ${principleName}`);
        }
        
        if (negative > 0) {
            feedback.push(`Found ${negative} concerning pattern${negative > 1 ? 's' : ''} that may undermine ${principleName}`);
        }
        
        if (positive === 0 && negative === 0) {
            feedback.push(`No specific indicators found for ${principleName} - consider adding relevant elements`);
        }

        return feedback.join('. ');
    }

    generateSuggestions(script, principleResults) {
        const suggestions = [];
        let priorityCounter = 0;

        for (const [principleKey, suggestionList] of Object.entries(this.suggestions)) {
            const principleScore = principleResults[principleKey].score;
            
            suggestionList.forEach(suggestion => {
                if (script.match(suggestion.trigger) || principleScore < 60) {
                    const priority = principleScore < 40 ? 'high' : principleScore < 70 ? 'medium' : 'low';
                    
                    suggestions.push({
                        id: priorityCounter++,
                        principle: this.principles[principleKey].name,
                        priority,
                        title: suggestion.improvement,
                        description: suggestion.example,
                        justification: suggestion.justification,
                        principleKey
                    });
                }
            });
        }

        // Sort by priority
        const priorityOrder = { high: 3, medium: 2, low: 1 };
        return suggestions.sort((a, b) => priorityOrder[b.priority] - priorityOrder[a.priority]);
    }

    generateImprovedScript(originalScript, suggestions) {
        let improvedScript = originalScript;
        
        // Add safety introduction
        if (!improvedScript.match(/voluntary|optional|stop at any time/gi)) {
            improvedScript = `[INTRODUCTION ADDED]
Thank you for your time today. Your participation is completely voluntary, and you can stop at any time without any consequences. This session will last approximately [X] minutes.

${improvedScript}`;
        }

        // Add topic outline if missing
        if (!improvedScript.match(/we will discuss|topics include|we'll be covering/gi)) {
            improvedScript = improvedScript.replace(
                /^(.*?)$/m,
                `$1\n\n[TOPIC OUTLINE ADDED]
Today we'll be discussing [main topics]. We won't ask about [sensitive areas you want to avoid]. You can choose which questions to answer and can take breaks whenever you need them.`
            );
        }

        // Add data usage clarity
        if (!improvedScript.match(/data will be|information will be used|responses will/gi)) {
            improvedScript += `\n\n[DATA USAGE CLARITY ADDED]
Your responses will be used to [specific purpose] and will be kept confidential. We will [specific commitment about data handling].`;
        }

        // Add empowerment language
        if (!improvedScript.match(/you are the expert|your choice|up to you/gi)) {
            improvedScript += `\n\n[EMPOWERMENT LANGUAGE ADDED]
Remember, you are the expert in your own experience. All of your responses are valuable and valid - there are no right or wrong answers.`;
        }

        // Add hope and impact
        if (!improvedScript.match(/will help|make a difference|positive impact/gi)) {
            improvedScript += `\n\n[IMPACT STATEMENT ADDED]
Your insights will help us [specific positive outcome] and will make a meaningful difference for others in similar situations.`;
        }

        return improvedScript;
    }
}

// DOM Management and Event Handlers
class ScriptAnalyzerApp {
    constructor() {
        this.analyzer = new TraumaInformedAnalyzer();
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        const analyzeBtn = document.getElementById('analyzeBtn');
        const copyBtn = document.getElementById('copyImproved');
        
        analyzeBtn.addEventListener('click', () => this.analyzeScript());
        copyBtn.addEventListener('click', () => this.copyImprovedScript());
        
        // Add enter key support for textarea
        document.getElementById('scriptInput').addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                this.analyzeScript();
            }
        });
    }

    analyzeScript() {
        const scriptInput = document.getElementById('scriptInput');
        const script = scriptInput.value.trim();

        if (!script) {
            alert('Please enter a research script to analyze.');
            return;
        }

        // Show loading state
        const analyzeBtn = document.getElementById('analyzeBtn');
        const originalText = analyzeBtn.innerHTML;
        analyzeBtn.innerHTML = '<span class="loading"></span> Analyzing...';
        analyzeBtn.disabled = true;

        // Simulate processing time for better UX
        setTimeout(() => {
            const results = this.analyzer.analyzeScript(script);
            this.displayResults(results, script);
            
            // Reset button
            analyzeBtn.innerHTML = originalText;
            analyzeBtn.disabled = false;
            
            // Show results section
            document.getElementById('resultsSection').style.display = 'block';
            document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
        }, 1500);
    }

    displayResults(results, originalScript) {
        this.displayOverallScore(results.overall);
        this.displayPrinciplesAnalysis(results.principles);
        this.displaySuggestions(results.suggestions);
        this.displayScriptComparison(originalScript, results.improvedScript);
    }

    displayOverallScore(overall) {
        const scoreDisplay = document.getElementById('overallScore');
        const summaryText = document.getElementById('summaryText');

        scoreDisplay.innerHTML = `
            <span class="score-${overall.grade}">${overall.score}/100</span>
            <div style="margin-top: 10px;">
                <strong>Grade: ${overall.grade.charAt(0).toUpperCase() + overall.grade.slice(1)}</strong>
            </div>
        `;

        summaryText.innerHTML = `<p>${overall.feedback}</p>`;
    }

    displayPrinciplesAnalysis(principles) {
        const principlesGrid = document.getElementById('principlesGrid');
        principlesGrid.innerHTML = '';

        for (const [key, result] of Object.entries(principles)) {
            const principle = this.analyzer.principles[key];
            const principleElement = document.createElement('div');
            principleElement.className = `principle-result ${result.grade}`;
            
            principleElement.innerHTML = `
                <h4>
                    <i class="${principle.icon}"></i>
                    ${principle.name}
                    <span class="principle-score score-${result.grade}">${result.score}/100</span>
                </h4>
                <p>${result.feedback}</p>
                <div style="margin-top: 10px; font-size: 0.9rem; color: #666;">
                    ${principle.description}
                </div>
            `;
            
            principlesGrid.appendChild(principleElement);
        }
    }

    displaySuggestions(suggestions) {
        const suggestionsList = document.getElementById('suggestionsList');
        suggestionsList.innerHTML = '';

        if (suggestions.length === 0) {
            suggestionsList.innerHTML = '<p>No specific suggestions needed - your script already incorporates trauma-informed principles well!</p>';
            return;
        }

        suggestions.forEach(suggestion => {
            const suggestionElement = document.createElement('div');
            suggestionElement.className = 'suggestion-item';
            
            suggestionElement.innerHTML = `
                <div class="suggestion-header">
                    <span class="suggestion-principle">${suggestion.principle}</span>
                    <span class="suggestion-priority priority-${suggestion.priority}">${suggestion.priority.toUpperCase()}</span>
                </div>
                <div class="suggestion-content">
                    <h4>${suggestion.title}</h4>
                    <p><strong>Example:</strong> "${suggestion.description}"</p>
                    <div class="suggestion-justification">
                        <strong>Why this matters:</strong> ${suggestion.justification}
                    </div>
                </div>
            `;
            
            suggestionsList.appendChild(suggestionElement);
        });
    }

    displayScriptComparison(original, improved) {
        document.getElementById('originalPreview').textContent = original;
        document.getElementById('improvedPreview').textContent = improved;
    }

    copyImprovedScript() {
        const improvedScript = document.getElementById('improvedPreview').textContent;
        
        if (navigator.clipboard) {
            navigator.clipboard.writeText(improvedScript).then(() => {
                const copyBtn = document.getElementById('copyImproved');
                const originalText = copyBtn.innerHTML;
                copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                setTimeout(() => {
                    copyBtn.innerHTML = originalText;
                }, 2000);
            });
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = improvedScript;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            alert('Script copied to clipboard!');
        }
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ScriptAnalyzerApp();
    
    // Check if there's a selected sample from the test page
    const selectedSample = localStorage.getItem('selectedSample');
    if (selectedSample && window.sampleScripts && window.sampleScripts[selectedSample]) {
        document.getElementById('scriptInput').value = window.sampleScripts[selectedSample];
        localStorage.removeItem('selectedSample');
        // Auto-analyze after a short delay
        setTimeout(() => {
            document.getElementById('analyzeBtn').click();
        }, 500);
    }
});

// Add some sample scripts for testing
window.sampleScripts = {
    poor: `Tell us about your experience. We need to understand what happened to you. You must answer all questions. This is required for our research. We will ask about everything.`,
    
    fair: `We want to learn about your experience. Please share what you feel comfortable discussing. This research will help us understand the topic better. We appreciate your time.`,
    
    good: `Thank you for participating in this voluntary research. We'll be discussing your experiences with [topic] for about 60 minutes. You can stop at any time, and all information will be kept confidential. Your insights will help improve services for others. You don't have to answer any question you're not comfortable with.`,
    
    excellent: `Welcome, and thank you for choosing to participate in this research. Your participation is completely voluntary, and you can stop at any time without any consequences. This session will last approximately 60 minutes, and we'll take a break halfway through.

Today we'll be discussing your experience with [specific topic], but we won't ask about [sensitive areas]. You are the expert in your own experience, and we're here to learn from your perspective. You can choose which questions to answer, respond in whatever way feels comfortable (verbally, in writing, or through drawings), and take breaks whenever you need them.

Your responses will be used specifically to improve support services and will be kept completely confidential. We commit to sharing our findings with participants within 3 months. Your insights will directly help us create better resources and support systems for others in similar situations.

All of your feelings and responses are valid - there are no right or wrong answers here. This work together will make a meaningful difference for the future.`
};

// Add sample script loader for testing
function loadSampleScript(type) {
    document.getElementById('scriptInput').value = window.sampleScripts[type];
}