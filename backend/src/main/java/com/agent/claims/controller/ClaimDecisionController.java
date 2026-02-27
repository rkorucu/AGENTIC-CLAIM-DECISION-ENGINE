package com.agent.claims.controller;

import com.agent.claims.model.ClaimDecisionDto;
import com.agent.claims.model.ClaimRequestDto;
import com.agent.claims.service.AgentClientService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/claims")
public class ClaimDecisionController {

    private final AgentClientService agentClientService;

    public ClaimDecisionController(AgentClientService agentClientService) {
        this.agentClientService = agentClientService;
    }

    @PostMapping("/analyze")
    public ResponseEntity<ClaimDecisionDto> analyze(@RequestBody ClaimRequestDto request) {
        ClaimDecisionDto decision = agentClientService.analyze(request);
        return ResponseEntity.ok(decision);
    }
}
