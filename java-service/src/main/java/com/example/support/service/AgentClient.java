package com.example.support.service;
import com.example.support.dto.SupportRequest; import org.springframework.beans.factory.annotation.Value; import org.springframework.stereotype.Service; import org.springframework.web.client.RestClient; import java.util.Map;
@Service public class AgentClient { private final RestClient client; public AgentClient(@Value("${agent.base-url:http://localhost:8000}") String url){client=RestClient.builder().baseUrl(url).build();} public Map chat(SupportRequest r){return client.post().uri("/v1/support/chat").body(r).retrieve().body(Map.class);} }
