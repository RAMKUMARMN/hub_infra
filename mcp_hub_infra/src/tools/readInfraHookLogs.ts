import fs from "fs";
import path from "path";
import { HUB_INFRA_PATH } from "../config.js";

export async function readInfraHookLogsHandler() {
  const logPath = path.join(
    HUB_INFRA_PATH,
    "hook_execution.log"
  );

  let logContent = "No hook log file found.";

  if (fs.existsSync(logPath)) {
    const content = fs.readFileSync(
      logPath,
      "utf8"
    );

    logContent = content.slice(-3000);
  }

  return {
    content: [
      {
        type: "text" as const,
        text: logContent,
      },
    ],
  };
}