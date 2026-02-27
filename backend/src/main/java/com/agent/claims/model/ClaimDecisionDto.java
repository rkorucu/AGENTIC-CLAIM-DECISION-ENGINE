package com.agent.claims.model;

import com.fasterxml.jackson.annotation.JsonInclude;

import java.util.List;
import java.util.Map;

@JsonInclude(JsonInclude.Include.NON_NULL)
public class ClaimDecisionDto {

    private String decision;
    private int riskScore;
    private String riskLevel;
    private List<FlagDto> flags;
    private String explanation;
    private List<String> reflectionNotes;
    private ToolSummaryDto toolSummary;

    public ClaimDecisionDto() {}

    public ClaimDecisionDto(String decision, int riskScore, String riskLevel,
                           List<FlagDto> flags, String explanation,
                           List<String> reflectionNotes, ToolSummaryDto toolSummary) {
        this.decision = decision;
        this.riskScore = riskScore;
        this.riskLevel = riskLevel;
        this.flags = flags;
        this.explanation = explanation;
        this.reflectionNotes = reflectionNotes;
        this.toolSummary = toolSummary;
    }

    public String getDecision() { return decision; }
    public void setDecision(String decision) { this.decision = decision; }

    public int getRiskScore() { return riskScore; }
    public void setRiskScore(int riskScore) { this.riskScore = riskScore; }

    public String getRiskLevel() { return riskLevel; }
    public void setRiskLevel(String riskLevel) { this.riskLevel = riskLevel; }

    public List<FlagDto> getFlags() { return flags; }
    public void setFlags(List<FlagDto> flags) { this.flags = flags; }

    public String getExplanation() { return explanation; }
    public void setExplanation(String explanation) { this.explanation = explanation; }

    public List<String> getReflectionNotes() { return reflectionNotes; }
    public void setReflectionNotes(List<String> reflectionNotes) { this.reflectionNotes = reflectionNotes; }

    public ToolSummaryDto getToolSummary() { return toolSummary; }
    public void setToolSummary(ToolSummaryDto toolSummary) { this.toolSummary = toolSummary; }

    public static class FlagDto {
        private String code;
        private String severity;
        private String message;

        public FlagDto() {}
        public FlagDto(String code, String severity, String message) {
            this.code = code;
            this.severity = severity;
            this.message = message;
        }
        public String getCode() { return code; }
        public void setCode(String code) { this.code = code; }
        public String getSeverity() { return severity; }
        public void setSeverity(String severity) { this.severity = severity; }
        public String getMessage() { return message; }
        public void setMessage(String message) { this.message = message; }
    }

    public static class ToolSummaryDto {
        private Map<String, Object> coverageCheck;
        private Map<String, Object> fraudSignals;

        public ToolSummaryDto() {}
        public ToolSummaryDto(Map<String, Object> coverageCheck, Map<String, Object> fraudSignals) {
            this.coverageCheck = coverageCheck;
            this.fraudSignals = fraudSignals;
        }
        public Map<String, Object> getCoverageCheck() { return coverageCheck; }
        public void setCoverageCheck(Map<String, Object> coverageCheck) { this.coverageCheck = coverageCheck; }
        public Map<String, Object> getFraudSignals() { return fraudSignals; }
        public void setFraudSignals(Map<String, Object> fraudSignals) { this.fraudSignals = fraudSignals; }
    }
}
