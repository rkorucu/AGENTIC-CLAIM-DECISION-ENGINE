package com.agent.claims.controller;

import com.agent.claims.model.ClaimDecisionDto;
import com.agent.claims.model.ClaimRequestDto;
import com.agent.claims.service.AgentClientService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(ClaimDecisionController.class)
class ClaimDecisionControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private AgentClientService agentClientService;

    @Test
    void analyze_forwardsToAgentServiceAndReturnsDecision() throws Exception {
        ClaimRequestDto request = new ClaimRequestDto();
        request.setClaimId("CLM-001");
        request.setClaimant(new ClaimRequestDto.ClaimantDto("Jane Doe", "CA"));
        request.setPolicy(new ClaimRequestDto.PolicyDto("POL-1", "AUTO", 25000, 500, true));
        request.setIncident(new ClaimRequestDto.IncidentDto("COLLISION", "2024-01-15", "Description"));
        request.setClaim(new ClaimRequestDto.ClaimDto(3500, 0, true, 5));

        ClaimDecisionDto decision = new ClaimDecisionDto();
        decision.setDecision("APPROVE");
        decision.setRiskScore(15);
        decision.setRiskLevel("LOW");
        decision.setFlags(List.of());
        decision.setExplanation("Claim approved.");
        decision.setReflectionNotes(List.of());

        when(agentClientService.analyze(any(ClaimRequestDto.class))).thenReturn(decision);

        mockMvc.perform(post("/api/claims/analyze")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.decision").value("APPROVE"))
                .andExpect(jsonPath("$.riskScore").value(15))
                .andExpect(jsonPath("$.riskLevel").value("LOW"))
                .andExpect(jsonPath("$.explanation").value("Claim approved."));
    }
}
