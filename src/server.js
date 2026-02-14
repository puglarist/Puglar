import express from "express";
import { z } from "zod";
import { prisma } from "./prisma.js";
import { config } from "./config.js";
import { createDeepSeekCompletion } from "./deepseek.js";

const app = express();
app.use(express.json());

const createAgentSchema = z.object({
  name: z.string().min(1),
  slug: z.string().min(1),
  description: z.string().optional(),
  type: z.enum(["CODING", "REVIEW", "PLANNING", "CUSTOM"]).default("CODING"),
  model: z.string().optional(),
  temperature: z.number().min(0).max(2).optional(),
  maxTokens: z.number().int().positive().optional(),
  systemPrompt: z.string().optional()
});

const createRunSchema = z.object({
  agentId: z.string().min(1),
  prompt: z.string().min(1),
  metadata: z.record(z.any()).optional()
});

app.get("/health", (_, res) => {
  res.json({ ok: true });
});

app.post("/api/agents", async (req, res) => {
  const parsed = createAgentSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ error: parsed.error.flatten() });
  }

  const agent = await prisma.agent.create({
    data: {
      ...parsed.data,
      config: parsed.data.systemPrompt ? { systemPrompt: parsed.data.systemPrompt } : undefined
    }
  });

  res.status(201).json(agent);
});

app.get("/api/agents", async (_, res) => {
  const agents = await prisma.agent.findMany({ orderBy: { createdAt: "desc" } });
  res.json(agents);
});

app.post("/api/runs", async (req, res) => {
  const parsed = createRunSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ error: parsed.error.flatten() });
  }

  const run = await prisma.agentRun.create({
    data: {
      agentId: parsed.data.agentId,
      input: {
        prompt: parsed.data.prompt,
        metadata: parsed.data.metadata ?? {}
      },
      messages: {
        create: [
          {
            role: "USER",
            content: parsed.data.prompt,
            metadata: parsed.data.metadata ?? null
          }
        ]
      }
    },
    include: {
      messages: true
    }
  });

  res.status(201).json(run);
});

app.post("/api/runs/:runId/start", async (req, res) => {
  const run = await prisma.agentRun.findUnique({
    where: { id: req.params.runId },
    include: { agent: true, messages: { orderBy: { createdAt: "asc" } } }
  });

  if (!run) {
    return res.status(404).json({ error: "Run not found" });
  }

  if (run.status === "RUNNING") {
    return res.status(409).json({ error: "Run is already running" });
  }

  await prisma.agentRun.update({ where: { id: run.id }, data: { status: "RUNNING", startedAt: new Date() } });

  try {
    const systemPrompt = run.agent.config && typeof run.agent.config === "object" ? run.agent.config.systemPrompt : undefined;

    const completion = await createDeepSeekCompletion(
      [
        ...(systemPrompt ? [{ role: "system", content: systemPrompt }] : []),
        ...run.messages.map((message) => ({
          role: message.role.toLowerCase(),
          content: message.content
        }))
      ],
      run.agent.model
    );

    const updated = await prisma.agentRun.update({
      where: { id: run.id },
      data: {
        status: "COMPLETED",
        output: completion.raw,
        promptTokens: completion.usage?.prompt_tokens,
        completionTokens: completion.usage?.completion_tokens,
        totalTokens: completion.usage?.total_tokens,
        finishedAt: new Date(),
        messages: {
          create: {
            role: "ASSISTANT",
            content: completion.text
          }
        }
      },
      include: { messages: { orderBy: { createdAt: "asc" } } }
    });

    return res.json(updated);
  } catch (error) {
    await prisma.agentRun.update({
      where: { id: run.id },
      data: {
        status: "FAILED",
        error: error instanceof Error ? error.message : "Unknown error",
        finishedAt: new Date()
      }
    });

    return res.status(500).json({
      error: error instanceof Error ? error.message : "Unknown error"
    });
  }
});

app.get("/api/runs/:runId", async (req, res) => {
  const run = await prisma.agentRun.findUnique({
    where: { id: req.params.runId },
    include: { agent: true, messages: { orderBy: { createdAt: "asc" } }, toolCalls: true }
  });

  if (!run) {
    return res.status(404).json({ error: "Run not found" });
  }

  res.json(run);
});

app.listen(config.port, () => {
  console.log(`Puglar agent API listening on http://localhost:${config.port}`);
});
