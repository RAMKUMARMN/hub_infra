import fs from "fs";
import path from "path";
import { HUB_INFRA_PATH } from "../config.js";

export async function discoverEnvironmentVariablesHandler() {
  const varsFile = path.join(
    HUB_INFRA_PATH,
    "terraform",
    "variables.tf"
  );

  return {
    content: [
      {
        type: "text" as const,
        text: JSON.stringify(
          {
            variablesFile: "terraform/variables.tf",
            exists: fs.existsSync(varsFile)
          },
          null,
          2
        ),
      },
    ],
  };
}