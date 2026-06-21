import fs from "fs";
import path from "path";
import { HUB_INFRA_PATH } from "../config.js";

export async function discoverAiRouterHandler() {
  const candidateFiles = [
    "ai/ai_router/api.py",
    "ai/ai_router/llm.py",
    "ai/ai_router/engine.py",
    "ai/ai_router/prompts.py",
  ];

  const results: Record<string, string> = {};

  for (const relativePath of candidateFiles) {
    const fullPath = path.join(
      HUB_INFRA_PATH,
      relativePath
    );

    if (fs.existsSync(fullPath)) {
      const content = fs.readFileSync(
        fullPath,
        "utf8"
      );

      results[relativePath] = content.slice(0, 1500);
    }
  }

  return {
    content: [
      {
        type: "text" as const,
        text: JSON.stringify(results, null, 2),
      },
    ],
  };
}