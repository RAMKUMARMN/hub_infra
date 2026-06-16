import fs from "fs";
import path from "path";
import { HUB_INFRA_PATH } from "../config.js";

export async function discoverTerraformModulesHandler() {
  const modulesDir = path.join(
    HUB_INFRA_PATH,
    "terraform",
    "modules"
  );

  const modules = fs.readdirSync(modulesDir);

  return {
    content: [
      {
        type: "text" as const,
        text: JSON.stringify(modules, null, 2),
      },
    ],
  };
}