package com.agent.claims.model;

public class ClaimRequestDto {

    private String claimId;
    private ClaimantDto claimant;
    private PolicyDto policy;
    private IncidentDto incident;
    private ClaimDto claim;

    public ClaimRequestDto() {}

    public ClaimRequestDto(String claimId, ClaimantDto claimant, PolicyDto policy,
                           IncidentDto incident, ClaimDto claim) {
        this.claimId = claimId;
        this.claimant = claimant;
        this.policy = policy;
        this.incident = incident;
        this.claim = claim;
    }

    public String getClaimId() { return claimId; }
    public void setClaimId(String claimId) { this.claimId = claimId; }

    public ClaimantDto getClaimant() { return claimant; }
    public void setClaimant(ClaimantDto claimant) { this.claimant = claimant; }

    public PolicyDto getPolicy() { return policy; }
    public void setPolicy(PolicyDto policy) { this.policy = policy; }

    public IncidentDto getIncident() { return incident; }
    public void setIncident(IncidentDto incident) { this.incident = incident; }

    public ClaimDto getClaim() { return claim; }
    public void setClaim(ClaimDto claim) { this.claim = claim; }

    public static class ClaimantDto {
        private String fullName;
        private String state;

        public ClaimantDto() {}
        public ClaimantDto(String fullName, String state) {
            this.fullName = fullName;
            this.state = state;
        }
        public String getFullName() { return fullName; }
        public void setFullName(String fullName) { this.fullName = fullName; }
        public String getState() { return state; }
        public void setState(String state) { this.state = state; }
    }

    public static class PolicyDto {
        private String policyId;
        private String coverageType;
        private double coverageLimit;
        private double deductible;
        private boolean active;

        public PolicyDto() {}
        public PolicyDto(String policyId, String coverageType, double coverageLimit,
                        double deductible, boolean active) {
            this.policyId = policyId;
            this.coverageType = coverageType;
            this.coverageLimit = coverageLimit;
            this.deductible = deductible;
            this.active = active;
        }
        public String getPolicyId() { return policyId; }
        public void setPolicyId(String policyId) { this.policyId = policyId; }
        public String getCoverageType() { return coverageType; }
        public void setCoverageType(String coverageType) { this.coverageType = coverageType; }
        public double getCoverageLimit() { return coverageLimit; }
        public void setCoverageLimit(double coverageLimit) { this.coverageLimit = coverageLimit; }
        public double getDeductible() { return deductible; }
        public void setDeductible(double deductible) { this.deductible = deductible; }
        public boolean isActive() { return active; }
        public void setActive(boolean active) { this.active = active; }
    }

    public static class IncidentDto {
        private String type;
        private String date;
        private String description;

        public IncidentDto() {}
        public IncidentDto(String type, String date, String description) {
            this.type = type;
            this.date = date;
            this.description = description;
        }
        public String getType() { return type; }
        public void setType(String type) { this.type = type; }
        public String getDate() { return date; }
        public void setDate(String date) { this.date = date; }
        public String getDescription() { return description; }
        public void setDescription(String description) { this.description = description; }
    }

    public static class ClaimDto {
        private double amount;
        private int priorClaimsCount;
        private boolean hasPoliceReport;
        private int attachmentsCount;

        public ClaimDto() {}
        public ClaimDto(double amount, int priorClaimsCount, boolean hasPoliceReport,
                        int attachmentsCount) {
            this.amount = amount;
            this.priorClaimsCount = priorClaimsCount;
            this.hasPoliceReport = hasPoliceReport;
            this.attachmentsCount = attachmentsCount;
        }
        public double getAmount() { return amount; }
        public void setAmount(double amount) { this.amount = amount; }
        public int getPriorClaimsCount() { return priorClaimsCount; }
        public void setPriorClaimsCount(int priorClaimsCount) { this.priorClaimsCount = priorClaimsCount; }
        public boolean isHasPoliceReport() { return hasPoliceReport; }
        public void setHasPoliceReport(boolean hasPoliceReport) { this.hasPoliceReport = hasPoliceReport; }
        public int getAttachmentsCount() { return attachmentsCount; }
        public void setAttachmentsCount(int attachmentsCount) { this.attachmentsCount = attachmentsCount; }
    }
}
