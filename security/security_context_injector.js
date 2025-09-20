#!/usr/bin/env node
/**
 * Python Security Context Injector
 *
 * Automatically detects Python development context and injects appropriate
 * security guidelines into Claude's working context.
 *
 * Integration: Called by enhanced doit system and project analysis workflows
 */

const fs = require('fs');
const path = require('path');

class PythonSecurityContextInjector {
    constructor(projectPath = '.') {
        this.projectPath = projectPath;
        this.securityRulesPath = path.join(__dirname, 'python_security_rules.json');
        this.contextTemplatesPath = path.join(__dirname, 'security_context_templates.md');
        this.securityRules = this.loadSecurityRules();
        this.contextTemplates = this.loadContextTemplates();
    }

    /**
     * Load security rules from JSON configuration
     */
    loadSecurityRules() {
        try {
            const rulesContent = fs.readFileSync(this.securityRulesPath, 'utf8');
            return JSON.parse(rulesContent);
        } catch (error) {
            console.error('❌ Failed to load security rules:', error.message);
            return null;
        }
    }

    /**
     * Load context templates from markdown file
     */
    loadContextTemplates() {
        try {
            return fs.readFileSync(this.contextTemplatesPath, 'utf8');
        } catch (error) {
            console.error('❌ Failed to load context templates:', error.message);
            return '';
        }
    }

    /**
     * Analyze project to determine if Python security context should be activated
     */
    analyzeProject() {
        const analysis = {
            isPythonProject: false,
            riskLevel: 'none',
            detectedPatterns: [],
            recommendedContext: null,
            triggers: []
        };

        // Check for Python project indicators
        const pythonIndicators = this.checkPythonIndicators();
        if (pythonIndicators.found) {
            analysis.isPythonProject = true;
            analysis.triggers.push(...pythonIndicators.indicators);
        }

        // Analyze file contents for security-relevant patterns
        const contentAnalysis = this.analyzeProjectContents();
        analysis.detectedPatterns = contentAnalysis.patterns;
        analysis.riskLevel = this.calculateRiskLevel(contentAnalysis.patterns);

        // Determine appropriate security context
        analysis.recommendedContext = this.selectSecurityContext(analysis.riskLevel, contentAnalysis.patterns);

        return analysis;
    }

    /**
     * Check for Python project indicators
     */
    checkPythonIndicators() {
        const indicators = [];
        const rules = this.securityRules?.activation_triggers;
        if (!rules) return { found: false, indicators: [] };

        // Check for Python files
        const pythonFiles = this.findFilesByExtensions(rules.file_extensions);
        if (pythonFiles.length > 0) {
            indicators.push(`Python files found: ${pythonFiles.slice(0, 3).join(', ')}`);
        }

        // Check for Python project files
        for (const indicator of rules.project_indicators) {
            if (fs.existsSync(path.join(this.projectPath, indicator))) {
                indicators.push(`Project file: ${indicator}`);
            }
        }

        return {
            found: indicators.length > 0,
            indicators
        };
    }

    /**
     * Analyze project contents for security patterns
     */
    analyzeProjectContents() {
        const patterns = [];
        const pythonFiles = this.findFilesByExtensions(['.py']);

        for (const file of pythonFiles.slice(0, 10)) { // Limit analysis to first 10 files
            try {
                const content = fs.readFileSync(file, 'utf8');
                const filePatterns = this.analyzeFileContent(content, file);
                patterns.push(...filePatterns);
            } catch (error) {
                // Skip files that can't be read
                continue;
            }
        }

        return { patterns };
    }

