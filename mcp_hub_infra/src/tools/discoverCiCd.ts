import fs from "fs";
import path from "path";
import { HUB_INFRA_PATH } from "../config.js";

export async function discoverCiCdHandler() {
  const workflowsDir = path.join(
    HUB_INFRA_PATH,
    "workflows"
  );

  const workflows = fs.readdirSync(workflowsDir);

  return {
    content: [
      {
        type: "text" as const,
        text: JSON.stringify(workflows, null, 2),
      },
    ],
  };
}