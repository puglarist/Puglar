import { config } from "./config.js";

export async function createDeepSeekCompletion(messages, modelOverride) {
  if (!config.deepseek.apiKey) {
    throw new Error("DEEPSEEK_API_KEY is not configured");
  }

  const response = await fetch(`${config.deepseek.baseUrl}/chat/completions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${config.deepseek.apiKey}`
    },
    body: JSON.stringify({
      model: modelOverride ?? config.deepseek.model,
      messages,
      temperature: 0.2
    })
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`DeepSeek request failed (${response.status}): ${detail}`);
  }

  const payload = await response.json();
  return {
    text: payload.choices?.[0]?.message?.content ?? "",
    usage: payload.usage ?? null,
    raw: payload
  };
}