    /**
     * Analyze individual file content for security patterns
     */
    analyzeFileContent(content, filePath) {
        const patterns = [];
        const rules = this.securityRules?.security_categories;
        if (!rules) return patterns;

        // Check for high-risk function usage
        for (const [category, categoryData] of Object.entries(rules)) {
            for (const pattern of categoryData.patterns || []) {
                for (const func of pattern.vulnerable_functions || []) {
                    // Simple regex to detect function usage
                    const funcName = func.replace(/\(\)/g, '').replace(/\[\]/g, '');
                    if (content.includes(funcName)) {
                        patterns.push({
                            type: category,
                            threat: pattern.threat,
                            function: func,
                            file: path.basename(filePath),
                            priority: categoryData.priority
                        });
                    }
                }
            }
        }

        // Check for specific security-relevant keywords
        const securityKeywords = [
            'password', 'authentication', 'encrypt', 'decrypt', 'hash',
            'database', 'sql', 'query', 'user_input', 'request.args',
            'file_upload', 'open(', 'subprocess', 'os.system'
        ];

        for (const keyword of securityKeywords) {
            if (content.toLowerCase().includes(keyword.toLowerCase())) {
                patterns.push({
                    type: 'security_keyword',
                    keyword: keyword,
                    file: path.basename(filePath),
                    priority: 'medium'
                });
            }
        }

        return patterns;
    }

    /**
     * Calculate overall risk level based on detected patterns
     */
    calculateRiskLevel(patterns) {
        if (!patterns.length) return 'none';

        const criticalCount = patterns.filter(p => p.priority === 'critical').length;
        const highCount = patterns.filter(p => p.priority === 'high').length;
        const mediumCount = patterns.filter(p => p.priority === 'medium').length;

        if (criticalCount > 0) return 'critical';
        if (highCount > 2) return 'high';
        if (highCount > 0 || mediumCount > 5) return 'medium';
        if (mediumCount > 0) return 'low';

        return 'none';
    }

    /**
     * Select appropriate security context based on risk level and patterns
     */
    selectSecurityContext(riskLevel, patterns) {
        if (riskLevel === 'none') return null;

        // Check for specific pattern types that require specialized contexts
        const hasAuthPatterns = patterns.some(p =>
            ['password', 'authentication', 'encrypt', 'hash'].includes(p.keyword)
        );
        const hasWebPatterns = patterns.some(p =>
            ['request.args', 'urllib', 'requests'].includes(p.keyword)
        );
        const hasDbPatterns = patterns.some(p =>
            ['database', 'sql', 'query'].includes(p.keyword)
        );
        const hasFilePatterns = patterns.some(p =>
            ['file_upload', 'open('].includes(p.keyword)
        );

        // Return specialized context based on patterns
        if (hasAuthPatterns) return 'CRYPTOGRAPHY_SECURITY_CONTEXT';
        if (hasWebPatterns) return 'WEB_SCRAPING_SECURITY_CONTEXT';
        if (hasDbPatterns) return 'DATABASE_SECURITY_CONTEXT';
        if (hasFilePatterns) return 'FILE_PROCESSING_SECURITY_CONTEXT';

        // Return general context based on risk level
        if (riskLevel === 'critical' || riskLevel === 'high') {
            return 'HIGH_RISK_SECURITY_CONTEXT';
        }

        return 'MEDIUM_RISK_SECURITY_CONTEXT';
    }

    /**
     * Find files by extensions in project
     */
    findFilesByExtensions(extensions) {
        const files = [];

        function scanDirectory(dir) {
            try {
                const entries = fs.readdirSync(dir);
                for (const entry of entries) {
                    const fullPath = path.join(dir, entry);
                    const stat = fs.statSync(fullPath);

                    if (stat.isDirectory() && !entry.startsWith('.')) {
                        scanDirectory(fullPath);
                    } else if (stat.isFile()) {
                        const ext = path.extname(entry);
                        if (extensions.includes(ext)) {
                            files.push(fullPath);
                        }
                    }
                }
            } catch (error) {
                // Skip directories that can't be read
            }
        }

        scanDirectory(this.projectPath);
        return files;
    }

    /**
     * Generate security context injection report
     */
    generateSecurityReport(analysis) {
        const report = {
            timestamp: new Date().toISOString(),
            projectPath: this.projectPath,
            analysis: analysis,
            injectedContext: null,
            recommendations: []
        };

        if (analysis.recommendedContext) {
            // Extract the relevant context from templates
            report.injectedContext = this.extractContextTemplate(analysis.recommendedContext);

            // Generate recommendations
            report.recommendations = this.generateRecommendations(analysis);
        }

        return report;
    }

