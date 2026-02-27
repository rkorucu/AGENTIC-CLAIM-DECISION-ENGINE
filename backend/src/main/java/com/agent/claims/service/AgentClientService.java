package com.agent.claims.service;

import com.agent.claims.model.ClaimDecisionDto;
import com.agent.claims.model.ClaimRequestDto;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

@Service
public class AgentClientService {

    private final RestTemplate restTemplate;
    private final String agentServiceUrl;

    public AgentClientService(RestTemplate restTemplate,
                              @Value("${agent.service.url:http://localhost:8000}") String agentServiceUrl) {
        this.restTemplate = restTemplate;
        this.agentServiceUrl = agentServiceUrl.endsWith("/") ? agentServiceUrl : agentServiceUrl + "/";
    }

    public ClaimDecisionDto analyze(ClaimRequestDto request) {
        String url = agentServiceUrl + "analyze";
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<ClaimRequestDto> entity = new HttpEntity<>(request, headers);

        try {
            ResponseEntity<ClaimDecisionDto> response = restTemplate.postForEntity(
                    url, entity, ClaimDecisionDto.class);

            if (!response.getStatusCode().is2xxSuccessful() || response.getBody() == null) {
                throw new RuntimeException("Agent service returned error: " + response.getStatusCode());
            }
            return response.getBody();
        } catch (RestClientException e) {
            throw new RuntimeException(
                    "Agent service unavailable at " + agentServiceUrl + ". Ensure agent-service is running on port 8000. " + e.getMessage(),
                    e);
        }
    }
}
