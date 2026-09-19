package com.example.support.controller;
import com.example.support.dto.SupportRequest; import com.example.support.service.AgentClient; import jakarta.validation.Valid; import org.springframework.web.bind.annotation.*; import java.util.Map;
@RestController @RequestMapping("/api/support") public class SupportController { private final AgentClient agent; public SupportController(AgentClient a){agent=a;} @PostMapping("/chat") public Map chat(@Valid @RequestBody SupportRequest r){return agent.chat(r);} @GetMapping("/health") public Map health(){return Map.of("status","ok");} }