    /**
     * Extract specific context template
     */
    extractContextTemplate(contextType) {
        const templates = this.contextTemplates;

        // Simple extraction - in production, this would be more sophisticated
        const contextMap = {
            'HIGH_RISK_SECURITY_CONTEXT': 'HIGH RISK SECURITY CONTEXT',
            'MEDIUM_RISK_SECURITY_CONTEXT': 'MEDIUM RISK SECURITY CONTEXT',
            'CRYPTOGRAPHY_SECURITY_CONTEXT': 'CRYPTOGRAPHY SECURITY CONTEXT',
            'WEB_SCRAPING_SECURITY_CONTEXT': 'WEB SCRAPING SECURITY CONTEXT',
            'DATABASE_SECURITY_CONTEXT': 'DATABASE SECURITY CONTEXT',
            'FILE_PROCESSING_SECURITY_CONTEXT': 'FILE PROCESSING SECURITY CONTEXT'
        };

        const searchHeader = contextMap[contextType];
        if (!searchHeader) return null;

        const startIndex = templates.indexOf(`### ${searchHeader}`);
        if (startIndex === -1) return null;

        const nextHeaderIndex = templates.indexOf('\n### ', startIndex + 1);
        const endIndex = nextHeaderIndex === -1 ? templates.length : nextHeaderIndex;

        return templates.slice(startIndex, endIndex).trim();
    }

    /**
     * Generate specific recommendations based on analysis
     */
    generateRecommendations(analysis) {
        const recommendations = [];

        for (const pattern of analysis.detectedPatterns) {
            if (pattern.priority === 'critical') {
                recommendations.push(`🚨 CRITICAL: Review usage of ${pattern.function} in ${pattern.file} - ${pattern.threat}`);
            } else if (pattern.priority === 'high') {
                recommendations.push(`⚠️ HIGH: Validate ${pattern.function} usage in ${pattern.file} - ${pattern.threat}`);
            }
        }

        return recommendations;
    }

    /**
     * Main execution method
     */
    run() {
        console.log('🔒 Python Security Context Injector Starting...\n');

        // Analyze project
        const analysis = this.analyzeProject();

        if (!analysis.isPythonProject) {
            console.log('ℹ️ No Python development detected - security context not required');
            return { activated: false, reason: 'No Python project detected' };
        }

        console.log(`📊 Analysis Results:`);
        console.log(`   Python Project: ${analysis.isPythonProject}`);
        console.log(`   Risk Level: ${analysis.riskLevel}`);
        console.log(`   Detected Patterns: ${analysis.detectedPatterns.length}`);
        console.log(`   Recommended Context: ${analysis.recommendedContext || 'None'}\n`);

        // Generate full security report
        const report = this.generateSecurityReport(analysis);

        if (analysis.recommendedContext) {
            console.log('🔒 SECURITY CONTEXT ACTIVATED\n');
            console.log('=' + '='.repeat(60));
            console.log(report.injectedContext);
            console.log('=' + '='.repeat(60));

            if (report.recommendations.length > 0) {
                console.log('\n📋 Immediate Security Recommendations:');
                for (const rec of report.recommendations) {
                    console.log(`   ${rec}`);
                }
            }

            console.log('\n✅ Security context successfully injected into Claude context');
        }

        return {
            activated: !!analysis.recommendedContext,
            analysis,
            report
        };
    }
}

// CLI execution
if (require.main === module) {
    const projectPath = process.argv[2] || '.';
    const injector = new PythonSecurityContextInjector(projectPath);
    const result = injector.run();

    // Exit with code 1 if high-risk issues were detected
    const hasHighRisk = result.analysis?.detectedPatterns?.some(p => p.priority === 'critical');
    process.exit(hasHighRisk ? 1 : 0);
}

module.exports = PythonSecurityContextInjector;
