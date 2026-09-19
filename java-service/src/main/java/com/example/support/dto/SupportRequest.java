package com.example.support.dto;
import com.fasterxml.jackson.annotation.JsonProperty; import jakarta.validation.constraints.NotBlank;
public record SupportRequest(@NotBlank @JsonProperty("customer_id") String customerId,@NotBlank String message,@JsonProperty("conversation_id") String conversationId,@JsonProperty("allow_actions") boolean allowActions) {}
